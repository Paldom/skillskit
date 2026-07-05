# Guide — research pack to published skills

The end-to-end skillskit flow, from raw research to a repo on skills.sh.

## 0. Install (once)

```bash
npx skills add Paldom/skillskit
```

(or `gh skill install Paldom/skillskit`, or the Claude Code plugin — see the
README). All four skills work in any Claude Code session afterwards.

## 1. Build a research pack

Gather everything about the topic into one folder: deep-research reports,
primary-source excerpts, notes, transcripts, examples, constraints. The
per-format rules and quality bar live in the
[research-pack reference](../skills/skill-from-research/references/research-pack.md).
Inside an existing skills repo, the conventional home is the gitignored
`.local/sources/`; anywhere else, any folder works.

## 2. Turn it into skills

In the session where the pack lives:

```
/skill-from-research .local/sources        # or the pack's path
```

The skill inventories the pack (empty/duplicate/unreadable files are flagged
before any time is spent), reads it in full, verifies load-bearing claims
against primary sources, splits the material into single-purpose skills, and
authors each one eval-first. If you're not in a skills repo yet, it routes to
`/create-skill-repo <name> <idea>` — a private GitHub repo with the complete
scaffold (hygiene, CI, hooks, manifests), left uncommitted.

## 3. Review and commit — you, not the agent

Nothing in this kit ever runs `git commit` or `git push`. The handoff is a
dirty working tree plus a summary and fact ledger; review the diff, then:

```bash
git add -A && git commit -m "feat: <skills>" && git push
```

CI runs the same validator the hooks ran locally, plus a real `npx skills`
consumer install of every skill.

## 4. Publish to skills.sh

When the catalogue is ready:

```
/publish-repo            # or /publish-repo --dry-run for a readiness report
```

It gates on the validator, discoverability, and your explicit confirmation of
the two manual blockers (full-history secret scan, personal-file review), then
flips visibility, enables protections, cuts a `gh skill publish` release, and
verifies with a consumer-style install. The skills.sh page appears after the
first real (non-CI) `npx skills add <owner>/<repo>` install seeds telemetry.

## Growing the catalogue later

- New research → new pack → `/skill-from-research` again.
- One-off skill from an idea → `/add-skill <name or idea>`.
- New collection → `/create-skill-repo <name> <idea>`.

## Rules the kit enforces everywhere

- **Eval-first**: trigger evals exist before any skill body.
- **Verify-before-encode**: pack claims are checked against primary sources;
  drift-prone facts are version-gated.
- **Owner-only git**: agents leave the working tree for your review, always.
- **Single purpose per skill**: descriptions stay disjoint; "and" means split.
