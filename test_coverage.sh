#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [1/4] Cleaning build & coverage artifacts ==="
rm -rf build/ dist/ *.egg-info python/involute/*.so
rm -f tests/c/runner tests/c/*.o src/**/*.o
find . -type f -name "*.gcda" -delete
find . -type f -name "*.gcno" -delete
find . -type f -name "*.gcov" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +

mkdir -p src/core src/math src/stream tests/c
mkdir -p python/involute/core python/involute/math python/involute/stream
touch python/involute/__init__.py \
      python/involute/core/__init__.py \
      python/involute/math/__init__.py \
      python/involute/stream/__init__.py

echo "=== [2/4] Compiling object files & running C coverage harness ==="
gcc -O0 -g -fopenmp --coverage -Iinclude -c src/core/register.c -o src/core/register.o
gcc -O0 -g -fopenmp --coverage -Iinclude -c src/math/diophantine.c -o src/math/diophantine.o
gcc -O0 -g -fopenmp --coverage -Iinclude -c src/math/radical.c -o src/math/radical.o
gcc -O0 -g -fopenmp --coverage -Iinclude -c src/stream/mmap_stream.c -o src/stream/mmap_stream.o
gcc -O0 -g -fopenmp --coverage -Iinclude -c tests/c/test_involute.c -o tests/c/test_involute.o

gcc -fopenmp --coverage \
    tests/c/test_involute.o \
    src/core/register.o \
    src/math/diophantine.o \
    src/math/radical.o \
    src/stream/mmap_stream.o \
    -lm -o tests/c/runner

./tests/c/runner
gcov src/core/register.o src/math/diophantine.o src/math/radical.o src/stream/mmap_stream.o tests/c/test_involute.o

echo "=== [3/4] Compiling Shared Library directly into Package Root ==="
gcc -shared -fPIC -O3 -march=native -flto -fopenmp \
    -Iinclude \
    src/core/register.c \
    src/math/diophantine.c \
    src/math/radical.c \
    src/stream/mmap_stream.c \
    -lm -o python/involute/libinvolute.so

echo "=== [4/4] Executing Pytest Coverage Suite ==="
PYTHONPATH=python pytest --cov=involute --cov-report=term-missing tests/

echo "=== ALL BUILD & COVERAGE TESTS PASSED GREEN ==="
