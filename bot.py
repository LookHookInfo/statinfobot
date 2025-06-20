import requests
import datetime
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, PicklePersistence
from telegram.constants import ParseMode
from caption_lines import get_caption_lines
from infographic import generate_infographic

# --- Настройки ---
BOT_TOKEN = "key"

POOL_API = "https://api.geckoterminal.com/api/v2/networks/base/pools/0x9ab05414f0a3872a78459693f3e3c9ea3f0d6e71"

# --- Каналы и форумы ---
# Обычные каналы — просто ID, форумы — (chat_id, thread_id)
CHANNELS = [
    -1002046496999,               # @commpost
    -1002007919999,               # ChainForum
    -1002070598999,               # Forum Chain
    (-1002126150999, 143),        # Genome Chat → тема 143
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --- Получение данных с API ---
def get_token_price():
    try:
        res = requests.get(POOL_API)
        res.raise_for_status()
        attrs = res.json()["data"]["attributes"]
        price = float(attrs.get("base_token_price_usd", 0))
        return round(price, 8)
    except Exception as e:
        logger.error(f"Price error: {e}")
        return None


def get_pool_stats():
    try:
        res = requests.get(POOL_API)
        res.raise_for_status()
        attrs = res.json()["data"]["attributes"]
        return {
            "reserve_usd": float(attrs.get("reserve_in_usd", 0)),
            "volume_24h": float(attrs.get("volume_usd", {}).get("h24", 0)),
            "fdv_usd": float(attrs.get("fdv_usd", 0)),
        }
    except Exception as e:
        logger.error(f"Pool stats error: {e}")
        return None


# --- Отправка инфографики во все каналы и темы ---
async def send_infographic(context: ContextTypes.DEFAULT_TYPE, chat_list=CHANNELS):
    price = get_token_price()
    stats = get_pool_stats()

    if price is None or stats is None:
        for chat in chat_list:
            chat_id = chat[0] if isinstance(chat, tuple) else chat
            await context.bot.send_message(chat_id=chat_id, text="❌ Ошибка получения данных.")
        return

    img_path = generate_infographic(price, stats)
    caption_lines = get_caption_lines()
    caption = "\n".join(caption_lines)

    try:
        with open(img_path, "rb") as img_file:
            img_data = img_file.read()

        for chat in chat_list:
            if isinstance(chat, tuple):
                chat_id, thread_id = chat
                await context.bot.send_photo(
                    chat_id=chat_id,
                    message_thread_id=thread_id,
                    photo=img_data,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await context.bot.send_photo(
                    chat_id=chat,
                    photo=img_data,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )

    except FileNotFoundError:
        logger.error(f"Image file not found: {img_path}")
        for chat in chat_list:
            chat_id = chat[0] if isinstance(chat, tuple) else chat
            await context.bot.send_message(chat_id=chat_id, text="❌ Ошибка с изображением.")


# --- Команда для ручной публикации ---
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_infographic(context)
    await update.message.reply_text("✅ Опубликовано в каналы и форумы.")


# --- Ежедневный пост ---
async def scheduled_post(context: ContextTypes.DEFAULT_TYPE):
    await send_infographic(context)


# --- Запуск бота ---
def main():
    persistence = PicklePersistence("bot_data")
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()

    app.add_handler(CommandHandler("info", info))

    # Автопост в 17:00 каждый день
    app.job_queue.run_daily(scheduled_post, time=datetime.time(hour=17, minute=0))

    logger.info("Bot started.")
    app.run_polling()


if __name__ == "__main__":
    main()
