#!/bin/bash
# All arguments of this script will be encoded to a JSON array and then transmitted to the "legacy run server"
#
# With jq1.6 we could greatly simplify this script to a single line:
#
# jq -cn --args '$ARGS.positional' "$@" | socat ...
#
# However for now we are stuck on jq1.5, where the option `--args` is not available


SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
counter=0
template="["
for f in "$@"
do
    args+=(--arg "arg$counter" "$f")
    template+="\$arg$counter,"
    ((counter++))
done
template=${template/%,}"]"
jq -cn "${args[@]}" "$template" | socat -t300 - "unix-client:$SCRIPT_DIR/legacy_run_server.sock"
