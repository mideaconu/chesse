#!/bin/sh

set -e

print_usage() {
   cat << EOF
NAME
    preprocess.sh -- preprocess a source PGN file

SYNOPSIS
    preprocess.sh [-a args_file] [--args-file args_file] [-h] [--help] [-o output_file] [--output-file output_file] file

DESCRIPTION
    Preprocesses the source PGN file.

    By default, it finds the occurences of the 'UTCDate' and 'UTCTime' labels in the PGN file and replaces them with the 'Date' and 'Time' labels. Additional rules can be set in the args_file.

    -a args_file, --args-file args_file
        Process the PGN file according to a set of rules defined in args_file. The args_file needs to be compatible with the pgn-extract arguments file format. See https://www.cs.kent.ac.uk/people/staff/djb/pgn-extract/help.html#-A for details.

    -h, --help
        Print preprocess.sh documentation to std output.

    -o output_file, --output output_file
        Print the output to the output_file. By default, the output is printed to output.pgn.

EXAMPLES
    Preprocess file1.pgn according to the criteria described above.
        preprocess.sh file1.pgn
EOF
   exit 1
}

main() {
    if [ $# -eq 0 ]; then print_usage; fi

    while [[ $# -gt 1 ]]; do
        key="$1"

        case "$key" in 
            -a|--args-file)
                PGN_EXTRACT_ARGS_FILE="$2"
                shift
                shift
                ;;
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

    if [ -e "$1" ]; then
        TEMP_FILE=temp_$(basename "$1")

        sed -e 's/\[UTCDate/\[Date/g' -e 's/\[UTCTime/\[Time/g' "$1" > "$TEMP_FILE"
        pgn-extract -A ${PGN_EXTRACT_ARGS_FILE} -o ${OUTPUT_FILE:-output.pgn} "$TEMP_FILE"

        rm "$TEMP_FILE"
    else
        echo "File $1 does not exist"
    fi
}

main $@
