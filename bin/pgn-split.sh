#!/bin/sh

set -e

print_usage() {
   cat << EOF
NAME
    pgn-split.sh -- splits a PGN file so that there is only one per game

SYNOPSIS
    pgn-split.sh [-h/--help] [-o/--output-dir dir_name] file

DESCRIPTION
    Splits the source PGN file into one game per PGN file.

    -h, --help
        Print pgn-split.sh documentation to stdout.

    -o dir_name, --output-dir dir_name
        The directory where the output is stored. By default, the output directory is the directory where the script is being called from.

EXAMPLES
    pgn-split.sh file.pgn
        Splits file file.pgn into one file per game into the current directory.
    pgn-split.sh -o data/split file.pgn
        Splits file file.pgn into one file per game into the data/split directory.
        
EOF
   exit 0
}

main() {
    if [ $# -eq 0 ]; then print_usage; fi
    for i in "$@" ; do [[ $i == "-h" ]] || [[ $i == "--help" ]] && print_usage ; done

    while [[ $# -gt 1 ]]; do
        key="$1"

        case "$key" in 
            -o|--output-dir)
                OUTPUT_DIR="$2"
                shift
                shift
                ;;
            *)
                echo "Unknown flag: $1"
                exit 1
                ;;
        esac 
    done

    INPUT_FILE="${1}"

    pgn-extract -#1 -s ${INPUT_FILE}

    if ls [0-9]*.pgn 1>/dev/null 2>&1; then
        if [[ ! -z "${OUTPUT_DIR}" ]]; then
            mv [0-9]*.pgn ${OUTPUT_DIR}
        fi
    fi
}

main $@
