from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.ui.language import language_handler
from .global_navigation import create_navigation_keyboard

async def handle_benefits_work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("benefits_work_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("family_lifestyle", telegram_id), callback_data="benefits_family"),
         InlineKeyboardButton(language_handler.get_text("personal_freedom", telegram_id), callback_data="benefits_freedom")],
        [InlineKeyboardButton(language_handler.get_text("financial_benefits", telegram_id), callback_data="benefits_financial"),
         InlineKeyboardButton(language_handler.get_text("social_environmental", telegram_id), callback_data="benefits_social")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("benefits_section", telegram_id), "explore_advantages", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_benefits_family(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("benefits_family_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("professional_work", telegram_id), callback_data="benefits_work"),
         InlineKeyboardButton(language_handler.get_text("personal_freedom", telegram_id), callback_data="benefits_freedom")],
        [InlineKeyboardButton(language_handler.get_text("financial_benefits", telegram_id), callback_data="benefits_financial"),
         InlineKeyboardButton(language_handler.get_text("social_environmental", telegram_id), callback_data="benefits_social")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("benefits_section", telegram_id), "explore_advantages", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_benefits_freedom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("benefits_freedom_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("professional_work", telegram_id), callback_data="benefits_work"),
         InlineKeyboardButton(language_handler.get_text("family_lifestyle", telegram_id), callback_data="benefits_family")],
        [InlineKeyboardButton(language_handler.get_text("financial_benefits", telegram_id), callback_data="benefits_financial"),
         InlineKeyboardButton(language_handler.get_text("social_environmental", telegram_id), callback_data="benefits_social")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("benefits_section", telegram_id), "explore_advantages", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_benefits_financial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("benefits_financial_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("professional_work", telegram_id), callback_data="benefits_work"),
         InlineKeyboardButton(language_handler.get_text("family_lifestyle", telegram_id), callback_data="benefits_family")],
        [InlineKeyboardButton(language_handler.get_text("personal_freedom", telegram_id), callback_data="benefits_freedom"),
         InlineKeyboardButton(language_handler.get_text("social_environmental", telegram_id), callback_data="benefits_social")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("benefits_section", telegram_id), "explore_advantages", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_benefits_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("benefits_social_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("professional_work", telegram_id), callback_data="benefits_work"),
         InlineKeyboardButton(language_handler.get_text("family_lifestyle", telegram_id), callback_data="benefits_family")],
        [InlineKeyboardButton(language_handler.get_text("personal_freedom", telegram_id), callback_data="benefits_freedom"),
         InlineKeyboardButton(language_handler.get_text("financial_benefits", telegram_id), callback_data="benefits_financial")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("benefits_section", telegram_id), "explore_advantages", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_benefits_comparison(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("benefits_comparison_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("professional_work", telegram_id), callback_data="benefits_work"),
         InlineKeyboardButton(language_handler.get_text("family_lifestyle", telegram_id), callback_data="benefits_family")],
        [InlineKeyboardButton(language_handler.get_text("personal_freedom", telegram_id), callback_data="benefits_freedom"),
         InlineKeyboardButton(language_handler.get_text("financial_benefits", telegram_id), callback_data="benefits_financial")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("benefits_section", telegram_id), "explore_advantages", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')