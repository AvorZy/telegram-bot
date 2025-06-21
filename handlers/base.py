from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from models.core.user import User
from models.data.message import Message, messages
from utils.ui.keyboards import Keyboards
from utils.ui.language import language_handler
from utils.services.user_api_service import user_api_service
import asyncio
import json
import os

# Local cache for users to reduce API calls (memory-only)
user_cache = {}

def clear_user_cache(telegram_id=None):
    """Clear user cache for specific user or all users"""
    global user_cache
    if telegram_id:
        if telegram_id in user_cache:
            del user_cache[telegram_id]
            pass
    else:
        user_cache.clear()
        pass

async def force_refresh_user(telegram_id):
    """Force refresh user data from API by clearing cache"""
    clear_user_cache(telegram_id)
    print(f"DEBUG: Forced refresh for user {telegram_id}")
    
    # Create a mock telegram user object for API call
    class MockTelegramUser:
        def __init__(self, user_id):
            self.id = user_id
            self.language_code = None
            self.first_name = "Test"
            self.last_name = None
            self.username = None
    
    mock_user = MockTelegramUser(telegram_id)
    user_data = await user_api_service.get_or_create_user(mock_user)
    return user_data

async def get_or_create_user(telegram_user):
    """Get or create user using API service with local caching"""
    telegram_id = telegram_user.id
    
    # Check local cache first
    if telegram_id in user_cache:
        return user_cache[telegram_id]
    
    # Get user from API
    try:
        user_data = await user_api_service.get_or_create_user(telegram_user)
        
        # Debug: Print the language from API
        print(f"DEBUG: User {telegram_id} language from API: {user_data.get('language', 'NOT_SET')}")
        
        # Cache the user data
        user_cache[telegram_id] = user_data
        return user_data
        
    except Exception as e:
        print(f"Error getting user from API: {e}")
        # Fallback to local user creation
        # Use Telegram's language_code if available, otherwise default to 'en'
        telegram_lang = getattr(telegram_user, 'language_code', 'en')
        # Map common language codes to supported languages
        if telegram_lang and telegram_lang.startswith('km'):
            default_language = 'kh'
        else:
            default_language = 'en'
            
        fallback_user = {
            'telegram_id': telegram_id,
            'first_name': telegram_user.first_name or '',
            'last_name': telegram_user.last_name or '',
            'username': telegram_user.username or '',
            'language': default_language,
            'source': 'local_fallback'
        }
        user_cache[telegram_id] = fallback_user
        return fallback_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    pass
    
    # Check if user already exists first (check cache and API)
    existing_user = None
    if telegram_id in user_cache:
        existing_user = user_cache[telegram_id]
        pass
    else:
        pass
        # Check API directly without creating
        try:
            existing_user = await user_api_service.get_user(telegram_id)
            if existing_user:
                pass
                # Convert API format to local format and cache it
                existing_user = user_api_service._convert_api_user_to_local(existing_user)
                user_cache[telegram_id] = existing_user
                pass
            else:
                pass
        except Exception as e:
            pass
    
    # If user exists, show main menu directly
    if existing_user:
        pass
        welcome_message = language_handler.get_text(
            "welcome_message", 
            telegram_id, 
            name=existing_user.get('first_name', '') or "there"
        )
        
        if update.callback_query:
            message = update.callback_query.message
            await update.callback_query.answer()
            await message.reply_text(
                welcome_message,
                reply_markup=Keyboards.main_menu(telegram_id)
            )
        else:
            await update.message.reply_text(
                welcome_message,
                reply_markup=Keyboards.main_menu(telegram_id)
            )
        return
    
    pass
    
    # User doesn't exist - show language selection for new users
    welcome_message = "🌐សូមជ្រើសរើសភាសា / Please select your preferred language "
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            welcome_message,
            reply_markup=Keyboards.initial_language_selection()
        )
    else:
        await update.message.reply_text(
            welcome_message,
            reply_markup=Keyboards.initial_language_selection()
        )

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_user(update.effective_user)
    telegram_id = update.effective_user.id
    
    # Regular welcome message for returning users
    welcome_message = language_handler.get_text(
        "welcome_message", 
        telegram_id, 
        name=user.get('first_name', '') or "there"
    )
    
    if update.callback_query:
        message = update.callback_query.message
        await update.callback_query.answer()
        
        # Always use reply_text for conversational flow - this affects ALL back buttons
        await message.reply_text(
            welcome_message,
            reply_markup=Keyboards.main_menu(telegram_id)
        )
    else:
        await update.message.reply_text(
            welcome_message,
            reply_markup=Keyboards.main_menu(telegram_id)
        )

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_or_create_user(update.effective_user)
    telegram_id = update.effective_user.id
    
    await update.message.reply_text(
        language_handler.get_text("settings_title", telegram_id),
        reply_markup=Keyboards.settings_menu(telegram_id)
    )

async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    
    if context.user_data.get('awaiting_support_message'):
        user = await get_or_create_user(update.effective_user)
        message = Message(
            id=len(messages) + 1,
            user_id=user.get('id', user.get('telegram_id')),
            message=update.message.text,
            direction="inbound",
            timestamp=datetime.now()
        )
        messages.append(message)
        
        await update.message.reply_text(
            "✅ Thank you for your message. Our support team will get back to you soon.",
            reply_markup=Keyboards.main_menu(telegram_id)
        )
        context.user_data['awaiting_support_message'] = False
    else:
        await update.message.reply_text(
            language_handler.get_text("unknown_command", telegram_id),
            reply_markup=Keyboards.main_menu(telegram_id)
        )