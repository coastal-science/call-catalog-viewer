from tests.TestCase import TestCase

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
desc = "Create a file with a nested folder which means a file"
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
expected = 'Error'

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1


###############
# TEST CASE 0
###############
desc = "Create a file with 1 line of content colon removed"
test_case = f"""
corner/{case_id}-{desc}/file.txt Line 1
"""
expected = 'Error'

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "Folder name ends in period"
test_case = f"""
corner/{case_id}-{desc}/file.:
"""
expected = f"corner/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1

###############
# TEST CASE 0
###############
desc = "File name ends in period"
test_case = f"""
corner/{case_id}-{desc}/file.: |
                            Level 1:
                                Level 2:
                                    - item 1
                                    - item 2
                                condition: True
                                number: 5
"""
expected = f"corner/{case_id}-{desc}"

all_tests.append(TestCase(case_id, test_case, expected, desc))
case_id += 1


print(*all_tests, sep='\n', end='\n\n')
