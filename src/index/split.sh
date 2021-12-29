#!/bin/sh

set -e

print_usage() {
   cat << EOF
NAME
    split.sh -- splits a PGN file into one game per file

SYNOPSIS
    split.sh [-h/--help] [-o/--output-dir dir_name] file

DESCRIPTION
    Splits the source PGN file into one game per PGN file.

    -h, --help
        Print split.sh documentation to stdout.

    -a args_file, --args-file args_file
        Process the PGN file according to a set of rules defined in args_file. The args_file needs to be compatible with the pgn-extract arguments file format. See https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/help.html#-A for details.

    -o dir_name, --output-dir dir_name
        The directory where the output is stored. By default, the output directory is the directory where the script is being called from.

EXAMPLES
    Split file file.pgn into one file per game into the current directory.
        split.sh file.pgn
    Split file file.pgn into one file per game into the data/split directory.
        split.sh -o data/split file.pgn
EOF
   exit 1
}

main() {
    if [ $# -eq 0 ]; then print_usage; fi
    for i in "$@" ; do [[ $i == "-h" ]] || [[ $i == "--help" ]] && print_usage ; done

    while [[ $# -gt 1 ]]; do
        key="$1"

        case "$key" in 
            -a|--args-file)
                PGN_EXTRACT_ARGS_FILE="$2"
                shift
                shift
                ;;
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

    pgn-extract -#1 -A ${PGN_EXTRACT_ARGS_FILE} "$1"

    if [[ ! -z "${OUTPUT_DIR}" ]]; then
        mv [0-9]*.pgn ${OUTPUT_DIR}
    fi
}

main $@
