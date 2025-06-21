from telegram import Update
from telegram.ext import ContextTypes
from utils.ui.keyboards import Keyboards
from utils.ui.language import language_handler
from .accessory_search import (
    handle_accessory_search_filters,
    handle_accessory_price_search,
    handle_accessory_location_search,
    handle_accessory_brand_search,
    handle_accessory_price_range_selection,
    handle_accessory_location_selection,
    handle_apply_accessory_filters,
    handle_clear_accessory_filters,
    handle_more_accessory_results
)
from .car_search import (
    handle_car_search_filters,
    handle_price_search,
    handle_year_search,
    handle_location_search,
    handle_price_range_selection,
    handle_year_range_selection,
    handle_location_selection,
    handle_brand_search,
    handle_brand_selection,
    handle_color_search,
    handle_color_selection,
    handle_category_search,
    handle_category_selection,
    handle_clear_filters,
    apply_search_filters,
    handle_more_search_results
)
from .charging_station_search import (
    handle_charging_station_search_filters,
    handle_charging_price_search,
    handle_charging_power_search,
    handle_charging_location_search,
    handle_charging_connector_search,
    handle_charging_price_range_selection,
    handle_charging_power_range_selection,
    handle_charging_location_selection,
    handle_charging_connector_selection,
    handle_clear_charging_filters,
    apply_charging_station_filters,
    handle_more_charging_results,
    handle_more_charging_search_results
)
from .garage_search import (
    handle_garage_search_filters,
    handle_garage_location_search,
    handle_garage_service_search,

    handle_garage_location_selection,
    handle_garage_service_selection,

    handle_clear_garage_filters,
    apply_garage_filters,
    handle_more_search_results as handle_garage_more_search_results
)

# SearchFilters class moved to car_search.py
# AccessorySearchFilters class moved to accessory_search.py

async def handle_search_cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle search cars command - redirect to advanced search"""
    await handle_advanced_search(update, context)

async def handle_advanced_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show search type selection menu"""
    query = update.callback_query
    await query.answer()
    
    # Show search type selection first
    message = language_handler.get_text("search_type_selection", update.effective_user.id)
    keyboard = Keyboards.search_type_selection_menu(update.effective_user.id)
    
    await query.message.reply_text(
        text=message,
        reply_markup=keyboard
    )

# handle_car_search_filters moved to car_search.py

async def handle_search_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle search type selection (car, accessory, charging station, or garage)"""
    query = update.callback_query
    await query.answer()
    
    search_type = query.data.split('_')[-1]  # Extract search type from callback data
    
    if search_type == 'car':
        await handle_car_search_filters(update, context)
    elif search_type == 'accessory':
        await handle_accessory_search_filters(update, context)
    elif search_type == 'charging':
        await handle_charging_station_search_filters(update, context)
    elif search_type == 'garage':
        await handle_garage_search_filters(update, context)

# Accessory search functions moved to accessory_search.py
# Car search functions moved to car_search.py

# handle_price_search, handle_year_search, handle_location_search moved to car_search.py

# handle_price_range_selection moved to car_search.py (car logic) and accessory_search.py (accessory logic)

# handle_year_range_selection moved to car_search.py

# handle_location_selection moved to car_search.py (car logic) and accessory_search.py (accessory logic)

# handle_brand_search moved to car_search.py

# handle_brand_selection moved to car_search.py

# handle_color_search moved to car_search.py

# handle_color_selection moved to car_search.py

# handle_category_search moved to car_search.py

# handle_category_selection moved to car_search.py

# handle_clear_filters moved to car_search.py
    
# apply_search_filters moved to car_search.py

# extract_year_from_model moved to car_search.py
# show_search_results_page moved to car_search.py

# handle_more_search_results moved to car_search.py

# Accessory filter functions moved to accessory_search.py

