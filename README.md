# Domain-Verified Skills (DVS) Protocol

An IETF Internet-Draft defining the Domain-Verified Skills (DVS) protocol — a lightweight mechanism for AI agents to discover, verify, and execute skill definitions served over HTTPS.

**Draft:** `draft-zzn-dvs` (run `make version` for the current revision)
**Author:** Zainan Victor Zhou (Namefi)
**Category:** Informational

## Overview

DVS enables AI agents to consume skills from any HTTPS URL without a centralized registry. A skill's identity and trustworthiness derive entirely from the URL at which it is served — the HTTPS origin operator is the authoritative endorser.

**Trust Root** is the core concept: an HTTPS URL prefix declared by the skill publisher that scopes the trust boundary. A skill is verified via origin-then-path matching — the domain must match exactly, then the path must match at segment boundaries.

- First-party domains: Trust Root = origin (e.g., `https://example.com/`)
- UGC platforms (GitHub, etc.): Trust Root = path-scoped to the publisher's content (e.g., `https://github.com/example-org/`) — trust does NOT extend to the entire platform

The protocol reuses existing DNS and TLS trust infrastructure and is backward-compatible with skills already served over HTTPS.

## Repository Contents

| File | Description |
|------|-------------|
| `draft-zzn-dvs.md` | Source document (kramdown-rfc Markdown) |
| `gen/draft-zzn-dvs-XX.xml` | Generated RFCXML (in `gen/`) |
| `gen/draft-zzn-dvs-XX.txt` | Generated plain-text RFC output (in `gen/`) |
| `Makefile` | Build toolchain |
| `setup.sh` | Dependency setup script |
| `pre-commit-hook.sh` | Git pre-commit hook for auto-building |
| `KNOWN_ISSUES.md` | Known tooling issues and workarounds |

## Building

### Prerequisites

- Ruby 3.3.0 (via [chruby](https://github.com/postmodern/chruby))
- [`kramdown-rfc`](https://github.com/cabo/kramdown-rfc) gem
- [`xml2rfc`](https://xml2rfc.tools.ietf.org/) tool

Run the setup script to install dependencies:

```sh
./setup.sh
```

### Build

```sh
make          # produces gen/draft-zzn-dvs-XX.txt
make clean    # remove generated files
```

The build pipeline: `draft-zzn-dvs.md` → `gen/draft-zzn-dvs-XX.xml` → `gen/draft-zzn-dvs-XX.txt`

### Submitting to IETF Datatracker

```sh
make submit   # upload the current XML draft to the IETF submission API
```

Requires `IETF_API_KEY` and `IETF_AUTHOR_EMAIL` to be set in `.env`. Note that the IETF submission window closes during IETF meeting weeks.

### Versioning and Tagging

The draft revision number is managed via `REVISION` in the Makefile.

```sh
make version   # print current draft identifier (e.g. draft-zzn-dvs-00)
make tag       # create an annotated git tag for the current revision
make bump      # increment REVISION (e.g. 00 → 01)
```

Typical release workflow:

1. Finalize work on the current revision
2. `make tag` — tags the current commit (e.g. `draft-zzn-dvs-00`)
3. `make bump` — updates `REVISION` in the Makefile for the next iteration
4. Commit the bumped Makefile

### Auto-build on commit

Install the pre-commit hook to automatically rebuild on each commit:

```sh
cp pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Key Protocol Concepts

- **Skill:** A directory containing a `SKILL.md` entry point and optional bundled resources, served over HTTPS
- **Trust Root:** An HTTPS URL prefix that scopes the publisher's trust boundary
- **Verification:** Origin-then-path matching — domain must match exactly, path must match at segment boundaries
- **Discovery:** Leverages `/.well-known/` endpoints and DNS/TLS for decentralized discovery

## References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs
- [RFC 4033](https://www.rfc-editor.org/rfc/rfc4033) — DNS Security Introduction
- [RFC 8615](https://www.rfc-editor.org/rfc/rfc8615) — Well-Known URIs
- [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — Anthropic's skill protocol

## License

This document is submitted as an independent submission to the IETF under the trust200902 IPR policy.
