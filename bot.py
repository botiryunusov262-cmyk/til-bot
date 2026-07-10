import json
import os
import random
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "words.json"), "r", encoding="utf-8") as f:
    WORDS = json.load(f)

user_stats = {}


def get_user(user_id):
    if user_id not in user_stats:
        user_stats[user_id] = {"correct": 0, "wrong": 0, "learned_words": set(), "last_word": None}
    return user_stats[user_id]


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot ishlayapti")

    def log_message(self, format, *args):
        pass


def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Salom! Men sizga ingliz tilini oʻrgatuvchi botman.\n\n"
        "📚 Buyruqlar:\n"
        "/soz — kunlik yangi soʻz olish\n"
        "/viktorina — soʻz bilish testini boshlash\n"
        "/statistika — natijalaringizni koʻrish\n\n"
        "Boshlash uchun /soz buyrugʻini yuboring!"
    )
    await update.message.reply_text(text)


async def soz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    word = random.choice(WORDS)
    user["last_word"] = word

    text = (
        f"📖 *Yangi soʻz*\n\n"
        f"🇬🇧 *{word['en']}*\n"
        f"🇺🇿 {word['uz']}\n\n"
        f"✏️ Misol: _{word['example']}_"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def viktorina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    correct_word = random.choice(WORDS)
    wrong_options = random.sample([w for w in WORDS if w != correct_word], 3)
    options = wrong_options + [correct_word]
    random.shuffle(options)

    keyboard = [
        [InlineKeyboardButton(opt["uz"], callback_data=f"quiz|{opt['uz']}|{correct_word['uz']}")]
        for opt in options
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"❓ *{correct_word['en']}* soʻzining oʻzbekcha tarjimasi qaysi?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, chosen, correct = query.data.split("|")
    user = get_user(update.effective_user.id)

    if chosen == correct:
        user["correct"] += 1
        user["learned_words"].add(correct)
        await query.edit_message_text(f"✅ Toʻgʻri! Javob: *{correct}*", parse_mode="Markdown")
    else:
        user["wrong"] += 1
        await query.edit_message_text(
            f"❌ Notoʻgʻri. Siz tanladingiz: {chosen}\nToʻgʻri javob: *{correct}*",
            parse_mode="Markdown"
        )


async def statistika(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    total = user["correct"] + user["wrong"]
    percent = (user["correct"] / total * 100) if total > 0 else 0

    text = (
        f"📊 *Sizning natijalaringiz*\n\n"
        f"✅ Toʻgʻri javoblar: {user['correct']}\n"
        f"❌ Notoʻgʻri javoblar: {user['wrong']}\n"
        f"📈 Aniqlik: {percent:.0f}%\n"
        f"📚 Oʻrgangan soʻzlar soni: {len(user['learned_words'])}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN muhit oʻzgaruvchisi topilmadi.")

    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("soz", soz))
    app.add_handler(CommandHandler("viktorina", viktorina))
    app.add_handler(CommandHandler("statistika", statistika))
    app.add_handler(CallbackQueryHandler(handle_quiz_answer, pattern="^quiz\\|"))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
