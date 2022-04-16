.DEFAULT_GOAL = index

ROOT_DIR := /Users/mihaideaconu/Documents/chessplusplus

scripts_dir := $(ROOT_DIR)/scripts
config_dir := $(ROOT_DIR)/config
data_dir := $(ROOT_DIR)/data
output_dir ?= $(data_dir)/output

pgn_dir := $(data_dir)/pgn
epd_dir := $(data_dir)/epd
fen_dir := $(data_dir)/fen

games_json_dir := $(data_dir)/games_json
positions_json_dir := $(data_dir)/positions_json

pgn ?= $(data_dir)/input.pgn
lock := $(data_dir)/encoding.lock

pgn_files = $(wildcard $(pgn_dir)/*.pgn)
epd_files = $(pgn_files:$(pgn_dir)/%.pgn=$(epd_dir)/%.epd)
fen_files = $(pgn_files:$(pgn_dir)/%.pgn=$(fen_dir)/%.fen)

games_json_files = $(pgn_files:$(pgn_dir)/%.pgn=$(games_json_dir)/%.json)
positions_json_files = $(pgn_files:$(pgn_dir)/%.pgn=$(positions_json_dir)/%.json)

games_file := $(output_dir)/games.json
positions_file := $(output_dir)/positions.json

games_es_query_file := $(output_dir)/games-query.txt
positions_es_query_file := $(output_dir)/positions-query.txt

pgn_extract_args := $(config_dir)/pgn-extract-args

filtered_pgn := $(data_dir)/filtered-games.pgn
preprocessed_pgn := $(data_dir)/preprocessed-games.pgn

# Coloured text
gprint := printf '\033[32m%s\033[0m'  # green
bprint := printf '\033[36m%s\033[0m'  # blue

checkmark := "  \xE2\x9C\x94\n"
VPATH := $(scripts_dir) $(data_dir) $(config_dir)

## Show a list of available commands
.PHONY += index/help
index/help :
	@grep -E '^[a-zA-Z_-]+ :.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


$(pgn_dir) : ; @mkdir $(pgn_dir)

## Filter the source PGN file
$(filtered_pgn) : $(pgn) | $(pgn_dir)
	@$(bprint) "- Filtering source PGN file"
	@pgn-filter.sh -o $(filtered_pgn) $(pgn_extract_args) $(pgn) 2>/dev/null
	@printf $(checkmark)


## Standardise the source PGN file
$(preprocessed_pgn) : $(filtered_pgn)
	@$(bprint) "- Standardising source PGN file"
	@pgn-standardise.sh -o $(preprocessed_pgn) $(filtered_pgn)
	@printf $(checkmark)


## Preprocess the source PGN file
.PHONY += init/preprocess
init/preprocess :  $(filtered_pgn) $(preprocessed_pgn)


## Split the source PGN file one game per file
.PHONY += init/split
init/split : init/preprocess
	@$(bprint) "- Splitting source PGN file"
	@pgn-split.sh -o $(pgn_dir) $(preprocessed_pgn)
	@printf $(checkmark)


## Initialise the indexing pipeline
.PHONY += pipeline/init
pipeline/init : init/preprocess init/split
	@$(gprint) "Pipeline initialisation"
	@printf $(checkmark)


$(epd_dir) : ; @mkdir $(epd_dir)

## Convert each PGN file to EPD
$(epd_files) : $(epd_dir)/%.epd : $(pgn_dir)/%.pgn | $(epd_dir)
	@perl -pi -e "chomp if eof" $<
	@pgn-extract -Wepd -A $(pgn_extract_args) -o $@ $<
	@perl -pi -e "chomp if eof" $@


$(fen_dir) : ; @mkdir $(fen_dir)

## Convert each EPD file to FEN
$(fen_files) : $(fen_dir)/%.fen : $(epd_dir)/%.epd | $(fen_dir)
	@sed -e "s/ c0 .*//" $< > $@
	@perl -pi -e "chomp if eof" $@


$(games_json_dir) : ; @mkdir $(games_json_dir)

## Convert each PGN file to a JSON object
$(games_json_files) : $(games_json_dir)/%.json : $(pgn_dir)/%.pgn | $(games_json_dir)
	@pgn-to-json --input-file $< --output-file $@


$(positions_json_dir) : ; @mkdir $(positions_json_dir)

## Convert each FEN file to a JSON object where each position in the game is encoded
$(positions_json_files) : $(positions_json_dir)/%.json : $(fen_dir)/%.fen | $(positions_json_dir)
	@generate-position-json.sh -o $@ $^


## Generate the JSON position encodings
.PHONY += pipeline/map
pipeline/map : $(games_json_files) $(positions_json_files)
	@$(gprint) "Result generation"
	@printf $(checkmark)


$(output_dir) : ; @mkdir $(output_dir)

## Aggregate the games into a JSON file
$(games_file) : | $(games_json_dir) $(output_dir)
	@$(bprint) "- Generating aggregated games object JSON"
	@jq -s '.' $(games_json_dir)/?.json > $(games_file)
	@printf $(checkmark)


## Aggregate the encoded positions into a JSON file
$(positions_file) : $(positions_json_files) | $(output_dir)
	@$(bprint) "- Generating aggregated positions object JSON"
	@jq -s 'add | unique_by(.position.fen)' $(positions_json_dir)/?.json > $@
	@printf $(checkmark)


## Aggregate the games and encoded positions
.PHONY += pipeline/reduce
pipeline/reduce : $(games_file) $(positions_file)
	@$(gprint) "Result collection"
	@printf $(checkmark)


## Generate Elasticsearch bulk-insert query file for games
$(games_es_query_file) : $(games_file)
	@$(bprint) "- Generating games ES query file"
	@jq -c '.[] | {"index": {"_index": "games", "_id": .id}}, .' $(games_file) > $(games_es_query_file)
	@printf $(checkmark)

## Generate Elasticsearch bulk-insert query file for positions
$(positions_es_query_file) : $(positions_file)
	@$(bprint) "- Generating positions ES query file"
	@jq -c '.[] | {"index": {"_index": "positions", "_id": .position.fen}}, .' $(positions_file) > $(positions_es_query_file)
	@printf $(checkmark)

## Generate Elasticsearch bulk-insert query files
.PHONY += pipeline/insert
pipeline/insert : $(games_es_query_file) $(positions_es_query_file)
	@$(gprint) "ES query files generation"
	@printf $(checkmark)


## Clean up the temporary files created during the pipeline run
.PHONY += index/clean
pipeline/clean :
	@$(gprint) "Pipeline cleanup"
	@rm $(filtered_pgn) $(preprocessed_pgn)
	@rm -rf $(pgn_dir) $(epd_dir) $(fen_dir) $(json_dir) $(games_json_dir) $(positions_json_dir)
	@printf $(checkmark)


## Run the indexing pipeline
.PHONY += index/pipeline
index/pipeline :
	@$(MAKE) pipeline/init
	@$(MAKE) pipeline/map -j 8
	@$(MAKE) pipeline/reduce
	@$(MAKE) pipeline/insert
	@$(MAKE) pipeline/clean


.PHONY += index
index :  ## Run the complete map-reduce indexing pipeline
	@$(MAKE) index/pipeline
