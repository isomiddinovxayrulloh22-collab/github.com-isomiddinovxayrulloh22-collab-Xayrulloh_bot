from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image

images = []

TOKEN = "8964959759:AAEB7WQ9CDBY9fmgGRWZpRu6DuGrEoeOxTg"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Rasmlarni yuboring. Tayyor bo‘lgach /pdf buyrug‘ini yuboring."
    )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    filename = f"photo_{len(images)}.jpg"
    await photo_file.download_to_drive(filename)

    images.append(filename)

    await update.message.reply_text("Rasm saqlandi.")


async def pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not images:
        await update.message.reply_text("Avval rasm yuboring.")
        return

    imgs = [Image.open(x).convert("RGB") for x in images]

    pdf_name = "result.pdf"

    imgs[0].save(
        pdf_name,
        save_all=True,
        append_images=imgs[1:]
    )

    await update.message.reply_document(pdf_name)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pdf", pdf))
app.add_handler(MessageHandler(filters.PHOTO, photo))

print("Bot ishga tushdi...")

app.run_polling()
