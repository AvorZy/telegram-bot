from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models.core.user import users
from utils.ui.language import language_handler
from utils.ui.keyboards import Keyboards

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("settings_title", telegram_id),
        reply_markup=Keyboards.settings_menu(telegram_id)
    )

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("select_language", telegram_id),
        reply_markup=Keyboards.language_selection(telegram_id)
    )

async def handle_language_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language change with API integration and cache management"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    language_code = query.data.split('_')[1]
    
    try:
        # Import the API service
        from utils.services.user_api_service import user_api_service
        from handlers.base import user_cache
        
        # Update language via API
        update_data = {'language': language_code}
        updated_user = await user_api_service.update_user(telegram_id, update_data)
        
        if updated_user:
            # Update local cache with fresh API data
            if telegram_id in user_cache:
                user_cache[telegram_id].update(user_api_service._convert_api_user_to_local(updated_user))
                print(f"DEBUG: Updated local cache for user {telegram_id} with language: {user_cache[telegram_id].get('language')}")
        else:
            # API update failed, but update local cache anyway
            if telegram_id in user_cache:
                user_cache[telegram_id]['language'] = language_code
        
        # Always update local language handler (fallback)
        language_handler.set_user_language(telegram_id, language_code)
        
        # Send confirmation message
        success_message = language_handler.get_text("language_changed", telegram_id)
            
        await query.message.reply_text(
            success_message,
            reply_markup=Keyboards.settings_menu(telegram_id)
        )
        
    except Exception as e:
        print(f"Error updating language for user {telegram_id}: {e}")
        
        # Fallback: update local cache only
        from handlers.base import user_cache
        if telegram_id in user_cache:
            user_cache[telegram_id]['language'] = language_code
        
        # Always update local language handler (fallback)
        language_handler.set_user_language(telegram_id, language_code)
        
        await query.message.reply_text(
            language_handler.get_text("language_changed", telegram_id),
            reply_markup=Keyboards.settings_menu(telegram_id)
        )

async def handle_english_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle English language selection"""
    # Modify the callback data to match the expected format
    update.callback_query.data = "lang_en"
    await handle_language_change(update, context)

async def handle_khmer_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Khmer language selection"""
    # Modify the callback data to match the expected format
    update.callback_query.data = "lang_kh"
    await handle_language_change(update, context)


async def handle_initial_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle initial language selection for first-time users"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    language_code = query.data.split('_')[2]  # Extract from 'initial_lang_en' or 'initial_lang_kh'
    
    # Set user's language preference
    language_handler.set_user_language(telegram_id, language_code)
    
    # Mark user as no longer first-time
    from models.core.user import users
    user = next((u for u in users if u.telegram_id == telegram_id), None)
    if user:
        user.is_first_time = False
    
    # Show welcome message in selected language
    welcome_message = language_handler.get_text(
        "welcome_message", 
        telegram_id, 
        name=user.first_name if user else "there"
    )
    
    await query.message.edit_text(
        welcome_message,
        reply_markup=Keyboards.main_menu(telegram_id)
    )
