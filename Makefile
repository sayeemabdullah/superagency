.PHONY: check skill hooks clean

SKILL := superagency.skill

## check — structural validation, same as CI
check:
	python3 scripts/validate.py

## skill — rebuild the archive locally (deterministic; CI owns the committed copy)
skill: check
	./scripts/build.sh

## hooks — install the pre-commit guard against hand-built archives
hooks:
	@git config core.hooksPath scripts/hooks
	@echo "hooks installed (core.hooksPath=scripts/hooks)"

clean:
	rm -f $(SKILL)
