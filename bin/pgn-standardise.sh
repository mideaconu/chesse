#!/bin/sh

set -e

print_usage() {
   cat << EOF
NAME
    pgn-standardise.sh -- standardise a PGN file for compatibility with PGN-processing software

SYNOPSIS
    pgn-standardise.sh [-h/--help] [-o/--output-file output_file] file

DESCRIPTION
    Standardises a PGN file for compatibility with PGN-processing software, perforing the following operations:
        - finds the occurence of the 'UTCDate' label in the PGN file (if present) and replaces it with the 'Date' label
        - finds the occurence of the 'UTCTime' label in the PGN file (if present) and replaces it with the 'Time' label

    -h, --help
        Print pgn-standardise.sh documentation to stdout.

    -o output_file, --output output_file
        Save the output to the output_file. By default, the operation is done in-place.

EXAMPLES
    pgn-standardise.sh file.pgn
        Standardises file.pgn according to the criteria described above.
    pgn-standardise.sh -o output_file.pgn file.pgn
        Standardises file.pgn according to the criteria described above, and saves the output to output_file.pgn.
EOF
   exit 0
}

main() {
    if [ $# -eq 0 ]; then print_usage; fi
    for i in "$@" ; do [[ $i == "-h" ]] || [[ $i == "--help" ]] && print_usage ; done

    while [[ $# -gt 1 ]]; do
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

    INPUT_FILE="${1}"

    if [ -e ${INPUT_FILE} ]; then
        # TODO make sed command OS-agnostic - it currently is written for OSX
        if [ -z "${OUTPUT_FILE}" ]; then
            sed -i '' -e 's/\[UTCDate/\[Date/g' -e 's/\[UTCTime/\[Time/g' ${INPUT_FILE}
        else
            sed -e 's/\[UTCDate/\[Date/g' -e 's/\[UTCTime/\[Time/g' ${INPUT_FILE} > ${OUTPUT_FILE}
        fi
    else
        echo "File $1 does not exist"
    fi
}

main $@
