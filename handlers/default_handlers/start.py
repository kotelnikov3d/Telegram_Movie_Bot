from telebot.types import Message
from loader import bot, UserState
from database.models import User
from peewee import IntegrityError


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    try:
        User.create(
            user_id=user_id,
            first_name=first_name,
        )
        bot.reply_to(message, "Добро пожаловать!")
    except IntegrityError:
        bot.reply_to(message, f"Рад вас снова видеть, {first_name}!")

    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
