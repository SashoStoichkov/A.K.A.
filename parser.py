import const

from db_manager import DBManager
from decks import Deck
from cards import Card


class Parser:
    def __init__(self, dbname):
        self.dbm = DBManager(dbname)

    def create_decks(self):
        def create():
            created_decks = {}
            deck_rows = self.dbm.get_decks()
            while deck_rows:
                for index, deck_row in enumerate(deck_rows):
                    current_id, current_name, parent_id = deck_row
                    if parent_id is None:
                        # the row represents a root deck
                        current_deck = Deck(id=current_id, name=current_name, dbm=self.dbm)
                        deck_rows.pop(index)
                        created_decks[current_id] = current_deck
                        break
                    elif parent_id in created_decks:
                        current_deck = Deck(id=current_id, name=current_name, dbm=self.dbm)
                        parent = created_decks[parent_id]
                        parent.subdecks[current_name] = current_deck
                        deck_rows.pop(index)
                        created_decks[current_id] = current_deck
                        break
            return created_decks
        
        def populate(created_decks):
            for deck_id, deck in created_decks.items():
                for card_row in self.dbm.get_cards_for_deck(deck_id):
                    card_id, EF, front, back, due_time, last_interval = card_row
                    deck.cards.append(Card(deck=deck, id=card_id, EF=EF, front=front,
                                           back=back, due_time=due_time,
                                           last_interval=last_interval, dbm=self.dbm))
            return created_decks

        return {deck.name: deck for deck in populate(create()).values()}
            
        
cd = Parser(const.DB_NAME).create_decks()
