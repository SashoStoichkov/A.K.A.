import sqlite3
import const


class DBManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def commit(self, func):
        def func_wrapper(*args, **kwrags):
            func(*args, **kwrags)
            self.conn.commit()
        return func_wrapper

    def get_decks(self):
        query ="""\
            SELECT * FROM Deck;
        """
        self.cursor.execute(query)

        data = self.cursor.fetchall()
        return data

    def get_cards_for_deck(self, deck_id):
        query = """\
            SELECT Card.id, EF, front, back, due_time, last_interval FROM Card
            	INNER JOIN Deck
            		ON Card.deck_id = Deck.id
            WHERE Deck.id = ?;
        """

        self.cursor.execute(query, (deck_id, ))

        cards = self.cursor.fetchall()
        return cards

    
    # def add_card(self, deck_id, card_obj):
    #     query = """\
    #         INSERT INTO Card(EF, front, back, due_time, last_interval, deck_id) 
    #         VALUES(2.5, "WHo am I?", "Sasho", "2019-05-30", null, ?)
    #     """

    #     self.cursor.execute(query, (deck_id))


if __name__ == "__main__":
    dbm = DBManager(const.DB_NAME)
    # [print(row_data) for row_data in dbm.get_decks()]
    [print(card) for card in dbm.get_cards_for_deck(1)]
