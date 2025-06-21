from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.ui.language import language_handler

async def view_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("help_browse_cars", telegram_id), callback_data="help_browse")],
        [InlineKeyboardButton(language_handler.get_text("help_explore", telegram_id), callback_data="help_explore")],
        [InlineKeyboardButton(language_handler.get_text("help_search", telegram_id), callback_data="help_search")],
        [InlineKeyboardButton(language_handler.get_text("help_charging_stations", telegram_id), callback_data="help_charging_stations")],
        [InlineKeyboardButton(language_handler.get_text("help_garage", telegram_id), callback_data="help_garage")],
        [InlineKeyboardButton(language_handler.get_text("help_favourites", telegram_id), callback_data="help_favourites")],
        [InlineKeyboardButton(language_handler.get_text("help_contact", telegram_id), callback_data="help_contact")],
        [InlineKeyboardButton(language_handler.get_text("help_settings", telegram_id), callback_data="help_settings")],
        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_center", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_browse_cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("try_browsing_now", telegram_id), callback_data="view_cars")],
        [InlineKeyboardButton(language_handler.get_text("back_to_help", telegram_id), callback_data="help")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_browse_cars_content", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_explore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("explore_car", telegram_id), callback_data="explore")],
        [InlineKeyboardButton(language_handler.get_text("back_to_help", telegram_id), callback_data="help")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_explore_content", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("advanced_search", telegram_id), callback_data="advanced_search")],
        [InlineKeyboardButton(language_handler.get_text("back_to_help", telegram_id), callback_data="help")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_search_content", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_favourites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("view_my_favourites", telegram_id), callback_data="view_favourites")],
        [InlineKeyboardButton(language_handler.get_text("back_to_help", telegram_id), callback_data="help")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_favourites_content", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("contact_support", telegram_id), callback_data="contact_support")],
        [InlineKeyboardButton(language_handler.get_text("back_to_help", telegram_id), callback_data="help")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_contact_content", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("open_settings", telegram_id), callback_data="settings")],
        [InlineKeyboardButton(language_handler.get_text("back_to_help", telegram_id), callback_data="help")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_settings_content", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_charging_stations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("charging_stations", telegram_id), callback_data="charging_stations")],
        [InlineKeyboardButton(language_handler.get_text("back_to_help", telegram_id), callback_data="help")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_charging_stations_content", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_garage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("garages", telegram_id), callback_data="garages")],
        [InlineKeyboardButton(language_handler.get_text("back_to_help", telegram_id), callback_data="help")]
    ]
    
    await query.answer()
    # Send NEW message instead of editing
    await query.message.reply_text(
        language_handler.get_text("help_garage_content", telegram_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )