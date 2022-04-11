import web3
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, InlineQueryResultArticle, \
    InputTextMessageContent
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler, MessageHandler, Filters, \
    InlineQueryHandler

from web3 import Web3
import boto3
import requests
import hashlib

from urllib.parse import urlparse
from datetime import datetime as dt

import os, django

from temple_island_bot.configs import configs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "temple_island.settings")
django.setup()

import temple_island_bot.commands as commands
from temple_island_bot.models import User, UserWallet
from temple_island_bot.enums import Commands

bot = Updater(token=configs['TOKEN'], use_context=True)

aws_access_key_id = configs['AWS_ACCESS_KEY_ID']
aws_secret_access_key = configs['AWS_SECRET_ACCESS_KEY']
aws_bucket_name = configs['AWS_BUCKET_NAME']
aws_bucket_region = configs['AWS_BUCKET_REGION']


def start(update: Update, context: CallbackContext):
    commands.start(update, context)


def my_wallet(update: Update, context: CallbackContext):
    commands.my_wallet(update, context)


def button(update: Update, context: CallbackContext):
    query = update.callback_query

    query.answer()

    command, *payload = query.data.split(':')
    command = int(command)

    if command == Commands.add_new_wallet.value:
        commands.add_wallet(update, context)


def inline(update: Update, context: CallbackContext):
    query = update.inline_query.query

    user = User.objects.get(
        chat_id=update.inline_query.from_user.id
    )

    wallets = UserWallet.objects.filter(user=user).all()

    wallet_inline = []

    for wallet in wallets:
        wallet_inline.append(InlineQueryResultArticle(
            id=wallet.id,
            title=wallet.name,
            description=wallet.address,
            thumb_url=wallet.image_url,
            # thumb_width=300,
            # thumb_height=300,
            input_message_content=InputTextMessageContent(f'{wallet.name}')))

    update.inline_query.answer(wallet_inline, cache_time=0)


def on_message(update: Update, context: CallbackContext):
    user = User.objects.get(
        chat_id=update.message.chat_id
    )

    if user.pending_state is not None:
        command, *payload = user.pending_state.split(':')

        if command == 'ADD_WALLET_ADDRESS':
            wallet_address = update.message.text

            if Web3.isAddress(wallet_address):
                try:
                    wallet = UserWallet.objects.get(
                        user=user,
                        address=wallet_address
                    )

                    context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=f'Wallet is already added',
                        parse_mode=ParseMode.HTML,
                    )
                except UserWallet.DoesNotExist:
                    wallet = UserWallet.objects.create(
                        user=user,
                        address=wallet_address
                    )
                    context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=f'✅ Address: <strong>{wallet_address}</strong> is saved',
                        parse_mode=ParseMode.HTML,
                    )

                    context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=f'Please type name for wallet...',
                    )

                    user.pending_state = f'ADD_WALLET_NAME:{wallet.id}'

                    user.save()
            else:
                context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text='address is not corrected'
                )
        elif command == 'ADD_WALLET_NAME':
            wallet_id = int(payload[0])

            wallet = UserWallet.objects.filter(
                id=wallet_id,
                user=user,
            ).get()

            wallet.name = update.message.text

            wallet.save()

            user.pending_state = f'ADD_WALLET_IMAGE:{wallet_id}'

            user.save()

            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f'✅ Name: <strong>{wallet.name}</strong> is saved',
                parse_mode=ParseMode.HTML,
            )

            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=f'Please send photo for wallet...',
            )


def on_photo(update: Update, context: CallbackContext):
    user = User.objects.get(
        chat_id=update.message.chat_id
    )

    command, *payload = user.pending_state.split(':')

    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    if command == 'ADD_WALLET_IMAGE':
        wallet_id = int(payload[0])

        wallet = UserWallet.objects.filter(
            id=wallet_id,
            user=user,
        ).get()

        file = context.bot.getFile(update.message.photo[2])
        file_path = file.file_path

        path = urlparse(file_path).path
        basename = os.path.basename(path)

        filename = os.path.splitext(basename)[0]
        ext = os.path.splitext(path)[1]

        r = requests.get(file_path, stream=True)

        new_filename = hashlib.md5(f'{filename}{str(dt.now())}'.encode()).hexdigest()

        s3.upload_fileobj(r.raw, aws_bucket_name, f'{new_filename}{ext}')

        uploaded_file_url = f'https://{aws_bucket_name}.s3.{aws_bucket_region}.amazonaws.com/{new_filename}{ext}'

        wallet.image_url = uploaded_file_url
        wallet.save()

        user.pending_state = None
        user.save()

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f'✅ Photo is successfully uploaded\n'
                 f'please type /start',
        )


def main():
    start_handler = CommandHandler('start', start)
    my_wallet_handler = CommandHandler('my_wallet', my_wallet)
    inline_handler = InlineQueryHandler(inline)
    button_handler = CallbackQueryHandler(button)
    message_handler = MessageHandler(Filters.text & ~Filters.command & ~Filters.reply, on_message)
    photo_handler = MessageHandler(Filters.photo, on_photo)

    bot.dispatcher.add_handler(start_handler)
    bot.dispatcher.add_handler(my_wallet_handler)
    bot.dispatcher.add_handler(inline_handler)
    bot.dispatcher.add_handler(button_handler)
    bot.dispatcher.add_handler(message_handler)
    bot.dispatcher.add_handler(photo_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
