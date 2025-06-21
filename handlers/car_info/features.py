from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from .global_navigation import create_navigation_keyboard
from utils.ui.language import language_handler

async def handle_features_safety(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    text = language_handler.get_text("features_safety_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("smart_technology", telegram_id), callback_data="features_tech"),
         InlineKeyboardButton(language_handler.get_text("comfort_luxury", telegram_id), callback_data="features_comfort")],
        [InlineKeyboardButton(language_handler.get_text("performance_features", telegram_id), callback_data="features_performance"),
         InlineKeyboardButton(language_handler.get_text("electric_features", telegram_id), callback_data="features_electric")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("features_section", telegram_id), "explore_features", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_features_tech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    telegram_id = update.effective_user.id
    

    
    text = language_handler.get_text("features_tech_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("safety_systems", telegram_id), callback_data="features_safety"),
         InlineKeyboardButton(language_handler.get_text("comfort_luxury", telegram_id), callback_data="features_comfort")],
        [InlineKeyboardButton(language_handler.get_text("performance_features", telegram_id), callback_data="features_performance"),
         InlineKeyboardButton(language_handler.get_text("electric_features", telegram_id), callback_data="features_electric")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("features_section", telegram_id), "explore_features", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_features_comfort(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    text = language_handler.get_text("features_comfort_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("safety_systems", telegram_id), callback_data="features_safety"),
         InlineKeyboardButton(language_handler.get_text("smart_technology", telegram_id), callback_data="features_tech")],
        [InlineKeyboardButton(language_handler.get_text("performance_features", telegram_id), callback_data="features_performance"),
         InlineKeyboardButton(language_handler.get_text("electric_features", telegram_id), callback_data="features_electric")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("features_section", telegram_id), "explore_features", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_features_performance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
 
    
    text = language_handler.get_text("features_performance_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("safety_systems", telegram_id), callback_data="features_safety"),
         InlineKeyboardButton(language_handler.get_text("smart_technology", telegram_id), callback_data="features_tech")],
        [InlineKeyboardButton(language_handler.get_text("comfort_luxury", telegram_id), callback_data="features_comfort"),
         InlineKeyboardButton(language_handler.get_text("electric_features", telegram_id), callback_data="features_electric")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("features_section", telegram_id), "explore_features", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_features_electric(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    
    text = language_handler.get_text("features_electric_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("safety_systems", telegram_id), callback_data="features_safety"),
         InlineKeyboardButton(language_handler.get_text("smart_technology", telegram_id), callback_data="features_tech")],
        [InlineKeyboardButton(language_handler.get_text("comfort_luxury", telegram_id), callback_data="features_comfort"),
         InlineKeyboardButton(language_handler.get_text("performance_features", telegram_id), callback_data="features_performance")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("features_section", telegram_id), "explore_features", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_features_entertainment(update: Update, context: ContextTypes.DEFAULT_TYPE ):
    query = update.callback_query
    telegram_id = update.effective_user.id
    

    
    text = language_handler.get_text("features_entertainment_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("safety_systems", telegram_id), callback_data="features_safety"),
         InlineKeyboardButton(language_handler.get_text("smart_technology", telegram_id), callback_data="features_tech")],
        [InlineKeyboardButton(language_handler.get_text("comfort_luxury", telegram_id), callback_data="features_comfort"),
         InlineKeyboardButton(language_handler.get_text("performance_features", telegram_id), callback_data="features_performance")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("features_section", telegram_id), "explore_features", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')