# Clipart Generator Telegram Bot

A simple Telegram bot that generates clipart images using AI, with options for PNG/JPEG format and transparent backgrounds.

## Features

- 🎨 Generate clipart from text descriptions
- 🖼️ Choose between PNG or JPEG format
- ✨ Optional transparent background (PNG only)
- 🚀 Free to use (Hugging Face free tier)

## Setup

### 1. Get API Tokens

**Telegram Bot Token:**
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Copy the token you receive

**Bing Cookies:**
1. Go to https://www.bing.com/images/create in your browser
2. Sign in with your Microsoft account
3. Open Developer Tools (F12) → Console tab
4. Run this code:
   ```javascript
   console.log(`_U:\n${document.cookie.match(/(?:^|;\s*)_U=(.*?)(?:;|$)/)[1]}\n\nSRCHHPGUSR:\n${document.cookie.match(/(?:^|;\s*)SRCHHPGUSR=(.*?)(?:;|$)/)[1]}`)
   ```
5. Copy both cookie values that are displayed

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your tokens:
   ```
   TELEGRAM_BOT_TOKEN=your_actual_token_here
   BING_COOKIE_U=your_actual_U_cookie_here
   BING_COOKIE_SRCHHPGUSR=your_actual_SRCHHPGUSR_cookie_here
   ```

### 4. Run the Bot

```bash
python bot.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to begin
3. Send `/settings` to choose format and transparency
4. Send any text description to generate clipart

Example prompts:
- "cute cat with flowers"
- "coffee cup icon, minimalist"
- "birthday cake clipart"

## Deployment (Free Options)

### Render.com
1. Create account on Render.com
2. Create new "Web Service"
3. Connect your GitHub repo
4. Add environment variables
5. Deploy!

### Railway.app
1. Create account on Railway.app
2. New Project → Deploy from GitHub
3. Add environment variables
4. Deploy!

## Notes

- Uses Microsoft Bing Image Creator (completely free!)
- First image generation might be slow (model loading)
- Transparent background removal takes extra time
- JPEG format doesn't support transparency
- Bing cookie expires periodically - just get a new one when it stops working
