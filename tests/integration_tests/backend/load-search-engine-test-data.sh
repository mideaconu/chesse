#!/bin/sh

set -euo pipefail

elasticsearch_data_dir="tests/data/backend/elasticsearch"

create_index() {
    echo "Creating index ${1}"
    curl -X PUT "https://localhost:9201/${1}?pretty" \
        -u elastic:elastic \
        --cacert config/ca.crt \
        --data-binary @"${elasticsearch_data_dir}/indices/${2}" \
        -H 'Content-Type: application/json'
}

bulk_insert() {
    echo "Bulk inserting documents from file ${1}"
    curl -X POST "https://localhost:9201/_bulk" \
        -u elastic:elastic \
        --cacert config/ca.crt \
        --data-binary @${1} \
        -H 'Content-Type: application/json' | jq \
            -s 'map({status_code: .items[].index.status}) | group_by(.status_code) | map({status_code: .[0].status_code, count: length}) | .[]' 
}

main() {
    for index in "games" "positions"; do
        create_index ${index} "${index}_index_mapping.json"

        for file in ${elasticsearch_data_dir}/documents/${index}/*; do
            if [ -f "${file}" ]; then
                bulk_insert "${file}" 
            fi
        done
    done
}

main "$@"
