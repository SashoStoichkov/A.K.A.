import utils

class Card:
    """
    attributes: id, front, back, due_time, last_interval, EF, deck
    """
    
    def __init__(self, deck, id, front, back, due_time, last_interval, EF, dbm):
        self.deck=deck
        self.id = id
        self.front = front
        self.back = back
        self.due_time = due_time
        self.last_interval = last_interval
        self.EF = EF
        self.dbm = dbm

    @staticmethod
    def new(front, back):
        return Card(front, back, due_time=utils.days(), last_interval=None, EF=2.5)

    def __setattr__(self, name, newval):
        super().__setattr__(name, newval)
        dct = {attr: getattr(self, attr) for attr in ('id', 'front', 'back', 'due_time', 'last_interval', 'EF')}
        dct['deck_id'] = self.deck.id
        self.dbm.update_card(dct)

