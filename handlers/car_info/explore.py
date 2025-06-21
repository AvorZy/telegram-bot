from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.ui.language import language_handler
from .global_navigation import create_navigation_keyboard

# Main explore menu
async def explore_cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query if update.callback_query else None
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("explore_car_types", telegram_id), callback_data="explore_types"),
         InlineKeyboardButton(language_handler.get_text("explore_benefits", telegram_id), callback_data="explore_advantages")],
        [InlineKeyboardButton(language_handler.get_text("explore_features", telegram_id), callback_data="explore_features"),
         InlineKeyboardButton(language_handler.get_text("explore_safety", telegram_id), callback_data="explore_safety")],
        [InlineKeyboardButton(language_handler.get_text("explore_eco", telegram_id), callback_data="explore_eco")],
        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
    ]
    
    text = language_handler.get_text("explore_welcome", telegram_id)
    
    if query:
        await query.answer()
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Car Types section
async def explore_types(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("sports_cars", telegram_id), callback_data="type_sports"),
         InlineKeyboardButton(language_handler.get_text("suvs_crossovers", telegram_id), callback_data="type_suv")],
        [InlineKeyboardButton(language_handler.get_text("sedans_saloons", telegram_id), callback_data="type_sedan"),
         InlineKeyboardButton(language_handler.get_text("hatchbacks_compacts", telegram_id), callback_data="type_hatchback")],
        [InlineKeyboardButton(language_handler.get_text("trucks_pickups", telegram_id), callback_data="type_truck"),
         InlineKeyboardButton(language_handler.get_text("convertibles", telegram_id), callback_data="type_convertible")],
        [InlineKeyboardButton(language_handler.get_text("wagons_estates", telegram_id), callback_data="type_wagon"),
         InlineKeyboardButton(language_handler.get_text("minivans_mpvs", telegram_id), callback_data="type_minivan")],
        [InlineKeyboardButton(language_handler.get_text("back_to_explorer", telegram_id), callback_data="explore")]
    ]
    
    text = language_handler.get_text("car_types_title", telegram_id)
    
    await query.answer()
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Car Benefits section
async def explore_advantages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("work_career", telegram_id), callback_data="benefits_work"),
         InlineKeyboardButton(language_handler.get_text("family_lifestyle", telegram_id), callback_data="benefits_family")],
        [InlineKeyboardButton(language_handler.get_text("personal_freedom", telegram_id), callback_data="benefits_freedom"),
         InlineKeyboardButton(language_handler.get_text("financial_benefits", telegram_id), callback_data="benefits_financial")],
        [InlineKeyboardButton(language_handler.get_text("social_freedom", telegram_id), callback_data="benefits_social"),
         InlineKeyboardButton(language_handler.get_text("cost_comparison", telegram_id), callback_data="benefits_comparison")],
        [InlineKeyboardButton(language_handler.get_text("back_to_explorer", telegram_id), callback_data="explore")]
    ]
    
    text = language_handler.get_text("benefits_title", telegram_id)
    
    await query.answer()
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')


async def explore_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("safety_features", telegram_id), callback_data="features_safety"),
         InlineKeyboardButton(language_handler.get_text("tech_features", telegram_id), callback_data="features_tech")],
        [InlineKeyboardButton(language_handler.get_text("comfort_features", telegram_id), callback_data="features_comfort"),
         InlineKeyboardButton(language_handler.get_text("performance_features", telegram_id), callback_data="features_performance")],
        [InlineKeyboardButton(language_handler.get_text("electric_features", telegram_id), callback_data="features_electric"),
         InlineKeyboardButton(language_handler.get_text("entertainment_features", telegram_id), callback_data="features_entertainment")],
        [InlineKeyboardButton(language_handler.get_text("back_to_explorer", telegram_id), callback_data="explore")]
    ]
    
    text = language_handler.get_text("features_title", telegram_id)
    
    await query.answer()
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Safety & Maintenance section
async def explore_safety(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("maintenance_schedule", telegram_id), callback_data="safety_maintenance"),
         InlineKeyboardButton(language_handler.get_text("driving_safety_tips", telegram_id), callback_data="safety_tips")],
        [InlineKeyboardButton(language_handler.get_text("warning_signs", telegram_id), callback_data="safety_warnings"),
         InlineKeyboardButton(language_handler.get_text("emergency_preparedness", telegram_id), callback_data="safety_emergency")],
        [InlineKeyboardButton(language_handler.get_text("seasonal_care", telegram_id), callback_data="safety_seasonal"),
         InlineKeyboardButton(language_handler.get_text("diy_checks", telegram_id), callback_data="safety_diy")],
        [InlineKeyboardButton(language_handler.get_text("back_to_explorer", telegram_id), callback_data="explore")]
    ]
    
    text = language_handler.get_text("safety_title", telegram_id)
    
    await query.answer()
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

# Eco-Friendly section
async def explore_eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton(language_handler.get_text("electric_vehicles", telegram_id), callback_data="eco_electric"),
         InlineKeyboardButton(language_handler.get_text("hybrid_technology", telegram_id), callback_data="eco_hybrid")],
        [InlineKeyboardButton(language_handler.get_text("fuel_efficiency", telegram_id), callback_data="eco_fuel"),
         InlineKeyboardButton(language_handler.get_text("environmental_impact", telegram_id), callback_data="eco_impact")],
        [InlineKeyboardButton(language_handler.get_text("cost_savings", telegram_id), callback_data="eco_savings"),
         InlineKeyboardButton(language_handler.get_text("charging_infrastructure", telegram_id), callback_data="eco_charging")],
        [InlineKeyboardButton(language_handler.get_text("back_to_explorer", telegram_id), callback_data="explore")]
    ]
    
    text = language_handler.get_text("eco_title", telegram_id)
    
    await query.answer()
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
