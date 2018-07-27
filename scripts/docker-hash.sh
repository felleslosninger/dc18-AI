if [[ $# < 1 ]]; then
    echo "Error: $0 must be called with at least one argument" >&2
    exit 1
fi

docker ps | grep "$1" | sed -n 's/\(............\).*/\1/p'
