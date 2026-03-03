# The Trust Problem Nobody Wants to Talk About

There's a pattern in technology that keeps repeating. A new capability emerges, everyone rushes to build on it, and the trust layer gets bolted on after the first disaster. We saw it with email (spam), with the web (phishing), with package registries (typosquatting), with browser extensions (malware). Every time, the industry says "we should have thought about this earlier."

We're watching it happen again with AI agent skills.

## What changed

AI agents aren't chatbots anymore. They execute shell commands, call APIs with your credentials, read your files, manage your cloud infrastructure, send emails on your behalf, and orchestrate multi-step workflows that span systems. An MCP-connected agent can reach into your database, your CI pipeline, your Kubernetes cluster. This is enormously powerful. It's also enormously dangerous if the wrong instruction gets in.

A year ago, the worst a bad skill could do was give you a wrong answer. Today, a malicious skill can instruct an agent to read your `.env` file, call your payment API, and exfiltrate data to an attacker-controlled endpoint — all while looking like it's helping you refactor a React component.

The more autonomy we hand to agents, the more the trust question matters. And right now, the trust question is mostly unanswered.

## The vibes era

Today's skill ecosystem works the way early app stores did. You find a skill, the name looks right, the description seems legitimate, the star rating is decent. You install it. This is trust-by-vibes.

We know how this story ends because we've lived it before. npm had `crossenv` (malicious) masquerading next to `cross-env` (legitimate). The Chrome Web Store has been a revolving door of malicious extensions wearing trusted names. Mobile app stores still deal with impersonation and fake reviews at industrial scale.

But the consequences with AI agents are worse than any of these. A browser extension can read your tabs. A malicious AI skill can instruct an agent to read your files, call your APIs with your credentials, and exfiltrate data — all through normal-looking conversation. The attack surface isn't a browser sandbox. It's everything the agent has access to.

We're at a point where the industry needs a real answer. Several good teams are working on this, and they deserve credit. But I think most of them are solving the wrong problem.

## The new approaches — and what they get right

Three efforts stand out.

**Skills.sh** is building an open directory of agent skills — over 82,000 and counting. You install skills via CLI, there's a leaderboard, telemetry-based ranking, routine security audits. It's well-executed and has broad agent support. Skills.sh did something important: it helped establish a shared format (SKILL.md) and proved that a lightweight, agent-agnostic skill ecosystem could work.

**ClawHub** took a similar approach with a curated marketplace — thousands of community-built skills, organized by category, with installation tooling and security scanning. They've built real infrastructure and attracted a real community.

**ERC-8004** went in a fundamentally different direction. It puts agent identity onchain using Ethereum — NFT-based registration, a reputation registry for feedback signals, and a validation registry with pluggable trust models including zero-knowledge proofs and TEE oracles. It's technically sophisticated and thoughtful about the trust problem.

Each of these represents genuine progress. They're all trying to answer the right question: how do you know a skill is what it claims to be?

But they all share a common assumption that I think is wrong. They all assume you have to *create* a new trust infrastructure. A new registry. A new reputation system. A new identity layer. A new smart contract.

What if you don't?

## The boring answer

Here's what I keep coming back to: the internet already solved this problem.

When you visit `https://stripe.com`, you know you're talking to Stripe. Not because a marketplace verified them. Not because they staked ETH. Not because their star rating is 4.8. You know because DNS maps the name, TLS proves the connection, and the certificate authority chain — battle-tested for decades, trusted by every browser, every device, every API client on Earth — vouches for the binding between the name and the server.

This system secures trillions of dollars in online commerce every day. It handles identity for billions of websites. It has been attacked relentlessly for thirty years and, while not perfect, has proven remarkably resilient. DNSSEC adds cryptographic signatures to DNS records. Certificate Transparency logs make misissued certificates publicly auditable. The entire trust chain, from root CAs down to individual TLS handshakes, is deeply integrated into every layer of the internet.

And it already exists. Nobody needs to build it. Nobody needs to bootstrap adoption. Nobody needs to convince anyone to join a new network.

This is the core insight behind the Domain-Verified Skills protocol: **if a skill is served from `https://example-brand.com/skills/support/SKILL.md`, then it is that brand's skill.** Not because someone reviewed it. Not because it was voted on. Because the same infrastructure that secures your bank's website says so.

