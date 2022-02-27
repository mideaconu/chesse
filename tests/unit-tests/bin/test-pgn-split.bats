setup_file() {
    touch tests/data/no-games.pgn
    mkdir tests/data/split
}

setup() {
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../../../bin:$PATH"
}

@test "pgn-split is executable" {
    [ -x bin/pgn-split.sh ]
}

@test "pgn-split splits games correctly to output directory" {
    run pgn-split.sh -o tests/data/split tests/data/games.pgn

    [ "$status" -eq 0 ]
    [ -d tests/data/split ]

    for i in {1..3}
    do
        [ -f tests/data/split/$i.pgn ]

        # Test that the resulting file contents are correct
        run pgn-extract tests/data/split/$i.pgn
        [ "$status" -eq 0 ]
    done
}

teardown_file() {
    rm tests/data/no-games.pgn
    rm -rf tests/data/split
}
