import sqlite3

import utils

from cards import Card

class Deck:
    """
    * attributes:
    - self.id: a unique (among all other decks) integer which is used
      as the connection between the instance and the database.
    - self.name
    - self.subdecks: a dict which maps names to decks (with the same name)
    - self.cards: a dict which maps card ids to cards
    - self.conn: a connection to the database which contains the
      persistent storage of the deck
    """

    def __init__(self, id, name, conn):
        self.id = id
        self.name = name
        self.subdecks = {}
        self.cards = {}
        self.conn = conn
                    
    def add_card(self, card):
        # adds a card to the deck's collection of cards
        self.cards[card.id] = card
                
    def flush(self):
        # possibly useful for renaming decks
        raise NotImplementedError

    @property
    def due_cards(self):
        # returns a list of all cards which are up for review
        raise NotImplementedError
