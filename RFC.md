```
Internet-Draft                                                Z. V. Zhou
Intended status: Proposed Standard                               Namefi
Expires: September 2026                                     March 2026


         Simple Named Skills (SNS) Protocol

Abstract

   This document defines the Simple Named Skills (SNS) protocol, a
   lightweight mechanism for AI Agents to discover, verify, and execute
   skill definitions served as Markdown files over HTTPS.  The protocol
   leverages the existing trust infrastructure of the Domain Name System
   (DNS) and Transport Layer Security (TLS) to establish skill identity
   and authenticity, eliminating the need for centralized skill
   registries.

Status of This Memo

   This Internet-Draft is submitted to the community for discussion.
   Distribution of this memo is unlimited.

Copyright Notice

   Copyright (c) 2026 Namefi.  All rights reserved.

Table of Contents

   1.  Introduction  . . . . . . . . . . . . . . . . . . . . . . .  1
   2.  Conventions and Definitions . . . . . . . . . . . . . . . .  2
   3.  Core Protocol . . . . . . . . . . . . . . . . . . . . . . .  2
     3.1.  Identity and Trust  . . . . . . . . . . . . . . . . . .  2
     3.2.  Discovery . . . . . . . . . . . . . . . . . . . . . . .  3
   4.  Skill Specification . . . . . . . . . . . . . . . . . . . .  3
     4.1.  File Format . . . . . . . . . . . . . . . . . . . . . .  3
     4.2.  Metadata  . . . . . . . . . . . . . . . . . . . . . . .  3
     4.3.  Instructions  . . . . . . . . . . . . . . . . . . . . .  4
     4.4.  Assets  . . . . . . . . . . . . . . . . . . . . . . . .  4
   5.  Security and Permissions  . . . . . . . . . . . . . . . . .  4
     5.1.  Same-Origin Isolation . . . . . . . . . . . . . . . . .  4
     5.2.  Explicit Consent  . . . . . . . . . . . . . . . . . . .  5
     5.3.  DNSSEC  . . . . . . . . . . . . . . . . . . . . . . . .  5
   6.  Composition . . . . . . . . . . . . . . . . . . . . . . . .  5
   7.  Security Considerations . . . . . . . . . . . . . . . . . .  5
   8.  IANA Considerations . . . . . . . . . . . . . . . . . . . .  6
   9.  References  . . . . . . . . . . . . . . . . . . . . . . . .  6
     9.1.  Normative References  . . . . . . . . . . . . . . . . .  6
     9.2.  Informative References  . . . . . . . . . . . . . . . .  6
   Author's Address  . . . . . . . . . . . . . . . . . . . . . . .  6


1.  Introduction

   Current AI Agent skills (such as those in the Claude Agentic Skill
   Protocol) are primarily distributed via centralized code repositories
   like GitHub.  This creates several friction points:

   o  Identity Ambiguity: Users cannot easily verify if a skill hosted
      on a third-party platform genuinely belongs to a brand.

   o  Hosting Friction: Brands must manage external accounts and
      synchronization instead of using their existing web
      infrastructure.

   o  Security Risks: Malicious skills can spoof brand names on open
      platforms to exfiltrate data.

   The Simple Named Skills (SNS) protocol returns to the fundamental
   logic of the Web: the Domain is the Identity.  By serving skills
   directly from a brand's domain, we leverage the existing global trust
   of the DNS and HTTPS infrastructure.

2.  Conventions and Definitions

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
   "OPTIONAL" in this document are to be interpreted as described in
   BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all
   capitals, as shown here.

   The following terms are used in this document:

   Skill:  A set of instructions, encoded as a Markdown file, that
      directs an AI Agent to perform a specific task or adopt a specific
      behavior.

   Agent:  An AI system capable of fetching, interpreting, and executing
      Skill instructions.

   Skill URL:  The HTTPS URL from which a Skill is served.  This URL
      serves as the globally unique identifier of the Skill.

   Hosting Domain:  The domain component of the Skill URL, considered
      the authoritative endorser of the Skill.

3.  Core Protocol

   The identity of a skill is defined strictly by its HTTPS URL.

3.1.  Identity and Trust

   Skills MUST be served via HTTPS [RFC9110].  Agents MUST NOT fetch or
   execute skills served over plain HTTP.

   The hosting domain is considered the authoritative endorser of the
   skill.  A skill served from "https://example.com/.well-known/
   skills/assistant.md" is attributed to and endorsed by the operator of
   "example.com".

3.2.  Discovery

   Skills MAY be hosted at any valid URL path on a domain (e.g.,
   "https://example.com/my-assistant.md").

   Official brand skills SHOULD be served from the well-known path
   prefix:

      /.well-known/skills/

   This follows the conventions established by [RFC8615] for well-known
   URIs.

   Skills MAY be indexed in the domain's "sitemap.xml" [SITEMAP] to
   enable automated agent discovery.  Agents supporting discovery SHOULD
   check for skill entries in the sitemap when exploring a domain's
   available skills.

4.  Skill Specification

4.1.  File Format

   A Simple Named Skill is a single Markdown file with the ".md" file
   extension, served with the media type "text/markdown" [RFC7763].

4.2.  Metadata

   Skill files MUST begin with a YAML frontmatter block delimited by
   "---" lines.  The frontmatter MUST contain the following fields:

   name:  A short, human-readable name for the skill.

   description:  A brief description of the skill's purpose and
      capabilities.

   Example:

      ---
      name: customer-support
      description: Handles common customer support inquiries for
        Acme Corp products.
      ---

4.3.  Instructions

   The body of the Markdown file, following the frontmatter, MUST
   contain human-readable instructions for the Agent.  These
   instructions define the behavior, constraints, and capabilities
   of the skill.

4.4.  Assets

   Skills MAY reference supplementary assets (e.g., shell scripts,
   templates, data files) via relative or absolute URLs.  Referenced
   assets MUST reside within the same origin as the skill file itself,
   in accordance with the Same-Origin Isolation requirement defined in
   Section 5.1.

5.  Security and Permissions

5.1.  Same-Origin Isolation

   Agents MUST restrict a skill's automated access to resources within
   its hosting domain (same-origin policy).  A skill served from
   "https://example.com" MUST NOT be permitted to automatically access
   resources on "https://other.com" without explicit user consent.

   This prevents a compromised or malicious skill from leveraging its
   trusted domain context to exfiltrate data from, or perform actions
   on, unrelated origins.

5.2.  Explicit Consent

   Agents MUST display the source domain to the user and request
   explicit confirmation before executing any non-textual instructions
   contained in a skill (e.g., shell commands, API calls, file system
   operations).

   The consent prompt SHOULD clearly indicate:

   o  The hosting domain of the skill.

   o  A description of the action to be performed.

   o  Any resources that will be accessed or modified.

5.3.  DNSSEC

   Domain operators SHOULD deploy DNSSEC [RFC4033] to prevent DNS
   spoofing attacks that could redirect agents to malicious skill
   files hosted on attacker-controlled infrastructure.

6.  Composition

   A skill MAY reference other skills via their full HTTPS URLs.  When
   an Agent encounters a referenced skill URL during execution, it
   SHOULD dynamically fetch and load the referenced skill if the current
   context requires the extended capabilities it provides.

   Each referenced skill is subject to its own origin's trust and
   security policies.  Agents MUST apply the Same-Origin Isolation
   policy (Section 5.1) independently to each loaded skill based on
   its own hosting domain.

7.  Security Considerations

   The primary security property of this protocol is that trust is
   anchored to domain ownership.  This inherits both the strengths and
   weaknesses of the existing Web PKI and DNS infrastructure.

   Skill spoofing is mitigated by the HTTPS requirement, which ensures
   that only the legitimate operator of a domain can serve skills from
   that domain.  DNSSEC (Section 5.3) provides an additional layer of
   protection against DNS-level attacks.

   Agents implementing this protocol should be aware of the following
   risks:

   o  Domain compromise: If a domain is compromised, all skills served
      from it should be considered compromised.

   o  Subdomain delegation: Skills on subdomains should be treated as
      distinct trust contexts from the parent domain.

   o  Transitive trust in composition: When skills reference other
      skills (Section 6), the trust chain extends across domains.
      Agents should clearly communicate this to users.

8.  IANA Considerations

   This document requests registration of the well-known URI suffix
   "skills" in the "Well-Known URIs" registry established by [RFC8615].

   URI suffix:  skills

   Change controller:  Namefi

   Specification document:  This document (Section 3.2)

9.  References

9.1.  Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119,
              DOI 10.17487/RFC2119, March 1997.

   [RFC4033]  Arends, R., Austein, R., Larson, M., Massey, D., and
              S. Rose, "DNS Security Introduction and Requirements",
              RFC 4033, DOI 10.17487/RFC4033, March 2005.

   [RFC7763]  Leonard, S., "The text/markdown Media Type", RFC 7763,
              DOI 10.17487/RFC7763, March 2016.

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in
              RFC 2119 Key Words", BCP 14, RFC 8174,
              DOI 10.17487/RFC8174, May 2017.

   [RFC8615]  Nottingham, M., "Well-Known Uniform Resource Identifiers
              (URIs)", RFC 8615, DOI 10.17487/RFC8615, May 2019.

   [RFC9110]  Fielding, R., Ed., Nottingham, M., Ed., and J. Reschke,
              Ed., "HTTP Semantics", STD 97, RFC 9110,
              DOI 10.17487/RFC9110, June 2022.

9.2.  Informative References

   [SITEMAP]  Sitemaps.org, "Sitemaps XML Format",
              <https://www.sitemaps.org/protocol.html>.

Author's Address

   Zainan Victor Zhou
   Namefi
   Email: zzn@namefi.io
```
