from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from temple_island_bot.enums import Commands


def get_start_keyboard(showMyWalletsBtn: bool):
    keyboard = [
        [
            InlineKeyboardButton(
                '🔍 Search on Temple',
                switch_inline_query_current_chat=f''
            )
        ],
        [
            InlineKeyboardButton(
                '➕ Add new wallet',
                callback_data=f'{Commands.add_new_wallet.value}'
            )
        ]
    ]

    if showMyWalletsBtn:
        keyboard.append([
            InlineKeyboardButton(
                '👛 My wallets',
                switch_inline_query_current_chat='my_wallets',
            )
        ])

    return InlineKeyboardMarkup(keyboard)
