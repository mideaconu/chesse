setup_file() {
    touch tests/data/scripts/no-games.pgn
    mkdir tests/data/scripts/split
}

setup() {
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../../../../scripts:$PATH"
}

@test "pgn-split is executable" {
    [ -x scripts/pgn-split.sh ]
}

@test "pgn-split splits games correctly to output directory" {
    run pgn-split.sh -o tests/data/scripts/split tests/data/scripts/games.pgn

    [ "$status" -eq 0 ]
    [ -d tests/data/scripts/split ]

    for i in {1..3}
    do
        [ -f tests/data/scripts/split/$i.pgn ]

        # Test that the resulting file contents are correct
        run pgn-extract tests/data/scripts/split/$i.pgn
        [ "$status" -eq 0 ]
    done
}

teardown_file() {
    rm tests/data/scripts/no-games.pgn
    rm -rf tests/data/scripts/split
}
