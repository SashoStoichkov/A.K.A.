import sqlite3

class Deck:
    """
    attributes: self.name, self.subdecks, self.cards, self.due_cards, self.dbm
    """

    def __init__(self, id, name, dbm):
        self.name = name
        self.id = id
        self.dbm = dbm
        self.subdecks = {}
        self.cards = []
        self.due_cards = set()

    def add_card(self, card):
        raise NotImplementedError
        
    def remove_card(self):
        raise NotImplementedError
    
    def refresh(self):
        # updates @self.due_cards
        raise NotImplementedError

