from .base import start, main_menu, settings_command, unknown_message
from .car_catalog.car_catalog import view_cars, handle_brand_selected, handle_more_cars
from .settings.settings import settings, change_language, handle_language_change, handle_initial_language_selection, handle_english_selection, handle_khmer_selection
from .support.support import contact_support
from .favorites.favorites import view_favourites, handle_favourite_car, handle_unfavourite_car, handle_favourite_accessory, handle_unfavourite_accessory
from .contact.contact import handle_contact_seller, handle_copy_phone


from .help.help import (
    view_help, help_browse_cars, help_explore, help_search, help_favourites, help_contact, help_settings,
    help_charging_stations, help_garage
)
from .search.search import (
    handle_search_cars, handle_advanced_search, handle_price_search, handle_year_search,
    handle_location_search, handle_brand_search, handle_color_search, handle_category_search,
    handle_price_range_selection, handle_year_range_selection, handle_location_selection,
    handle_brand_selection, handle_color_selection, handle_category_selection,
    handle_clear_filters, apply_search_filters, handle_more_search_results,
    handle_search_type_selection, handle_car_search_filters
)
from .search.charging_station_search import (
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
from .search.garage_search import (
    handle_garage_search_filters,
    handle_garage_location_search,
    handle_garage_service_search,

    handle_garage_location_selection,
    handle_garage_service_selection,

    handle_clear_garage_filters,
    apply_garage_filters,
    handle_more_search_results as handle_garage_more_search_results
)
from .search.accessory_search import (
    handle_accessory_search_filters, handle_accessory_price_search, handle_accessory_location_search,
    handle_accessory_brand_search, handle_accessory_category_search, handle_accessory_location_selection,
    handle_accessory_category_selection, handle_apply_accessory_filters, handle_clear_accessory_filters,
    handle_more_accessory_results
)

# Add these imports to the existing imports from .explore
from .car_info.explore import (
    explore_cars, explore_types, explore_advantages, explore_features, 
    explore_safety, explore_eco,
)
from .car_info.safety import(
        # Safety handler
    handle_safety_maintenance,
    handle_safety_tips, 
    handle_safety_warnings,
    handle_safety_emergency,
    handle_safety_seasonal,
    handle_safety_diy,
)
from .car_info.car_types import (
    handle_type_sports, handle_type_suv, handle_type_sedan, handle_type_hatchback,
    handle_type_truck, handle_type_convertible, handle_type_wagon, handle_type_minivan,
)
from .car_info.benefits import (
    handle_benefits_work, handle_benefits_family, handle_benefits_financial, 
    handle_benefits_social, handle_benefits_comparison, handle_benefits_freedom,
)
from .car_info.features import(
    handle_features_safety, handle_features_tech, handle_features_comfort,
    handle_features_performance, handle_features_electric, handle_features_entertainment,
)
from .car_info.eco import (
    handle_eco_electric,
    handle_eco_hybrid,
    handle_eco_fuel,
    handle_eco_impact,
    handle_eco_savings,
    handle_eco_charging
)
from .charging_station.charging_station import (
    view_charging_stations, view_location_stations, view_station_navigation,
    handle_show_by_location, handle_show_nearby, handle_more_stations, handle_more_location_stations
)
from .garage.garage import (
    view_garages, view_location_garages,
    handle_show_by_location as garage_handle_show_by_location,
    handle_show_nearby as garage_handle_show_nearby,
    handle_more_garages
)
from .accessory.accessory import (
    view_accessories, handle_accessory_type_selection, handle_more_accessories,
    handle_contact_accessory_seller, handle_copy_accessory_phone
)

# Add these to the __all__ list
__all__ = [
    'start',
    'main_menu',
    'settings_command',
    'unknown_message', 
    'view_cars',
    'handle_brand_selected',
    'handle_more_cars',
    'settings',
    'change_language',


    'handle_language_change',
    'handle_english_selection',
    'handle_khmer_selection',
    'handle_initial_language_selection',
    'contact_support',
    'view_favourites',
    'handle_favourite_car',
    'handle_unfavourite_car',
    'handle_favourite_accessory',
    'handle_unfavourite_accessory',
    'handle_contact_seller',
    'view_accessories',
    'handle_accessory_type_selection',
    'handle_more_accessories',
    'handle_contact_accessory_seller',
    'handle_copy_accessory_phone',
    'view_help',
    'help_browse_cars',
    'help_explore',
    'help_search',
    'help_favourites',
    'help_contact',
    'help_settings',
    'help_charging_stations',
    'help_garage',
    'handle_advanced_search',
    'handle_price_search', 
    'handle_year_search',
    'handle_location_search',
    'handle_price_range_selection',
    'handle_year_range_selection',
    'handle_location_selection',
    'handle_clear_filters',
    'apply_search_filters',
    'handle_more_search_results',
    'explore_cars',
    'explore_types', 
    'explore_advantages',
    'explore_features',
    'explore_safety',
    'explore_eco',
    'handle_type_sports', 'handle_type_suv', 'handle_type_sedan', 'handle_type_hatchback',
    'handle_type_truck', 'handle_type_convertible', 'handle_type_wagon', 'handle_type_minivan',
    'handle_safety_maintenance',
    'handle_safety_tips', 
    'handle_safety_warnings',
    'handle_safety_emergency',
    'handle_safety_seasonal',
    'handle_safety_diy',
    'handle_eco_electric',
    'handle_eco_hybrid',
    'handle_eco_fuel',
    'handle_eco_impact',
    'handle_eco_savings',
    'handle_eco_charging',
    'handle_brand_search', 
    'handle_color_search', 'handle_category_search',
    'handle_brand_selection', 'handle_color_selection', 'handle_category_selection',
    'handle_search_type_selection', 'handle_car_search_filters', 'handle_accessory_search_filters',
    'handle_accessory_price_search', 'handle_accessory_location_search', 'handle_accessory_brand_search',
    'handle_accessory_category_search', 'handle_accessory_location_selection', 'handle_accessory_category_selection',
    'handle_apply_accessory_filters', 'handle_clear_accessory_filters', 'handle_more_accessory_results',
    'handle_benefits_work', 'handle_benefits_family', 'handle_benefits_financial',
    'handle_benefits_social', 'handle_benefits_comparison', 'handle_benefits_freedom',
    'handle_features_safety', 'handle_features_tech', 'handle_features_comfort',
    'handle_features_performance', 'handle_features_electric', 'handle_features_entertainment',
    'handle_copy_phone',
    'view_charging_stations',
    'view_location_stations',
    'view_station_navigation',
    'view_garages',
    'view_location_garages',
    # Charging station search functions
    'handle_charging_station_search_filters',
    'handle_charging_price_search',
    'handle_charging_power_search',
    'handle_charging_location_search',
    'handle_charging_connector_search',
    'handle_charging_rating_search',
    'handle_charging_price_range_selection',
    'handle_charging_power_range_selection',
    'handle_charging_location_selection',
    'handle_charging_connector_selection',
    'handle_charging_rating_selection',
    'handle_clear_charging_filters',
    'apply_charging_station_filters',
    'handle_more_charging_results',
    'handle_more_charging_search_results',
    # Garage search functions
    'handle_garage_search_filters',
    'handle_garage_location_search',
    'handle_garage_service_search',

    'handle_garage_location_selection',
    'handle_garage_service_selection',

    'handle_clear_garage_filters',
    'apply_garage_filters',
    'handle_garage_more_search_results'
]