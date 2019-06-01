import sqlite3

class Deck:
    """
    * attributes:
    - self.id: a unique (among all other decks) integer which is used
      as the connection between the instance and the database.
    - self.name
    - self.subdecks: a dict which maps names to decks (with the same name)
    - self.cards: a list of Card instances
    - self.conn: a connection to the database which contains the
      persistent storage of the deck
    """

    def __init__(self, id, name, conn):
        self.id = id
        self.name = name
        self.subdecks = {}
        self.cards = []
        self.conn = conn

    def add_card(self, card):
        raise NotImplementedError
        
    def remove_card(self):
        raise NotImplementedError
    
    def flush(self):
        raise NotImplementedError
