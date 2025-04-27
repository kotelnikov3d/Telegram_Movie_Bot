from telebot.types import Message
from loader import bot, UserState


@bot.message_handler(state='*', commands=["exit"])
def bot_start(message: Message):
    bot.reply_to(message, "Вы вышли из режима поиска")
    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
