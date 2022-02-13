#!/bin/sh

set -e

print_usage() {
   cat << EOF
NAME
    pgn-flter.sh -- filter a PGN file according to given criteria

SYNOPSIS
    pgn-flter.sh [-h/--help] [-o/--output-file output_file] args_file file

DESCRIPTION
    Filters the source PGN file according to rules defined in args_file. args_file needs to be compatible with the pgn-extract arguments file format. See https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/help.html#-A for details.

    -h, --help
        Print pgn-filter.sh documentation to stdout.

    -o output_file, --output output_file
        Save the output to the output_file. By default, the operation is done in-place.

EXAMPLES
    pgn-flter.sh pgn-extract-args-file file.pgn
        Filters file.pgn according to the rules laid out in pgn-extract-args-file.
    pgn-flter.sh -o output_file.pgn pgn-extract-args-file file.pgn
        Filters file.pgn according to the rules laid out in pgn-extract-args-file, and saves the output to output_file.pgn.
EOF
   exit 0
}

main() {
    if [ $# -eq 0 ]; then print_usage; fi
    for i in "$@" ; do [[ $i == "-h" ]] || [[ $i == "--help" ]] && print_usage ; done

    while [[ $# -gt 2 ]]; do
        key="$1"

        case "${key}" in 
            -o|--output-file)
                OUTPUT_FILE="$2"
                shift
                shift
                ;;
            *)
                echo "Unknown flag: $1"
                exit 1
                ;;
        esac 
    done

    ARGS_FILE="${1}"
    INPUT_FILE="${2}"

    if [ ! -e "${ARGS_FILE}" ]; then
        echo "File ${ARGS_FILE} does not exist"
    elif [ ! -e "${INPUT_FILE}" ]; then
        echo "File ${INPUT_FILE} does not exist"
    elif [ -z "${OUTPUT_FILE}" ]; then
        pgn-extract -A ${ARGS_FILE} ${INPUT_FILE}
    else
        pgn-extract -A ${ARGS_FILE} -o ${OUTPUT_FILE} ${INPUT_FILE}
    fi
}

main $@
