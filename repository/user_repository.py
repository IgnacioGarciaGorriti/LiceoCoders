from models.user import User
from repository.abstract_repository import AbstractRepository
import models.user


class UserRepository(AbstractRepository):
    def get(self, user_id):
        return self.session.query(User).filter_by(id=user_id).one_or_none()

    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).one_or_none()

    def list(self):
        return self.session.query(User).all()

    def add(self, user: User):
        self.session.add(user)
        self.session.commit()

