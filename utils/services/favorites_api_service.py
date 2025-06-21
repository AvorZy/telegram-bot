from telegram import Update
import aiohttp
import asyncio
import os
from typing import Dict, Optional, List
from telegram import Update
from telegram.ext import ContextTypes
from utils.ui.language import language_handler
from utils.ui.keyboards import Keyboards
from utils.services import user_api_service
from handlers.base import get_or_create_user
from dotenv import load_dotenv

def _run_async_in_sync(async_func, *args, **kwargs):
    """Helper function to run async functions in sync context"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(async_func(*args, **kwargs))
        loop.close()
        return result
    except Exception as e:
        print(f"Error running async function: {e}")
        return None

# Load environment variables
load_dotenv()

async def add_to_favorites_api(update: Update, context: ContextTypes.DEFAULT_TYPE, car_id: int):
    """Add car to user's favorites via API"""
    user = await get_or_create_user(update.effective_user)
    telegram_id = user.get('telegram_id')
    user_language = user.get('language', 'en')
    
    try:
        # Add to favorites via API
        success = await user_api_service.add_favorite(telegram_id, car_id)
        
        if success:
            message = language_handler.get_text("favorite_added", user_language)
        else:
            message = language_handler.get_text("favorite_add_failed", user_language)
            
    except Exception as e:
        print(f"Error adding favorite for user {telegram_id}: {e}")
        message = language_handler.get_text("favorite_add_error", user_language)
    
    # Send response
    if update.callback_query:
        await update.callback_query.answer(message)
    else:
        await update.message.reply_text(message)

async def remove_from_favorites_api(update: Update, context: ContextTypes.DEFAULT_TYPE, car_id: int):
    """Remove car from user's favorites via API"""
    user = await get_or_create_user(update.effective_user)
    telegram_id = user.get('telegram_id')
    user_language = user.get('language', 'en')
    
    try:
        # Remove from favorites via API
        success = await user_api_service.remove_favorite(telegram_id, car_id)
        
        if success:
            message = language_handler.get_text("favorite_removed", user_language)
        else:
            message = language_handler.get_text("favorite_remove_failed", user_language)
            
    except Exception as e:
        print(f"Error removing favorite for user {telegram_id}: {e}")
        message = language_handler.get_text("favorite_remove_error", user_language)
    
    # Send response
    if update.callback_query:
        await update.callback_query.answer(message)
    else:
        await update.message.reply_text(message)

async def get_user_favorites_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get and display user's favorites from API"""
    user = await get_or_create_user(update.effective_user)
    telegram_id = user.get('telegram_id')
    user_language = user.get('language', 'en')
    
    try:
        # Get favorites from API
        favorites = await user_api_service.get_user_favorites(telegram_id)
        
        if not favorites:
            message = language_handler.get_text("no_favorites", user_language)
            await update.message.reply_text(
                message,
                reply_markup=Keyboards.get_main_menu_keyboard(user_language)
            )
            return
        
        # Display favorites
        favorites_text = language_handler.get_text("your_favorites", user_language)
        favorites_text += "\n\n"
        
        for i, favorite in enumerate(favorites[:10], 1):  # Limit to 10 favorites
            car_info = f"{i}. {favorite.get('brand', 'Unknown')} {favorite.get('model', 'Unknown')}"
            if favorite.get('price'):
                car_info += f" - ${favorite.get('price'):,.0f}"
            favorites_text += car_info + "\n"
        
        await update.message.reply_text(
            favorites_text,
            reply_markup=Keyboards.get_favorites_keyboard(user_language)
        )
        
    except Exception as e:
        print(f"Error getting favorites for user {telegram_id}: {e}")
        error_message = language_handler.get_text("favorites_load_error", user_language)
        await update.message.reply_text(
            error_message,
            reply_markup=Keyboards.get_main_menu_keyboard(user_language)
        )

def sync_add_to_favorites(telegram_user, car_id: int) -> bool:
    """Synchronous wrapper for adding to favorites (for use in sync contexts)"""
    telegram_id = telegram_user.id
    
    try:
        success = _run_async_in_sync(
            user_api_service.add_favorite, telegram_id, car_id
        )
        return success if success is not None else False
        
    except Exception as e:
        print(f"Error adding favorite for user {telegram_id}: {e}")
        return False

def sync_remove_from_favorites(telegram_user, car_id: int) -> bool:
    """Synchronous wrapper for removing from favorites (for use in sync contexts)"""
    telegram_id = telegram_user.id
    
    try:
        success = _run_async_in_sync(
            user_api_service.remove_favorite, telegram_id, car_id
        )
        return success if success is not None else False
        
    except Exception as e:
        print(f"Error removing favorite for user {telegram_id}: {e}")
        return False

def sync_get_user_favorites(telegram_user) -> list:
    """Synchronous wrapper for getting user favorites (for use in sync contexts)"""
    telegram_id = telegram_user.id
    
    try:
        favorites = _run_async_in_sync(
            user_api_service.get_user_favorites, telegram_id
        )
        return favorites if favorites else []
        
    except Exception as e:
        print(f"Error getting favorites for user {telegram_id}: {e}")
        return []