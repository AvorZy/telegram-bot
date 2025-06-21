# Keep only these imports at the top:
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from utils.config.settings import validate_required_env_vars
from handlers import (
    start, main_menu, settings_command, unknown_message,
    view_cars, handle_brand_selected, handle_more_cars,
    settings, change_language, handle_language_change, handle_initial_language_selection,
    handle_english_selection, handle_khmer_selection,
    handle_contact_seller, handle_copy_phone,
    contact_support,
    view_favourites, handle_favourite_car, handle_unfavourite_car, handle_favourite_accessory, handle_unfavourite_accessory,
    view_help, help_browse_cars, help_explore, help_search, help_favourites, help_contact, help_settings,
    help_charging_stations, help_garage,
    handle_advanced_search, handle_price_search, handle_year_search, 
    handle_location_search, handle_price_range_selection,
    handle_brand_search, handle_color_search, handle_category_search,
    handle_brand_selection, handle_color_selection, 
    handle_year_range_selection, handle_location_selection,
    handle_clear_filters, apply_search_filters, handle_more_search_results,
    handle_search_type_selection, handle_car_search_filters, handle_accessory_search_filters, handle_accessory_price_search, handle_accessory_location_search,
    handle_accessory_brand_search, handle_accessory_category_search, handle_accessory_location_selection, handle_accessory_category_selection,
    handle_apply_accessory_filters, handle_clear_accessory_filters, handle_more_accessory_results,
    # Charging station search handlers
    handle_charging_station_search_filters, handle_charging_price_search, handle_charging_power_search,
    handle_charging_location_search, handle_charging_connector_search,
    handle_charging_price_range_selection, handle_charging_power_range_selection,
    handle_charging_location_selection, handle_charging_connector_selection,
    handle_clear_charging_filters, apply_charging_station_filters,
    handle_more_charging_results, handle_more_charging_search_results,
    # Garage search handlers
    handle_garage_search_filters, handle_garage_location_search, handle_garage_service_search,
    handle_garage_location_selection, handle_garage_service_selection,
    handle_clear_garage_filters,
    apply_garage_filters, handle_garage_more_search_results,
    explore_cars, explore_types, explore_advantages, explore_features, explore_safety, 
    explore_eco,
    # Car type handlers
    handle_type_sports, handle_type_suv, handle_type_sedan, handle_type_hatchback,
    handle_type_truck, handle_type_convertible, handle_type_wagon, handle_type_minivan,
    # Benefits handlers
    handle_benefits_work, handle_benefits_family, handle_benefits_financial, 
    handle_benefits_social, handle_benefits_comparison, handle_benefits_freedom,
    # Feature handlers
    handle_features_safety, handle_features_tech, handle_features_comfort,
    handle_features_performance, handle_features_electric, handle_features_entertainment,
    handle_safety_maintenance,
    handle_safety_tips,
    handle_safety_warnings, 
    handle_safety_emergency,
    handle_safety_seasonal,
    handle_safety_diy,
    handle_eco_electric,
    handle_eco_hybrid,
    handle_eco_fuel,
    handle_eco_impact,
    handle_eco_savings,
    handle_eco_charging,
    view_charging_stations,
    view_location_stations,
    view_station_navigation,
    handle_show_by_location,
    handle_show_nearby,
    handle_more_stations,
    handle_more_location_stations,
    view_garages,
    view_location_garages,
    garage_handle_show_by_location,
    garage_handle_show_nearby,
    handle_more_garages,
    view_accessories,
    handle_accessory_type_selection,
    handle_more_accessories,
    handle_contact_accessory_seller,
    handle_copy_accessory_phone,
)
from utils.config.settings import TELEGRAM_TOKEN
from models.core.product import initialize_product_data  # Changed from initialize_car_data
from models.core.user import initialize_user_data
from utils.services.data_loader import car_data_loader  # Import directly from utils.services.data_loader



