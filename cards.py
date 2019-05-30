import utils

class Card:
    """
    attributes: front, back, due_time, last_interval, efactor
    """
    
    def __init__(self, front, back, due_time, last_interval, efactor):
        self.front = front
        self.back = back
        self.due_time = due_time
        self.last_interval = last_interval
        self.efactor = efactor

    @staticmethod
    def new(front, back):
        return Card(front, back, due_time=utils.days(), last_interval=None, efactor=2.5)
