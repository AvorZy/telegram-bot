from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes
from .global_navigation import create_navigation_keyboard
from utils.ui.language import language_handler

async def handle_type_sports(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("type_sports_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("suvs_crossovers", telegram_id), callback_data="type_suv"),
         InlineKeyboardButton(language_handler.get_text("sedans_saloons", telegram_id), callback_data="type_sedan")],
        [InlineKeyboardButton(language_handler.get_text("convertibles", telegram_id), callback_data="type_convertible"),
         InlineKeyboardButton(language_handler.get_text("trucks_pickups", telegram_id), callback_data="type_truck")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("car_types_section", telegram_id), "explore_types", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_type_suv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("type_suv_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("sports_cars", telegram_id), callback_data="type_sports"),
         InlineKeyboardButton(language_handler.get_text("sedans_saloons", telegram_id), callback_data="type_sedan")],
        [InlineKeyboardButton(language_handler.get_text("trucks_pickups", telegram_id), callback_data="type_truck"),
         InlineKeyboardButton(language_handler.get_text("minivans_mpvs", telegram_id), callback_data="type_minivan")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("car_types_section", telegram_id), "explore_types", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_type_sedan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    text = language_handler.get_text("type_sedan_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("sports_cars", telegram_id), callback_data="type_sports"),
         InlineKeyboardButton(language_handler.get_text("suvs_crossovers", telegram_id), callback_data="type_suv")],
        [InlineKeyboardButton(language_handler.get_text("hatchbacks_compacts", telegram_id), callback_data="type_hatchback"),
         InlineKeyboardButton(language_handler.get_text("wagons_estates", telegram_id), callback_data="type_wagon")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("car_types_section", telegram_id), "explore_types", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_type_hatchback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("type_hatchback_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("sedans_saloons", telegram_id), callback_data="type_sedan"),
         InlineKeyboardButton(language_handler.get_text("wagons_estates", telegram_id), callback_data="type_wagon")],
        [InlineKeyboardButton(language_handler.get_text("convertibles", telegram_id), callback_data="type_convertible"),
         InlineKeyboardButton(language_handler.get_text("minivans_mpvs", telegram_id), callback_data="type_minivan")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("car_types_section", telegram_id), "explore_types", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_type_truck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("type_truck_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("suvs_crossovers", telegram_id), callback_data="type_suv"),
         InlineKeyboardButton(language_handler.get_text("wagons_estates", telegram_id), callback_data="type_wagon")],
        [InlineKeyboardButton(language_handler.get_text("sports_cars", telegram_id), callback_data="type_sports"),
         InlineKeyboardButton(language_handler.get_text("minivans_mpvs", telegram_id), callback_data="type_minivan")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("car_types_section", telegram_id), "explore_types", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_type_convertible(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("type_convertible_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("sports_cars", telegram_id), callback_data="type_sports"),
         InlineKeyboardButton(language_handler.get_text("sedans_saloons", telegram_id), callback_data="type_sedan")],
        [InlineKeyboardButton(language_handler.get_text("hatchbacks_compacts", telegram_id), callback_data="type_hatchback"),
         InlineKeyboardButton(language_handler.get_text("wagons_estates", telegram_id), callback_data="type_wagon")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("car_types_section", telegram_id), "explore_types", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_type_wagon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("type_wagon_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("sedans_saloons", telegram_id), callback_data="type_sedan"),
         InlineKeyboardButton(language_handler.get_text("suvs_crossovers", telegram_id), callback_data="type_suv")],
        [InlineKeyboardButton(language_handler.get_text("hatchbacks_compacts", telegram_id), callback_data="type_hatchback"),
         InlineKeyboardButton(language_handler.get_text("minivans_mpvs", telegram_id), callback_data="type_minivan")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("car_types_section", telegram_id), "explore_types", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')

async def handle_type_minivan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    await query.answer()
    
    text = language_handler.get_text("type_minivan_content", telegram_id)
    
    related_buttons = [
        [InlineKeyboardButton(language_handler.get_text("suvs_crossovers", telegram_id), callback_data="type_suv"),
         InlineKeyboardButton(language_handler.get_text("wagons_estates", telegram_id), callback_data="type_wagon")],
        [InlineKeyboardButton(language_handler.get_text("trucks_pickups", telegram_id), callback_data="type_truck"),
         InlineKeyboardButton(language_handler.get_text("sedans_saloons", telegram_id), callback_data="type_sedan")]
    ]
    
    keyboard = create_navigation_keyboard(telegram_id, language_handler.get_text("car_types_section", telegram_id), "explore_types", related_buttons)
    await query.message.reply_text(text, reply_markup=keyboard, parse_mode='Markdown')
