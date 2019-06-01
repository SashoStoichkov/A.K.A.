from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

import const
from models import Deck, Card, Base

if __name__ == "__main__":
    engine = create_engine(f'sqlite:///{const.DB_NAME}')
    Base.metadata.create_all(engine)
