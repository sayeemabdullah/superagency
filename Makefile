.PHONY: check route test eval skill hooks clean

SKILL := superagency.skill

## check — structural validation, same as CI
check:
	python3 scripts/validate.py

## route — deterministic offline routing proxy; runs in CI, watch the delta
route:
	python3 scripts/route_lint.py --fail-under 0.60

## test — unit tests for the bundled tools
test:
	python3 -m unittest discover -s tests -q

## eval — routing accuracy against a real model; needs ANTHROPIC_API_KEY, costs money, not in CI
eval:
	python3 scripts/eval_routing.py

## skill — rebuild the archive locally (deterministic; CI owns the committed copy)
skill: check test
	./scripts/build.sh

## hooks — install the pre-commit guard against hand-built archives
hooks:
	@git config core.hooksPath scripts/hooks
	@echo "hooks installed (core.hooksPath=scripts/hooks)"

clean:
	rm -f $(SKILL)
	rm -rf superagency/scripts/__pycache__ tests/__pycache__
