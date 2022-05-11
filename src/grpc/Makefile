.DEFAULT_GOAL = help

# Coloured text
gprint := printf '\033[32m%s\033[0m'  # green
bprint := printf '\033[36m%s\033[0m'  # blue

checkmark := "  \xE2\x9C\x94\n"

.PHONY: help
help :  ## Show a list of available commands
	@grep -E '^[a-zA-Z]+(\/[a-zA-Z]*){0,1} :.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: proto/build
proto/build :  ## Compile the protobuf files
	@$(gprint) "Compilation of protobuf files"
	@buf build
	@printf $(checkmark)


.PHONY: proto/lint
proto/lint :  ## Lint the protobuf files
	@$(gprint) "Linting of protobuf files"
	@buf lint
	@printf $(checkmark)


.PHONY: proto/gen-py
proto/gen-py :  ## Generate the Python protobuf files
	@$(bprint) "- Python code generation"
	@buf generate --template buf.gen.py.yaml
	@printf $(checkmark)

.PHONY: proto/gen-js
proto/gen-js :  ## Generate the JavaScript protobuf files
	@$(bprint) "- JavaScript code generation"
	@buf generate --template buf.gen.js.yaml
	@printf $(checkmark)

.PHONY: proto/gen
proto/gen :  ## Generate the protobuf code
	@$(MAKE) proto/gen-py
	@$(MAKE) proto/gen-js
	@$(gprint) "Code generation"
	@printf $(checkmark)


.PHONY: proto
proto :  ## Run the protobuf code generation pipeline
	@$(MAKE) proto/build
	@$(MAKE) proto/lint
	@$(MAKE) proto/gen
