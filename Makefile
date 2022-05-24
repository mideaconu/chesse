protobufs_dir := pb
index_dir := src/backend/search_engine/index

# Coloured text
gprint := printf '\033[32m%s\033[0m'  # green
bprint := printf '\033[36m%s\033[0m'  # blue

checkmark := "  \xE2\x9C\x94\n"

.PHONY: help
help :  ## Show a list of available commands
	@grep -E '^[a-zA-Z]+(\/[a-zA-Z]*){0,1} :.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean/py
clean/py :  ## Clean up the Python caches
	@$(bprint) "- Cleaning up Python caches"
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '*__pycache__' -delete
	@printf $(checkmark)

.PHONY: clean
clean : clean/py  ## Clean up the repository
	@$(gprint) "Cleanup"
	@printf $(checkmark)


.PHONY: proto
proto :  ## Run the protobuf code generation pipeline
	@$(MAKE) -C $(protobufs_dir) proto

.PHONY: index
index :  ## Run the indexing pipeline
	@$(MAKE) -C $(index_dir) index


.PHONY: start/backend-api
start/backend-api : ### Start backend API
	@python src/backend/api/main.py

.PHONY: start/frontend-server
start/frontend-server :  ## Start frontend server
	@DEBUG=server:* npm start --prefix src/frontend
