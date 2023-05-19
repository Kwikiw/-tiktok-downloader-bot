from datetime import datetime, timedelta
import sqlite3
import pytz

import config


def connect():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    return conn, cursor


def get_date() -> datetime:
    date = datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
    return date


def first_join(user_id: int, username: str) -> bool:
    conn, cursor = connect()
    cursor.execute(f"SELECT username FROM users WHERE user_id = ?", [user_id])
    row = cursor.fetchone()
    if not row:
        cursor.execute(f"INSERT INTO users (user_id, username, date, last_active) "
                       f"VALUES (?, ?, ?, ?)", (user_id, username, get_date(), get_date()))
    conn.commit()
    conn.close()
    if row:
        update_user(user_id, username)
    return row is None


def update_user(user_id: int, username: str):
    conn, cursor = connect()
    cursor.execute("UPDATE users SET last_active = ? WHERE user_id = ?", [get_date(), user_id])
    cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", [username, user_id])
    cursor.execute("UPDATE users SET username = NULL WHERE user_id != ?", [user_id])
    conn.commit()
    conn.close()


def get_users() -> list[tuple[int]]:
    conn, cursor = connect()
    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_count_users(date: datetime = None, date2: datetime = None, active=False) -> int:
    conn, cursor = connect()
    column = "date"
    if active:
        column = "last_active"
    if date2:
        cursor.execute(f"SELECT COUNT(id) FROM users WHERE {column} >= ? AND {column} <= ?", [date2, date])
    elif date:
        cursor.execute(f"SELECT COUNT(id) FROM users WHERE {column} >= ?", [date])
    else:
        cursor.execute(f"SELECT COUNT(id) FROM users")
    row, = cursor.fetchone()
    conn.close()
    return row


def admin_stats():
    day = get_date()
    day = day.replace(hour=0, minute=0, second=1)
    month = day.replace(day=1)
    yesterday = day - timedelta(days=1)
    text = f"<b>Статистика</b>\n\n" \
           f"➖➖ @{config.bot_username} ➖➖\n" \
           f"<b>Пользователей:</b> {get_count_users()}\n" \
           f"Новых | Активных\n" \
           f"  ├ Сегодня: {get_count_users(day)} | {get_count_users(day, active=True)}\n" \
           f"  ├ Вчера: {get_count_users(day, yesterday)} | {get_count_users(day, yesterday, active=True)}\n" \
           f"  └ Месяц: {get_count_users(month)} | {get_count_users(month, active=True)}"
    return text
