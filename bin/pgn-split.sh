#!/bin/sh

set -euo pipefail

output_file=""

## Prints script usage to stdout
print_usage() {
   cat << EOF
NAME
    pgn-split.sh -- splits a PGN file into one game per file

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
        key="$1"

        case "$key" in 
            -o|--output-dir)
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

    pgn-extract -#1 -s "${input_file}"

    if ls [0-9]*.pgn 1>/dev/null 2>&1; then
        if [[ ! -z "${output_file}" ]]; then
            mv [0-9]*.pgn "${output_file}"
        fi
    fi
}

main "$@"
