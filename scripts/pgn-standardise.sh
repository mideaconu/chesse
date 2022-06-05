#!/bin/sh

set -euo pipefail

output_file=""

## Prints script usage to stdout
print_usage() {
   cat << EOF
NAME
    pgn-standardise.sh -- standardise a PGN file

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

## Checks if any arguments are passed to the script and prints usage if not
check_no_flags() {
    if [ "${1}" -eq 0 ]; then print_usage; fi
}

## Checks if a help flag is passed to the script
check_help_flags() {
    if [[ " ${1} " =~ .*\ "-h"\ .* ]] || [[ " ${1} " =~ .*\ "--help"\ .* ]]; then print_usage; fi
}

main() {
    check_no_flags "$#"
    check_help_flags "$@"

    while [[ "$#" -gt 1 ]]; do
        key="${1}"

        case "$key" in 
            -o|--output-file)
                output_file="${2}"
                shift
                shift
                ;;
            *)
                echo "Unknown flag: ${1}" >&2
                exit 1
                ;;
        esac 
    done

    input_file="${1}"

    if [ -e "${input_file}" ]; then
        # TODO make sed command OS-agnostic - it currently is written for OSX
        if [ -z "${output_file}" ]; then
            sed -i '' -e 's/\[UTCDate/\[Date/g' -e 's/\[UTCTime/\[Time/g' "${input_file}"
        else
            sed -e 's/\[UTCDate/\[Date/g' -e 's/\[UTCTime/\[Time/g' "${input_file}" > "${output_file}"
        fi
    else
        echo "File ${input_file} does not exist" >&2
    fi
}

main "$@"
