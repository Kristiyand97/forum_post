from mariadb import IntegrityError

from data.database_queries import insert_query
from data.models import User


def create(email: str, username: str, password: str) -> User | None:

    try:
        generated_id = insert_query(
            'insert into user(email, username, password) values(?, ?, ?)',
            (email, username, password))

        return User(id=generated_id, email=email, username=username, password='')

    except IntegrityError:
        return None
