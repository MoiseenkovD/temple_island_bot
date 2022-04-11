from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from temple_island_bot.enums import Commands


def get_start_keyboard(showMyWalletsBtn: bool):
    keyboard = [
        [
            InlineKeyboardButton(
                '🔍 Search on Temple',
                callback_data=f'1'
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
                switch_inline_query_current_chat=''
            )
        ])

    return InlineKeyboardMarkup(keyboard)
