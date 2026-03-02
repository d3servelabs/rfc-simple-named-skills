# Domain-Verified Skills (DVS) Protocol

An IETF Internet-Draft defining the Domain-Verified Skills (DVS) protocol — a lightweight mechanism for AI agents to discover, verify, and execute skill definitions served over HTTPS.

**Draft:** `draft-zhou-dvs-00`
**Author:** Zainan Victor Zhou (Namefi)
**Category:** Informational

## Overview

DVS enables AI agents to consume skills from any HTTPS URL without a centralized registry. A skill's identity and trustworthiness derive entirely from the URL at which it is served — the HTTPS origin operator is the authoritative endorser.

**Trust Root** is the core concept: an HTTPS URL prefix declared by the skill publisher that scopes the trust boundary. A skill is verified if and only if its URL begins with the declared Trust Root.

- First-party domains: Trust Root = origin (e.g., `https://microsoft.com/`)
- UGC platforms (GitHub, etc.): Trust Root = path-scoped to the publisher's content (e.g., `https://github.com/microsoft/`) — trust does NOT extend to the entire platform

The protocol reuses existing DNS and TLS trust infrastructure and is backward-compatible with skills already served over HTTPS.

## Repository Contents

| File | Description |
|------|-------------|
| `draft-zhou-dvs-00.md` | Source document (kramdown-rfc Markdown) |
| `draft-zhou-dvs-00.xml` | Generated RFCXML |
| `draft-zhou-dvs-00.txt` | Generated plain-text RFC output |
| `Makefile` | Build toolchain |
| `setup.sh` | Dependency setup script |
| `pre-commit-hook.sh` | Git pre-commit hook for auto-building |

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
make          # produces draft-zhou-dvs-00.txt
make clean    # remove generated files
```

The build pipeline: `draft-zhou-dvs-00.md` → `draft-zhou-dvs-00.xml` → `draft-zhou-dvs-00.txt`

### Auto-build on commit

Install the pre-commit hook to automatically rebuild on each commit:

```sh
cp pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## Key Protocol Concepts

- **Skill:** A directory containing a `SKILL.md` entry point and optional bundled resources, served over HTTPS
- **Trust Root:** An HTTPS URL prefix that scopes the publisher's trust boundary
- **Verification:** A skill URL MUST begin with the declared Trust Root to be considered verified
- **Discovery:** Leverages `/.well-known/` endpoints and DNS/TLS for decentralized discovery

## References

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) — Key words for use in RFCs
- [RFC 4033](https://www.rfc-editor.org/rfc/rfc4033) — DNS Security Introduction
- [RFC 8615](https://www.rfc-editor.org/rfc/rfc8615) — Well-Known URIs
- [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — Anthropic's skill protocol

## License

This document is submitted as an independent submission to the IETF under the trust200902 IPR policy.
