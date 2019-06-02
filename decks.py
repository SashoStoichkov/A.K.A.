import itertools
import random
import sqlite3

import utils

from cards import Card

class Deck:
    """
    * attributes:
    - self.id: a unique (among all other decks) integer which is used
      as the connection between the instance and the database.
    - self.name
    - self.parent: the parent deck. None if the current deck is a root.
    - self.subdecks: a list of the subdecks of the deck
    - self.cards: a dict which maps card ids to cards
    - self.conn: a connection to the database which contains the
      persistent storage of the deck
    """

    def __init__(self, id, name, conn, parent):
        self.id = id
        self.name = name
        self.parent = parent
        self.subdecks = []
        self.cards = {}
        self.conn = conn
                    
    def add_card(self, card):
        # adds a card to the deck's collection of cards
        self.cards[card.id] = card
                
    def flush(self):
        # possibly useful for renaming decks
        raise NotImplementedError

    @property
    def due_cards(self):
        """Returns a list of all cards which are up for review."""
        today = utils.today()
        def is_due(card):
            return card.due <= today
        return [card for card in self.all_cards if is_due(card)]

    @property
    def all_cards(self):
        """Returns a list of all cards in the deck (including those in
        the deck's subdeck). The order of the cards is random"""
        result = list(self._cards_iter)
        random.shuffle(result)
        return result
    
    @property
    def _cards_iter(self):
        """Returns an iterator of all cards in the deck (including the
        deck's subdecks). The order of the cards is not specified."""
        for card in self.cards.values():
            yield card
        for subdeck in self.subdecks:
            for card in subdeck._cards_iter:
                yield card

    @property
    def subdecks_iter(self):
        """Just a utility function which returns an iterator of all
        subdecks of @self. Using this iterator, a child is always
        yielded before it's parent."""
        
        for child in self.subdecks:
            for deep_subdeck in child.subdecks_iter:
                yield deep_subdeck
        yield self

    def get_subdeck(self, **kwargs):
        """Allows you to get a deck having a given property (for example, a deck having a
        given name or a deck having a given id). Passing in non-existing attributes is
        harmless."""

        def check_attr(attr, value):
            sentinel = object()
            for subdeck in self.subdecks:
                subdeck_val = getattr(subdeck, attr, sentinel)
                if subdeck_val is sentinel or subdeck_val != value:
                    continue
                return subdeck
            return None
        
        for attr, value in kwargs:
            subdeck = check_attr(attr, value)
            if subdeck is not None:
                return subdeck

        raise ValueError(f'no subdeck with any of the attributes: {kwargs.keys()}')
       
        
