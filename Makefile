.PHONY: check skill clean

SKILL := superagency.skill
SRC := $(shell find superagency -type f)

check:
	python3 scripts/validate.py

skill: check
	rm -f $(SKILL)
	zip -rq $(SKILL) superagency/ -x "*.DS_Store" "*__pycache__*"
	@unzip -Z1 $(SKILL) | grep -qv '^superagency/' \
		&& { echo "error: archive contains paths outside superagency/"; exit 1; } \
		|| echo "built $(SKILL) ($$(du -h $(SKILL) | cut -f1))"

clean:
	rm -f $(SKILL)
