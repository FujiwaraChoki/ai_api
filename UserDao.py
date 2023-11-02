import sqlite3


class UserDao:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.conn = sqlite3.connect(self.file_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_authenticated INTEGER NOT NULL DEFAULT 0,
            REPLICATE_API_KEY TEXT NOT NULL
        );"""
        )
        self.conn.commit()

    def insert_user(self, username, password, created_at, api_key):
        try:
            self.cursor.execute(
                """
            INSERT INTO users (username, password_hash, created_at, REPLICATE_API_KEY) VALUES (?, ?, ?, ?);
            """,
                (username, password, created_at, api_key),
            )
            self.conn.commit()

            # Return user id
            self.cursor.execute(
                """
            SELECT id FROM users WHERE username=?;
            """,
                (username,),
            )
            user_id = self.cursor.fetchone()
            if user_id:
                return user_id[0]
            else:
                return None
        except sqlite3.Error as e:
            print("Error inserting user:", e)
            return None

    def get_user_by_username(self, username):
        self.cursor.execute(
            """
        SELECT * FROM users WHERE username=?;
        """,
            (username,),
        )
        return self.cursor.fetchone()

    def get_user_by_id(self, user_id):
        self.cursor.execute(
            """
        SELECT * FROM users WHERE id=?;
        """,
            (user_id,),
        )
        return self.cursor.fetchone()

    def update_user(self, username, api_key):
        self.cursor.execute(
            """
        UPDATE users SET REPLICATE_API_KEY=? WHERE username=?;
        """,
            (api_key, username),
        )
        self.conn.commit()

    # Add other methods as needed

    def __del__(self):
        self.conn.close()
