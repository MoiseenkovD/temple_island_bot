from telegram import Update
from telegram.ext import CallbackContext

from temple_island_bot.models import User
from temple_island_bot.bot import on_photo


def upload_image_for_wallet(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    user = User.objects.get(
        chat_id=query.message.chat_id
    )

    command, *payload = query.data.split(':')
    command = int(command)

    wallet_id = payload[0]

    user.pending_state = f'ADD_WALLET_IMAGE:{wallet_id}'

    user.save()

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=f'Please send photo for wallet...',
    )

    on_photo(update, context)

