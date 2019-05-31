import utils

class Card:
    """
    attributes: id, front, back, due_time, last_interval, EF, deck, dbm
    """
    
    def __init__(self, deck, id, front, back, due_time, last_interval, EF, dbm):
        self.__dict__['deck'] = deck
        self.__dict__['id'] = id
        self.__dict__['front'] = front
        self.__dict__['back'] = back
        self.__dict__['due_time'] = due_time
        self.__dict__['last_interval'] = last_interval
        self.__dict__['EF'] = EF
        self.__dict__['dbm'] = dbm

    @staticmethod
    def new(front, back):
        return Card(front, back, due_time=utils.days(), last_interval=None, EF=2.5)

    def __setattr__(self, name, newval):
        super().__setattr__(name, newval)
        dct = {attr: getattr(self, attr) for attr in ('id', 'front', 'back', 'due_time', 'last_interval', 'EF')}
        dct['deck_id'] = self.deck.id
        self.dbm.update_card(dct)

