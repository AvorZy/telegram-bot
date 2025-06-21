from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.ui.language import language_handler
from .global_navigation import create_navigation_keyboard

async def handle_eco_electric(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("eco_electric_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("hybrid_technology", telegram_id), callback_data="eco_hybrid"),
         InlineKeyboardButton(language_handler.get_text("fuel_efficiency_tips", telegram_id), callback_data="eco_fuel")],
        [InlineKeyboardButton(language_handler.get_text("environmental_impact", telegram_id), callback_data="eco_impact"),
         InlineKeyboardButton(language_handler.get_text("cost_savings", telegram_id), callback_data="eco_savings")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("eco_section", telegram_id), "explore_eco", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_eco_hybrid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("eco_hybrid_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("electric_vehicles", telegram_id), callback_data="eco_electric"),
         InlineKeyboardButton(language_handler.get_text("fuel_efficiency_tips", telegram_id), callback_data="eco_fuel")],
        [InlineKeyboardButton(language_handler.get_text("environmental_impact", telegram_id), callback_data="eco_impact"),
         InlineKeyboardButton(language_handler.get_text("charging_infrastructure", telegram_id), callback_data="eco_charging")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("eco_section", telegram_id), "explore_eco", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_eco_fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("eco_fuel_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("electric_vehicles", telegram_id), callback_data="eco_electric"),
         InlineKeyboardButton(language_handler.get_text("hybrid_technology", telegram_id), callback_data="eco_hybrid")],
        [InlineKeyboardButton(language_handler.get_text("environmental_impact", telegram_id), callback_data="eco_impact"),
         InlineKeyboardButton(language_handler.get_text("cost_savings", telegram_id), callback_data="eco_savings")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("eco_section", telegram_id), "explore_eco", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_eco_impact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("eco_impact_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("electric_vehicles", telegram_id), callback_data="eco_electric"),
         InlineKeyboardButton(language_handler.get_text("hybrid_technology", telegram_id), callback_data="eco_hybrid")],
        [InlineKeyboardButton(language_handler.get_text("fuel_efficiency_tips", telegram_id), callback_data="eco_fuel"),
         InlineKeyboardButton(language_handler.get_text("cost_savings", telegram_id), callback_data="eco_savings")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("eco_section", telegram_id), "explore_eco", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_eco_savings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("eco_savings_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("electric_vehicles", telegram_id), callback_data="eco_electric"),
         InlineKeyboardButton(language_handler.get_text("hybrid_technology", telegram_id), callback_data="eco_hybrid")],
        [InlineKeyboardButton(language_handler.get_text("fuel_efficiency_tips", telegram_id), callback_data="eco_fuel"),
         InlineKeyboardButton(language_handler.get_text("environmental_impact", telegram_id), callback_data="eco_impact")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("eco_section", telegram_id), "explore_eco", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_eco_charging(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("eco_charging_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("electric_vehicles", telegram_id), callback_data="eco_electric"),
         InlineKeyboardButton(language_handler.get_text("hybrid_technology", telegram_id), callback_data="eco_hybrid")],
        [InlineKeyboardButton(language_handler.get_text("fuel_efficiency_tips", telegram_id), callback_data="eco_fuel"),
         InlineKeyboardButton(language_handler.get_text("cost_savings", telegram_id), callback_data="eco_savings")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("eco_section", telegram_id), "explore_eco", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')