# Add these CallbackQueryHandlers in the main() function
def main():
    # Validate required environment variables
    validate_required_env_vars()
    
    # Initialize car data before starting bot
    print("🚗 Initializing car data from external files...")
    initialize_product_data()  # Changed from initialize_car_data
    
    # Initialize user data
    print("👤 Initializing user data...")
    initialize_user_data()
    
    # Increase timeout values to handle slow connections
    application = Application.builder()\
        .token(TELEGRAM_TOKEN)\
        .connect_timeout(30.0)\
        .read_timeout(30.0)\
        .write_timeout(30.0)\
        .pool_timeout(30.0)\
        .build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("main_menu", main_menu))
    application.add_handler(CommandHandler("settings", settings_command))
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(view_cars, pattern="^view_cars$"))
    application.add_handler(CallbackQueryHandler(view_cars, pattern="^refresh_cars$"))
    
    # Advanced Search handlers - MUST come BEFORE generic brand handler
    application.add_handler(CallbackQueryHandler(handle_advanced_search, pattern="^advanced_search$"))
    application.add_handler(CallbackQueryHandler(handle_search_type_selection, pattern="^search_type_"))
    application.add_handler(CallbackQueryHandler(handle_car_search_filters, pattern="^car_search_filters$"))
    application.add_handler(CallbackQueryHandler(handle_accessory_search_filters, pattern="^accessory_search_filters$"))
    application.add_handler(CallbackQueryHandler(handle_charging_station_search_filters, pattern="^charging_station_search_filters$"))
    application.add_handler(CallbackQueryHandler(handle_garage_search_filters, pattern="^garage_search_filters$"))
    application.add_handler(CallbackQueryHandler(handle_accessory_price_search, pattern="^accessory_search_price$"))
    application.add_handler(CallbackQueryHandler(handle_accessory_location_search, pattern="^accessory_search_location$"))
    application.add_handler(CallbackQueryHandler(handle_accessory_brand_search, pattern="^accessory_search_brand$"))
    application.add_handler(CallbackQueryHandler(handle_accessory_category_search, pattern="^accessory_search_category$"))
    application.add_handler(CallbackQueryHandler(handle_accessory_location_selection, pattern="^accessory_location_"))
    application.add_handler(CallbackQueryHandler(handle_accessory_category_selection, pattern="^accessory_category_"))
    application.add_handler(CallbackQueryHandler(handle_price_search, pattern="^search_price$"))
    application.add_handler(CallbackQueryHandler(handle_year_search, pattern="^search_year$"))
    application.add_handler(CallbackQueryHandler(handle_location_search, pattern="^search_location$"))
    application.add_handler(CallbackQueryHandler(handle_price_range_selection, pattern=r"^price_\d+_\d+$"))
    application.add_handler(CallbackQueryHandler(handle_year_range_selection, pattern=r"^year_\d+_\d+$"))
    application.add_handler(CallbackQueryHandler(handle_location_selection, pattern="^location_"))
    application.add_handler(CallbackQueryHandler(handle_clear_filters, pattern="^clear_filters$"))
    application.add_handler(CallbackQueryHandler(apply_search_filters, pattern="^apply_filters$"))
    application.add_handler(CallbackQueryHandler(handle_apply_accessory_filters, pattern="^apply_accessory_filters$"))
    application.add_handler(CallbackQueryHandler(handle_clear_accessory_filters, pattern="^clear_accessory_filters$"))
    application.add_handler(CallbackQueryHandler(handle_more_search_results, pattern="^more_search_results_"))
    application.add_handler(CallbackQueryHandler(handle_more_accessory_results, pattern="^more_accessory_results_"))
    
    # Charging Station Search handlers
    application.add_handler(CallbackQueryHandler(handle_charging_price_search, pattern="^charging_station_price_search$"))
    application.add_handler(CallbackQueryHandler(handle_charging_power_search, pattern="^charging_station_power_search$"))
    application.add_handler(CallbackQueryHandler(handle_charging_location_search, pattern="^charging_station_location_search$"))

    application.add_handler(CallbackQueryHandler(handle_charging_connector_search, pattern="^charging_station_connector_search$"))
    application.add_handler(CallbackQueryHandler(handle_charging_price_range_selection, pattern="^charging_station_price_"))
    application.add_handler(CallbackQueryHandler(handle_charging_power_range_selection, pattern="^charging_station_power_"))
    application.add_handler(CallbackQueryHandler(handle_charging_location_selection, pattern="^charging_search_location_"))

    application.add_handler(CallbackQueryHandler(handle_charging_connector_selection, pattern="^charging_station_connector_"))
    application.add_handler(CallbackQueryHandler(handle_clear_charging_filters, pattern="^clear_charging_station_filters$"))
    application.add_handler(CallbackQueryHandler(apply_charging_station_filters, pattern="^apply_charging_station_filters$"))
    application.add_handler(CallbackQueryHandler(handle_more_charging_results, pattern="^charging_station_results_"))
    application.add_handler(CallbackQueryHandler(handle_more_charging_search_results, pattern="^more_charging_search_results_"))
    
    # Garage Search handlers
    application.add_handler(CallbackQueryHandler(handle_garage_location_search, pattern="^garage_location_search$"))
    application.add_handler(CallbackQueryHandler(handle_garage_service_search, pattern="^garage_service_search$"))

    application.add_handler(CallbackQueryHandler(handle_garage_location_selection, pattern="^search_garage_location_"))
    application.add_handler(CallbackQueryHandler(handle_garage_service_selection, pattern="^garage_service_"))

    application.add_handler(CallbackQueryHandler(handle_clear_garage_filters, pattern="^clear_garage_filters$"))
    application.add_handler(CallbackQueryHandler(apply_garage_filters, pattern="^apply_garage_filters$"))
    application.add_handler(CallbackQueryHandler(handle_garage_more_search_results, pattern="^more_garage_search_results_"))
    
    application.add_handler(CallbackQueryHandler(handle_brand_search, pattern="^search_brand$"))
    application.add_handler(CallbackQueryHandler(handle_color_search, pattern="^search_color$"))
    application.add_handler(CallbackQueryHandler(handle_category_search, pattern="^search_category$"))
    # Specific search patterns MUST come before generic patterns
    application.add_handler(CallbackQueryHandler(handle_brand_selection, pattern="^brand_search_"))
    application.add_handler(CallbackQueryHandler(handle_color_selection, pattern="^color_search_"))
    
    # Generic brand handler - MUST come AFTER specific search handlers
    application.add_handler(CallbackQueryHandler(handle_brand_selected, pattern="^brand_"))
    
    # Gallery functionality removed for cleaner interface

    # Settings handlers
    application.add_handler(CallbackQueryHandler(settings, pattern="^settings$"))
    application.add_handler(CallbackQueryHandler(change_language, pattern="^change_language$"))
    application.add_handler(CallbackQueryHandler(handle_initial_language_selection, pattern="^initial_lang_"))
    application.add_handler(CallbackQueryHandler(handle_language_change, pattern="^lang_"))


    
    # IMPORTANT: Support handler MUST come BEFORE contact seller handler
    application.add_handler(CallbackQueryHandler(contact_support, pattern="^contact_support$"))
    
        # Contact seller handler - only match contact_ followed by digits (car IDs)
    application.add_handler(CallbackQueryHandler(handle_contact_seller, pattern=r"^contact_\d+$"))

    # Copy phone handler
    application.add_handler(CallbackQueryHandler(handle_copy_phone, pattern=r"^copy_phone_\d+$"))
        
    # Favourites handlers
    application.add_handler(CallbackQueryHandler(view_favourites, pattern="^view_favourites$"))
    application.add_handler(CallbackQueryHandler(handle_favourite_car, pattern="^favourite_[0-9]+$"))
    application.add_handler(CallbackQueryHandler(handle_unfavourite_car, pattern="^unfavourite_[0-9]+$"))
    

    
    # Help handlers
    application.add_handler(CallbackQueryHandler(view_help, pattern="^view_help$"))
    application.add_handler(CallbackQueryHandler(view_help, pattern="^help$"))
    application.add_handler(CallbackQueryHandler(help_browse_cars, pattern="^help_browse$"))
    application.add_handler(CallbackQueryHandler(help_explore, pattern="^help_explore$"))
    application.add_handler(CallbackQueryHandler(help_search, pattern="^help_search$"))
    application.add_handler(CallbackQueryHandler(help_charging_stations, pattern="^help_charging_stations$"))
    application.add_handler(CallbackQueryHandler(help_garage, pattern="^help_garage$"))
    application.add_handler(CallbackQueryHandler(help_favourites, pattern="^help_favourites$"))
    application.add_handler(CallbackQueryHandler(help_contact, pattern="^help_contact$"))
    application.add_handler(CallbackQueryHandler(help_settings, pattern="^help_settings$"))
    
    # Commands handlers

    
    # Explore handlers - Add these HERE (before run_polling)
    # Make sure these imports are present:

    
    # And these callback handlers should be registered:
    # Explore handlers
    application.add_handler(CallbackQueryHandler(explore_cars, pattern="^explore_cars$"))
    application.add_handler(CallbackQueryHandler(explore_cars, pattern="^explore$"))
    application.add_handler(CallbackQueryHandler(explore_types, pattern="^explore_types$"))
    application.add_handler(CallbackQueryHandler(explore_advantages, pattern="^explore_advantages$"))
    application.add_handler(CallbackQueryHandler(explore_features, pattern="^explore_features$"))
    application.add_handler(CallbackQueryHandler(explore_safety, pattern="^explore_safety$"))
    application.add_handler(CallbackQueryHandler(explore_eco, pattern="^explore_eco$"))

    
    # Car type handlers - ADD THESE
    application.add_handler(CallbackQueryHandler(handle_type_sports, pattern="^type_sports$"))
    application.add_handler(CallbackQueryHandler(handle_type_suv, pattern="^type_suv$"))
    application.add_handler(CallbackQueryHandler(handle_type_sedan, pattern="^type_sedan$"))
    application.add_handler(CallbackQueryHandler(handle_type_hatchback, pattern="^type_hatchback$"))
    application.add_handler(CallbackQueryHandler(handle_type_truck, pattern="^type_truck$"))
    application.add_handler(CallbackQueryHandler(handle_type_convertible, pattern="^type_convertible$"))
    application.add_handler(CallbackQueryHandler(handle_type_wagon, pattern="^type_wagon$"))
    application.add_handler(CallbackQueryHandler(handle_type_minivan, pattern="^type_minivan$"))
    
    # Benefits handlers - ADD THESE
    application.add_handler(CallbackQueryHandler(handle_benefits_work, pattern="^benefits_work$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_family, pattern="^benefits_family$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_financial, pattern="^benefits_financial$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_social, pattern="^benefits_social$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_comparison, pattern="^benefits_comparison$"))
    application.add_handler(CallbackQueryHandler(handle_benefits_freedom, pattern="^benefits_freedom$"))
    
    
    # Feature handlers
    application.add_handler(CallbackQueryHandler(handle_features_safety, pattern="^features_safety$"))
    application.add_handler(CallbackQueryHandler(handle_features_tech, pattern="^features_tech$"))
    application.add_handler(CallbackQueryHandler(handle_features_comfort, pattern="^features_comfort$"))
    application.add_handler(CallbackQueryHandler(handle_features_performance, pattern="^features_performance$"))
    application.add_handler(CallbackQueryHandler(handle_features_electric, pattern="^features_electric$"))
    application.add_handler(CallbackQueryHandler(handle_features_entertainment, pattern="^features_entertainment$"))


    # Safety handlers
    application.add_handler(CallbackQueryHandler(handle_safety_maintenance, pattern="^safety_maintenance$"))
    application.add_handler(CallbackQueryHandler(handle_safety_tips, pattern="^safety_tips$"))
    application.add_handler(CallbackQueryHandler(handle_safety_warnings, pattern="^safety_warnings$"))
    application.add_handler(CallbackQueryHandler(handle_safety_emergency, pattern="^safety_emergency$"))
    application.add_handler(CallbackQueryHandler(handle_safety_seasonal, pattern="^safety_seasonal$"))
    application.add_handler(CallbackQueryHandler(handle_safety_diy, pattern="^safety_diy$"))
    
    # Eco handlers
    application.add_handler(CallbackQueryHandler(handle_eco_electric, pattern="^eco_electric$"))
    application.add_handler(CallbackQueryHandler(handle_eco_hybrid, pattern="^eco_hybrid$"))
    application.add_handler(CallbackQueryHandler(handle_eco_fuel, pattern="^eco_fuel$"))
    application.add_handler(CallbackQueryHandler(handle_eco_impact, pattern="^eco_impact$"))
    application.add_handler(CallbackQueryHandler(handle_eco_savings, pattern="^eco_savings$"))
    application.add_handler(CallbackQueryHandler(handle_eco_charging, pattern="^eco_charging$"))
    
    # Charging Station handlers
    application.add_handler(CallbackQueryHandler(view_charging_stations, pattern="^view_charging_stations$"))
    application.add_handler(CallbackQueryHandler(view_charging_stations, pattern="^charging_stations$"))
    application.add_handler(CallbackQueryHandler(view_location_stations, pattern="^charging_location_"))
    application.add_handler(CallbackQueryHandler(view_station_navigation, pattern=r"^station_\d+"))
    application.add_handler(CallbackQueryHandler(handle_show_by_location, pattern="^charging_show_by_location$"))
    application.add_handler(CallbackQueryHandler(handle_show_nearby, pattern="^charging_show_nearby$"))
    application.add_handler(CallbackQueryHandler(handle_more_stations, pattern="^more_stations_"))
    application.add_handler(CallbackQueryHandler(handle_more_location_stations, pattern="^more_location_stations_"))
    
    # Garage handlers
    application.add_handler(CallbackQueryHandler(view_garages, pattern="^view_garages$"))
    application.add_handler(CallbackQueryHandler(view_garages, pattern="^garages$"))
    application.add_handler(CallbackQueryHandler(view_location_garages, pattern="^garage_location_"))
    application.add_handler(CallbackQueryHandler(garage_handle_show_by_location, pattern="^garage_show_by_location$"))
    application.add_handler(CallbackQueryHandler(garage_handle_show_nearby, pattern="^garage_show_nearby$"))
    application.add_handler(CallbackQueryHandler(handle_more_garages, pattern="^more_garages_"))
    
    # Accessory handlers
    application.add_handler(CallbackQueryHandler(view_accessories, pattern="^view_accessories$"))
    application.add_handler(CallbackQueryHandler(handle_accessory_type_selection, pattern="^accessory_type_"))
    application.add_handler(CallbackQueryHandler(handle_more_accessories, pattern="^more_accessories_"))
    application.add_handler(CallbackQueryHandler(handle_contact_accessory_seller, pattern="^contact_accessory_"))
    application.add_handler(CallbackQueryHandler(handle_copy_accessory_phone, pattern="^copy_accessory_phone_"))
    # Accessory favorites handler
    application.add_handler(CallbackQueryHandler(handle_favourite_accessory, pattern="^favourite_accessory_"))
    application.add_handler(CallbackQueryHandler(handle_unfavourite_accessory, pattern="^unfavourite_accessory_"))
    
    # Accessory handlers
    application.add_handler(CallbackQueryHandler(view_accessories, pattern="^view_accessories$"))
    application.add_handler(CallbackQueryHandler(handle_more_accessories, pattern="^more_accessories_"))
    application.add_handler(CallbackQueryHandler(handle_contact_accessory_seller, pattern="^contact_accessory_"))
    application.add_handler(CallbackQueryHandler(handle_favourite_accessory, pattern="^favourite_accessory_"))
    application.add_handler(CallbackQueryHandler(handle_unfavourite_accessory, pattern="^unfavourite_accessory_"))

    # More cars handler
    application.add_handler(CallbackQueryHandler(handle_more_cars, pattern=r"^more_cars_"))
    
    # Generic handlers (these should be at the end)
    application.add_handler(CallbackQueryHandler(start, pattern="^back_to_main$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))
    

    
    
    print("🤖 Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    # Clear all user cache on startup for fresh language detection
    from handlers.base import clear_user_cache
    clear_user_cache()
    
    main()



