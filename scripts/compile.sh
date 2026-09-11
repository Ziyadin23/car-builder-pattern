#!/usr/bin/env bash
set -eu

project_dir=$(cd "$(dirname "$0")/.." && pwd)
main_output="$project_dir/build/classes/main"

mkdir -p "$main_output"
find "$project_dir/src/main/java" -name '*.java' -print | sort > "$project_dir/build/main-sources.txt"
javac --release 17 -d "$main_output" @"$project_dir/build/main-sources.txt"

echo "Compilation successful. Classes are in build/classes/main."

