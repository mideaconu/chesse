.PHONY = help init split pipeline
.DEFAULT_GOAL = help

DATA_DIR ?= $(PWD)/data
PGN_EXTRACT_ARGS = $(PWD)/pgn-extract-args

DOWNLOAD_DIR = $(DATA_DIR)/download
INPUT_DIR = $(DATA_DIR)/input

AGG_FILE = $(INPUT_DIR)/games.pgn

PGN_FILES=$(wildcard $(INPUT_DIR)/*.pgn)
FEN_FILES=$(PGN_FILES:%.pgn=%.fen)

gprint := printf '\033[32m%s\033[0m\n'  # green text


help:  # Show list of available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


$(INPUT_DIR): $(DOWNLOAD_DIR)
	mkdir $(INPUT_DIR)
	@$(gprint) "Successfully created directory $(INPUT_DIR)"

$(AGG_FILE): $(INPUT_DIR)
	pgn-extract -A $(PGN_EXTRACT_ARGS) $(DOWNLOAD_DIR)/*.pgn -o $(AGG_FILE)
	@$(gprint) "Successfully aggregated PGN files from $(DOWNLOAD_DIR) into $(AGG_FILE)"

aggregate: | $(AGG_FILE)  ## Aggregate PGN files from each month into one PGN file

split: aggregate  ## Break aggregated input file into one game per PGN file
	cd $(INPUT_DIR); pgn-extract -#1 -A $(PGN_EXTRACT_ARGS) $(AGG_FILE)
	@$(gprint) "Successfully split $(AGG_FILE) into game-level PGN files"
	rm $(AGG_FILE)
	@$(gprint) "Successfully deleted $(AGG_FILE)"

init: split  ## Initialise the map-reduce pipeline


pipeline:  ## Run map-reduce pipeline end-to-end
	$(MAKE) init