It sounds almost too simple. That's because it is simple. And that's the point.

## Why domains are better than registries

Let me be specific about why I think domain-based trust is superior to purpose-built registries for this problem.

**They already exist.** Every company already has a domain. Every brand already controls a URL namespace. There's no cold-start problem, no bootstrapping, no "we need a critical mass of participants." The participation pool is literally everyone who has a website, which is to say, everyone who matters for this use case.

Skills.sh has 82,000 skills. ClawHub has a few thousand. ERC-8004 requires registration transactions and gas fees. But there are over 350 million registered domain names in the world. The namespace is already fully populated.

**They're human-readable and machine-readable simultaneously.** A domain name like `example-brand.com` communicates identity to humans in a way that an Ethereum address or a registry ID never will. And it resolves to an IP address, which means machines can verify it programmatically. This dual readability isn't a nice-to-have — it's essential for a system where both humans and AI agents need to make trust decisions.

**They integrate with the entire existing trust chain.** DNS, DNSSEC, TLS, Certificate Authorities, Certificate Transparency, HTTPS, HSTS — these aren't separate systems. They're layers of a deeply integrated trust stack that's been refined through decades of adversarial pressure. When you verify a skill by checking its domain, you're not using one trust signal. You're using all of them.

ERC-8004 builds its own trust stack from scratch — identity registry, reputation registry, validation registry. That's ambitious, but it also means bootstrapping three new trust layers simultaneously. Every new layer is a new attack surface that hasn't been battle-tested. The existing web trust stack has been battle-tested by every state actor, criminal organization, and bored teenager on the planet for thirty years.

**Search engines can index and compete.** Skills served from domains are just HTTPS resources. Google can index them. Bing can index them. Any future skill-specific search engine can crawl them. Discovery becomes a competitive market, not a single registry you have to go through. Sitemap.xml already exists. Web crawling already exists.

With registry-based approaches, discovery is controlled by whoever operates the registry. With domain-based skills, discovery is decentralized by default. This matters more than it sounds — it means no single entity decides which skills are visible and which aren't.

**Publication is self-served and decentralized.** If you own a domain, you can publish skills right now. No approval process. No listing fees. No marketplace account. No publisher certification. Just put a SKILL.md file on your web server and you're a skill publisher.

This is the same principle that made the web work. Nobody needed permission to put up a website. The web grew to billions of pages because publishing was permissionless. Skill publication should work the same way.

**Existing trust is leveraged, not rebuilt.** When Stripe publishes a skill at `stripe.com`, agents trust it because they already trust `stripe.com`. The decades of brand equity, SEO authority, TLS certificate history, DNSSEC deployment — it all transfers automatically. With a new registry, everyone starts from zero. With domains, everyone starts from wherever their web presence already is.

**They're naturally hierarchical.** Domains have structure: `api.example.com`, `skills.example.com`, `example.com/teams/billing/`. This hierarchy maps naturally to organizational structure. Different teams can publish skills under different paths. Subdomains can represent different services. The URL structure reflects real organizational boundaries without requiring any additional metadata.

ERC-8004 tries to solve this with "pluggable trust models" and separate registries. But domains already have a natural hierarchy that mirrors how organizations actually work. You don't need to design it — it emerges from the structure of DNS itself.

**And most importantly: they're trivially verifiable.** Does the skill URL start with the declared trust root? Does the domain match? Does the path prefix match at segment boundaries? Two checks. That's it. No reputation queries, no blockchain lookups, no API calls to a registry service. The verification is so simple that any agent can implement it in a few lines of code, and so fast that it adds zero perceptible latency.

Compare this to ERC-8004's verification: look up the agent's NFT, check the identity registry, query the reputation registry, potentially verify a zero-knowledge proof or contact a TEE oracle. Each step adds latency, complexity, and a potential failure mode. For what? To answer the same question: "Is this skill really from who it claims to be from?"

## What about the things domains don't do?

I want to be honest about the limitations.

Domains don't give you reputation. They don't tell you whether a skill is *good*. They don't give you download counts, star ratings, or community reviews. A brand new domain could publish a perfectly verified but terrible skill.

