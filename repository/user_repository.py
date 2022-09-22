import mysql.connector

from models.user import User


class UserRepository:
    connection = mysql.connector.connect(
        host="localhost",
        user="usr_my_project",
        password="pwd_my_project",
        database="db_my_project_liceocoders"
    )

    def get(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('select * from users where id = %s', (user_id,))
        user = self.__compound_user(cursor.fetchone())
        cursor.close()
        return user

    def get_by_email(self, email):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('select * from users where email = %s', (email,))
        user = self.__compound_user(cursor.fetchone())
        cursor.close()
        return user

    def list(self):
        user_list = []
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute('select * from users')
        rows = cursor.fetchall()
        for row in rows:
            user_list.append(self.__compound_user(row))
        cursor.close()
        return user_list

    def add(self, user: User):
        cursor = self.connection.cursor()
        cursor.execute('insert into users values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (
                           user.id,
                           user.username,
                           user.name,
                           user.surname,
                           user.email,
                           user.password,
                           user.age,
                           user.gender,
                           user.role,
                           user.points,
                           user.status
                       ))
        self.connection.commit()
        cursor.close()

    def __compound_user(self, row):
        if row is None:
            return None

        user = User(
            row['username'],
            row['name'],
            row['surname'],
            row['email'],
            row['password'],
            row['age'],
            row['gender'],
            row['role'],
            row['points'],
            row['status']
        )
        user.id = row['id']
        user.password = row['password']

        return user
