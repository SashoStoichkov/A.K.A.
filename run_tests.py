import unittest
from tests.test_collection import TestLoader, TestCreateDecks, TestFindDeck, TestRemoveDeck
from stub_manager import StubManager

if __name__ == "__main__":
    test_cases = [TestRemoveDeck, TestLoader, TestFindDeck, TestCreateDecks]
    for suite in [test_case.build_suite() for test_case in test_cases]:
        with StubManager():
            unittest.TextTestRunner().run(suite)
