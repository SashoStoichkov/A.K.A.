import sqlite3

import const

from decks import Deck
from cards import Card


class Loader:
    def __init__(self, dbname):
        self.session = models.func(dbname)

    @property
    def deck_rows(self):
        # just a utility function
        # returns a list of rows (<deck-id>, <deck-name>, <deck-parent-id>)
        
        query ="""\
            SELECT * FROM Deck;
        """
        
        cursor = self.conn.execute(query)

        data = cursor.fetchall()
        self.conn.commit()
        return data

    
    def card_rows(self, deck_id):
        # just a utility function
        # returns a list of card rows, which have the form
        # (id, EF, front, back, due_time, last_interval)
        
        query = """\
            SELECT Card.id, EF, front, back, due, last_interval FROM Card
            	INNER JOIN Deck
            		ON Card.deck_id = Deck.id
            WHERE Deck.id = ?;
        """

        cursor = self.conn.execute(query, (deck_id, ))
        cards = cursor.fetchall()
        self.conn.commit()
        return cards

    def load(self):
        def create():
            created_decks = {} # maps ids to decks            
            deck_rows = self.deck_rows
            for deck_row in deck_rows:
                current_id, current_name, parent_id = deck_row
                if parent_id is None:
                    # the row represents a root deck
                    current_deck = Deck(id=current_id, name=current_name, conn=self.conn)
                    created_decks[current_id] = current_deck
                elif parent_id in created_decks:
                    parent = created_decks[parent_id]
                    current_deck = Deck(id=current_id, name=current_name, conn=self.conn)
                    parent.subdecks[current_name] = current_deck
                    created_decks[current_id] = current_deck
            return created_decks
        
        def populate(created_decks):
            for deck_id, deck in created_decks.items():
                for card_row in self.card_rows(deck_id):
                    card_id, EF, front, back, due, last_interval = card_row
                    deck.add_card((Card(deck=deck, id=card_id, EF=EF, front=front,
                                        back=back, due=due,
                                        last_interval=last_interval, conn=self.conn)))
            return created_decks

        return populate(create())
            
        
cd = Loader(const.DB_NAME).load()
deck1 = cd[1]
card1, card2 = deck1.cards
