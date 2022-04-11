from telegram import Update
from telegram.ext import CallbackContext

from temple_island_bot.models import User, UserWallet


def my_wallet(update: Update, context: CallbackContext):

    user = User.objects.get(
        chat_id=update.message.chat_id
    )

    wallets = UserWallet.objects.filter(
        user=user
    )

    user_wallet = []

    for wallet in wallets:
        wallet_address = wallet.address
        user_wallet.append(f'{wallet_address}')

    user_wallet_str = '\n'.join(user_wallet)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=user_wallet_str
    )