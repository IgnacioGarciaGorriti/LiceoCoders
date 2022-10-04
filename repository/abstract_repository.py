import abc
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base


class AbstractRepository(abc.ABC):
    engine = create_engine(os.environ.get('DATABASE_URL'))
    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    def get(self, entity_id):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

