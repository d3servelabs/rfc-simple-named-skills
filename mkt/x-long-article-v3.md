# Standing on Giants' Shoulders: Why We Submitted an IETF Draft for AI Skill Trust

## 1. Agents Are Dangerously Powerful

Here's a question nobody seems to be asking loudly enough: what happens when the thing you're trusting with your API keys, your database credentials, your cloud infrastructure, and your CI pipeline takes instructions from a stranger?

That's the situation we're in right now with AI agents.

A year ago, agents were glorified chatbots. They could generate text, answer questions, maybe write some code you'd copy-paste into a file. The worst-case failure mode was a wrong answer. You'd roll your eyes, fix it, move on.

That era is over. Today's agents execute shell commands. They call APIs with your credentials. They read and write files on your machine. They manage cloud infrastructure, send emails on your behalf, orchestrate multi-step workflows that span systems. An MCP-connected agent can reach into your database, trigger your CI pipeline, spin up containers in your Kubernetes cluster. Tools like computer use let agents click through your actual desktop. Multi-agent delegation means Agent A can invoke Agent B, who invokes Agent C, each with its own expanding sphere of access.

This is extraordinarily powerful. It's also extraordinarily dangerous when the wrong instruction gets in. A malicious skill can instruct an agent to read your `.env` file, call your payment API, and exfiltrate data to an attacker-controlled endpoint — all while appearing to help you refactor a React component. The agent doesn't know it's being malicious. It's just following instructions. That's what agents do.

Power demands trust. The more capable agents become, the more it matters that every instruction they follow comes from who it claims to come from. And right now, for the vast majority of the skill ecosystem, nobody is checking.

## 2. Current Trust Is Vibes-Based

So how do people decide which skills to trust today? The same way they decided which npm packages to trust in 2015, which Chrome extensions to trust in 2018, which mobile apps to trust in 2012. They look at the name. They read the description. They check the star rating. They install it.

This is trust-by-vibes.

The skill's name looks like it belongs to a legitimate brand? Good enough. The description mentions the right product? Seems legit. A few hundred downloads? Must be safe. This is the same model that gave us `crossenv` masquerading next to `cross-env` on npm. The same model that let malicious extensions sit in the Chrome Web Store for months wearing trusted names. The same model that still floods mobile app stores with impersonation and fake reviews at industrial scale.

We know how this movie ends because we've seen it three times already. And each time, the industry says "we should have built the trust layer earlier." Each time, the trust layer gets retrofitted after the damage is done. Email didn't get SPF and DKIM until spam was already a multi-billion dollar problem. Package registries didn't get signing until supply chain attacks were routine.

But here's what makes the AI agent version worse than all the previous iterations: the blast radius. A malicious browser extension can read your tabs. A malicious npm package can run code during installation. A malicious AI skill can instruct an agent to do *anything the agent has access to* — which, increasingly, is everything. Read your files. Call your APIs with your credentials. Send emails. Execute arbitrary commands. And it does all of this through natural language, which means there's no binary to scan, no signature to check, no sandbox to contain it. The attack surface is the entire capability set of the agent.

The ClawHavoc incident — 341 malicious skills discovered on ClawHub in a single month — is a preview. Not an anomaly. A preview.

Several smart teams are working on this problem. Skills.sh has built an impressive open directory with over 82,000 skills, broad agent support, and a community-driven leaderboard. ClawHub offers curated categories with installation tooling and security scanning. ERC-8004 took a fundamentally different approach with onchain identity — NFT-based registration, a reputation registry, pluggable validation through zero-knowledge proofs and TEE oracles. These are all genuine efforts by people who see the problem clearly.

But they all share an assumption I think is wrong: that you need to *build* trust infrastructure. A new registry. A new reputation system. A new blockchain. A new identity layer.

What if the trust infrastructure already exists?

## 3. The Internet Already Solved Identity

