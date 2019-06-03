import utils

class Card:
    """
    * attributes:
    - self.id: a unique integer (among all cards) which identifies the card in the database
    - self.front
    - self.back
    - self.due: an integer which signifies the epoch day in which the
      card is up for review.
    - self.last_interval: used by the scheduler
    - self.EF: used by the scheduler
    - self.deck: the deck to which the card belongs to
    - self.conn: a connection to the database which contains the
      persistent storage of the card
    """

    def __init__(self, id, front, back, deck, conn, due, last_interval, EF):
        self.id = id
        self.front = front
        self.back = back
        self.due = due
        self.last_interval = last_interval
        self.EF = EF
        self.deck = deck
        self.conn = conn
        
    def flush(self):
        query = """
            UPDATE Card SET EF=:EF, front=:front, back=:back, due=:due,
                            last_interval=:last_interval, deck_id=:deck_id
            WHERE id = :id;
        """
        dct = dict(id=self.id, front=self.front, back=self.back,
                   due=self.due, last_interval=self.last_interval,
                   EF=self.EF, deck_id=self.deck.id)
        self.conn.execute(query, dct)
        self.conn.commit()


    def reschedule(self, ans):
        # ans is an int such that 0 <= ans <= 5
        self.EF = max(1.3, min(2.5, self.EF - 0.8 + 0.28 * ans - 0.02 * ans * ans))
        if ans < 3:
            self.last_interval = None
            self.due = utils.today() + 1
        else:
            self.last_interval = int(1 if self.last_interval is None
                                     else 6 if self.last_interval == 1
                                     else self.last_interval * self.EF)
            self.due = utils.today() + self.last_interval
