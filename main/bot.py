import telebot

bot = telebot.TeleBot("8263185174:AAHOToGEXIO-ji_oXPhRtLLgZgmUEhsEIhU")
admin_id = 663285366

def send_to_admin(text):
    bot.send_message(admin_id, text)

@bot.message_handler(commands=['start'])
def start(message):
    send_to_admin("A user pressed /start")
    bot.reply_to(message, "Message sent to admin!")


