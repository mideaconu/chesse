#!/bin/sh

set -euo pipefail

output_file="output.json"

## Prints script usage to stdout
print_usage() {
   cat << EOF
NAME
    generate-games-json.sh -- TBC
SYNOPSIS
    generate-games-json.sh [-h/--help] [-o/--output-file output_file] pgn_dir

DESCRIPTION
    TBC

    -h, --help
        Print generate-games-json.sh documentation to stdout.

    -o output_file, --output output_file
        Save the output to the output_file. By default, the output is saved to output.json.

EXAMPLES
    generate-games-json.sh pgn
        TBC
    generate-games-json.sh -o file.json pgn
        TBC
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

    pgn_dir="${1}"

    echo "[]" > "${output_file}"

    for file in "${pgn_dir}"/*.pgn; do
        pgn=$(cat "${file}")
        pgn_gzip=$(cat "${file}" | gzip | base64)
        cat <<< $(jq --arg id "${pgn_gzip}" --arg pgn "${pgn}" '. += [{"id": $id, "pgn": $pgn}]' "${output_file}") > "${output_file}"
    done
}

main "$@"
