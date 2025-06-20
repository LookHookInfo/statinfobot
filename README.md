# 📊 Look Hook InfoBot

> **Developer:** [Look Hook](https://lookhook.info)

This Telegram bot generates and posts real-time infographics with key token metrics (price, liquidity, volume, FDV) to multiple Telegram channels and forum threads.

---

## 🚀 0. What This Bot Does

- Fetches token stats from GeckoTerminal API
- Generates a visual infographic with:
  - Token price in USD
  - Liquidity
  - 24h volume
  - FDV (Fully Diluted Valuation)
- Automatically posts the infographic to:
  - Regular Telegram channels
  - Telegram forum threads

---

## 🔐 1. Where to Get API & Keys

- **GeckoTerminal API**: No API key required (public endpoint).
- **Telegram Bot Token**:
  - Open [@BotFather](https://t.me/BotFather)
  - Create a bot and get your token (format: `123456:ABC-DEF...`)

---

## 🤖 2. Create and Add the Bot

1. Create the bot using @BotFather  
2. Add the bot to each channel or forum:
   - Give it `Can Post Messages` permission
3. Get the Chat IDs and Thread IDs:
   - Use [@userinfobot](https://t.me/userinfobot) to get chat IDs
   - For threads, right-click on a message in the thread and copy its link to extract the `message_id` (used as `message_thread_id`)

---

## ⚙️ 3. Configure the Files

1. Install the dependencies:
   ```bash
   pip install python-telegram-bot==20.7 requests



BOT_TOKEN = "YOUR_BOT_TOKEN"
CHANNELS = [
    -1001234569990,                      # Regular channel
    (-1009876543990, 143),              # Forum thread: (chat_id, message_thread_id)
]
python main.py
