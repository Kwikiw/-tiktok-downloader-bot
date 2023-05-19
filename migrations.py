import sqlite3


def run():
    count_db = 1
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    k = 1

    if len(cursor.execute("PRAGMA table_info(users)").fetchall()) > 0:
        print(f"Table was found({k}/{count_db})")
    else:
        cursor.execute("CREATE TABLE users("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "user_id INTEGER,"
                       "username TEXT,"
                       "date DATETIME,"
                       "last_active DATETIME)")
        print(f"Table was not found({k}/{count_db}) | Creating...")
    k += 1

    conn.commit()
    conn.close()


if __name__ == '__main__':
    run()
