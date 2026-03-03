#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
# ]
# ///
"""Generate animated SVG with minimal system constraints — let the model be creative."""

import argparse
import os
import re
import signal
import sys
import time

MODELS = {
    "pro": "gemini-3.1-pro-preview",
    "flash": "gemini-3-flash-preview",
}


def main():
    parser = argparse.ArgumentParser(
        description="Generate animated SVG (minimal constraints, creative freedom)",
        epilog="Examples:\n"
               "  uv run --script generate_svg_minimal_req.py -p 'A rocket launch' -f rocket.svg\n"
               "  uv run --script generate_svg_minimal_req.py -p 'A rocket launch' -f rocket.svg -m flash\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--prompt", "-p", required=True)
    parser.add_argument("--filename", "-f", required=True)
    parser.add_argument(
        "--model", "-m", default="pro",
        help=f"Model alias ({', '.join(MODELS)}) or full model name (default: pro)",
    )
    parser.add_argument("--api-key", "-k", default=None)
    parser.add_argument("--timeout", "-t", type=int, default=30,
                        help="Seconds to wait for first chunk (default: 30)")
    args = parser.parse_args()
    args.model = MODELS.get(args.model, args.model)

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: No API key.", file=sys.stderr)
        sys.exit(1)

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    system_prompt = """You are a world-class SVG infographic designer.

Output a single animated SVG file. Be creative with layout, colors, shapes, and animation.

Hard rules (only these):
- Output ONLY the raw SVG XML. No markdown, no explanation.
- Wrap <style> content in <![CDATA[ ... ]]>.
- Use &amp; instead of bare &. Use &lt; &gt; instead of < > in text.
- viewBox: 1600 900.
- Use CSS @keyframes for animation. Total duration 6-8s.
- The result must be valid XML.

Everything else — style, palette, typography, layout, iconography — is up to you.
Make it beautiful."""

    timeout = args.timeout
    print(f"Generating SVG with {args.model} (streaming, {timeout}s timeout)...")

    chunks = []
    char_count = 0
    first_chunk = True

    def _timeout_handler(signum, frame):
        raise TimeoutError()

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)
    t0 = time.monotonic()

    try:
        for chunk in client.models.generate_content_stream(
            model=args.model,
            contents=args.prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=1.0,
            ),
        ):
            if first_chunk:
                signal.alarm(0)
                elapsed = time.monotonic() - t0
                print(f"  ↳ first chunk in {elapsed:.1f}s")
                first_chunk = False
            text = chunk.text or ""
            chunks.append(text)
            char_count += len(text)
            print(f"\r  ↳ received {char_count:,} chars", end="", flush=True)
    except (TimeoutError, Exception):
        signal.alarm(0)
        if first_chunk:
            print(
                f"\nError: No response from {args.model} within {timeout}s — "
                "model name may be wrong or the API is unreachable.",
                file=sys.stderr,
            )
            sys.exit(1)
        raise

    elapsed = time.monotonic() - t0
    print(f"\n  ↳ done in {elapsed:.1f}s ({char_count:,} chars total)")

    svg_content = "".join(chunks)
    svg_match = re.search(r"(<svg[\s\S]*?</svg>)", svg_content)
    if svg_match:
        svg_content = svg_match.group(1)

    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(svg_content)
        print("XML validation: PASSED")
    except ET.ParseError as e:
        print(f"XML validation: FAILED — {e}", file=sys.stderr)
        print("Attempting auto-fix...", file=sys.stderr)
        svg_content = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#)', '&amp;', svg_content)
        try:
            ET.fromstring(svg_content)
            print("XML validation after fix: PASSED")
        except ET.ParseError as e2:
            print(f"XML validation still failing: {e2}", file=sys.stderr)

    from pathlib import Path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg_content, encoding="utf-8")
    print(f"SVG saved: {output_path.resolve()}")


if __name__ == "__main__":
    main()
