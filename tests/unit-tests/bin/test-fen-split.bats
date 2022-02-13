setup_file() {
    touch tests/data/no-games.pgn
    mkdir tests/data/split
}

setup() {
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../../../bin:$PATH"
}

@test "fen-split is executable" {
    [ -x bin/fen-split.sh ]
}

@test "fen-split splits games correctly to output directory" {
    run fen-split.sh -o tests/data/split tests/data/games.pgn

    [ "$status" -eq 0 ]
    [ -d tests/data/split ]

    # TODO parse positions
    # for file in tests/data/split/*; do
    #     # Test that the resulting file contents are correct
    #     run ...
    #     [ "$status" -eq 0 ]
    # done
}

teardown_file() {
    rm tests/data/no-games.pgn
    rm -rf tests/data/split
}