When you visit `https://stripe.com`, you know you're talking to Stripe. Not because a marketplace verified them. Not because they staked ETH. Not because their star rating is 4.8. You know because DNS maps the name to an address, TLS proves you're connected to the right server, and the certificate authority chain — battle-tested for decades, trusted by every browser, every device, every API client on Earth — vouches for the binding.

This system secures trillions of dollars in commerce every day. It handles identity for billions of websites. It has been attacked relentlessly for thirty years by every state actor, criminal organization, and bored teenager on the planet, and while not perfect, it has proven remarkably resilient. DNSSEC adds cryptographic signatures to DNS records. Certificate Transparency logs make misissued certificates publicly auditable. HSTS prevents downgrade attacks. The entire trust chain, from root CAs to individual TLS handshakes, is deeply integrated into every layer of the internet.

And it already exists. Nobody needs to build it. Nobody needs to bootstrap adoption. Nobody needs to convince anyone to join a new network or buy into a new token.

This is what keeps striking me about the current landscape of AI skill trust proposals: so many teams are building elaborate new trust infrastructure when the most battle-tested identity system in human history is sitting right there, free to use.

Domains are human-readable and machine-readable simultaneously. `stripe.com` communicates identity to a human in a way that `0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D` never will. And it resolves to an IP address that machines can verify programmatically. This dual readability isn't a convenience — it's essential for a system where both humans and AI agents need to make trust decisions.

Domains integrate with the entire existing trust chain. DNS, DNSSEC, TLS, Certificate Authorities, Certificate Transparency, HTTPS — these aren't separate systems. They're layers of a deeply integrated stack refined through decades of adversarial pressure. When you verify identity by checking a domain, you're not using one trust signal. You're using all of them simultaneously.

Domains are naturally hierarchical. `api.example.com`, `skills.example.com`, `example.com/teams/billing/` — this structure maps directly to organizational boundaries. Different teams publish under different paths. Subdomains represent different services. The URL hierarchy mirrors how organizations actually work, without requiring any metadata schema to express it.

Search engines can already index domains. Skills served from domains are just HTTPS resources. Google can crawl them. Bing can index them. Any future skill-specific search engine can discover them. Discovery becomes a competitive market, not a single registry that controls visibility.

And most importantly: domains are trivially verifiable. Does the skill URL share the same domain and path prefix as the declared trust root? Two checks. That's it. No reputation queries, no blockchain lookups, no API calls to a registry service. Any agent can implement this in a few lines of code, and it adds zero perceptible latency.

Compare this to verifying identity through a purpose-built registry — looking up NFTs, querying reputation scores, potentially verifying zero-knowledge proofs. Each step adds latency, complexity, and a potential failure mode. All to answer the same binary question: "Is this really from who it claims to be from?"

The boring answer is usually the right one. The internet already solved identity. We should use its solution.

## 4. DVS Is Intentionally Minimal

There's a temptation, when you're writing a protocol, to solve everything. Add a reputation layer. Add a discovery engine. Add a versioning system. Add a permissions model. Add a governance framework.

We resisted that temptation.

The Domain-Verified Skills protocol specifies almost nothing new. A skill is a directory with a SKILL.md entry point — YAML metadata plus Markdown instructions. That's the format. Identity is derived entirely from the HTTPS URL at which the skill is served. Trust is verified by checking that the skill URL matches the declared Trust Root at origin and path-prefix boundaries.

That's the entire protocol. No new packaging format. No build steps. No signing ceremonies. No manifest schemas. No key management. No custom sandbox.

This minimalism is a feature, not a limitation. Here's why.

