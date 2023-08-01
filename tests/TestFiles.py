from tests.TestCase import TestCase

all_tests = []
case_id = 0

###############
# TEST CASE 0
###############
desc = "Create an empty file."
test_case = f"""
files/{case_id}-{desc}/empty_file.txt:
"""
expected = f"files/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1


###############
# TEST CASE 0
###############
desc = "Create a file with 1 line of content"
test_case = f"""
files/{case_id}-{desc}/file.txt: Line 1
"""
expected = f"files/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "Create a file with multiple lines of content"
test_case = f"""
files/{case_id}-{desc}/file.txt: |
                            Line 1
                            Line 2
"""
expected = f"files/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "Create a file without extension and multiple lines of content"
test_case = f"""
files/{case_id}-{desc}/file: |
                            Line 1
                            Line 2
"""
expected = f"files/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "Create a yaml formatted file"
test_case = f"""
files/{case_id}-{desc}/file.yaml: |
                            Level 1:
                                Level 2:
                                    - item 1
                                    - item 2
                                condition: True
                                number: 5
"""
expected = f"files/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "Create a json formatted file"
test_case = f"""
files/{case_id}-{desc}/file.json""" + """: |
                            'Level 1':
                                { 'Level 2': ['item 1', 'item 2'], 
                                'condition': True, 
                                'number': 5
                                }
"""
expected = f"files/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1


print(*all_tests, sep='\n', end='\n\n')
