from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.error import TelegramError
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import logging

# Bot token
TOKEN = "7929440474:AAEPEIl6MZNpX5J0qhQ86-Pjberu-ZuXfxA"

# Telegram ID
USER_ID = 6131621482 

def check_bot_status():
    try:
        # Botun çalıştığını bildiren basit bir mesaj gönder
        bot.send_message(chat_id=CHAT_ID, text="✅ Bot çalışıyor! (Saatlik kontrol)")
        logging.info("Kontrol mesajı başarıyla gönderildi.")
    except TelegramError as e:
        logging.error(f"Kontrol mesajı gönderilemedi: {e}")

# Arka plan zamanlayıcısını oluştur ve kontrol işini ekle
scheduler = BackgroundScheduler()
scheduler.add_job(check_bot_status, 'interval', hours=1)  # SAATTE 1 KEZ çalışır
scheduler.start()

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

    # Komutları ekleyelim deneme yorumu
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Hatırlatıcıyı başlat
    schedule_reminder()

    # Botu çalıştır
    print("Bot çalışıyor ve hatırlatıcı ayarlandı...")
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Bot kapatıldı.")
