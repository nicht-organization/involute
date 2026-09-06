# 1. Clean build environment
./clean_builtest.sh

# 2. Run C unit tests with coverage
gcc -O0 -g --coverage -Iinclude tests/test_involute.c src/involute_wrapper.c -lm -o tests/test_involute
./tests/test_involute
gcov src/involute_wrapper.c

# 3. Run Python test suite with pytest-cov
pip install pytest-cov
pytest --cov=involute --cov-report=term-missing tests/