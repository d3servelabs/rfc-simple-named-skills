#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
# ]
# ///
"""Generate animated SVG infographics from text prompts using Gemini.

SVG is XML code, so this uses Gemini's text/code generation models
(not the -image-preview variants which output raster PNG/JPEG).

Recommended models:
  gemini-3.1-pro-preview — highest quality SVG, best spatial reasoning (Feb 2026)
  gemini-3-flash-preview — faster and cheaper, good for iteration (Dec 2025)
"""

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
        description="Generate animated SVG from prompt",
        epilog="Examples:\n"
               "  uv run generate_svg.py -p 'A rocket launch diagram' -f rocket.svg\n"
               "  uv run generate_svg.py -p 'A rocket launch diagram' -f rocket.svg -m flash\n",
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

    system_prompt = """You are an expert SVG animator and infographic designer.
Given an infographic description, produce a single self-contained animated SVG file.

CRITICAL XML RULES (violations will break the file):
- Wrap ALL <style> content in <![CDATA[ ... ]]> to avoid XML parsing errors.
- NEVER use bare & in any text or attribute — always use &amp; instead.
- NEVER use < or > in text content — use &lt; and &gt; instead.
- Ensure the SVG is valid XML that passes xmllint.

Design requirements — FLAT UI STYLE:
- Output ONLY the SVG code, no explanation, no markdown fences.
- Use a modern Flat UI / Material Design aesthetic.
- Background: soft off-white (#F5F7FA) or very light grey.
- Use vibrant, saturated flat colors for shapes and icons:
  - Primary blue: #4A90D9
  - Success green: #27AE60
  - Danger red: #E74C3C
  - Warning amber: #F39C12
  - Neutral dark: #2C3E50
  - Light card bg: #FFFFFF with subtle box-shadow effect (use filter or light stroke)
- All shapes should have generous border-radius (rx/ry ≥ 8 for rects).
- NO outlines/strokes on filled shapes — rely on solid color fills and contrast.
- Use drop-shadow filters sparingly for depth on card elements.
- Fonts: font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif.
- Header text: bold, 30-34px, color #2C3E50.
- Body/label text: 13-16px, color #555 or #2C3E50.
- Icons should be simple filled geometric shapes (not line-art).
- viewBox should be 1600 900 (widescreen).
- Use CSS @keyframes for smooth animations: fadeIn, slideUp, scaleIn, etc.
- Animate elements sequentially with staggered delays.
- Total animation duration ~6-8 seconds.
- Make it polished and visually appealing — think Dribbble / Behance quality."""

    timeout = args.timeout
    print(f"Generating animated SVG with {args.model} (streaming, {timeout}s timeout for first chunk)...")

    chunks = []
    char_count = 0
    first_chunk = True

    def _timeout_handler(signum, frame):
        raise TimeoutError(
            f"No response from {args.model} within {timeout}s — "
            "model name may be wrong or the API is unreachable."
        )

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)
    t0 = time.monotonic()

    try:
        for chunk in client.models.generate_content_stream(
            model=args.model,
            contents=f"Create an animated SVG infographic based on this description:\n\n{args.prompt}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,
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
    except (TimeoutError, Exception) as e:
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
