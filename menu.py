from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config


def main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="📊 Статистика", callback_data="statistic"),
        InlineKeyboardButton(text="📢 Рассылка", url=f"https://t.me/{config.bot_username}?start=email"),
    )
    return markup
