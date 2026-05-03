import os
import telebot
from telebot import types

# جلب التوكن من الإعدادات التي حفظتها الآن
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🛠️ إنشاء تطبيق ملغم (APK)", callback_data='create_apk')
    btn2 = types.InlineKeyboardButton("📱 قائمة الضحايا المتصلين", callback_data='list_victims')
    btn3 = types.InlineKeyboardButton("⚙️ إعدادات الاختراق", callback_data='settings')
    markup.add(btn1, btn2, btn3)
    
    welcome_text = (
        "💀 **انت هنا للانتقام v2.0**\n\n"
        "مرحباً يا شبح في وحدة التحكم المركزية.\n"
        "الآن السيرفر مهيأ للبدء في عمليات الحقن السحابي."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'create_apk':
        msg = bot.edit_message_text("ارسل لي الآن رابط التطبيق (APK) الذي تريد حقنه، أو ارفع ملف الـ APK مباشرة هنا.", call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(msg, process_apk_step)

def process_apk_step(message):
    bot.reply_to(message, "✅ استلمت الملف/الرابط. جاري فحص بيئة الجافا وتهيئة أدوات التشفير للبدء...")

if __name__ == "__main__":
    bot.infinity_polling()
