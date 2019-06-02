import unittest
from tests.test_collection import TestLoader, TestCollection
from stub_manager import StubManager

if __name__ == "__main__":
    test_cases = [TestLoader, TestCollection]
    for suite in [test_case.build_suite() for test_case in test_cases]:
        with StubManager():
            unittest.TextTestRunner().run(suite)
