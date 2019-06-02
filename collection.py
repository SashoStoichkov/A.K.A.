import sqlite3

import const
import utils

from decks import Deck
from cards import Card

class Loader:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)

    @property
    def deck_rows(self):
        """just a utility function.
        returns a list of rows (<deck-id>, <deck-name>, <deck-parent-id>)"""
        
        query ="""
            SELECT * FROM Deck;
        """
        cursor = self.conn.execute(query)
        data = cursor.fetchall()
        self.conn.commit()
        return data

    
    def card_rows(self, deck_id):
        """just a utility function
        returns a list of card rows, which have the form
        (id, EF, front, back, due_time, last_interval)"""
        
        query = """
            SELECT Card.id, EF, front, back, due, last_interval FROM Card
            	INNER JOIN Deck
            		ON Card.deck_id = Deck.id
            WHERE Deck.id = ?;
        """
        cursor = self.conn.execute(query, (deck_id, ))
        cards = cursor.fetchall()
        self.conn.commit()
        return cards

    def load(self):
        """creates the Collection determined by the database at self.conn"""
        
        def create():
            main_deck = Deck(id=const.MAIN_DECK_ID, name='main',
                             conn=self.conn, parent=None)
            decks = {main_deck.id: main_deck} # maps ids to decks
            for deck_row in self.deck_rows[1:]: # skip main deck row
                id, name, parent_id = deck_row
                parent = decks[parent_id]
                deck = Deck(id=id, name=name, conn=self.conn, parent=parent)
                parent.add_subdeck(deck)
                decks[id] = deck
            return main_deck, decks
        
        def populate(created_decks):
            for deck_id, deck in created_decks.items():
                for card_row in self.card_rows(deck_id):
                    card_id, EF, front, back, due, last_interval = card_row
                    deck.add_card((Card(deck=deck, id=card_id, EF=EF, front=front,
                                        back=back, due=due,
                                        last_interval=last_interval, conn=self.conn)))
            return created_decks
        
        main_deck, decks = create()
        populate(decks)
        return Collection(self.conn, main_deck)

    
class Collection:
    """
    * attributes:
    - conn: the connection to the database containing the collection
    - main_deck
    """

    def __init__(self, conn, main_deck):
        self.conn = conn
        self.main_deck = main_deck
        
    def create_decks(self, dotted_name):
        """
        @dotted_name must a dotted name. If it is not valid, an error is raised.
        Already existing decks are not created. For example, if @dotted_name ==
        'english::vocabulary::animals' and the deck 'english' already exists, only the
        decks 'vocabulary' and 'animals' will be created. The deck 'vocabulary' will
        become a subdeck of 'english' and 'animals' will become a subdeck of 'vocabulary'.
        """
        
        names = utils.validate_dotted_name(dotted_name)        
        division = self._divide(names)
        
        if division is None:
            # all names exist
            return
        
        parent, names = division
        self._create_deck_path(names, parent)

    def _divide(self, names):
        """
        Just a utility for self.create_decks.
        Returns a pair (deck, sublist) where deck exists in the collection, sublist is not
        empty and sublist[0] is supposed to the name of a subdeck of deck, but deck has no
        such subdeck. For example, if the deck 'english' exists, and @names == ['english',
        'vocabulary', 'animals'], the function will return the pair (<english-deck python
        instance>, ['vocabulary', 'animals']). However, if both the decks 'english' and
        'vocabulary' exist, the function will return (<vocabulary-deck>,
        ['animals']). Finally, if all three decks exist, the function just returns
        None. If the 'english' deck does not exist, the function will just return (None,
        ['english', 'vocabulary', 'animals'])
        """
        
        if not names:
            return None
        
        deck = self.main_deck
        ni = 0 # name index
        
        while ni < len(names):
            name = names[ni]
            subdeck = deck.get_subdeck(name=name)
            
            if subdeck is None:
                return (deck, names[ni:])
            else:
                deck = subdeck
                ni += 1
        else:
            # names are exhausted and all decks exist
            return None  

    def _create_deck_path(self, names, parent):
        """
        Just a utility for self.create_decks.
        @names must be a non-empty list of deck names.
        @parent must be a deck.
        This function creates a deck for each name, with names[-1] being a child of
        names[-2] being a child of names[-3] and so on. The deck determined by names[0]
        will have @parent as a parent. This function returns the deck associated with
        names[0]
        """
        
        result = None
        for name in names:
            deck = self._create_deck(name, parent)
            parent = deck
            if result is None: # will return the first deck 
                result = deck
        return result
    
    def _create_deck(self, name, parent):
        """
        Just a utility for self._create_deck_path.
        Creates the deck instance and writes it to the database
        """
        
        deck = Deck(id=utils.getid(self.conn, 'deck'), name=name,
                    conn=self.conn, parent=parent)        
        parent.add_subdeck(deck)
        parent_id = parent.id
        deck.conn.execute('INSERT INTO deck(id, name, parent_id) VALUES (?, ?, ?)',
                          (deck.id, deck.name, parent_id))
        deck.conn.commit()
        return deck
    
    def remove_deck(self, dotted_name):
        """
        @deck_name can be a top-level name, like 'english', or a dotted name, like
        'english::vocabulary'.  In the latter case, only the innermost deck is removed, so
        with 'english::vocabulary' only the deck named 'vocabulary' that is a subdeck of
        'english' will be removed. By removed I mean that the deck and all of it's
        subdecks and all cards belonging to these subdecks will be removed both from the
        collection and from the database.
        """

        deck = self.find_deck(dotted_name)        
        parent = deck.parent
        parent.remove_subdeck(deck)
            
        for subdeck in deck.subdecks_iter:
            # remove cards from the db
            self.conn.execute('DELETE FROM card WHERE deck_id = ?', (subdeck.id,))            
            # remove the deck itself from the db
            self.conn.execute('DELETE FROM deck WHERE id = ?', (subdeck.id,))
            
        self.conn.commit()

    def find_deck(self, dotted_name):
        """
        Accepts a dotted name dotted_name and returns the corresponding deck. If no such
        deck exists, None is returned.
        """
        
        names = utils.validate_dotted_name(dotted_name)
        deck = self.main_deck
        for name in names:
            deck = deck.get_subdeck(name=name)
            if deck is None:
                raise ValueError(f'the dotted name "{dotted_name}" does not correspond '
                                 'to a deck in the collection')
        return deck
        
    def create_card(self, front, back, dotted_name):
        """Creates a card and adds it to the deck at @dotted_name. The card is stored in
        the database aswell"""
        deck = self.find_deck(dotted_name)
        dct = dict(id=utils.getid(self.conn, 'card'), front=front, back=back,
                   deck=deck, due=utils.today(), last_interval=None,
                   EF=2.5, conn=self.conn)
        card = Card(**dct)

        ##################################################
        # insert the card into the database
        
        # dct contains almost all attributes needed for inserting
        # a row into the database, except deck_id
        
        dct['deck_id'] = deck.id        
        card.conn.execute("""
            INSERT INTO card (id, front, back, deck_id, due, last_interval, EF)
            VALUES (:id, :front, :back, :deck_id, :due, :last_interval, :EF)""",
                          dct)        
        card.conn.commit()
        deck.add_card(card)
        return card
            
    def remove_card(self, card):
        """Removes the card @card from it's deck and from the database."""
        deck = card.deck
        del deck.cards[card.id]
        card.conn.execute('DELETE FROM card WHERE id = ?', (card.id,))
        card.conn.commit()

# loader = Loader(const.DB_NAME)
# col = loader.load()

