#!/bin/sh

set -e

print_usage() {
   cat << EOF
NAME
    fen-split.sh -- splits a FEN file so that there is only one per position

SYNOPSIS
    fen-split.sh [-h/--help] [-o/--output-dir dir_name] file

DESCRIPTION
    Splits the source FEN file into one position per FEN file.

    -h, --help
        Print fen-split.sh documentation to stdout.

    -o dir_name, --output-dir dir_name
        The directory where the output is stored. By default, the output directory is the same directory as the input file.

EXAMPLES
    fen-split.sh file.fen
        Splits file file.fen into one file per position into the current directory.
    fen-split.sh -o data/split file.fen
        Splits file file.fen into one file per position into the data/split directory.
        
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

    DIRNAME=$(dirname ${INPUT_FILE})
    FILENAME=$(basename ${INPUT_FILE})

    split -l 1 ${INPUT_FILE} "${INPUT_FILE%.*}-"
    find ${DIRNAME} -type f \( -name "${FILENAME%.*}-*" -and \! -name "*.*" \) -exec mv {} {}.fen \;

    if ls ${INPUT_FILE%.*}-*.fen 1>/dev/null 2>&1; then
        if [[ ! -z "${OUTPUT_DIR}" ]]; then
            mv ${INPUT_FILE%.*}-*.fen ${OUTPUT_DIR}
        fi
    fi
}

main $@
