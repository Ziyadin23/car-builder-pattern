#!/usr/bin/env bash
set -eu

project_dir=$(cd "$(dirname "$0")/.." && pwd)
"$project_dir/scripts/compile.sh"
java -cp "$project_dir/build/classes/main" kz.aitu.builder.app.Main

