---
title: "Domain-Verified Skills (DVS) Protocol"
abbrev: "DVS"
docname: draft-zzn-dvs-latest
category: info
ipr: trust200902
submissiontype: independent

stand_alone: yes
smart_quotes: no
pi: [toc, sortrefs, symrefs]

author:
  -
    fullname: Zainan Victor Zhou
    organization: Namefi
    email: zzn@namefi.io

normative:
  RFC2119:
  RFC3986:
  RFC4033:
  RFC4343:
  RFC7763:
  RFC8174:
  RFC9110:

informative:
  RFC8615:
  CLAUDE-SKILLS:
    title: "Agent Skills Overview"
    author:
      - org: Anthropic
    target: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  SITEMAP:
    title: "Sitemaps XML Format"
    author:
      - org: Sitemaps.org
    target: https://www.sitemaps.org/protocol.html

--- abstract

This document defines the Domain-Verified Skills (DVS) protocol, a
lightweight mechanism for AI Agents to discover, verify, and execute
skill definitions served over HTTPS.  A skill is a directory
containing a SKILL.md entry point and optional bundled resources
that instructs an AI Agent to perform a specific task or adopt a
specific behavior.

The central design principle of DVS is that a skill's identity and
trustworthiness are derived entirely from the HTTPS URL at which it
is served -- no centralized registry or third-party certification is
required.  The operator of the URL's origin is the authoritative
endorser of the skill.

This trust is formalized through the concept of a Trust Root: an
HTTPS URL prefix declared by the skill publisher that scopes the
trust boundary for their skills.  A skill is considered verified
if and only if its URL begins with the declared Trust Root.  For
brands with first-party domains, the Trust Root is the domain
origin.  For brands publishing on user-generated content platforms
where the platform operator does not vouch for individual
publishers, the Trust Root MUST be path-scoped to content the
brand controls, ensuring that trust does not extend to the entire
platform.

The protocol leverages the existing trust infrastructure of the
Domain Name System (DNS) and Transport Layer Security (TLS) and is
backward compatible with skills already served over HTTPS, including
those hosted on GitHub or other platforms.

--- middle

# Introduction

Current AI Agent skills (such as those in the Claude Agent Skills
protocol {{CLAUDE-SKILLS}}) are primarily distributed via centralized
code repositories or platform-specific upload mechanisms.  This
creates several friction points:

- Identity Ambiguity: Users cannot easily verify if a skill hosted
  on a third-party platform genuinely belongs to a brand.

- Hosting Friction: Brands must manage external accounts and
  synchronization instead of using their existing web
  infrastructure.

- Security Risks: Malicious skills can spoof brand names on open
  platforms to exfiltrate data.

The Domain-Verified Skills (DVS) protocol returns to the fundamental
logic of the Web: the URL is the Identity.  By serving skills
directly from a brand-controlled URL prefix, we leverage the existing
global trust of the DNS and HTTPS infrastructure.

For brands with first-party domains, the Trust Root is the domain
itself (e.g., `https://example.com/`).  For brands that publish on
user-generated content platforms such as GitHub or Hugging Face,
the Trust Root is scoped to the brand's path on that platform (e.g.,
`https://github.com/example-org/`).  This allows DVS to provide
brand-verified skill identity across all hosting configurations,
without requiring brands to self-host infrastructure.

This protocol is designed to be compatible with existing skill
formats and distributions.  A skill already hosted on GitHub
(e.g., `https://github.com/example-org/repo/blob/main/.../SKILL.md`)
is immediately usable under DVS by registering
`https://github.com/example-org/` as the Trust Root, with no changes
to the skill files themselves.  In particular, a skill directory
conforming to DVS can be directly consumed by any agent that
understands the SKILL.md convention, while also gaining the identity
and trust properties conferred by domain-verified hosting.

# Conventions and Definitions

{::boilerplate bcp14-tagged}

The following terms are used in this document:

Skill:
: A directory containing a SKILL.md entry point and optional
  bundled resources (scripts, templates, data files, additional
  instructions) that directs an AI Agent to perform a specific task
  or adopt a specific behavior.

SKILL.md:
: The mandatory Markdown entry-point file within a skill
  directory.  It contains YAML frontmatter metadata and human-
  readable instructions for the Agent.

Agent:
: An AI system capable of fetching, interpreting, and executing
  Skill instructions.

