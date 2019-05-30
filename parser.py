import db_manager

from decks import Deck

def create_decks(deck_rows):
    created_decks = {}
    while deck_rows:
        for index, deck_row in enumerate(deck_rows):
            current_id, current_name, parent_id = deck_row
            if parent_id is None:
                # current_id is a root node of a deck
                current_deck = Deck(current_name)
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

def populate_decks(created_decks):
    for deck_id, deck in created_decks.items():
        for card in get_cards_for_deck(deck_id):
            deck.add_card(card)

lst = db_manager.DBManager('database.db').get_decks()

