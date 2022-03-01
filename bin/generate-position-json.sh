#!/bin/sh

set -euo pipefail

output_file="output.json"

## Prints script usage to stdout
print_usage() {
   cat << EOF
NAME
    generate-position-json.sh -- TBC
SYNOPSIS
    generate-position-json.sh [-h/--help] [-o/--output-file output_file] fen_file json_game_file

DESCRIPTION
    TBC

    -h, --help
        Print generate-position-json.sh documentation to stdout.

    -o output_file, --output output_file
        Save the output to the output_file. By default, the output is saved to output.json.

EXAMPLES
    generate-position-json.sh file.fen file.pgn
        TBC
    generate-position-json.sh -o file.json file.fen file.pgn
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
    json_game_file="${2}"

    echo "[]" > "${output_file}"

    game_id=$(jq -r '.id' ${json_game_file})

    while IFS= read -r line; do
        encoding=$(encode similarity --fen "${line}")
        cat <<< $(jq --arg encoding "${encoding}" --arg fen "${line}" --arg game_id "${game_id}" '. += [{"position": {"fen": $fen, "encoding": $encoding}, "games": [{"id": $game_id}]}]' ${output_file}) > ${output_file}
    done < "${fen_file}"
}

main "$@"
