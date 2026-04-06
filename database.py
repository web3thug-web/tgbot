import sqlite3
from datetime import datetime

DB_PATH = "dialogs.db"

def init_db():
    # Создаём таблицу если её ещё нет
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dialogs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id   INTEGER NOT NULL,
            user_msg  TEXT NOT NULL,
            bot_resp  TEXT NOT NULL,
            intent    TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_dialog(user_id: int, user_msg: str, bot_resp: str, intent: str):
    # Сохраняем одно сообщение в базу
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO dialogs VALUES (NULL,?,?,?,?,?)",
        (user_id, user_msg, bot_resp, intent,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()