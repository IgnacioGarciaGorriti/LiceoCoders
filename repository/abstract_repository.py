import abc
import mysql.connector
from sqlalchemy import create_engine



class AbstractRepository(abc.ABC):
    connection = mysql.connector.connect(
        host="localhost",
        user="usr_my_project",
        password="pwd_my_project",
        database="db_my_project_liceocoders"
    )

    engine = create_engine('mysql+pymysql://usr_my_project:pwd_my_project@127.0.0.1:3306/db_my_project_liceocoders')

    def get(self, entity_id):
        raise NotImplementedError

    def list(self):
        raise NotImplementedError

