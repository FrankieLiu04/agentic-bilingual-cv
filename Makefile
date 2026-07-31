BUILD_DIR := build
EXAMPLE_BUILD_DIR := $(BUILD_DIR)/examples
EXAMPLE_COMPILE_DIR := $(BUILD_DIR)/example-compile
EXAMPLE_DATA := examples/fictional-resume.yaml

SKILL_SOURCE := skills/resume-builder/SKILL.md
SKILL_COPIES := .agents/skills/resume-builder/SKILL.md \
	.claude/skills/resume-builder/SKILL.md

.PHONY: all check test privacy examples check-data \
	render-example skills skills-sync clean

all: examples

check: all skills-sync test privacy

test:
	scripts/test

privacy:
	scripts/privacy-scan

examples: check-data
	scripts/render $(EXAMPLE_DATA) \
		--output-dir $(EXAMPLE_BUILD_DIR) \
		--build-dir $(EXAMPLE_COMPILE_DIR) \
		--force

check-data:
	scripts/validate-data $(EXAMPLE_DATA)

render-example: check-data
	scripts/render $(EXAMPLE_DATA) --output-dir output/example

skills:
	cp $(SKILL_SOURCE) .agents/skills/resume-builder/
	cp $(SKILL_SOURCE) .claude/skills/resume-builder/

skills-sync:
	@for copy in $(SKILL_COPIES); do \
		cmp -s $(SKILL_SOURCE) $$copy || { \
			echo "out of sync: $$copy (run 'make skills')"; \
			exit 1; \
		}; \
	done
	@echo "ok: agent skill copies match $(SKILL_SOURCE)"

clean:
	@if [ -d "$(BUILD_DIR)" ]; then \
		find $(BUILD_DIR) -type f -delete; \
		find $(BUILD_DIR) -depth -type d -empty -delete; \
	fi
