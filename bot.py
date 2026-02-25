import os
import io
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from PIL import Image
from rembg import remove
from dotenv import load_dotenv
from bingart import BingArt, Model, Aspect

load_dotenv()

# Initialize Bing Art with cookie
bing_cookie_u = os.getenv("BING_COOKIE_U")
bing_art = BingArt(auth_cookie_U=bing_cookie_u) if bing_cookie_u else None

# User preferences storage (in-memory, resets on restart)
user_prefs = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    user_id = update.effective_user.id
    user_prefs[user_id] = {
        "format": "png",
        "transparent": False,
        "model": "dalle",
        "aspect": "square"
    }
    
    await update.message.reply_text(
        "👋 Welcome to Clipart Generator Bot!\n\n"
        "Send me a text description and I'll generate clipart for you.\n\n"
        "Commands:\n"
        "/settings - Choose format, model, and aspect ratio\n"
        "/help - Show this message"
    )

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings menu"""
    user_id = update.effective_user.id
    prefs = user_prefs.get(user_id, {
        "format": "png",
        "transparent": False,
        "model": "dalle",
        "aspect": "square"
    })
    
    keyboard = [
        [
            InlineKeyboardButton("PNG ✓" if prefs["format"] == "png" else "PNG", callback_data="format_png"),
            InlineKeyboardButton("JPEG ✓" if prefs["format"] == "jpeg" else "JPEG", callback_data="format_jpeg")
        ],
        [
            InlineKeyboardButton(
                f"Transparent: {'ON ✓' if prefs['transparent'] else 'OFF'}", 
                callback_data="toggle_transparent"
            )
        ],
        [
            InlineKeyboardButton("DALL-E ✓" if prefs["model"] == "dalle" else "DALL-E", callback_data="model_dalle"),
            InlineKeyboardButton("MAI1 ✓" if prefs["model"] == "mai1" else "MAI1", callback_data="model_mai1")
        ],
        [
            InlineKeyboardButton("Square ✓" if prefs["aspect"] == "square" else "Square", callback_data="aspect_square"),
            InlineKeyboardButton("Landscape ✓" if prefs["aspect"] == "landscape" else "Landscape", callback_data="aspect_landscape"),
            InlineKeyboardButton("Portrait ✓" if prefs["aspect"] == "portrait" else "Portrait", callback_data="aspect_portrait")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⚙️ Settings:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    user_id = query.from_user.id
    
    print(f"Button callback triggered! Data: {query.data}")
    
    if user_id not in user_prefs:
        user_prefs[user_id] = {
            "format": "png",
            "transparent": False,
            "model": "dalle",
            "aspect": "square"
        }
    
    prefs = user_prefs[user_id]
    
    # Format selection
    if query.data == "format_png":
        prefs["format"] = "png"
    elif query.data == "format_jpeg":
        prefs["format"] = "jpeg"
        prefs["transparent"] = False  # JPEG doesn't support transparency
    elif query.data == "toggle_transparent":
        if prefs["format"] == "png":
            prefs["transparent"] = not prefs["transparent"]
    
    # Model selection
    elif query.data == "model_dalle":
        prefs["model"] = "dalle"
    elif query.data == "model_mai1":
        prefs["model"] = "mai1"
    
    # Aspect ratio selection
    elif query.data == "aspect_square":
        prefs["aspect"] = "square"
    elif query.data == "aspect_landscape":
        prefs["aspect"] = "landscape"
    elif query.data == "aspect_portrait":
        prefs["aspect"] = "portrait"
    
    await query.answer()
    
    # Update the settings menu
    keyboard = [
        [
            InlineKeyboardButton("PNG ✓" if prefs["format"] == "png" else "PNG", callback_data="format_png"),
            InlineKeyboardButton("JPEG ✓" if prefs["format"] == "jpeg" else "JPEG", callback_data="format_jpeg")
        ],
        [
            InlineKeyboardButton(
                f"Transparent: {'ON ✓' if prefs['transparent'] else 'OFF'}", 
                callback_data="toggle_transparent"
            )
        ],
        [
            InlineKeyboardButton("DALL-E ✓" if prefs["model"] == "dalle" else "DALL-E", callback_data="model_dalle"),
            InlineKeyboardButton("MAI1 ✓" if prefs["model"] == "mai1" else "MAI1", callback_data="model_mai1")
        ],
        [
            InlineKeyboardButton("Square ✓" if prefs["aspect"] == "square" else "Square", callback_data="aspect_square"),
            InlineKeyboardButton("Landscape ✓" if prefs["aspect"] == "landscape" else "Landscape", callback_data="aspect_landscape"),
            InlineKeyboardButton("Portrait ✓" if prefs["aspect"] == "portrait" else "Portrait", callback_data="aspect_portrait")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_reply_markup(reply_markup=reply_markup)

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate image from text prompt"""
    import asyncio
    
    user_id = update.effective_user.id
    prompt = update.message.text
    
    prefs = user_prefs.get(user_id, {
        "format": "png",
        "transparent": False,
        "model": "dalle",
        "aspect": "square"
    })
    
    status_msg = await update.message.reply_text("🎨 Generating your image...")
    
    try:
        if not bing_art:
            await status_msg.edit_text("❌ Bing cookie not configured. Please add BING_COOKIE_U to .env file.")
            return
        
        # Map user preferences to bingart enums
        model_map = {
            "dalle": Model.DALLE,
            "mai1": Model.MAI1
        }
        aspect_map = {
            "square": Aspect.SQUARE,
            "landscape": Aspect.LANDSCAPE,
            "portrait": Aspect.PORTRAIT
        }
        
        selected_model = model_map.get(prefs["model"], Model.DALLE)
        selected_aspect = aspect_map.get(prefs["aspect"], Aspect.SQUARE)
        
        # Generate images using BingArt with timeout
        print(f"Generating images for prompt: {prompt}")
        print(f"Model: {prefs['model']}, Aspect: {prefs['aspect']}")
        
        # Run generation with timeout (120 seconds max)
        try:
            result = await asyncio.wait_for(
                bing_art.generate(prompt, model=selected_model, aspect=selected_aspect),
                timeout=120.0
            )
        except asyncio.TimeoutError:
            await status_msg.edit_text(
                "⏱️ Generation timed out after 2 minutes.\n"
                "The model might be slow or unavailable. Please try again."
            )
            return
        
        print(f"Received result: {result}")
        
        if not result or 'images' not in result or len(result['images']) == 0:
            await status_msg.edit_text("❌ No images generated. Your cookie might be expired.")
            return
        
        # Download the first image
        image_url = result['images'][0]['url']
        print(f"Downloading image from: {image_url}")
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))
        
        # Remove background if transparent is enabled
        if prefs["transparent"] and prefs["format"] == "png":
            await status_msg.edit_text("🎨 Generating your image... Removing background...")
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            
            output = remove(image_bytes.read())
            image = Image.open(io.BytesIO(output))
        
        # Convert to desired format
        output_buffer = io.BytesIO()
        if prefs["format"] == "jpeg":
            # Convert RGBA to RGB for JPEG
            if image.mode == "RGBA":
                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3] if len(image.split()) == 4 else None)
                image = rgb_image
            image.save(output_buffer, format="JPEG", quality=95)
            filename = "clipart.jpg"
        else:
            image.save(output_buffer, format="PNG")
            filename = "clipart.png"
        
        output_buffer.seek(0)
        
        # Send the image with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await update.message.reply_document(
                    document=output_buffer,
                    filename=filename,
                    caption=f"✨ Generated: {prompt[:100]}...",
                    read_timeout=60,
                    write_timeout=60
                )
                # Delete status message after successful send
                try:
                    await status_msg.delete()
                except:
                    pass  # Ignore if already deleted
                print("Image sent successfully!")
                break
            except Exception as upload_error:
                if attempt < max_retries - 1:
                    await status_msg.edit_text(f"⏳ Upload timeout, retrying... ({attempt + 1}/{max_retries})")
                    output_buffer.seek(0)  # Reset buffer for retry
                else:
                    await status_msg.edit_text(
                        "❌ Upload failed after multiple attempts. The image was generated but couldn't be sent.\n"
                        "This might be due to network issues. Please try again."
                    )
                    raise
        
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        await status_msg.edit_text(f"❌ Error: {str(e)}\n\nTry a different prompt or check your settings.")

def main():
    """Start the bot"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    app = Application.builder().token(token).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
    
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
