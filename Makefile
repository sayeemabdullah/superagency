.PHONY: check test eval skill clean

SKILL := superagency.skill

## check — structural validation, same as CI
check:
	python3 scripts/validate.py

## test — unit tests for the bundled tools
test:
	python3 -m unittest discover -s tests -q

## eval — routing accuracy; needs ANTHROPIC_API_KEY, costs money, not in CI
eval:
	python3 scripts/eval_routing.py

## skill — rebuild the archive locally (deterministic; CI owns the committed copy)
skill: check test
	./scripts/build.sh

clean:
	rm -f $(SKILL)
	rm -rf superagency/scripts/__pycache__ tests/__pycache__
