from telegram import Update
from telegram.ext import CallbackContext


from temple_island_bot.models import User, UserWallet


def add_wallet(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')

    user = User.objects.get(
        chat_id=query.message.chat_id
    )

    user.pending_state = 'ADD_WALLET_ADDRESS'

    user.save()

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text='Type wallet address'
    )
