import utils
import const
from sqlalchemy import ForeignKey, Column, Integer, String, REAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Deck(Base):
    """columns: id PK, name"""
    __tablename__ = 'Deck'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    cards = relationship('Card')

    # def __str__(self):
    #     return f'{self.name}'

    @classmethod
    def get_decks(cls, session):
        return session.query(cls)


class Card(Base):
    """
    attributes: id PK, EF front, back, due, last_interval, deck_id
    """

    __tablename__ = 'Card'

    id = Column(Integer, primary_key=True)
    EF = Column(REAL, nullable=False)
    front = Column(String, nullable=False)
    back = Column(String, nullable=False)
    due = Column(Integer, nullable=False)
    last_interval = Column(Integer)
    deck_id = Column(Integer, ForeignKey("Deck.id"), nullable=False)


# Base.metadata.create_all(engine) WILL BE used in create_db.py !

if __name__ == "__main__":
    # examples
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine(f'sqlite:///{const.DB_NAME}')
    Session = sessionmaker(bind=engine)
    session = Session()

    # gets all decks
    for deck in Deck.get_decks(session):
        print(deck)
    
    # gets all the cards of a deck
    user = session.query(Deck).filter_by(name='dev names').first()
    for card in user.cards:
        print(card.front, card.back)
    
