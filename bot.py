from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# Bot tokenını buraya yapıştır
TOKEN = "7929440474:AAEPEIl6MZNpX5J0qhQ86-Pjberu-ZuXfxA"

# Kullanıcının Telegram ID'si (Bunu bulmak için @userinfobot kullan)
USER_ID = 6131621482  # Buraya kendi Telegram ID'ni koy

async def start(update: Update, context: CallbackContext) -> None:
    """Kullanıcı /start komutunu gönderdiğinde çalışacak."""
    await update.message.reply_text("Merhaba! Ben senin Telegram botunum. Her gün tansiyonunu ölçmeni hatırlatacağım.")

async def echo(update: Update, context: CallbackContext) -> None:
    """Kullanıcının gönderdiği mesajı aynen geri yollar."""
    await update.message.reply_text(update.message.text)

async def remind():
    """Kullanıcıya her gün tansiyon ölçümünü hatırlatan mesajı yollar."""
    app = Application.builder().token(TOKEN).build()
    async with app:
        await app.bot.send_message(chat_id=USER_ID, text="Günaydın! Tansiyonunu ölçmeyi unutma. 🩺📊")

def schedule_reminder():
    """Hatırlatıcıyı her gün belirli bir saatte çalışacak şekilde ayarla."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(remind()), 'cron', hour=0, minute=0)  # Sabah 09:00'da çalışır
    scheduler.start()

def main():
    """Botu çalıştıran ana fonksiyon."""
    app = Application.builder().token(TOKEN).build()

    # Komutları ekleyelim
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Hatırlatıcıyı başlat
    schedule_reminder()

    # Botu çalıştır
    print("Bot çalışıyor ve hatırlatıcı ayarlandı...")
    app.run_polling()

if __name__ == "__main__":
    main()
