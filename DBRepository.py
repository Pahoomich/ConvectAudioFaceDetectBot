import psycopg2
import config


class DBRepository:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost",
                                               database=config.db_name,
                                               user=config.db_user_name,
                                               password=config.db_user_password)
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def find_voice_all(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM voices").fetchall()

    def find_user_by_uid(self, uid):
        select_query = "SELECT * FROM users WHERE users.uid = %s"
        with self.connection:
            self.cursor.execute(select_query, (uid,))
            return self.cursor.fetchone() is not None

    def count_voice_rows_by_id(self, uid):
        select_query = "SELECT * FROM voices WHERE voices.user_id = %s"
        with self.connection:
            self.cursor.execute(select_query, (uid,))
            return len(self.cursor.fetchall())

    def save_voice(self, record_to_insert):
        insert_query = "INSERT INTO voices (path_to_voice_message, user_id) VALUES (%s,%s)"
        with self.connection:
            self.cursor.execute(insert_query, record_to_insert)
            self.connection.commit()

    def save_new_user(self, record_to_insert):
        insert_query = " INSERT INTO users (uid, username) VALUES (%s,%s)"
        with self.connection:
            self.cursor.execute(insert_query, record_to_insert)
            self.connection.commit()

    def close(self):
        if (self.connection):
            self.cursor.close()
            self.connection.close()
