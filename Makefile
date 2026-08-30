.PHONY: check validate lint evals test hooks

## check: run every quality gate (what CI runs)
check: validate lint evals test

## validate: validate SKILL.md files, evals, security rules, and plugin manifests
validate:
	python3 scripts/validate_skills.py

## lint: ruff over the Python this repo ships (config: ruff.toml)
#  uvx runs the pinned version with no local install; a PATH ruff is the fallback
#  and refuses to run if it is the wrong version (required-version in ruff.toml).
lint:
	@if command -v uvx >/dev/null 2>&1; then \
		uvx --from 'ruff==0.15.10' ruff check . && uvx --from 'ruff==0.15.10' ruff format --check .; \
	else \
		ruff check . && ruff format --check .; \
	fi

## evals: score every trigger case against every description (routing + ratchet)
#  --min-rank1 is the checked-in ratchet floor. It sits a little under the
#  current number so ordinary description edits don't fail spuriously; raise it
#  deliberately when the number improves, never lower it to get green.
evals:
	python3 scripts/run_evals.py --min-rank1 85

## test: self-checks for the scorer, the security rules, and the duplicated copies
test:
	python3 scripts/test_run_evals.py
	python3 scripts/test_validate_skills.py
	python3 scripts/check_sync.py

## hooks: install the commit-time layer (pre-commit + pre-push)
hooks:
	pre-commit install --install-hooks
