# 1. Clean build artifacts
rm -rf python/involute/libinvolute.so tests/test_involute build/

# 2. Compile and run direct C unit tests
gcc -O3 -Iinclude tests/test_involute.c -lm -o tests/test_involute
./tests/test_involute

# 3. Rebuild shared library & install Python package in editable mode
pip install -e .

# 4. Run full Python test suite (integration, diophantine, schema)
pytest -v