Skill URL:
: The HTTPS URL of the skill directory (or its SKILL.md
  entry point).  This URL serves as the globally unique identifier
  of the Skill.

Trust Root:
: An HTTPS URL prefix that defines the trust boundary for a skill
  or set of skills.  A skill is considered verified under a Trust
  Root if and only if its Skill URL matches the Trust Root by
  origin-then-path verification (see {{trust-root-verification}}).
  For first-party brand domains, the Trust Root is
  typically the domain origin (e.g., `https://example.com/`).
  For user-generated content platforms, the Trust Root MUST be
  scoped to a path controlled by the brand (e.g.,
  `https://github.com/example-org/`).

Hosting Domain:
: The domain component of the Trust Root URL, considered the
  network-level endorser of the Skill via DNS and TLS.

Bundled Resource:
: Any file within the skill directory other than
  SKILL.md, including additional instruction files, executable
  scripts, templates, schemas, and data files.

# Core Protocol

The identity of a skill is defined strictly by its HTTPS URL.

## Identity and Trust

Skills MUST be served via HTTPS {{RFC9110}}.  Agents MUST NOT fetch or
execute skills served over plain HTTP.

The identity and trust of a skill is defined by its Trust Root.  A
skill is considered verified under a Trust Root only when the
verification procedure in {{trust-root-verification}} succeeds.

For first-party brand hosting, the Trust Root is the domain origin:

    Trust Root: https://example.com/
    Skill URL:  https://example.com/skills/support/SKILL.md

For user-generated content platforms, the Trust Root MUST be scoped
to a path controlled by the brand.  Agents MUST NOT accept a bare
UGC platform domain (e.g., `https://github.com/`) as a Trust Root,
as this would confer trust to all content on the platform:

    Trust Root: https://github.com/example-org/
    Skill URL:  https://github.com/example-org/
                repo/blob/main/skills/SKILL.md

A skill URL that fails Trust Root verification MUST be rejected by
the Agent.

### Trust Root Verification {#trust-root-verification}

To verify that a Skill URL belongs to a declared Trust Root, agents
MUST perform origin-then-path matching rather than a naive string
prefix check.  A simple string prefix comparison is insecure because
an attacker could register a domain such as `example.com.evil.com`
or a path such as `github.com/example-org-malicious/` that would
pass a prefix test.

The verification procedure is:

1. Parse both the Trust Root URL and the Skill URL per {{RFC3986}}.

2. Verify that the scheme of both URLs is `https`.

3. Verify that the host component of the Skill URL exactly matches
   the host component of the Trust Root URL.  This comparison MUST
   be case-insensitive per {{RFC4343}}.

4. Verify that the path component of the Skill URL starts with the
   path component of the Trust Root URL, using segment-by-segment
   comparison.  The Trust Root path MUST end with `/` to ensure
   matching occurs at a path segment boundary (e.g., Trust Root
   path `/example-org/` matches Skill path `/example-org/repo/...`
   but does NOT match `/example-org-malicious/...`).

All four checks MUST pass for verification to succeed.

### Trust Root Extensions {#trust-root-extensions}

The base Trust Root model uses exact domain matching and path-prefix
matching.  Future extensions MAY allow additional scoping mechanisms,
including but not limited to:

- **Subdomain matching:** A Trust Root of `https://*.example.com/`
  could allow skills hosted on any subdomain (e.g.,
  `skills.example.com`, `api.example.com`).

- **Path pattern matching:** A Trust Root could use glob-style
  patterns (e.g., `https://example.com/teams/*/skills/`) to allow
  multiple path hierarchies.

- **Regular expression matching:** A Trust Root could specify a
  regex pattern for more flexible URL matching.

Implementors SHOULD exercise caution when designing such extensions.
Overly permissive matching rules can inadvertently widen the trust
boundary and create security vulnerabilities.  In particular:

- Subdomain wildcards risk matching attacker-controlled subdomains
  on platforms that allow user-created subdomains.
- Regex patterns are difficult to audit, may exhibit catastrophic
  backtracking, and can be error-prone in ways that silently widen
  the trust scope.

Any Trust Root extension mechanism MUST be opt-in, clearly documented,
and subject to the same security analysis as the base verification
procedure.  This document does not define the syntax or semantics
of any extension; such work is deferred to future specifications.

## Discovery

Skills MAY be hosted at any valid URL path on a domain (e.g.,
`https://example.com/skills/my-assistant/SKILL.md`).  There is no
mandatory path structure; domain operators choose the URL layout
that fits their infrastructure.

