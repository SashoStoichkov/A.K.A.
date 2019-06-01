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

    @staticmethod
    def new(front, back, deck, conn):
        dct = dict(id=utils.getid(conn, 'card'), front=front, back=back,
                   deck=deck, due=utils.today(), last_interval=None,
                   EF=2.5, conn=conn)
        new_card = Card(**dct)

        ##################################################
        # insert into the card into the database
        
        # dct contains almost all attributes needed for inserting
        # a row into the database, except deck_id
        dct['deck_id'] = deck.id
        
        conn.execute("""
            INSERT INTO card (id, front, back, deck_id, due, last_interval, EF)
            VALUES (:id, :front, :back, :deck_id, :due, :last_interval, :EF)""",
                     dct)
        
        conn.commit()
                
    def flush(self):
        dct = {attr: getattr(self, attr) for attr in ('id', 'front', 'back', 'due', 'last_interval', 'EF')}
        dct['deck_id'] = self.deck.id
        
        query = """
            UPDATE Card SET EF=:EF, front=:front, back=:back, due=:due,
                            last_interval=:last_interval, deck_id=:deck_id
            WHERE id = :id;
        """

        self.conn.execute(query, dct)
        self.conn.commit()

    def reschedule(self, ans):
        self.EF = max(1.3, min(2.5, self.EF - 0.8 + 0.28 * ans - 0.02 * ans * ans))
        self.last_interval = int((1 if self.last_interval is None
                                  else 6 if self.last_interval is 1
                                  else self.last_interval * self.EF))
        self.due = utils.today() + self.last_interval

    def removed_from_deck(self):
        # called when the card is removed from it's deck
        self.conn.execute('DELETE FROM card WHERE id = ?', (self.id,))
