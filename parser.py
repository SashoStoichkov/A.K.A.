import const

from db_manager import DBManager
from decks import Deck
from cards import Card


def create_decks(deck_rows):
    created_decks = {}
    while deck_rows:
        for index, deck_row in enumerate(deck_rows):
            current_id, current_name, parent_id = deck_row
            if parent_id is None:
                # the row represents a root deck
                current_deck = Deck(id=current_id, name=current_name)
                deck_rows.pop(index)
                created_decks[current_id] = current_deck
                break
            elif parent_id in created_decks:
                current_deck = Deck(current_name)
                parent = created_decks[parent_id]
                parent.subdecks[current_name] = current_deck
                deck_rows.pop(index)
                created_decks[current_id] = current_deck
                break                
    return created_decks


# TODO: change efactor to EF and test this
def populate_decks(created_decks):
    dbm = DBManager(const.DB_NAME)
    for deck_id, deck in created_decks.items():
        for card_row in dbm.get_cards_for_deck(deck_id):
            card_id, EF, front, back, due_time, last_interval = card_row
            deck.cards.add(Card(deck=deck, id=card_id, EF=EF, front=front,
                                back=back, due_time=due_time,
                                last_interval=last_interval))
    return created_decks



lst = DBManager('database.db').get_decks()
cd = create_decks(lst)
populate_decks(cd)
