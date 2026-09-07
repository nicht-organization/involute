#!/usr/bin/env bash
set -e

echo "=== [1/3] Cleaning build artifacts ==="
rm -rf build/ dist/ *.egg-info python/involute/libinvolute.so

echo "=== [2/3] Compiling Modular OpenMP + MMAP Shared Library ==="
gcc -shared -fPIC -O3 -march=native -flto -fopenmp \
    -Iinclude \
    src/core/*.c src/math/*.c src/stream/*.c \
    -lm -o python/involute/libinvolute.so

echo "=== [3/3] Compiling & Running C Suite ==="
gcc -O3 -march=native -Iinclude tests/c/test_involute.c python/involute/libinvolute.so -lm -o tests/c/runner
./tests/c/runner
rm -f tests/c/runner

echo "=== PRODUCTION BUILD READY IN python/involute/libinvolute.so ==="
