protobufs_dir := pb
index_dir := src/backend/search_engine/index

backend_version := 0.0.1
frontend_version := 0.0.1

# Coloured text
gprint := printf '\033[32m%s\033[0m'  # green
bprint := printf '\033[36m%s\033[0m'  # blue

checkmark := "  \xE2\x9C\x94\n"

.PHONY: help
help :  ## Show a list of available commands
	@grep -E '^[a-zA-Z\-]+(\/[a-zA-Z\-]*){0,1} :.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: init/scripts
init/scripts :  ## Make repository scripts executable
	@$(bprint) "- Making scripts executable"
	@chmod +x tests/integration_tests/backend/load-search-engine-test-data.sh
	@printf $(checkmark)

.PHONY: init
init : init/scripts  ## Initialise the repository
	@$(gprint) "Initialise the repository"
	@printf $(checkmark)


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


.PHONY: test/unit
test/unit :  ## Run unit tests
	pytest --cov=src --cov=scripts --cov=encoding --cov-report term-missing tests/unit_tests
	bats -r tests/unit_tests

.PHONY: test/integration
test/integration : init/scripts  ## Run integration tests
	@$(bprint) "> docker pull docker.elastic.co/elasticsearch/elasticsearch:8.2.2"
	@echo
	@docker pull docker.elastic.co/elasticsearch/elasticsearch:8.2.2
	@$(bprint) "> docker run --name es -e ELASTIC_PASSWORD=elastic -p 9201:9200 -p 9301:9300 -itd docker.elastic.co/elasticsearch/elasticsearch:8.2.2"
	@echo
	@docker run --name es -e ELASTIC_PASSWORD=elastic -p 9201:9200 -p 9301:9300 -itd docker.elastic.co/elasticsearch/elasticsearch:8.2.2
	@sleep 30
	@$(bprint) "> docker cp es:/usr/share/elasticsearch/config/certs/http_ca.crt config/ca.crt"
	@echo
	@docker cp es:/usr/share/elasticsearch/config/certs/http_ca.crt config/ca.crt
	@$(bprint) "> ./tests/integration_tests/backend/load-search-engine-test-data.sh"
	@echo
	@./tests/integration_tests/backend/load-search-engine-test-data.sh


.PHONY: test
test : test/unit test/integration clean  ## Run whole test suite


.PHONY: build/backend
build/backend :  ## Build the backend service Docker image
	@docker build \
		--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg BUILD_VERSION=$(backend_version) \
		-t chesse/backend:$(backend_version) \
		-f src/backend/Dockerfile \
		.

.PHONY: build/frontend
build/frontend :  ## Build the frontend service Docker image
	@docker build \
		--build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
		--build-arg BUILD_VERSION=$(frontend_version) \
		-t chesse/frontend:$(frontend_version) \
		-f src/frontend/Dockerfile \
		.

.PHONY: build
build : build/backend build/frontend  ## Build the Docker images


.PHONY: run
run : build  # Run the application
	@docker compose -f src/docker-compose.yml up
