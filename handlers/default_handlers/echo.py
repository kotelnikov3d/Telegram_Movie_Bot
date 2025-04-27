from telebot.types import Message
from loader import bot, UserState


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    current_state = bot.get_state(user_id=message.from_user.id)
    print(current_state)
    bot.reply_to(
        message, f"Неизвестная команда: {message.text}\nПолучить список команд /help"
    )
    bot.set_state(user_id=message.from_user.id, state=UserState.idle_state)
