import firebase_admin
from firebase_admin import credentials, db
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN_BOT = os.getenv("6353819966:AAEYvw6BqsfeueVrjvcSt6oPk9-A8_ba_sk")
ADMIN_CHAT_ID = int(os.getenv("5066579029"))
DB_URL = os.getenv("https://rmd-pulsa-default-rtdb.asia-southeast1.firebasedatabase.app")

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': DB_URL})

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        await update.message.reply_text("🚫 Kamu tidak punya izin.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Ketik: /done <id_transaksi>")
        return

    trx_id = context.args[0]
    ref = db.reference(f'pembelian/{trx_id}')
    if ref.get() is None:
        await update.message.reply_text("❌ ID tidak ditemukan.")
        return

    ref.update({'status': 'sukses'})
    await update.message.reply_text(f"✅ Transaksi {trx_id} sudah diupdate ke *sukses*", parse_mode='Markdown')

app = ApplicationBuilder().token(TOKEN_BOT).build()
app.add_handler(CommandHandler("done", done))

print("BOT SIAP...")
app.run_polling()
