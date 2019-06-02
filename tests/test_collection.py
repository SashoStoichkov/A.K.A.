import unittest
import sqlite3
from collection import Loader
from collection import Collection
from const import STUB_NAME


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.loader = Loader(STUB_NAME)
    
    def test_when_deck_rows_is_called_return_all_rows_of_deck_table(self):
        expected_result = [
            (0, 'main', None),
            (1, 'prog-langs', 0), 
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
        self.decks_for_cleaning = [('text-editors', ), ('atom',), ('C++', )]
        self.conn = sqlite3.connect(STUB_NAME)
        self.collection = Loader(STUB_NAME).load()
        self.loader = Loader(STUB_NAME)

    def tearDown(self):
        query = """\
            DELETE FROM Deck WHERE name = ?;
        """
        self.conn.executemany(query, self.decks_for_cleaning)
        self.conn.commit()
        self.conn.close()
    
    def test_when_create_decks_is_called_with_an_empty_string_raise_value_error(self):
        self.assertRaises(ValueError, self.collection.create_decks, "")
     
    def test_when_create_decks_is_called_with_new_root_deck_return_expected_result(self):
        new_deck = 'text-editors'
        self.collection.create_decks(new_deck)
        expected_result = [
            (0, 'main', None),
            (1, 'prog-langs', 0), 
            (2, 'Python', 1), 
            (3, 'C', 1),
            (4, 'text-editors', 0)
        ]
        self.assertEqual(self.loader.deck_rows, expected_result)
        

    def test_when_create_decks_is_called_with_new_subdeck_of_proglangs_return_expected_result(self):
        new_deck = 'prog-langs::C++'
        self.collection.create_decks(new_deck)
        expected_result = [
            (0, 'main', None),
            (1, 'prog-langs', 0), 
            (2, 'Python', 1), 
            (3, 'C', 1),
            (4, 'C++', 1)
        ]
        self.assertEqual(self.loader.deck_rows, expected_result)
    
    def test_when_create_decks_is_called_with_new_root_and_subdeck_return_expected_result(self):
        new_deck = 'text-editors::atom'
        self.collection.create_decks(new_deck)
        expected_result = [
            (0, 'main', None),
            (1, 'prog-langs', 0), 
            (2, 'Python', 1), 
            (3, 'C', 1),
            (4, 'text-editors', 0),
            (5, 'atom', 4)
        ]
        self.assertEqual(self.loader.deck_rows, expected_result)
    
    
    @classmethod
    def build_suite(cls):
        test_suite = unittest.TestSuite()
        test_suite.addTests(unittest.makeSuite(cls))
        return test_suite