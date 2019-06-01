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

        
    @staticmethod
    def create_root(name, conn):
        newdeck = Deck(id=utils.getid(conn, 'deck'), name=name, conn=conn)

        parent_id = None if parent is None else parent.id            
        conn.execute('INSERT INTO deck(id, name, parent_id) VALUES (?, ?, ?)',
                     (newdeck.id, newdeck.name, parent_id))
        conn.commit()
        return newdeck

        
    def create_card(self, front, back):
        dct = dict(id=utils.getid(self.conn, 'card'), front=front, back=back,
                   deck=self, due=utils.today(), last_interval=None,
                   EF=2.5, conn=self.conn)
        
        card = Card(**dct)

        ##################################################
        # insert the card into the database
        
        # dct contains almost all attributes needed for inserting
        # a row into the database, except deck_id
        dct['deck_id'] = self.id
        
        card.conn.execute("""
            INSERT INTO card (id, front, back, deck_id, due, last_interval, EF)
            VALUES (:id, :front, :back, :deck_id, :due, :last_interval, :EF)""",
                          dct)
        
        card.conn.commit()

        self.cards[card.id] = card
        return card

    def create_subdeck(self, name):
        newdeck = Deck(id=utils.getid(conn, 'deck'), name=name, conn=self.conn)
        conn.execute('INSERT INTO deck(id, name, parent_id) VALUES (?, ?, ?)',
                     (newdeck.id, newdeck.name, self.id))
        conn.commit()
        return newdeck
            
    def add_card(self, card):
        self.cards[card.id] = card
        
    def remove_card(self, card_id):
        card = self.cards.get(card_id)
        if card is None:
            raise ValueError(f"the deck doesn't have a card with id {card_id}")
        del self.cards[card_id]
        card.removed_from_deck()
        
    def flush(self):
        raise NotImplementedError

    def remove_from_db(self):
        # call automatically when the object is destroyed?
        raise NotImplementedError

    @property
    def due_cards(self):
        # returns a list of all cards which are up for review
        raise NotImplementedError
