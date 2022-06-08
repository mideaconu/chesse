setup() {
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../../../../scripts:$PATH"
}

@test "pgn-filter is executable" {
    [ -x scripts/pgn-filter.sh ]
}

@test "pgn-filter fails when args file does not exist" {
    run pgn-filter.sh missing-args-file tests/data/scripts/games.pgn
    [ "$output" = "File missing-args-file does not exist" ]
}

@test "pgn-filter fails when input file does not exist" {
    run pgn-filter.sh tests/data/scripts/pgn-extract-args missing-games.pgn
    [ "$output" = "File missing-games.pgn does not exist" ]
}

@test "pgn-filter filters games correctly to output directory" {
    run pgn-filter.sh -o tests/data/scripts/filtered-games.pgn tests/data/scripts/pgn-extract-args tests/data/scripts/games.pgn
    [ "$status" -eq 0 ]
    [ -f tests/data/scripts/filtered-games.pgn ]
    [ -s tests/data/scripts/filtered-games.pgn ]

    run diff tests/data/scripts/games.pgn tests/data/scripts/filtered-games.pgn
    [ $? -eq 0 ]
}

teardown_file() {
    rm tests/data/scripts/filtered-games.pgn
}
