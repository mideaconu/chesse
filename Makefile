.PHONY = help preprocess 
.DEFAULT_GOAL = help

DATA_DIR = $(PWD)/data
CONFIG_DIR = $(PWD)/config

PGN ?= $(DATA_DIR)/input.pgn
PREPROCESSED_PGN = $(DATA_DIR)/preprocessed.pgn

# Set of predefined rules for processing PGN files
PGN_EXTRACT_ARGS = $(CONFIG_DIR)/pgn-extract-args


help:  # Show list of available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


preprocess:  ## Preprocess the source PGN file. By default, the input file is data/input.pgn.
	@$(INDEX_DIR)/preprocess.sh -a $(PGN_EXTRACT_ARGS) -o $(PREPROCESSED_PGN) $(PGN)
