import random
from pydantic import BaseModel
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from models.core.product import Product  # Changed from Car
from utils.ui.language import language_handler
from utils.services.data_loader import car_data_loader
from utils.services.charging_station_service import ChargingStationService
from utils.services.accessory_service import AccessoryService

class Keyboards:
    # Class variable to track the current page/offset
    _current_offset = 0
    
    @staticmethod
    def create_back_to_menu_button(telegram_id: int) -> InlineKeyboardButton:
        """Create a standardized back to menu button"""
        return InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id), 
            callback_data="back_to_main"
        )
    
    @staticmethod
    def create_navigation_row(telegram_id: int, back_callback: str = None, include_menu: bool = True) -> List[InlineKeyboardButton]:
        """Create a standardized navigation row with optional back button and menu button"""
        row = []
        if back_callback:
            row.append(InlineKeyboardButton(
                language_handler.get_text("back_to_search_type", telegram_id), 
                callback_data=back_callback
            ))
        if include_menu:
            row.append(Keyboards.create_back_to_menu_button(telegram_id))
        return row
    
    @staticmethod
    def main_menu(telegram_id: int) -> InlineKeyboardMarkup:
        """Create main menu keyboard"""
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("view_cars", telegram_id), callback_data="view_cars"),
             InlineKeyboardButton(language_handler.get_text("search_filter", telegram_id), callback_data="advanced_search")],
            [InlineKeyboardButton(language_handler.get_text("view_accessories", telegram_id), callback_data="view_accessories"),
             InlineKeyboardButton(language_handler.get_text("view_charging_stations", telegram_id), callback_data="view_charging_stations")],
            [InlineKeyboardButton(language_handler.get_text("view_garages", telegram_id), callback_data="view_garages"),
             InlineKeyboardButton(language_handler.get_text("explore_cars", telegram_id), callback_data="explore_cars")],
            [InlineKeyboardButton(language_handler.get_text("view_favourites", telegram_id), callback_data="view_favourites"),
             InlineKeyboardButton(language_handler.get_text("view_help", telegram_id), callback_data="view_help")],
            [InlineKeyboardButton(language_handler.get_text("contact_support", telegram_id), callback_data="contact_support"),
             InlineKeyboardButton(language_handler.get_text("settings", telegram_id), callback_data="settings")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def settings_menu(telegram_id: int) -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("change_language", telegram_id), callback_data="change_language")],
            [InlineKeyboardButton(language_handler.get_text("location_settings", telegram_id), callback_data="location_settings")],
            [Keyboards.create_back_to_menu_button(telegram_id)]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def language_selection(telegram_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
             InlineKeyboardButton("🇰🇭 ខ្មែរ", callback_data="lang_kh")],
            [InlineKeyboardButton(language_handler.get_text("back_to_settings", telegram_id), callback_data="settings")]
        ])


    
    @staticmethod
    def car_brands(available_cars: List[Product], telegram_id: int, is_refreshed: bool = False) -> InlineKeyboardMarkup:
        # This function has the actual car brand logos like 🚗 AC (7), 🚗 ACURA (59)
        # AND it has the Refresh and Back buttons at the bottom
        brands = sorted(list(set(car.brand for car in available_cars)))
        keyboard = []
        
        max_brands = 50  # Changed from 30 to 50 brands
        
        if is_refreshed:
            # When refreshed, move to next set of 50 brands
            Keyboards._current_offset += max_brands
            # If we've reached the end, start from a random position
            if Keyboards._current_offset >= len(brands):
                Keyboards._current_offset = random.randint(0, max(0, len(brands) - max_brands))
        else:
            # Reset offset for initial view
            Keyboards._current_offset = 0
            
        # Get the slice of brands to display
        end_index = min(Keyboards._current_offset + max_brands, len(brands))
        limited_brands = brands[Keyboards._current_offset:end_index]
        
        # If we don't have enough brands from current offset, wrap around
        if len(limited_brands) < max_brands and len(brands) > max_brands:
            remaining_needed = max_brands - len(limited_brands)
            limited_brands.extend(brands[:remaining_needed])
        
        # Display brands in 3 columns
        for i in range(0, len(limited_brands), 3):
            row = []
            for j in range(3):
                if i + j < len(limited_brands):
                    brand = limited_brands[i + j]
                    brand_count = len([car for car in available_cars if car.brand == brand])
                    brand_display = f"🚗 {brand} ({brand_count})"
                    
                    row.append(InlineKeyboardButton(
                        brand_display,
                        callback_data=f"brand_{brand}"
                    ))
            keyboard.append(row)
        
        # Always add refresh and back buttons at the end (with proper translation)
        keyboard.append([InlineKeyboardButton(language_handler.get_text("refresh", telegram_id), callback_data="refresh_cars")])
        keyboard.append([InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def initial_language_selection() -> InlineKeyboardMarkup:
        """Initial language selection for first-time users"""
        keyboard = [
            [InlineKeyboardButton("🇺🇸 English", callback_data="initial_lang_en"),
             InlineKeyboardButton("🇰🇭 ខ្មែរ (Khmer)", callback_data="initial_lang_kh")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def search_type_selection_menu(telegram_id: int) -> InlineKeyboardMarkup:
        """Menu to select between car, accessory, charging station, and garage search"""
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("search_cars", telegram_id), callback_data="search_type_car")],
            [InlineKeyboardButton(language_handler.get_text("search_accessories", telegram_id), callback_data="search_type_accessory")],
            [InlineKeyboardButton(language_handler.get_text("search_charging_stations", telegram_id), callback_data="search_type_charging")],
            [InlineKeyboardButton(language_handler.get_text("search_garages", telegram_id), callback_data="search_type_garage")],
            [Keyboards.create_back_to_menu_button(telegram_id)]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def car_search_menu(telegram_id: int) -> InlineKeyboardMarkup:
        """Car-specific search filters menu"""
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("search_by_price", telegram_id), callback_data="search_price"),
             InlineKeyboardButton(language_handler.get_text("search_by_year", telegram_id), callback_data="search_year")],
            [InlineKeyboardButton(language_handler.get_text("search_by_location", telegram_id), callback_data="search_location"),
             InlineKeyboardButton(language_handler.get_text("search_by_brand", telegram_id), callback_data="search_brand")],
            [InlineKeyboardButton(language_handler.get_text("search_by_color", telegram_id), callback_data="search_color"),
             InlineKeyboardButton(language_handler.get_text("search_by_category", telegram_id), callback_data="search_category")],
            [InlineKeyboardButton(language_handler.get_text("apply_filters", telegram_id), callback_data="apply_filters"),
             InlineKeyboardButton(language_handler.get_text("clear_filters", telegram_id), callback_data="clear_filters")],
            Keyboards.create_navigation_row(telegram_id, "advanced_search")
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def accessory_search_menu(telegram_id: int) -> InlineKeyboardMarkup:
        """Accessory-specific search filters menu - price, location, and category"""
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("search_by_price", telegram_id), callback_data="accessory_search_price"),
             InlineKeyboardButton(language_handler.get_text("search_by_location", telegram_id), callback_data="accessory_search_location")],
            [InlineKeyboardButton(language_handler.get_text("search_by_category", telegram_id), callback_data="accessory_search_category"),
             InlineKeyboardButton(language_handler.get_text("apply_filters", telegram_id), callback_data="apply_accessory_filters")],
            [InlineKeyboardButton(language_handler.get_text("clear_filters", telegram_id), callback_data="clear_accessory_filters")],
            Keyboards.create_navigation_row(telegram_id, "advanced_search")
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def advanced_search_menu(telegram_id: int) -> InlineKeyboardMarkup:
        """Legacy method - now redirects to search type selection"""
        return Keyboards.search_type_selection_menu(telegram_id)

    @staticmethod
    def price_range_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("$0 - $10,000", callback_data="price_0_10000"),
             InlineKeyboardButton("$10,000 - $25,000", callback_data="price_10000_25000")],
            [InlineKeyboardButton("$25,000 - $50,000", callback_data="price_25000_50000"),
             InlineKeyboardButton("$50,000 - $100,000", callback_data="price_50000_100000")],
            [InlineKeyboardButton("$100,000+", callback_data="price_100000_999999")],
            [InlineKeyboardButton(language_handler.get_text("back_to_search", telegram_id), callback_data="advanced_search")]
        ])

    @staticmethod
    def year_range_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("2020-2024", callback_data="year_2020_2024"),
             InlineKeyboardButton("2015-2019", callback_data="year_2015_2019")],
            [InlineKeyboardButton("2010-2014", callback_data="year_2010_2014"),
             InlineKeyboardButton("2005-2009", callback_data="year_2005_2009")],
            [InlineKeyboardButton("Before 2005", callback_data="year_1990_2004")],
            [InlineKeyboardButton(language_handler.get_text("back_to_search", telegram_id), callback_data="advanced_search")]
        ])

    @staticmethod
    def location_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        # Get unique locations from API data
        locations = car_data_loader.get_unique_locations()
        
        # Create buttons for locations (2 per row)
        location_buttons = []
        for i in range(0, len(locations), 2):
            row = []
            # First location in the row
            location1 = locations[i]
            callback_data1 = f"location_{location1.replace(' ', '_')}"
            row.append(InlineKeyboardButton(f"📍 {location1}", callback_data=callback_data1))
            
            # Second location in the row (if exists)
            if i + 1 < len(locations):
                location2 = locations[i + 1]
                callback_data2 = f"location_{location2.replace(' ', '_')}"
                row.append(InlineKeyboardButton(f"📍 {location2}", callback_data=callback_data2))
            
            location_buttons.append(row)
        
        # Add back button
        location_buttons.append([
            InlineKeyboardButton(language_handler.get_text("back_to_search", telegram_id), callback_data="advanced_search")
        ])
        
        return InlineKeyboardMarkup(location_buttons)

    @staticmethod
    async def charging_location_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        """Create location selection keyboard for charging station search"""
        # Get unique locations from charging station API data
        charging_service = ChargingStationService()
        locations = await charging_service.get_unique_locations()
        
        # Create buttons for locations (2 per row)
        location_buttons = []
        for i in range(0, len(locations), 2):
            row = []
            # First location in the row
            location1 = locations[i]
            callback_data1 = f"charging_search_location_{location1.replace(' ', '_')}"
            row.append(InlineKeyboardButton(f"📍 {location1}", callback_data=callback_data1))
            
            # Second location in the row (if exists)
            if i + 1 < len(locations):
                location2 = locations[i + 1]
                callback_data2 = f"charging_search_location_{location2.replace(' ', '_')}"
                row.append(InlineKeyboardButton(f"📍 {location2}", callback_data=callback_data2))
            
            location_buttons.append(row)
        
        # Add back button
        location_buttons.append([
            InlineKeyboardButton(language_handler.get_text("back", telegram_id), callback_data="charging_station_search_filters")
        ])
        
        return InlineKeyboardMarkup(location_buttons)

    @staticmethod
    def brand_selection_keyboard(telegram_id: int, language_handler, brands: list, brand_emojis: dict = None) -> InlineKeyboardMarkup:
        """Create brand selection keyboard for search"""
        keyboard = []
        
        if brand_emojis is None:
            brand_emojis = {}
        
        # Add brand buttons in pairs
        for i in range(0, len(brands), 2):
            row = []
            # First brand in the row
            brand1 = brands[i]
            emoji1 = brand_emojis.get(brand1, '🚗')
            row.append(InlineKeyboardButton(
                f"{emoji1} {brand1}", 
                callback_data=f"brand_search_{brand1}"
            ))
            
            # Second brand in the row (if exists)
            if i + 1 < len(brands):
                brand2 = brands[i + 1]
                emoji2 = brand_emojis.get(brand2, '🚗')
                row.append(InlineKeyboardButton(
                    f"{emoji2} {brand2}", 
                    callback_data=f"brand_search_{brand2}"
                ))
            
            keyboard.append(row)
        
        # Add "Any Brand" option
        keyboard.append([InlineKeyboardButton(
            language_handler.get_text('any_brand', telegram_id),
            callback_data="brand_search_any"
        )])
        
        # Add back button
        keyboard.append([InlineKeyboardButton(
            language_handler.get_text('back_to_search', telegram_id),
            callback_data="advanced_search"
        )])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def color_selection_keyboard(telegram_id: int, language_handler, colors: list = None, color_emojis: dict = None) -> InlineKeyboardMarkup:
        """Create color selection keyboard for search"""
        if colors is None:
            colors = ['Red', 'Blue', 'Black', 'White', 'Silver', 'Gray', 'Green', 'Yellow']
        
        if color_emojis is None:
            color_emojis = {
                'Red': '🔴', 'Blue': '🔵', 'Black': '⚫', 'White': '⚪',
                'Silver': '⚪', 'Gray': '🔘', 'Green': '🟢', 'Yellow': '🟡'
            }
        
        keyboard = []
        # Add colors in pairs
        for i in range(0, len(colors), 2):
            row = []
            # First color in the row
            color1 = colors[i]
            emoji1 = color_emojis.get(color1, '🎨')
            # Try to get translation, fallback to color name
            color1_text = language_handler.get_text(color1.lower(), telegram_id) or color1
            # Check if color already contains emoji to avoid duplicates
            if any(ord(char) > 127 for char in color1_text):
                # Color text already has emoji, don't add another
                display_text = color1_text
            else:
                # Add emoji to plain text
                display_text = f"{emoji1} {color1_text}"
            row.append(InlineKeyboardButton(
                display_text,
                callback_data=f"color_search_{color1}"
            ))
            
            # Second color in the row (if exists)
            if i + 1 < len(colors):
                color2 = colors[i + 1]
                emoji2 = color_emojis.get(color2, '🎨')
                color2_text = language_handler.get_text(color2.lower(), telegram_id) or color2
                # Check if color already contains emoji to avoid duplicates
                if any(ord(char) > 127 for char in color2_text):
                    # Color text already has emoji, don't add another
                    display_text2 = color2_text
                else:
                    # Add emoji to plain text
                    display_text2 = f"{emoji2} {color2_text}"
                row.append(InlineKeyboardButton(
                    display_text2,
                    callback_data=f"color_search_{color2}"
                ))
            
            keyboard.append(row)
        
        # Add "Any Color" option
        keyboard.append([InlineKeyboardButton(
            language_handler.get_text('any_color', telegram_id),
            callback_data="color_search_any"
        )])
        
        # Add back button
        keyboard.append([InlineKeyboardButton(
            language_handler.get_text('back_to_search', telegram_id),
            callback_data="advanced_search"
        )])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def category_selection_keyboard(telegram_id: int, language_handler, categories: list = None, category_emojis: dict = None) -> InlineKeyboardMarkup:
        """Create category selection keyboard for search"""
        if categories is None:
            categories = ['Electric Vehicles', 'Sedan', 'SUV', 'Hatchback', 'Truck', 'Convertible']
        
        if category_emojis is None:
            category_emojis = {
                'Electric Vehicles': '⚡', 'Sedan': '🚗', 'SUV': '🚙',
                'Hatchback': '🚘', 'Truck': '🚚', 'Convertible': '🏎️'
            }
        
        keyboard = []
        # Add categories in pairs
        for i in range(0, len(categories), 2):
            row = []
            # First category in the row
            category1 = categories[i]
            emoji1 = category_emojis.get(category1, '🚗')
            # Try to get translation, fallback to category name
            category1_key = category1.lower().replace(' ', '_')
            category1_text = language_handler.get_text(category1_key, telegram_id) or category1
            # Check if category already contains emoji to avoid duplicates
            if any(ord(char) > 127 for char in category1_text):
                # Category text already has emoji, don't add another
                display_text = category1_text
            else:
                # Add emoji to plain text
                display_text = f"{emoji1} {category1_text}"
            row.append(InlineKeyboardButton(
                display_text,
                callback_data=f"category_search_{category1.replace(' ', '_')}"
            ))
            
            # Second category in the row (if exists)
            if i + 1 < len(categories):
                category2 = categories[i + 1]
                emoji2 = category_emojis.get(category2, '🚗')
                category2_key = category2.lower().replace(' ', '_')
                category2_text = language_handler.get_text(category2_key, telegram_id) or category2
                # Check if category already contains emoji to avoid duplicates
                if any(ord(char) > 127 for char in category2_text):
                    # Category text already has emoji, don't add another
                    display_text2 = category2_text
                else:
                    # Add emoji to plain text
                    display_text2 = f"{emoji2} {category2_text}"
                row.append(InlineKeyboardButton(
                    display_text2,
                    callback_data=f"category_search_{category2.replace(' ', '_')}"
                ))
            
            keyboard.append(row)
        
        # Add "Any Category" option
        keyboard.append([InlineKeyboardButton(
            language_handler.get_text('any_category', telegram_id),
            callback_data="category_search_any"
        )])
        
        # Add back button
        keyboard.append([InlineKeyboardButton(
            language_handler.get_text('back_to_search', telegram_id),
            callback_data="advanced_search"
        )])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_no_cars_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(language_handler.get_text("refresh", telegram_id), callback_data="view_cars")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
        ])

    @staticmethod
    def accessory_type_selection_keyboard(telegram_id: int, accessory_types: List[str]) -> InlineKeyboardMarkup:
        """Create keyboard for accessory type selection"""
        keyboard = []
        
        # Create rows with 2 buttons each
        for i in range(0, len(accessory_types), 2):
            row = []
            for j in range(2):
                if i + j < len(accessory_types):
                    accessory_type = accessory_types[i + j]
                    row.append(InlineKeyboardButton(
                        accessory_type,
                        callback_data=f"search_accessory_type_{accessory_type.replace(' ', '_').lower()}"
                    ))
            keyboard.append(row)
        
        # Add back button
        keyboard.append([InlineKeyboardButton(
            language_handler.get_text('back_to_search', telegram_id),
            callback_data="accessory_search_filters"
        )])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_no_accessories_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        """Create keyboard when no accessories are available"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(language_handler.get_text("refresh", telegram_id), callback_data="view_accessories")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
        ])

    @staticmethod
    def accessory_categories(categories: List[str], telegram_id: int, is_refreshed: bool = False) -> InlineKeyboardMarkup:
        """Create accessory categories keyboard"""
        keyboard = []
        
        # Create category buttons in pairs
        for i in range(0, len(categories), 2):
            row = []
            # First category in the row
            category1 = categories[i]
            row.append(InlineKeyboardButton(
                f"⚙️ {category1}",
                callback_data=f"category_{category1.replace(' ', '_').lower()}"
            ))
            
            # Second category in the row (if exists)
            if i + 1 < len(categories):
                category2 = categories[i + 1]
                row.append(InlineKeyboardButton(
                    f"⚙️ {category2}",
                    callback_data=f"category_{category2.replace(' ', '_').lower()}"
                ))
            
            keyboard.append(row)
        
        # Add back button
        keyboard.append([InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )])
        
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    async def accessory_location_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        """Create location keyboard for accessory search using API data"""
        try:
            # Get unique locations from accessory API data
            service = AccessoryService()
            locations = await service.get_unique_locations()
            
            # Create buttons for locations (2 per row)
            location_buttons = []
            for i in range(0, len(locations), 2):
                row = []
                # First location in the row
                location1 = locations[i]
                callback_data1 = f"accessory_location_{location1.replace(' ', '_').replace('/', '_')}"
                row.append(InlineKeyboardButton(f"📍 {location1}", callback_data=callback_data1))
                
                # Second location in the row (if exists)
                if i + 1 < len(locations):
                    location2 = locations[i + 1]
                    callback_data2 = f"accessory_location_{location2.replace(' ', '_').replace('/', '_')}"
                    row.append(InlineKeyboardButton(f"📍 {location2}", callback_data=callback_data2))
                
                location_buttons.append(row)
            
            # Add back button
            location_buttons.append([
                InlineKeyboardButton(language_handler.get_text("back_to_search", telegram_id), callback_data="accessory_search_filters")
            ])
            
            return InlineKeyboardMarkup(location_buttons)
        except Exception as e:
            print(f"Error creating accessory location keyboard: {e}")
            # Fallback keyboard
            return InlineKeyboardMarkup([
                [InlineKeyboardButton(language_handler.get_text("back_to_search", telegram_id), callback_data="accessory_search_filters")]
            ])
    
    @staticmethod
    async def accessory_category_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        """Create category keyboard for accessory search using API data"""
        try:
            # Get unique categories from accessory API data
            service = AccessoryService()
            categories = await service.get_unique_types()
            
            # Create buttons for categories (2 per row)
            category_buttons = []
            for i in range(0, len(categories), 2):
                row = []
                # First category in the row
                category1 = categories[i]
                callback_data1 = f"accessory_category_{category1.replace(' ', '_').replace('/', '_')}"
                row.append(InlineKeyboardButton(f"🔧 {category1}", callback_data=callback_data1))
                
                # Second category in the row (if exists)
                if i + 1 < len(categories):
                    category2 = categories[i + 1]
                    callback_data2 = f"accessory_category_{category2.replace(' ', '_').replace('/', '_')}"
                    row.append(InlineKeyboardButton(f"🔧 {category2}", callback_data=callback_data2))
                
                category_buttons.append(row)
            
            # Add back button
            category_buttons.append([
                InlineKeyboardButton(language_handler.get_text("back_to_search", telegram_id), callback_data="accessory_search_filters")
            ])
            
            return InlineKeyboardMarkup(category_buttons)
        except Exception as e:
            print(f"Error creating accessory category keyboard: {e}")
            # Fallback keyboard
            return InlineKeyboardMarkup([
                [InlineKeyboardButton(language_handler.get_text("back_to_search", telegram_id), callback_data="accessory_search_filters")]
            ])

    @staticmethod
    def help_menu(telegram_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(language_handler.get_text("help_browse_cars", telegram_id), callback_data="help_browse_cars")],
            [InlineKeyboardButton(language_handler.get_text("help_explore", telegram_id), callback_data="help_explore")],
            [InlineKeyboardButton(language_handler.get_text("help_search", telegram_id), callback_data="help_search")],
            [InlineKeyboardButton(language_handler.get_text("help_favourites", telegram_id), callback_data="help_favourites")],
            [InlineKeyboardButton(language_handler.get_text("help_contact", telegram_id), callback_data="help_contact")],
            [InlineKeyboardButton(language_handler.get_text("help_settings", telegram_id), callback_data="help_settings")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="main_menu")]
        ])

    @staticmethod
    def location_settings_menu(telegram_id: int) -> InlineKeyboardMarkup:
        """Create location settings menu keyboard"""
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("request_location_button", telegram_id), callback_data="request_location")],
            [InlineKeyboardButton(language_handler.get_text("clear_location_button", telegram_id), callback_data="clear_location")],
            [InlineKeyboardButton(language_handler.get_text("back_to_settings", telegram_id), callback_data="settings")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def location_request_keyboard(telegram_id: int) -> ReplyKeyboardMarkup:
        """Create keyboard for requesting location"""
        keyboard = [
            [KeyboardButton(language_handler.get_text("share_location_button", telegram_id), request_location=True)],
            [KeyboardButton(language_handler.get_text("cancel_button", telegram_id))]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def location_options_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        """Create keyboard for location-based options"""
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("nearby_charging_stations_button", telegram_id), callback_data="nearby_charging_stations")],
            [InlineKeyboardButton(language_handler.get_text("nearby_garages_button", telegram_id), callback_data="nearby_garages")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="main_menu")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def charging_station_location_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        """Create keyboard for charging station with location request"""
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("request_location_button", telegram_id), callback_data="request_location")],
            [InlineKeyboardButton(language_handler.get_text("back_to_charging_options", telegram_id), callback_data="view_charging_stations")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def garage_location_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
        """Create keyboard for garage with location request"""
        keyboard = [
            [InlineKeyboardButton(language_handler.get_text("request_location_button", telegram_id), callback_data="request_location")],
            [InlineKeyboardButton(language_handler.get_text("back_to_garage_options", telegram_id), callback_data="view_garages")]
        ]
        return InlineKeyboardMarkup(keyboard)
