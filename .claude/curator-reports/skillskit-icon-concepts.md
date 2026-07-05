# Curator cross-validation report

Generated: 2026-07-05T23:20:29Z
Subject: Icon concept ideation for skillskit (bracket-family glyph, sibling of brainkit)
Kind: plan

## Aggregate

PASS_WITH_CHANGES — PASS_WITH_CHANGES from openai.

## Provider status

- **openai** `gpt-5.5`: ok (64.2s; verdict=PASS_WITH_CHANGES, confidence=0.82, tokens=4981)

## openai — gpt-5.5 (round 1)

## Verdict
Verdict: PASS_WITH_CHANGES — the brief is directionally sound, but it lacks enough validation criteria, reference material, and collision checks to defensibly choose the top 3 as-is.

## Strongest objections
- **No actual brainkit reference is provided.** Family resemblance cannot be judged from “uses square brackets [ ]” alone; stroke weight, corner radius, proportions, color, and optical balance matter. **Fix:** include the brainkit SVG/PNG and require side-by-side comparison at 16/32/128px.
- **Several concepts likely violate the stated 16px and shape-budget constraints.** “Stack” with 2–3 bracket pairs can exceed `<=5 major shapes`; “tool-morph” will likely lose the wrench silhouette at favicon size; `[s]` risks becoming an illegible squiggle. **Fix:** define minimum rendered stroke/gap sizes and reject concepts that cannot survive at 16px.
- **Trademark/confusion risk is asserted but not operationalized.** Bracket-container marks are inherently close to developer-tool iconography, especially Brackets.io and generic code-editor/package-manager marks. **Fix:** require a documented collision pass before finalizing any bracket-heavy design.
- **Semantic priorities are unresolved.** “Family resemblance to brainkit” and “installable skills/toolkit” may point to different winners. If family identity dominates, `[s]` or `[✦]` rise; if installability dominates, “module-slide” likely wins. **Fix:** explicitly weight brand-family fit vs semantic fit before ranking.
- **Color constraints are underspecified.** The background is fixed, but foreground/accent colors are not tied to contrast, brainkit palette, or trademark avoidance. **Fix:** define allowable foreground/accent palette and minimum contrast against `#2A2A2E`.

## Missing assumptions or evidence
- Whether the icon must be recognizable as “skillskit” without adjacent wordmark.
- Whether the mark should read as developer tooling, AI capability, package installation, or brand sibling first.
- Actual brainkit mark geometry and palette.
- Target rendering environments: browser favicon, npm/package page, GitHub avatar, macOS/iOS app icon mask, social preview, etc.
- Whether letter-like glyphs are acceptable despite the “no text” constraint.
- Whether the final SVG will use strokes or expanded filled paths; this affects rasterization consistency.
- Evidence that any candidate remains legible at 16px after anti-aliasing.
- Evidence that bracket marks do not collide with Brackets.io, code editor icons, package-manager logos, or common AI sparkle marks.

## Risks
- **IP/trademark risk:** bracket-based developer marks and sparkle/AI marks are crowded. Avoid npm red, VS Code blue-like silhouettes, Brackets.io-like bracket styling, and generic package/cube motifs without clearance.
- **Reliability risk:** thin strokes, narrow bracket gaps, small spark points, or wrench details may disappear at 16px or under platform icon masks.
- **Maintainability risk:** if the mark is delivered as editable strokes with live effects, different renderers/exporters may produce inconsistent favicons. Keep a parametric source, but ship normalized outlined SVG/PNG assets.
- **Licensing risk:** do not trace font glyphs, emoji stars, wrench icons, or third-party SVG assets unless licenses are verified.

## Validation
- Render every candidate at `16x16`, `24x24`, `32x32`, `64x64`, and `1024x1024`; judge only from raster outputs, not the master SVG.
- Run an SVG lint check for:
  - no `<text>`
  - no scripts
  - no external images/fonts/styles
  - `<=3` unique colors
  - `<=5` major foreground shapes
  - consistent stroke width or expanded filled paths
- Compare each rasterized candidate side-by-side with brainkit at 16/32/128px.
- Minimum geometry checks on a 1024 grid:
  - foreground strokes should generally render at least ~2px at 16px, i.e. about `120–140` units wide;
  - critical negative gaps should generally be at least ~1px at 16px, i.e. about `64+` units;
  - avoid details smaller than ~80–100 units.
- Perform reverse-image and trademark searches for the shortlisted marks:
  - Google Lens / image search
  - USPTO / WIPO / EUIPO where relevant
  - search specifically for Brackets.io, npm, CodePen, VS Code, Prettier, TypeScript, GitHub, package-manager, and AI-sparkle logo similarities.
- Do a quick recognition test with developers: show each 16px/32px icon for a few seconds and ask what it suggests; reject icons that primarily read as editor, settings, generic AI, or another known brand.

## Minimal revision
- Add the actual brainkit icon source/reference and define measurable family-fit requirements.
- Add a required 16px raster validation step before choosing finalists.
- Add a documented trademark/collision screening step.
- Clarify priority weighting: recommended default is **family fit 35%, 16px legibility 30%, distinctiveness 20%, semantic fit 15%**.
- Tentative ranking after applying the stated constraints:
  1. **Module-slide** — strongest semantic fit for installable modules and likely distinctive if simplified.
  2. **`[✦]`** — very legible and family-compatible, but generic AI/sparkle risk.
  3. **`[s]`** — strong naming/family tie, but only if the `s` is abstracted enough to survive 16px.
  4. **Stack** — kit/multiplicity idea is good, but likely exceeds shape budget and becomes noisy.
  5. **Tool-morph** — weakest at favicon size; wrench detail is generic and likely illegible.
- Draw the top 3 only after these geometry constraints are added:
  - bracket stroke: about `120–140` units;
  - live glyph area: roughly `680–760` units inside the 1024 canvas;
  - bracket gaps and internal negative spaces: at least `64–80` units;
  - drop all secondary details at 16px;
  - use one bright foreground color plus at most one accent against `#2A2A2E`.

```json
{"verdict":"PASS_WITH_CHANGES","confidence":0.82,"summary":"The icon brief is viable, but it needs measurable 16px, brainkit-family, color, and collision-validation requirements before the top concepts can be chosen safely.","top_issues":["No brainkit reference provided","16px legibility not validated","Trademark/collision screening missing","Shape-budget violations likely for stack/tool concepts","Semantic priorities not weighted"]}
```

## Curation instructions for Claude

Use this report as critique, not authority. Accept findings only when supported by evidence or cheap to mitigate; resolve disagreements with tests, code reads, or explicit user constraints. Model consensus never overrides failing tests, compiler errors, or specs.
