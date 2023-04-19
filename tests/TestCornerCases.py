from test.TestCase import TestCase

all_tests = []
case_id = 0

###############
# TEST CASE 0
###############
desc = "Create an empty folder end space."
test_case = f"""
corner/{case_id}-{desc}/empty_folder: 
"""
expected = f"corner/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
# BUG?: expected a folder, but got a file with 1 line of text
desc = "Create a file with a nested folder which means a folder"
test_case = f"""
corner/{case_id}-{desc}/file: a/new/folder
"""
expected = f"corner/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1


###############
# TEST CASE 0
###############
desc = "Create a file with 1 line of content space removed"
test_case = f"""
corner/{case_id}-{desc}/file.txt:Line 1
"""
expected = f"corner/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1


###############
# TEST CASE 0
###############
desc = "Create a file with 1 line of content colon removed"
test_case = f"""
corner/{case_id}-{desc}/file.txt Line 1
"""
expected = False

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

print(*all_tests, sep='\n', end='\n\n')
