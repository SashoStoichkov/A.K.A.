import const
from models import Deck, Card
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

enigne = create_engine('sqlite:///'+const.DB_NAME)
Session = sessionmaker(bind=enigne)


if __name__ == "__main__":
    session = Session()
    session.add_all(
        [
            Deck(name='dev names'),
            Deck(name='dev ages'), 
            Deck(name='dev hometowns'), 
            Deck(name='dev jobs')
        ])
    session.commit()
    session.add_all(
        [
            Card(EF=2.5, front="Who is something?", back="Kamen", due=22165, last_interval=2, deck_id=1),
            Card(EF=2.5, front="Who is backend?", back="Alex", due=22165, last_interval=2, deck_id=1),
            Card(EF=2.5, front="Who is frontend?", back="Sasho", due=22165, last_interval=2, deck_id=1),
            Card(EF=2.5, front="What age is Kamen?", back="21", due=22165, last_interval=2, deck_id=2),
            Card(EF=2.5, front="What age is Alex?", back="100", due=22165, last_interval=2, deck_id=2),
            Card(EF=2.5, front="What age is Sasho", back="16", due=22165, last_interval=2, deck_id=2),     
            Card(EF=2.5, front="Where is Kamen from?", back="somewhere", due=22165, last_interval=2, deck_id=3),
            Card(EF=2.5, front="Where is Alex from?", back="Mars", due=22165, last_interval=2, deck_id=3),
            Card(EF=2.5, front="Where is Sashi from", back="TUES", due=22165, last_interval=2, deck_id=3),     
            Card(EF=2.5, front="What does Kamen do?", back="something", due=22165, last_interval=2, deck_id=4),
            Card(EF=2.5, front="What does Alex do?", back="backend", due=22165, last_interval=2, deck_id=4),
            Card(EF=2.5, front="What does Sashi do?", back="frontend", due=22165, last_interval=2, deck_id=4),     
        ])
    session.commit()
    session.close()

