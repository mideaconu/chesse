setup() {
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../../../bin:$PATH"
}

@test "pgn-standardise is executable" {
    [ -x bin/pgn-standardise.sh ]
}

@test "pgn-standardise fails when input file does not exist" {
    run pgn-standardise.sh tests/data/missing-games.pgn

    [ "$output" = "File tests/data/missing-games.pgn does not exist" ]
}

@test "pgn-standardise replaces UTCDate with Date to output directory" {
    run pgn-standardise.sh -o tests/data/standardised-games.pgn tests/data/games.pgn

    run grep -Rq "UTCDate" tests/data/standardised-games.pgn
    [ "$status" -eq 1 ]

    run grep -Rq "Date" tests/data/standardised-games.pgn
    [ "$status" -eq 0 ]
}

@test "pgn-standardise replaces UTCTime with Time to output directory" {
    run pgn-standardise.sh -o tests/data/standardised-games.pgn tests/data/games.pgn

    run grep -Rq "UTCTime" tests/data/standardised-games.pgn
    [ "$status" -eq 1 ]

    run grep -Rq "Time" tests/data/standardised-games.pgn
    [ "$status" -eq 0 ]
}

teardown_file() {
    rm tests/data/standardised-games.pgn
}
