# Why We Submitted an IETF Draft for Domain-Verified Skills

## AI Agents Are Powerful — and That's the Problem

AI agents aren't toys anymore. They write code, execute shell commands, make API calls, manage files, send emails, and orchestrate multi-step workflows across systems. An agent with MCP tools can reach into your database, your CI pipeline, your cloud infrastructure. This is incredibly useful — and incredibly dangerous if the wrong instruction gets in.

The more powerful agents become, the higher the stakes when they execute something they shouldn't. A misplaced skill from an impersonator isn't just an annoyance — it's a potential data breach, an unauthorized transaction, a supply chain attack through your AI assistant.

**Power demands trust. And right now, the trust layer for AI agent skills doesn't exist.**

## We Need Trust More Than Ever

Today's skill ecosystem works on vibes. You find a skill in a marketplace, the name looks right, the description sounds legitimate, you install it. Sound familiar? It's the same model that gave us typosquatting on npm, malicious browser extensions, and fake apps on mobile stores.

But the consequences with AI agents are worse. A browser extension can read your tabs. A malicious AI skill can instruct an agent to read your files, call your APIs with your credentials, and exfiltrate data — all while looking like it's helping you.

We're handing agents more autonomy every month. Tool use, computer use, multi-agent delegation, autonomous coding — the trajectory is clear. The question isn't whether agents will have broad access to our systems. It's whether we'll have a trust framework in place before they do.

**The time to build that trust layer is now, not after the first major incident.**

## Skills Are New. Verifiability Is Not.

Here's the thing: we don't need to invent trust from scratch. The internet already solved this problem.

When you visit `https://example-brand.com`, you don't need a third party to tell you it's that brand. DNS maps the name. TLS proves the connection. The certificate authority chain has been battle-tested for decades. Every browser, every device, every API client already trusts this infrastructure.

Domain-Verified Skills (DVS) simply extends this proven model to AI agent skills:

**If a skill is served from `https://example-brand.com/skills/support/SKILL.md`, it's that brand's skill.** Not because a marketplace verified it. Not because someone reviewed the code. Because DNS, TLS, and the Web PKI — the same stack that secures trillions of dollars in online commerce — says so.

We call this the Trust Root: the URL origin (and optionally path) that defines who vouches for a skill. For brands with their own domains, it's the domain origin. For brands on GitHub or similar platforms, it's their path-scoped prefix (e.g., `https://github.com/example-org/`). Verification is origin-then-path matching — check the domain first, then the path at segment boundaries. No new infrastructure. No new key management. No new certificate authorities.

The concept of "verified" accounts, verified domains, verified publishers — it's everywhere. DVS just applies it to AI skills using the verification system the internet already has.

## What DVS Actually Specifies

The protocol is intentionally minimal:

- **Skills are directories** with a `SKILL.md` entry point (YAML metadata + Markdown instructions) and optional bundled resources.

- **Discovery** uses `/.well-known/skills/` paths and `sitemap.xml` — existing web infrastructure, nothing new to deploy.

- **Trust verification** is origin-then-path matching: does the skill URL share the same domain and path prefix as the declared Trust Root? The base model is deliberately simple, but the spec acknowledges that future extensions could support subdomain wildcards (`*.example.com`), path patterns, or even regex — though each must be designed carefully, since overly permissive matching can silently widen the trust boundary.

- **Progressive loading** — metadata first (~100 tokens), instructions on trigger, resources on demand. Efficient by design.

- **Same-origin isolation** — a skill can't reach outside its trust boundary without user consent.

- **Composition** — skills can reference other skills via URL, each evaluated against its own Trust Root.

## Why This Matters Now

Three trends are colliding:

**Agents are gaining real-world capabilities.** MCP (Anthropic), A2A (Google), and similar protocols are giving agents the plumbing to act on the world. But plumbing without trust is a liability. When Agent A invokes a skill published by Company B, what's the verification path? Today: none.

**Every brand will need AI-accessible skills.** Just as every company needed a website in the 2000s, every company will need to publish capabilities that AI agents can discover and use. They shouldn't need a gatekeeper's permission.

**Attackers are already paying attention.** Prompt injection, skill spoofing, malicious tool definitions — the attack surface is growing faster than the defenses. DVS doesn't solve everything, but it establishes the foundational identity layer.

## Why an IETF Draft?

We want this to be an open standard. The IETF is where HTTP, TLS, DNS, and WebSocket were built. Submitting `draft-zzn-dvs-00` as an Internet-Draft means:

- The spec is public and citable
- Anyone can review, critique, and contribute
- It can evolve through community consensus
- It has a path to becoming an RFC

This is the starting point, not the finish line.

## What We're Looking For

- **Is the Trust Root model sufficient?** Are there hosting scenarios we haven't considered?
- **Is the security model adequate?** What attack vectors are we missing?
- **How should discovery evolve?** Is sitemap.xml + index.json enough?
- **Should the spec address versioning?** The current draft doesn't — should it?

Read the full draft: https://datatracker.ietf.org/doc/draft-zzn-dvs/

If you're building agent frameworks, platforms, or security tools — we'd love your feedback. Reply here, open an issue, or email zzn@namefi.io.

Agents are powerful. Trust is essential. And the infrastructure for verifiability already exists — we just need to use it.

---

*Zainan Victor Zhou, Namefi*
*draft-zzn-dvs-00 — Domain-Verified Skills (DVS) Protocol*

#IETF #AIAgents #AgentProtocol #OpenStandards #DVS
