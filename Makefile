.PHONY = help init preprocess split
.DEFAULT_GOAL = help

DATE := $(shell date +"%FT%H%M%S")

# Directories
INDEX_DIR = $(PWD)/src/index
CONFIG_DIR = $(PWD)/config
DATA_DIR = $(PWD)/data
PROCESSING_DIR = $(DATA_DIR)/processing_$(DATE)

# Files
PGN ?= $(DATA_DIR)/input.pgn
PREPROCESSED_PGN = $(PROCESSING_DIR)/preprocessed.pgn

# Set of predefined rules for processing PGN files
PGN_EXTRACT_ARGS = $(CONFIG_DIR)/pgn-extract-args


# Prints green text to stdout
gprint := printf '\033[32m%s\033[0m\n'


help:  # Show list of available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


init:  ## Initialises the environment
	@mkdir $(PROCESSING_DIR)
	@$(gprint) "Successfully initialised the environment"

preprocess: init  ## Preprocess the source PGN file. By default, the input file is data/input.pgn.
	@$(INDEX_DIR)/preprocess.sh -a $(PGN_EXTRACT_ARGS) -o $(PREPROCESSED_PGN) $(PGN)
	@$(gprint) "Successfully preprocessed PGN file $(PGN) into $(PREPROCESSED_PGN)"

split: preprocess  ## Split the PGN file into one game per PGN file
	@$(INDEX_DIR)/split.sh -a $(PGN_EXTRACT_ARGS) -o $(PROCESSING_DIR) $(PREPROCESSED_PGN)
	@rm $(PREPROCESSED_PGN)
	@$(gprint) "Successfully split PGN file $(PREPROCESSED_PGN). The result has been saved to $(PROCESSING_DIR)"
