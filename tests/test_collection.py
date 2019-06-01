import unittest
from collection import Loader
from collection import Collection
from const import STUB_NAME


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.loader = Loader(STUB_NAME)
    
    def test_when_deck_rows_is_called_return_all_rows_of_deck_table(self):
        expected_result = [
            (1, 'prog-langs', None), 
            (2, 'Python', 1), 
            (3, 'C', 1)
        ]
        self.assertEqual(self.loader.deck_rows, expected_result)

    def test_when_card_rows_is_called_with_id_1_return_expected_cards(self):
        expected_result = [
            (1, 2.5, 'general question 1', 'general answer 1', 12345, 6), 
            (2, 2.5, 'general question 2', 'general answer 2', 10000, 54)]
        self.assertEqual(self.loader.card_rows(1), expected_result)

    def test_when_a_missing_deck_id_is_given_return_empty_list_of_cards(self):
        expected_result = []
        self.assertEqual(self.loader.card_rows(4), expected_result)

    def test_when_load_is_return_collection_instance(self):
        obj = self.loader.load()
        self.assertIsInstance(obj, Collection)

    @classmethod
    def build_suite(cls):
        test_suite = unittest.TestSuite()
        test_suite.addTests(unittest.makeSuite(cls))
        return test_suite



class TestCollection(unittest.TestCase):
    def setUp(self):
        self.collection = Loader(STUB_NAME).load()
        self.loader = Loader(STUB_NAME)
     
    def test_when_create_decks_is_called_with_new_root_deck_return_updates_decks(self):
        self.collection.create_decks('text-editors')
        expected_result = [
            (1, 'prog-langs', None), 
            (2, 'Python', 1), 
            (3, 'C', 1),
            (4, 'text-editors', None)
        ]
        self.assertEqual(self.loader.deck_rows, expected_result)

    def test_when_create_decks_is_called_with_new_subdeck_of_proglangs_return_updates_decks(self):
        self.collection.create_decks('prog-langs::C++')
        expected_result = [
            (1, 'prog-langs', None), 
            (2, 'Python', 1), 
            (3, 'C', 1),
            (4, 'text-editors', None),
            (5, 'C++', 1)
        ]
        self.assertEqual(self.loader.deck_rows, expected_result)

    @classmethod
    def build_suite(cls):
        test_suite = unittest.TestSuite()
        test_suite.addTests(unittest.makeSuite(cls))
        return test_suite
