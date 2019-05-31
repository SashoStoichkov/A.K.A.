import utils

# invariant: all cards and decks have a reference to the same DBManager instance

class Card:
    """
    attributes: id, front, back, due_time, last_interval, EF, deck, dbm
    """
    
    def __init__(self, deck, id, front, back, due_time, last_interval, EF):
        self.deck = deck
        self.id = id
        self.front = front
        self.back = back
        self.due_time = due_time
        self.last_interval = last_interval
        self.EF = EF
        self.dbm = deck.dbm

    @classmethod
    def new(deck, front, back):
        card.dbm = deck.dbm
        card.id = None

    def write_to_db(self, dbm):
        dct = {attr: getattr(self, attr) for attr in ('id', 'front', 'back', 'due_time', 'last_interval', 'EF')}
        dct['deck_id'] = self.deck.id
        dbm.update_card(dct)
