#!/usr/bin/env bash
set -eu

project_dir=$(cd "$(dirname "$0")/.." && pwd)
main_output="$project_dir/build/classes/main"
test_output="$project_dir/build/classes/test"

# Compile the application first, then compile the tests against its classes.
"$project_dir/scripts/compile.sh"
mkdir -p "$test_output"
find "$project_dir/src/test/java" -name '*.java' -print | sort > "$project_dir/build/test-sources.txt"
javac --release 17 -cp "$main_output" -d "$test_output" @"$project_dir/build/test-sources.txt"

java -cp "$main_output:$test_output" kz.aitu.builder.car.CarBuilderTest