But here's the thing: reputation and identity are different problems, and conflating them is a mistake. Identity answers "is this really from Stripe?" Reputation answers "is this any good?" You need both, but you need identity *first*. Without identity, reputation is meaningless — you're rating a costume, not a person.

Skills.sh's leaderboard and ClawHub's community ratings do useful things. But they're built on an identity layer that's fundamentally vibes-based. DVS provides the identity layer. Reputation can be built on top by anyone — and it'll be more trustworthy because it's attached to cryptographically verified identities rather than self-declared names.

Domains also don't solve prompt injection, skill sandboxing, or runtime security. They're not meant to. They solve one problem: *who published this skill?* Everything else — sandboxing, consent, auditing — builds on top of that foundation. You can't build a wall on quicksand, and you can't build security on unverified identity.

## Standing on giants' shoulders

When I look at the landscape of solutions, what strikes me is how many teams are trying to reinvent infrastructure that already exists. New registries, new blockchains, new identity systems, new discovery protocols.

DVS does none of that. It takes the existing web trust infrastructure — DNS, TLS, HTTPS, the global PKI — and applies it to a new problem. The protocol itself is intentionally minimal: a skill is a directory with a SKILL.md file, identity is derived from the URL, trust is verified by checking domain and path prefix.

That's it. No new certificate authorities. No new key management. No new consensus mechanisms. No gas fees. No staking. Just the infrastructure that already secures the internet, applied to AI skills.

We formalized this as a Trust Root: the URL prefix that defines who vouches for a skill. For a brand with its own domain, it's the domain origin. For a brand on GitHub, it's their path-scoped prefix. Verification is origin-then-path matching at segment boundaries. Simple, deterministic, and impossible to spoof without compromising the domain itself.

There's a reason we submitted this as an IETF Internet-Draft rather than shipping a proprietary solution. The IETF is where HTTP, TLS, DNS, and WebSocket were standardized. If you're going to build on the internet's trust infrastructure, you should go through the internet's standards process. The draft (`draft-zzn-dvs`) is public, citable, and open to community review. It has a path to becoming an RFC through consensus, not corporate fiat.

This isn't about replacing what Skills.sh, ClawHub, or ERC-8004 are building. Their work on skill formats, discovery, community, and tooling is valuable. What DVS provides is the missing foundation: a verifiable identity layer that all of these systems can anchor to, built on infrastructure the world already trusts.

## The timing argument

Three things are happening simultaneously.

First, agents are gaining real-world capabilities at an accelerating pace. MCP, A2A, tool use, computer use, multi-agent delegation, autonomous coding — the plumbing for agents to act on the world is being built right now. But plumbing without trust is a liability.

Second, every brand will need to publish AI-accessible capabilities. Just as every company needed a website in the 2000s and a mobile app in the 2010s, every company will need skills that agents can discover and invoke. The publishing model matters.

Third, attackers are already paying attention. The ClawHavoc incident — 341 malicious skills discovered on ClawHub in a single month — is a preview, not an anomaly. Prompt injection, skill spoofing, malicious tool definitions — the attack surface is growing faster than the defenses.

The window for building the trust layer is now, while the ecosystem is still taking shape. Retrofitting trust after a major incident is always more expensive and less effective than building it in from the start. Email tried to retrofit trust with SPF, DKIM, and DMARC — thirty years later, spam is still a multi-billion dollar problem. We have a chance to do this right the first time.

## What we're asking

We're not asking anyone to abandon what they've built. We're asking the community to consider that the foundation for skill trust might already exist, and that the simplest approach might also be the most robust one.

Read the draft: [https://datatracker.ietf.org/doc/draft-zzn-dvs/](https://datatracker.ietf.org/doc/draft-zzn-dvs/)

If you're building agent frameworks, skill platforms, or security tools — we'd love your feedback. The draft is a starting point. What we care about is getting the trust model right, and that requires pressure-testing from people who are building in this space.

The infrastructure for verifiable AI skills already exists. It's the same infrastructure that verifies your bank, your email provider, and every website you visit. We just need to use it.

---

*Zainan Victor Zhou, Namefi*
*draft-zzn-dvs — Domain-Verified Skills (DVS) Protocol*

#IETF #AIAgents #AgentProtocol #OpenStandards #DVS
