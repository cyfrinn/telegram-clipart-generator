# 🎨 Telegram Clipart Generator

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-archived-orange.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)

**AI-powered clipart generation bot for Telegram**

Generate stunning clipart images using Microsoft Bing's DALL-E 3, with customizable formats, aspect ratios, and automatic background removal.

[Features](#-features) • [Demo](#-demo) • [Quick Start](#-quick-start) • [Documentation](#-documentation)

</div>

---

## 📖 Overview

A fully-featured Telegram bot that transforms text descriptions into professional clipart images. Built for an Etsy clipart business, this bot leverages Microsoft's free DALL-E 3 API through Bing Image Creator to generate high-quality images with extensive customization options.

### Why This Bot?

- 🆓 **Completely Free** - Uses Bing Image Creator (no API costs)
- 🎯 **User-Friendly** - Intuitive inline keyboard interface
- 🎨 **Customizable** - Multiple formats, models, and aspect ratios
- ✨ **Professional** - Automatic background removal for transparent PNGs
- ⚡ **Fast** - 20-40 second generation time
- 🔄 **Reliable** - Built-in retry logic and error handling

---

## ✨ Features

### 🖼️ Image Generation
- **AI Models**: DALL-E 3 and MAI1 support
- **Aspect Ratios**: Square (1:1), Landscape (7:4), Portrait (4:7)
- **Format Options**: PNG or JPEG output
- **Batch Results**: 4 images generated per prompt

### 🎨 Image Processing
- **Background Removal**: AI-powered transparency using U2-Net
- **Format Conversion**: Automatic RGBA to RGB conversion for JPEG
- **Quality Control**: 95% JPEG quality, lossless PNG

### 🛠️ User Experience
- **Interactive Settings**: Inline keyboard with real-time updates
- **Per-User Preferences**: Personalized settings for each user
- **Progress Feedback**: Status messages during generation
- **Error Recovery**: Automatic retry with user notifications

---

## 🎬 Demo

### Bot Interface

```
👋 Welcome to Clipart Generator Bot!

Send me a text description and I'll generate clipart for you.

Commands:
/settings - Choose format, model, and aspect ratio
/help - Show this message
```

### Settings Menu

```
⚙️ Settings:

[PNG ✓] [JPEG]
[Transparent: ON ✓]
[DALL-E ✓] [MAI1]
[Square ✓] [Landscape] [Portrait]
```

### Generation Flow

1. User sends: `"cute ninja toy, soft pastel colors, 3d render"`
2. Bot responds: `🎨 Generating your image...`
3. Bot delivers: High-quality clipart in chosen format

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Bing Cookie (from [bing.com/images/create](https://www.bing.com/images/create))

### Installation

```bash
# Clone the repository
git clone https://github.com/cyfrinn/telegram-clipart-generator.git
cd telegram-clipart-generator

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your tokens
```

### Configuration

Create a `.env` file with your credentials:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
BING_COOKIE_U=your_bing_cookie_here
```

#### Getting Your Bing Cookie

1. Go to [bing.com/images/create](https://www.bing.com/images/create)
2. Sign in with your Microsoft account
3. Open Developer Tools (F12)
4. Go to Application → Cookies → `https://www.bing.com`
5. Find the `_U` cookie and copy its value

### Running the Bot

```bash
# Start the bot
python bot.py

# You should see:
# 🤖 Bot is running...
```

---

## 📚 Documentation

### Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot and set default preferences |
| `/help` | Show help message |
| `/settings` | Open interactive settings menu |

### Settings Options

#### Format
- **PNG** - Lossless, supports transparency
- **JPEG** - Smaller file size, no transparency

#### Transparency
- **ON** - Remove background (PNG only)
- **OFF** - Keep original background

#### AI Model
- **DALL-E** - Microsoft's DALL-E 3 (fast, reliable)
- **MAI1** - Alternative model (experimental)

#### Aspect Ratio
- **Square** - 1:1 ratio (default)
- **Landscape** - 7:4 ratio (wide)
- **Portrait** - 4:7 ratio (tall)

### Usage Examples

**Basic Generation:**
```
User: "cute cat illustration"
Bot: [Generates 4 square PNG images with transparent background]
```

**Custom Settings:**
```
1. /settings
2. Select: JPEG, Landscape, DALL-E
3. Send: "mountain landscape sunset"
4. Receive: Landscape JPEG image
```

---

## 🏗️ Architecture

```
┌─────────────┐
│   Telegram  │
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Bot Application               │
│   • Command Handlers            │
│   • Message Processing          │
│   • Settings Management         │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Bing Image Creator API        │
│   • DALL-E 3 / MAI1             │
│   • Cookie Authentication       │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   Image Processing Pipeline     │
│   • Download                    │
│   • Background Removal (rembg)  │
│   • Format Conversion (Pillow)  │
│   • Upload to Telegram          │
└─────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Core
- **Python 3.9+** - Programming language
- **python-telegram-bot 21.0** - Telegram Bot API wrapper
- **asyncio** - Asynchronous operations

### AI & Image Processing
- **bingart 1.5.1** - Bing Image Creator wrapper
- **rembg 2.0.62+** - AI background removal (U2-Net)
- **Pillow 11.0.0** - Image manipulation

### Utilities
- **python-dotenv** - Environment configuration
- **requests** - HTTP client

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Generation Time | 20-40 seconds |
| Background Removal | 5-10 seconds |
| Total Processing | 30-50 seconds |
| Memory Usage | ~300MB peak |
| Disk Space | ~200MB (with dependencies) |

---

## ⚠️ Known Limitations

1. **Cookie Expiration** - Bing cookies expire every 2-4 weeks (manual refresh required)
2. **Single User Auth** - One Bing account shared across all bot users
3. **No Persistence** - User preferences reset on bot restart
4. **Rate Limits** - Bing provides 25 "boosts" per week (then slower generation)
5. **Deployment** - Requires ~200MB disk space (limits free hosting options)

---

## 🚧 Deployment Status

**Current Status:** ⚠️ Archived (Not Deployed)

This project was successfully developed and tested locally but is **not currently deployed** due to scalability considerations. The bot works perfectly for small-scale use (2-3 users) but was deemed unsuitable for public deployment.

### Deployment Attempts

| Platform | Status | Reason |
|----------|--------|--------|
| Render.com | ❌ Failed | No free tier for background workers |
| Alwaysdata | ❌ Failed | Insufficient disk space (100MB limit) |
| AWS EC2 | ✅ Worked | Terminated (cost vs. usage) |

### Running Locally

For personal or small team use, run the bot on your local machine:

```bash
python bot.py
# Keep terminal open while bot is running
```

### Production Deployment (If Needed)

For production deployment, consider:
- **AWS EC2** (t3.micro) - ~$8/month
- **Railway.app** - $5 free credit/month
- **DigitalOcean Droplet** - $6/month

See [PROJECT_ANALYSIS.md](PROJECT_ANALYSIS.md) for detailed deployment analysis.

---

## 🤝 Contributing

Contributions are welcome! This project is archived but open for improvements.

### Areas for Contribution

- [ ] Add database for persistent user preferences
- [ ] Implement automatic cookie refresh
- [ ] Add rate limiting per user
- [ ] Create web interface alternative
- [ ] Add unit tests
- [ ] Improve error handling
- [ ] Add monitoring/analytics

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Microsoft Bing** - For free DALL-E 3 access via Image Creator
- **python-telegram-bot** - Excellent Telegram Bot API wrapper
- **rembg** - AI-powered background removal
- **bingart** - Bing Image Creator API wrapper

---

## 📧 Contact

**Project Maintainer:** [@cyfrinn](https://github.com/cyfrinn)

**Project Link:** [https://github.com/cyfrinn/telegram-clipart-generator](https://github.com/cyfrinn/telegram-clipart-generator)

---

## 📖 Additional Resources

- [PROJECT_ANALYSIS.md](PROJECT_ANALYSIS.md) - Comprehensive technical analysis
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [Bing Image Creator](https://www.bing.com/images/create)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)

---

<div align="center">

**⭐ Star this repo if you found it helpful!**

Made with ❤️ for the Etsy clipart community

</div>
