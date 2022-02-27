setup() {
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../../../bin:$PATH"
}

@test "pgn-filter is executable" {
    [ -x bin/pgn-filter.sh ]
}

@test "pgn-filter fails when args file does not exist" {
    run pgn-filter.sh missing-args-file tests/data/games.pgn
    [ "$output" = "File missing-args-file does not exist" ]
}

@test "pgn-filter fails when input file does not exist" {
    run pgn-filter.sh tests/data/pgn-extract-args missing-games.pgn
    [ "$output" = "File missing-games.pgn does not exist" ]
}

@test "pgn-filter filters games correctly to output directory" {
    run pgn-filter.sh -o tests/data/filtered-games.pgn tests/data/pgn-extract-args tests/data/games.pgn
    [ "$status" -eq 0 ]
    [ -f tests/data/filtered-games.pgn ]
    [ -s tests/data/filtered-games.pgn ]

    run diff tests/data/games.pgn tests/data/filtered-games.pgn
    [ $? -eq 0 ]
}

teardown_file() {
    rm tests/data/filtered-games.pgn
}
