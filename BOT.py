import telebot
from telebot import types
from deep_translator import GoogleTranslator

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot('your token')

# Список доступных стран и соответствующих им языков
countries = {
    'Russia🇷🇺': 'ru',
    'USA🇺🇸': 'en',
    'Spain🇪🇸': 'es',
    'Germany🇩🇪': 'de',
    'France🇫🇷': 'fr',
    'Italy🇮🇹': 'it',
    'Brazil🇧🇷': 'pt',
    'China🇨🇳': 'zh-CN',
    'Taiwan🇹🇼': 'zh-TW',
    'Japan🇯🇵': 'ja',
    'Korea🇰🇷': 'ko',
    'Saudi Arabia🇸🇦': 'ar',
    'India🇮🇳': 'hi'
}

# Словарь для хранения предпочтительного языка для каждого пользователя
user_languages = {}

# Множество для хранения идентификаторов пользователей, которые начали диалог с ботом
active_users = set()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    active_users.add(user_id)  # Добавляем пользователя в множество активных пользователей
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add(*[types.KeyboardButton(country) for country in countries])
    bot.reply_to(message, "Hello! I am a translator bot. Select your country: \nTo get information about the bot, send the command /help.", reply_markup=markup)
    user_languages[user_id] = 'en'  # Устанавливаем английский язык по умолчанию для нового пользователя

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "I'm a translator bot. Here's what I can do:\n\n" \
                "- When starting a conversation with a bot, select your country to set your preferred language.\n" \
                "- Send text messages in the group chat and I will translate them into other users' preferred languages.\n" \
                "- To change your preferred language, simply send the country name in a private chat with the bot.\n" \
                "- To get this help, send the command /help."
    bot.reply_to(message, help_text)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def translate_message(message):
    user_id = message.from_user.id
    active_users.add(user_id)  # Добавляем пользователя в множество активных пользователей

    if user_id not in user_languages:
        user_languages[user_id] = 'en'  # Устанавливаем английский язык по умолчанию для нового пользователя

    if message.text in countries:
        # Если сообщение содержит название страны, сохраняем соответствующий язык как предпочтительный для пользователя
        user_languages[user_id] = countries[message.text]
        bot.reply_to(message, f"Your preferred language: {user_languages[user_id]}")
    else:
        chat_id = message.chat.id  # Получаем идентификатор группового чата
        for user_id in active_users:
            if user_id != message.from_user.id:
                target_lang = user_languages.get(user_id, 'en')  # Получаем предпочтительный язык пользователя или 'en' по умолчанию
                translator = GoogleTranslator(source='auto', target=target_lang)
                translation = translator.translate(message.text)
                # Получаем имя пользователя, который получает сообщение
                recipient_user = bot.get_chat_member(chat_id, user_id).user
                recipient_username = recipient_user.username
                bot.send_message(chat_id, f"Translation for {recipient_username}:\n{translation}")  # Отправляем переведенное сообщение в групповой чат

# Запуск бота
bot.polling()
