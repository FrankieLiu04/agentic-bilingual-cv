LATEX := xelatex
LATEX_FLAGS := -interaction=nonstopmode -halt-on-error -file-line-error
TEMPLATE_DIR := template
BUILD_DIR := build
TEMPLATES := resume-en resume-zh
PDFS := $(TEMPLATES:%=$(BUILD_DIR)/%.pdf)
EXAMPLE_BUILD_DIR := $(BUILD_DIR)/examples
EXAMPLE_COMPILE_DIR := $(BUILD_DIR)/example-compile
EXAMPLE_DATA := examples/fictional-resume.yaml

.PHONY: all check test privacy templates examples check-data \
	validate-templates render-example en zh example-en example-zh clean

all: templates examples

check: all validate-templates test privacy

test:
	scripts/test

privacy:
	scripts/privacy-scan

templates: $(PDFS)

examples: check-data
	scripts/render $(EXAMPLE_DATA) \
		--output-dir $(EXAMPLE_BUILD_DIR) \
		--build-dir $(EXAMPLE_COMPILE_DIR) \
		--force

check-data:
	scripts/validate-data $(EXAMPLE_DATA)

validate-templates: templates
	scripts/validate --expected-pages 1 --log-dir $(BUILD_DIR) $(PDFS)

render-example: check-data
	scripts/render $(EXAMPLE_DATA) --output-dir output/example

en: $(BUILD_DIR)/resume-en.pdf

zh: $(BUILD_DIR)/resume-zh.pdf

example-en: examples

example-zh: examples

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/%.pdf: $(TEMPLATE_DIR)/%.tex $(TEMPLATE_DIR)/cv.cls | $(BUILD_DIR)
	cd $(TEMPLATE_DIR) && $(LATEX) $(LATEX_FLAGS) \
		-output-directory=../$(BUILD_DIR) $*.tex
	cd $(TEMPLATE_DIR) && $(LATEX) $(LATEX_FLAGS) \
		-output-directory=../$(BUILD_DIR) $*.tex

clean:
	@if [ -d "$(BUILD_DIR)" ]; then \
		find $(BUILD_DIR) -type f -delete; \
		find $(BUILD_DIR) -depth -type d -empty -delete; \
	fi
