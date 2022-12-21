# tile-engine

# Commands

pipenv shell # Activate virtual environment

# Check for vulnerabilities

pipenv check

# Run Tests

pytest

# Run Test with Logs

pytest --log-cli-level=INFO

# Run Specific Test

pytest test_mod.py::TestClass::test_method
pytest test/assembler_test.py::TestAssembler::test_add_text_all_blocks

# Run the application

pipenv run python3 main.py test/inputs/sample_input_payload.json

# Pipenv guide: https://realpython.com/pipenv-guide/

# Organize ouput files:

Let's put all output files into a folder called temp_output/
Name files based off of their assembler / downloader step name
Steps:

1. Downloader - download the tiles
2. Assembler - assemble-tiles to one image
3. Assembler - crop-image to the bbox
4. Assembler - add-pin to the image
5. Assembler - add-style to the map image (transparency etc.)
6. Assembler - add-text to the image
7. Assembler - add-border to the image

TO DO List:

1. Ctrl shift I thing to automatically fix spacing stuff.
2. Clean up import so that they don’t have \*. Only import functions
3. Exception Handling
4. Logging
5. Result Codes
6. Validating Engine inputs
7. Strong typing / hybrid? Not sure? Research pros and cons. Might not be worth doing.
8. Unit Testing - PyTest
9. Integration Testing
10. Acceptance Testing
11. Delete images we downloaded once we are done with them. Clean up functions for each engine call (assembler, downloader, etc.)
12. Bbox edge cases: lon and lat across prime meridian /equator. How are those handled.
13. Think of better way to separate engine_utils into multiple utils.

14. FIll in ValueValidator Class