Domain operators managing sensitive first-party skills MAY place
them under the `/.well-known/skills/` path prefix per {{RFC8615}},
but this is not required.

Skills MAY be indexed in the domain's `sitemap.xml` {{SITEMAP}} to
enable automated agent discovery.  Agents supporting discovery SHOULD
check for skill entries in the sitemap when exploring a domain's
available skills.

A domain MAY serve a skill index document (e.g., at a path such as
`/skills/index.json`).  The index document, if present, SHOULD
contain an array of objects, each with `name`, `description`, and
`path` fields pointing to available skills on the domain.

# Skill Specification

## Directory Structure

A Domain-Verified Skill is a directory containing at minimum a SKILL.md
file.  The directory MAY contain additional files organized by
purpose:

~~~
my-skill/
+-- SKILL.md              (entry point - REQUIRED)
+-- ADVANCED.md           (additional instructions - OPTIONAL)
+-- REFERENCE.md          (detailed reference docs - OPTIONAL)
+-- scripts/
|   +-- process.py        (executable script - OPTIONAL)
|   +-- validate.sh       (executable script - OPTIONAL)
+-- templates/
|   +-- report.html       (template file - OPTIONAL)
+-- data/
    +-- schema.json       (data/reference file - OPTIONAL)
~~~

When served over HTTPS, the directory structure is represented by
URL paths relative to the skill's base URL.  For example, a skill
at `https://example.com/skills/my-skill/` would have its entry
point at:

    https://example.com/skills/my-skill/SKILL.md

And a bundled script at:

    https://example.com/skills/my-skill/scripts/process.py

## SKILL.md Entry Point

Every skill directory MUST contain a file named `SKILL.md`.  This
file MUST be encoded in UTF-8 and served with the media type
`text/markdown` {{RFC7763}}.

The file consists of two parts:

1. YAML frontmatter (metadata) - REQUIRED
2. Markdown body (instructions) - REQUIRED

## Metadata (Frontmatter)

SKILL.md files MUST begin with a YAML frontmatter block delimited
by `---` lines.  The frontmatter MUST contain the following fields:

name:
: A short, human-readable name for the skill.
  MUST NOT exceed 64 characters.
  MUST contain only lowercase letters, numbers, and hyphens.

description:
: A brief description of the skill's purpose and
  capabilities, including guidance on when an Agent should trigger
  the skill.
  MUST NOT be empty.
  MUST NOT exceed 1024 characters.

Example:

~~~
name: customer-support
description: Handles common customer support inquiries for
  Acme Corp products. Use when the user asks about product
  returns, warranty claims, or order status.
~~~

## Instructions (Body)

The body of SKILL.md, following the frontmatter, MUST contain
human-readable instructions for the Agent.  These instructions
define the behavior, constraints, and capabilities of the skill.

Instructions SHOULD be written as clear, step-by-step procedural
guidance.  They MAY reference bundled resources using relative URLs
(e.g., `[see advanced guide](ADVANCED.md)` or `run the script at
scripts/process.py`).

## Bundled Resources

Skills MAY include additional files alongside SKILL.md.  These
bundled resources fall into three categories:

### Additional Instructions

Additional Markdown files (e.g., ADVANCED.md, REFERENCE.md,
FORMS.md) provide specialized guidance, detailed API references,
or extended workflows.  These files:

- SHOULD use the `.md` extension and `text/markdown` media type.
- Are loaded by the Agent only when referenced from SKILL.md or
  when the task context requires them.

### Executable Scripts

Scripts (e.g., Python, Shell, JavaScript) provide deterministic
operations that the Agent can execute.  These files:

- MUST reside within the same skill directory (same-origin).
- Are executed by the Agent via its runtime environment; only the
  script's output enters the Agent's context, not the script
  source code itself.
- MUST be subject to the Explicit Consent requirement defined in
  {{explicit-consent}} before execution.

### Data and Reference Materials

Data files (e.g., JSON schemas, CSV datasets, configuration
templates, API documentation) provide factual lookup material.
These files:

- MUST reside within the same skill directory (same-origin).
- Are read by the Agent on demand when the task requires specific
  reference information.
- Impose no context cost until actually accessed.

## Progressive Loading

Agents implementing DVS SHOULD employ a progressive loading strategy
to manage context efficiently:

