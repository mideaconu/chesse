#!/bin/sh

set -euo pipefail

output_file=""

## Prints script usage to stdout
print_usage() {
   cat << EOF
NAME
    pgn-flter.sh -- filter a PGN file

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

    while [[ "$#" -gt 2 ]]; do
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
    
    args_file="${1}"
    input_file="${2}"

    if [ ! -e "${args_file}" ]; then
        echo "File ${args_file} does not exist" >&2
    elif [ ! -e "${input_file}" ]; then
        echo "File ${input_file} does not exist" >&2
    elif [ -z "${output_file}" ]; then
        pgn-extract -A "${args_file}" "${input_file}"
    else
        pgn-extract -A "${args_file}" -o "${output_file}" "${input_file}"
    fi
}

main "$@"
