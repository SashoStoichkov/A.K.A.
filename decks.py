import sqlite3

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
        self.cards[card.id] = card
        
    def remove_card(self, card_id):
        card = self.cards.get(card_id)
        if card is None:
            raise ValueError(f"the deck doesn't have a card with id {card_id}")
        del self.cards[card_id]
        card.removed_from_deck()
            
    def flush(self):
        raise NotImplementedError