Level 1 - Metadata (always loaded):
: The YAML frontmatter (name and description) is loaded at agent
  startup or skill registration time.  This enables skill discovery
  with minimal token cost (approximately 100 tokens per skill).

Level 2 - Instructions (loaded on trigger):
: The body of SKILL.md is fetched and loaded into the agent's
  context only when the skill is triggered by a matching user
  request.

Level 3 - Resources (loaded as needed):
: Bundled resources (additional markdown files, scripts, data
  files) are accessed only when referenced during execution.
  Scripts are executed and only their output is loaded into context.

This three-level approach ensures that a domain can publish many
skills without imposing context overhead on agents, as only the
metadata of registered skills is persistently loaded.

# Security and Permissions

## Same-Origin Isolation

Agents MUST restrict a skill's automated access to resources within
its Trust Root prefix.  A skill with Trust Root
`https://github.com/example-org/` MUST NOT
be permitted to automatically access resources outside that prefix
(including other GitHub users or repos) without explicit user
consent.

Bundled resources (scripts, data files, templates) referenced by a
skill MUST reside within the same Trust Root prefix as the SKILL.md
file.  Agents MUST reject references to resources outside the
skill's Trust Root unless the user explicitly approves the access.

This prevents a compromised or malicious skill from leveraging its
trusted context to exfiltrate data from, or perform actions on,
unrelated origins or paths.

## Explicit Consent {#explicit-consent}

Agents MUST display the source domain to the user and request
explicit confirmation before executing any non-textual instructions
contained in a skill (e.g., shell commands, API calls, file system
operations, running bundled scripts).

The consent prompt SHOULD clearly indicate:

- The Trust Root of the skill.
- A description of the action to be performed.
- Any resources that will be accessed or modified.

Textual instructions (Markdown content) MAY be loaded without
additional consent beyond the initial skill activation.  Executable
content (scripts, commands) MUST always require explicit consent.

## DNSSEC

Domain operators SHOULD deploy DNSSEC {{RFC4033}} to prevent DNS
spoofing attacks that could redirect agents to malicious skill
files hosted on attacker-controlled infrastructure.

# Composition

A skill MAY reference other skills via their full HTTPS URLs.  When
an Agent encounters a referenced skill URL during execution, it
SHOULD dynamically fetch and load the referenced skill if the current
context requires the extended capabilities it provides.

Each referenced skill is subject to its own Trust Root's trust and
security policies.  Agents MUST apply the Same-Origin Isolation
policy ({{same-origin-isolation}}) independently to each loaded skill
based on its own Trust Root.

When composing skills across domains, agents SHOULD clearly
communicate to the user that the trust context is being extended
to additional domains.

# Security Considerations

The primary security property of this protocol is that trust is
anchored to domain ownership.  This inherits both the strengths and
weaknesses of the existing Web PKI and DNS infrastructure.

Skill spoofing is mitigated by the HTTPS requirement, which ensures
that only the legitimate operator of a domain can serve skills from
that domain.  DNSSEC ({{dnssec}}) provides an additional layer of
protection against DNS-level attacks.

Agents implementing this protocol should be aware of the following
risks:

- Domain compromise: If a domain is compromised, all skills served
  from it should be considered compromised.

- Subdomain delegation: Skills on subdomains should be treated as
  distinct trust contexts from the parent domain.

- UGC platform Trust Roots: On user-generated content platforms,
  agents MUST enforce path-scoped Trust Roots.  Accepting a bare
  platform domain (e.g., `https://github.com/`) as a Trust Root
  would allow any user on that platform to publish skills that
  appear equally trusted as a legitimate brand's skills.

- Transitive trust in composition: When skills reference other
  skills ({{composition}}), the trust chain extends across domains.
  Agents should clearly communicate this to users.

- Script execution: Bundled scripts execute with the permissions
  of the agent's runtime environment.  Malicious scripts could
  perform unauthorized file access, network calls, or data
  exfiltration.  The Explicit Consent requirement ({{explicit-consent}})
  mitigates this risk, but agents SHOULD also sandbox script
  execution where possible.

- External resource fetching: Skills that instruct agents to fetch
  data from external URLs pose particular risk, as fetched content
  may contain malicious instructions.  Agents SHOULD treat
  externally-fetched content as untrusted.

# IANA Considerations

This document has no IANA actions.

--- back

# Acknowledgments
{:numbered="false"}

The authors would like to thank the broader AI agent community for
discussions that informed this protocol design.
