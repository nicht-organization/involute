#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [1/3] Cleaning debug build artifacts ==="
rm -rf build/ dist/ *.egg-info python/involute/*.so tests/test_involute_prod
find . -type f -name "*.gcda" -delete
find . -type f -name "*.gcno" -delete

echo "=== Compiling OpenMP Parallel + MMAP Production Library ==="
gcc -O3 -march=native -flto -fopenmp -s -fPIC -shared \
    -Iinclude \
    src/involute_wrapper.c \
    -lm -o python/involute/libinvolute.so

echo "=== [3/3] Compiling Benchmark & Production Test Harness ==="
gcc -O3 -march=native -flto -Iinclude \
    tests/test_involute.c \
    src/involute_wrapper.c \
    -lm -o tests/test_involute_prod

./tests/test_involute_prod

echo "=== PRODUCTION BUILD READY IN python/involute/libinvolute.so ==="
