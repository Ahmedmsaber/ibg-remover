


# --------------------------------------------------------------------------------
import os
from PIL import Image
from rembg import remove
from telegram import Update , Bot
from telegram.ext import ApplicationBuilder , CommandHandler , ContextTypes,filters,MessageHandler
# Set your OpenAI API key here

# Set your Telegram bot token here
telegram_bot_token = '6381663194:AAHF--htReyUlE8RmwEoj8N-yAewRe2LzKo'
channel_id ="iGunter"



async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text="Hi i am background remover bot to start type /start")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_id = update.message.from_user.name
    user_id = user_id.split("@")[-1]
    welcome_message = f'''
    Hi {user_id}, Welcome to bg-remover bot.
    i am bot for remove background image.
    just send me image and i will remove background.
    Don't forget subscribe to developer channel: @iGunter
    '''
    await context.bot.send_message(chat_id=update.effective_chat.id,text=welcome_message)

async def process_image(photo_name:str):
    name ,_ = os.path.splitext(photo_name)
    out_photo_path = f"./processed/{name}.png"
    input = Image.open(f"./temp/{photo_name}")
    output = remove(input)
    output.save(out_photo_path)
    os.remove(f"./temp/{photo_name}")
    return out_photo_path

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if filters.PHOTO.check_update(update):
        file_id  = update.message.photo[-1].file_id
        unique_file_id = update.message.photo[-1].file_unique_id
        photo_name = f"{unique_file_id}.jpg"
    elif filters.Document.IMAGE:
        file_id = update.message.document.file_id
        _, f_ext = os.path.splitext(update.message.document.file_name)
        unique_file_id = update.message.document.file_unique_id
        photo_name = f"{unique_file_id}.{f_ext}"
    photo_file = await context.bot.get_file(file_id)
    await photo_file.download_to_drive(custom_path=f"./temp/{photo_name}")
    await context.bot.send_message(chat_id=update.effective_chat.id,text="we processing your photo please wait....")
    processed_image = await process_image(photo_name)
    await context.bot.send_document(chat_id=update.effective_chat.id,document=processed_image)
    os.remove(processed_image)

async def main():
    bot = Bot(telegram_bot_token)
    async with bot:
        print((await bot.get_updates())[-1])


if __name__=="__main__":
    application = ApplicationBuilder().token(telegram_bot_token).build()
    help_handler = CommandHandler("help",help)
    start_handler = CommandHandler("start",start)
    message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE,handle_message)

    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    application.run_polling()