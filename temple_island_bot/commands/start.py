from telegram import Update
from telegram.ext import CallbackContext

from temple_island_bot.keyboards import get_start_keyboard
from temple_island_bot.models import User, UserWallet


def start(update: Update, context: CallbackContext):
    user = User.objects.get_or_create(
        chat_id=update.message.chat_id,
    )[0]

    user.first_name = update.message.chat.first_name
    user.last_name = update.message.chat.last_name
    user.username = update.message.chat.username

    user.save()

    wallets = UserWallet.objects.filter(
        user=user
    )

    text = 'ok'

    keyboard = get_start_keyboard(len(wallets) > 0)

    if len(wallets) == 0:
        text = 'Wallets not found. Please add new wallet...'

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
        reply_markup=keyboard
    )
