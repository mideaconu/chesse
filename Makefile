.PHONY = help preprocess split init epd fen map pipeline
.DEFAULT_GOAL = help

# Directories
INDEX_DIR := $(PWD)/src/index
CONFIG_DIR := $(PWD)/config
DATA_DIR := $(PWD)/data
PROCESSING_DIR := $(DATA_DIR)/processing

# Files
PGN ?= $(DATA_DIR)/input.pgn
PREPROCESSED_PGN = $(PROCESSING_DIR)/preprocessed.pgn
PGN_FILES = $(wildcard $(PROCESSING_DIR)/*.pgn)
EPD_FILES = $(PGN_FILES:%.pgn=%.epd)
FEN_FILES = $(EPD_FILES:%.epd=%.fen)

# Set of predefined rules for processing PGN files
PGN_EXTRACT_ARGS = $(CONFIG_DIR)/pgn-extract-args


bprint := printf '\033[36m%s\033[0m\n'  # blue text
gprint := printf '\033[32m%s\033[0m\n'  # green text


help:  # Show list of available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


$(PROCESSING_DIR):
	@mkdir $(PROCESSING_DIR)

preprocess: $(PROCESSING_DIR)  ## Preprocess the source PGN file. By default, the input file is data/input.pgn.
	@$(bprint) "Preprocessing..."
	@$(INDEX_DIR)/preprocess.sh -a $(PGN_EXTRACT_ARGS) -o $(PREPROCESSED_PGN) $(PGN)
	@echo ""

split: preprocess  ## Split the PGN file into one game per PGN file
	@$(bprint) "Splitting..."
	@$(INDEX_DIR)/split.sh -a $(PGN_EXTRACT_ARGS) -o $(PROCESSING_DIR) $(PREPROCESSED_PGN)
	@rm $(PREPROCESSED_PGN)

init: split  ## Initialise the map-reduce pipeline
	@$(gprint) "Successfully initialised the map-reduce pipeline"


epd: $(EPD_FILES)  ## Convert PGN files to EDP files
	@$(bprint) "Converting to EPD..."

%.epd: %.pgn
	@pgn-extract -Wepd -A $(PGN_EXTRACT_ARGS) -o $@ $<
	@rm $<

fen: $(FEN_FILES)  ## Convert EPD files to FEN files
	@$(bprint) "Converting to FEN..."

%.fen: %.epd
	@sed -e "s/ c0 .*//" $< > $@
	@rm $<

map: fen
	@$(gprint) "Successfully converted PGN files to FEN in $(PROCESSING_DIR)"


pipeline:  ## Run the complete map-reduce pipeline
	@$(MAKE) init
	@$(MAKE) map -j 8
