import utils

class Card:
    """
    attributes: id, front, back, due_time, last_interval, efactor, deck
    """
    
    def __init__(self, deck, id, front, back, due_time, last_interval, EF):
        self.deck=deck
        self.id = id
        self.front = front
        self.back = back
        self.due_time = due_time
        self.last_interval = last_interval
        self.EF = EF

    @staticmethod
    def new(front, back):
        return Card(front, back, due_time=utils.days(), last_interval=None, EF=2.5)

    

    
