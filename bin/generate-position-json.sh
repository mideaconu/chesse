#!/bin/sh

set -euo pipefail

output_file="output.json"

## Prints script usage to stdout
print_usage() {
   cat << EOF
NAME
    generate-position-json.sh -- generates a position object JSON

SYNOPSIS
    generate-position-json.sh [-h/--help] [-o/--output-file output_file] fen_file

DESCRIPTION
    Generated a position object JSON file from a FEN file. The position object contains the FEN representation of the position (excluding castling, en pessant, or move count) and the similarity encoding for that position.

    -h, --help
        Print generate-position-json.sh documentation to stdout.

    -o output_file, --output output_file
        Save the output to the output_file. By default, the output is saved to output.json.

EXAMPLES
    generate-position-json.sh file.fen
        Generates the position object JSON from file.fen and writes is to output.json.
    generate-position-json.sh -o file.json file.fen
        Generates the position object JSON from file.fen and writes is to file.json.
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

    fen_file="${1}"

    echo "[]" > "${output_file}"

    cut -d ' ' -f 1 < "${fen_file}" | while IFS= read -r line; do
        encoding=$(encode similarity --fen "${line}")
        cat <<< $(jq --arg encoding "${encoding}" --arg fen "${line}" '. += [{"position": {"fen": $fen, "encoding": $encoding}}]' ${output_file}) > ${output_file}
    done
}

main "$@"
