#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [1/4] Cleaning build & coverage artifacts ==="
rm -rf build/ dist/ *.egg-info python/involute/*.so
rm -f tests/test_involute tests/test_involute_prod
rm -f tests/*.o src/*.o tests/*.gcda tests/*.gcno tests/*.gcov src/*.gcda src/*.gcno src/*.gcov *.gcov
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +

echo "=== [2/4] Compiling object files & running C coverage harness ==="
# Step A: Compile sources individually to .o files (preserves exact gcno/gcda filenames)
gcc -O0 -g --coverage -Iinclude -c tests/test_involute.c -o tests/test_involute.o
gcc -O0 -g --coverage -Iinclude -c src/involute_wrapper.c -o src/involute_wrapper.o

# Step B: Link object files into binary
gcc --coverage tests/test_involute.o src/involute_wrapper.o -lm -o tests/test_involute

# Step C: Execute test binary to write .gcda files
./tests/test_involute

# Step D: Run gcov directly on object paths
gcov tests/test_involute.o src/involute_wrapper.o

echo "=== [3/4] Rebuilding Python package ==="
pip install --no-build-isolation --no-deps -e .

echo "=== [4/4] Executing Pytest Coverage Suite ==="
pytest --cov=involute --cov-report=term-missing tests/

echo "=== ALL BUILD & COVERAGE TESTS PASSED GREEN ==="