The protocol leverages progressive loading: metadata first (about 100 tokens — the skill's name and description), full instructions only when the skill is triggered, bundled resources only when referenced during execution. A domain can publish a thousand skills and agents only pay context cost for the ones they actually use. Current marketplace approaches tend to require downloading entire skill packages upfront, most of which goes unused.

Same-origin isolation falls out naturally from URL scoping. A skill can't reach outside its Trust Root prefix without explicit user consent. No custom sandboxing engine, no kernel-level isolation, no policy language. The URL boundary *is* the security boundary. It's the same principle that makes the browser same-origin policy work — one of the most successful security boundaries in the history of software.

The skill format itself is deliberately human-readable. YAML frontmatter for metadata, Markdown for instructions. Any developer can read it. Any agent can parse it. No proprietary SDK, no platform-specific build chain, no binary format.

When I look at what other skill systems require — build steps, manifests, signing, compression, schema validation, platform-specific uploads — I think of the famous Perlis epigram: "Simplicity does not precede complexity, but follows it." We didn't arrive at minimalism by being lazy. We arrived at it by realizing that most of the complexity in other approaches exists to compensate for the lack of a trust root — and once you have a trust root anchored to DNS, most of that complexity becomes unnecessary.

## 5. Every Brand Will Need to Publish Skills

There's a wave coming that most companies aren't ready for.

In the early 2000s, every company needed a website. It seems obvious in retrospect, but at the time it wasn't. Many businesses thought their customers would always pick up the phone or walk into a store. In the early 2010s, every company needed a mobile presence. Again, obvious now, controversial then. Many businesses thought mobile was a fad or only for consumer apps.

We're at the beginning of the same transition for AI agent skills. Every company will need to publish capabilities that AI agents can discover and invoke. Your customer support skill, your API integration skill, your product documentation skill — these will be how agents interact with your brand.

The publishing model matters enormously. If skill publication requires going through a centralized marketplace — creating accounts, paying listing fees, getting approved, maintaining publisher profiles — you're recreating the app store model with all its gatekeeping, rent-seeking, and bottlenecks. You're asking brands to get permission to publish information about their own products and services.

With domain-based publishing, the cost of entry is zero. If you have a website, you can publish skills. No approval process. No listing fees. No marketplace account. No certification program. Just put a SKILL.md file on your web server and you're a skill publisher. This is the same principle that made the World Wide Web explode: permissionless publishing. Nobody needed AOL's approval to put up a website. The web grew to billions of pages because the barrier to entry was essentially nothing.

And existing trust transfers immediately. When Stripe publishes a skill at `stripe.com`, agents trust it because they already trust `stripe.com`. Decades of brand equity, SEO authority, TLS certificate history — it all carries over. With a new registry, every brand starts from zero regardless of how established they are. With domains, everyone starts from wherever their web presence already is.

The companies that understand this will have a significant advantage. They'll publish skills on their own domains, indexed by search engines, discoverable by any agent, verified by the same infrastructure that secures everything else they do online. The companies that don't will be fighting for visibility in marketplace listings, competing with impersonators, and paying rent to stand on what should be public land.

## 6. Autonomy Is Accelerating Faster Than Defenses

Three trends are converging, and the gap between them is growing.

MCP (Anthropic), A2A (Google), and similar protocols are giving agents the plumbing to act on the world. Tool use lets agents call functions. Computer use lets agents interact with desktop applications. Multi-agent delegation lets agents invoke other agents. Autonomous coding lets agents write, test, and deploy software. The trajectory is clear: agents will have broad, deep access to our systems. The only question is when.

Meanwhile, every protocol, framework, and platform is making agents *more* autonomous. More capable of acting without human oversight. More able to chain together complex multi-step operations. More empowered to delegate tasks across boundaries.

And on the other side of the equation: trust verification at the skill layer is essentially nonexistent. When Agent A invokes a skill published by Company B, which triggers a tool from Provider C, what's the verification path? Today, there isn't one.

This is like turning up the volume on an amplifier without testing what's plugged into the input. If the input is clean, you get amplified value. If the input is malicious, you get amplified damage. Autonomy is an amplifier. Without verification at the input, more autonomy means more risk, not more safety.

The window for building the trust layer is now, while the ecosystem is still forming. Retrofitting trust into a mature ecosystem is orders of magnitude harder than building it in from the start. Every major trust system that was retrofitted — email authentication, package signing, certificate transparency — took years to reach adoption and still hasn't fully solved the problem. The systems that built trust in from the beginning — HTTPS, TLS, the Web PKI — became invisible, ubiquitous infrastructure.

DVS is designed to be adopted before it's urgently needed, so that when the urgency arrives — and it will — the foundation is already in place. The protocol is simple enough that any agent framework can implement it today. The infrastructure it relies on is already deployed everywhere. The only thing missing is consensus that this is the right approach.

## 7. Open Standards Beat Proprietary Conventions

There's a reason we submitted this as an IETF Internet-Draft rather than shipping a proprietary solution.

Proprietary skill platforms — however well-intentioned — create walled gardens. You publish in their format, using their SDK, through their portal, under their terms. Your skills work with agents that integrate with their platform and don't work with agents that don't. Your discovery is controlled by their algorithms. Your identity is defined by their registry.

This is fine for a while. It's how new markets often start — someone builds a good product and a community forms around it. But long-term, proprietary conventions fracture the ecosystem. Publishers have to maintain skills in multiple formats across multiple registries. Agents have to integrate with multiple discovery systems. Users can't easily compare skills across platforms. And every platform becomes a chokepoint for rent-seeking.

Open standards solve this by establishing a shared foundation that anyone can build on.

The IETF is where HTTP, TLS, DNS, WebSocket, and the protocols that underpin the internet were standardized. It's the right venue for a protocol that builds on those same foundations. Submitting `draft-zzn-dvs` means the specification is public and citable, anyone can review and critique it, it evolves through community consensus rather than corporate fiat, and it has a defined path to becoming an RFC.

But there's a deeper reason open standards matter here, beyond the usual arguments about interoperability and vendor lock-in: the trust layer needs to be bigger than any single platform.

If the trust layer for AI skills is controlled by one company, that company becomes a single point of failure and a single point of control. If they get compromised, the entire ecosystem's trust is compromised. If they change their policies, every publisher and every agent is affected. If they go out of business, the trust layer disappears.

Domain-based trust doesn't have this problem because there is no single entity operating it. DNS is operated by thousands of registrars. TLS certificates are issued by dozens of CAs. The web PKI is governed by the CA/Browser Forum. No single company controls any of it, and none of them can unilaterally change the rules.

DVS inherits this decentralization. Any company can publish skills on their domain. Any agent can verify skills using standard HTTPS. Any search engine can discover skills by crawling the web. No single entity is a gatekeeper, a bottleneck, or a single point of failure.

This is what "standing on giants' shoulders" really means. We're not building a new tower. We're extending one that's already taller, stronger, and more widely trusted than anything we could build from scratch.

---

## What We're Asking

We're not asking anyone to abandon what they've built. Skills.sh's directory, ClawHub's community, ERC-8004's onchain innovation — these efforts have value. What we're asking is whether the *foundation* for skill trust should be new infrastructure or existing infrastructure. Whether identity should be something you build or something you inherit from the most successful identity system ever created.

Read the draft: [https://datatracker.ietf.org/doc/draft-zzn-dvs/](https://datatracker.ietf.org/doc/draft-zzn-dvs/)

If you're building agent frameworks, skill platforms, or security tools — we'd love your feedback. The spec is a starting point. What matters is getting the trust model right, and that requires pressure-testing from people who are building in this space.

The infrastructure for verifiable AI skills already exists. It's the same infrastructure that verifies your bank, your email provider, and every website you visit. We just need to use it.

---

*Zainan Victor Zhou, Namefi*
*draft-zzn-dvs — Domain-Verified Skills (DVS) Protocol*

#IETF #AIAgents #AgentProtocol #OpenStandards #DVS
