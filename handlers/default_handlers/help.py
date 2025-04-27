from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot, UserState


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
