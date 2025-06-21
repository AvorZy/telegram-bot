from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.ui.language import language_handler
from .global_navigation import create_navigation_keyboard

async def handle_safety_maintenance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("safety_maintenance_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("driving_safety_tips", telegram_id), callback_data="safety_tips"),
         InlineKeyboardButton(language_handler.get_text("warning_signs", telegram_id), callback_data="safety_warnings")],
        [InlineKeyboardButton(language_handler.get_text("emergency_preparedness", telegram_id), callback_data="safety_emergency"),
         InlineKeyboardButton(language_handler.get_text("seasonal_care", telegram_id), callback_data="safety_seasonal")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("safety_section", telegram_id), "explore_safety", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_safety_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("safety_tips_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("maintenance_schedule", telegram_id), callback_data="safety_maintenance"),
         InlineKeyboardButton(language_handler.get_text("warning_signs", telegram_id), callback_data="safety_warnings")],
        [InlineKeyboardButton(language_handler.get_text("emergency_preparedness", telegram_id), callback_data="safety_emergency"),
         InlineKeyboardButton(language_handler.get_text("diy_checks", telegram_id), callback_data="safety_diy")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("safety_section", telegram_id), "explore_safety", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_safety_warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("safety_warnings_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("maintenance_schedule", telegram_id), callback_data="safety_maintenance"),
         InlineKeyboardButton(language_handler.get_text("driving_safety_tips", telegram_id), callback_data="safety_tips")],
        [InlineKeyboardButton(language_handler.get_text("emergency_preparedness", telegram_id), callback_data="safety_emergency"),
         InlineKeyboardButton(language_handler.get_text("diy_checks", telegram_id), callback_data="safety_diy")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("safety_section", telegram_id), "explore_safety", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_safety_emergency(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("safety_emergency_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("maintenance_schedule", telegram_id), callback_data="safety_maintenance"),
         InlineKeyboardButton(language_handler.get_text("driving_safety_tips", telegram_id), callback_data="safety_tips")],
        [InlineKeyboardButton(language_handler.get_text("warning_signs", telegram_id), callback_data="safety_warnings"),
         InlineKeyboardButton(language_handler.get_text("seasonal_care", telegram_id), callback_data="safety_seasonal")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("safety_section", telegram_id), "explore_safety", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_safety_seasonal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("safety_seasonal_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("maintenance_schedule", telegram_id), callback_data="safety_maintenance"),
         InlineKeyboardButton(language_handler.get_text("driving_safety_tips", telegram_id), callback_data="safety_tips")],
        [InlineKeyboardButton(language_handler.get_text("warning_signs", telegram_id), callback_data="safety_warnings"),
         InlineKeyboardButton(language_handler.get_text("diy_checks", telegram_id), callback_data="safety_diy")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("safety_section", telegram_id), "explore_safety", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_safety_diy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("safety_diy_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("maintenance_schedule", telegram_id), callback_data="safety_maintenance"),
         InlineKeyboardButton(language_handler.get_text("driving_safety_tips", telegram_id), callback_data="safety_tips")],
        [InlineKeyboardButton(language_handler.get_text("warning_signs", telegram_id), callback_data="safety_warnings"),
         InlineKeyboardButton(language_handler.get_text("emergency_preparedness", telegram_id), callback_data="safety_emergency")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("safety_section", telegram_id), "explore_safety", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')