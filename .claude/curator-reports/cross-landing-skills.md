# Curator cross-validation report

Generated: 2026-07-06T08:14:01Z
Subject: Validate 8 landing-page Agent Skills: skill split/scoping, single-line descriptions (disjointness/trigger theft, esp. nextjs-landing-page vs web-vitals-and-seo indexing overlap), and SKILL.md+references content. Check technical correctness and version-gating of encoded facts: CVE-2025-55182 (React 19.0-19.2.0/Next 15.x-16.x, fixed React 19.2.1/Next 16.0.7), WCAG 2.5.8 target size 24x24 CSS px, GSAP free under GreenSock standard license (not MIT), DESIGN.md (Google Labs, alpha), shadcn Base UI default July 2026, FAQ rich results stopped May 2026 but schema still parsed. Flag any directional stat stated as fact (repo policy: % lifts are directional only).
Kind: implementation

## Aggregate

NO_EXTERNAL_REVIEW: no configured provider returned a review.

## Provider status

- **openai** `gpt-5.5`: skipped/error (5.4s; HTTP 429: {
  "error": {
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.",
    "type": "insufficient_quota",
    "param": null,
    "code": "insufficient_quota"
  }
})

## openai — gpt-5.5 (round 1)

Skipped or failed: HTTP 429: {
  "error": {
    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.",
    "type": "insufficient_quota",
    "param": null,
    "code": "insufficient_quota"
  }
}

## Curation instructions for Claude

Use this report as critique, not authority. Accept findings only when supported by evidence or cheap to mitigate; resolve disagreements with tests, code reads, or explicit user constraints. Model consensus never overrides failing tests, compiler errors, or specs.

---

## Internal curation fallback (external review unavailable)

External cross-review did not run: sole configured provider (OpenAI gpt-5.5)
returned HTTP 429 insufficient_quota; no other providers configured. Verdict on
the external review itself: NOT VALID / UNAVAILABLE this session. Owner must add
OpenAI credits or configure a second provider key in the cross skill's .env to
obtain an independent opinion.

Substituted the cross skill's free, always-on curation loop (local evidence).
Dispositions:

- FIXED — nextjs-landing-page <-> web-vitals-and-seo residual indexing trigger
  overlap: added "Next.js 'use client'/build bugs" to web-vitals' Not-for clause
  so the boundary is now mutual (nextjs already excludes "SEO strategy").
- FIXED — directional stat stated as bare fact in landing-page-structure body
  ("57%/64% never scroll") -> hedged as directional in cited studies.
- NO CHANGE (verified against primary sources this session): CVE-2025-55182
  version/fix list; WCAG 2.5.8 24x24 CSS px; GSAP free under GreenSock standard
  license (not MIT); DESIGN.md alpha (Google Labs, Apr 2026); shadcn Base UI
  default (July 2026); FAQ rich results stopped May 7 2026 (schema still parsed).
- REJECTED (with rationale) — "visual-design-system joins two topics with 'and'":
  the aesthetic + encode/enforce halves are one coherent 'design system' purpose;
  splitting would create trigger theft between "choose colors" and "encode colors".
  Kept merged; disjointness reasoning recorded.

make check: 0 errors, 0 warnings after fixes.
