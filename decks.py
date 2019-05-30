import sqlite3

class Deck:
    """
    attributes: self.name, self.subdecks, self.cards, self.due_cards
    """

    def __init__(self, name):
        self.name = name
        self.subdecks = {}
        self.cards = set()
        self.due_cards = set()
    
    def add_card(self, card):
        raise NotImplementedError

    def remove_card(self):
        raise NotImplementedError
    
    def refresh(self):
        # updates @self.due_cards
        raise NotImplementedError
