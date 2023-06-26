from tests.TestCase import TestCase

all_tests = []
case_id = 0

###############
# TEST CASE 0
###############
desc = "Create an empty folder."
test_case = f"""
folders/{case_id}-{desc}/empty_folder:
"""
expected = f"folders/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1


###############
# TEST CASE 0
###############
desc = "Create a folder with 1 file"
test_case = f"""
folders/{case_id}-{desc}/folder/file.txt: Line 1
"""
expected = f"folders/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "Create nested folders"
test_case = f"""
folders/{case_id}-{desc}/folder: 
                                subdir1:
                                subdir2:
"""
expected = f"folders/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "Create nested folders and files"
test_case = f"""
folders/{case_id}-{desc}:
                        file.txt: |
                            Line 1
                            Line 2
                        First year:
                            English: |
                                    Line 1
                                    Line 2
                            Maths.txt: E=mc^2
                            CS.yaml: "Key: Value"
                            History.json:
                            Art:
                        Second year: 2
                        Third year:
"""
expected = f"folders/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "Create a yaml formatted file"
test_case = f"""
folders/{case_id}-{desc}/file.yaml: |
                            Level 1:
                                Level 2:
                                    - item 1
                                    - item 2
                                condition: True
                                number: 5
"""
expected = f"folders/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE N
###############
case_n = """abc:
    Download:
        Music:
        Movies:
    University:
        First year:
            English: |
                    Line 1
                    Line 3
            Maths.txt: E=mc^2
            CS.yaml: "Key: Value"
            History.json:
            Art:
        Second year: 2
        Third year:
"""
expected = f"folders/{case_id}-{desc}"

print(*all_tests, sep='\n', end='\n\n')
