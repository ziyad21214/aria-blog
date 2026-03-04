import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

class DatabaseManager():
    @staticmethod
    def init_db():
        conn: sqlite3.Connection = sqlite3.connect('blog.db')
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
            )
        ''')
        load_dotenv()
        ADMIN_USERNAME: str = os.environ.get('ADMIN_USERNAME')
        ADMIN_PASSWORD: str = os.environ.get('ADMIN_PASSWORD')
        hashed = generate_password_hash(ADMIN_PASSWORD)

        try:
            cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (ADMIN_USERNAME, hashed))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()

    @staticmethod
    def get_admin_hash_from_db(admin_name: str) -> str | None:
        conn: sqlite3.Connection = sqlite3.connect('blog.db')
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (admin_name,)
        )
        result: str = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        else:
            return None

if __name__ == '__main__':
    DatabaseManager.init_db()
   # print(DatabaseManager.get_admin_hash_from_db('admin'))
    hash1 = generate_password_hash('123')
    print(check_password_hash(hash1, '123'))

        