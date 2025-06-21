from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.ui.language import language_handler
from utils.ui.keyboards import Keyboards
from typing import List, Dict, Any, Callable

class FilterHelpers:
    """Utility class to reduce code duplication in filter handling"""
    
    @staticmethod
    async def handle_generic_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                     filter_key: str, value: str, 
                                     success_message_key: str = None,
                                     back_callback: str = None) -> None:
        """Generic handler for filter selections"""
        query = update.callback_query
        await query.answer()
        
        telegram_id = update.effective_user.id
        
        # Update the filter in context
        if 'search_filters' not in context.user_data:
            context.user_data['search_filters'] = {}
        
        context.user_data['search_filters'][filter_key] = value
        
        # Send confirmation message
        if success_message_key:
            message = language_handler.get_text(success_message_key, telegram_id, value=value)
        else:
            message = language_handler.get_text("filter_updated", telegram_id, filter=filter_key, value=value)
        
        # Create back navigation
        keyboard = []
        if back_callback:
            keyboard.append(Keyboards.create_navigation_row(telegram_id, back_callback))
        else:
            keyboard.append([Keyboards.create_back_to_menu_button(telegram_id)])
        
        await query.edit_message_text(
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    @staticmethod
    def create_range_keyboard(telegram_id: int, ranges: List[Dict[str, Any]], 
                            callback_prefix: str, back_callback: str = None) -> InlineKeyboardMarkup:
        """Create a keyboard for range selections (price, year, etc.)"""
        keyboard = []
        
        # Create range buttons (2 per row)
        for i in range(0, len(ranges), 2):
            row = []
            for j in range(2):
                if i + j < len(ranges):
                    range_item = ranges[i + j]
                    callback_data = f"{callback_prefix}_{range_item['min']}_{range_item['max']}"
                    row.append(InlineKeyboardButton(range_item['label'], callback_data=callback_data))
            keyboard.append(row)
        
        # Add navigation
        if back_callback:
            keyboard.append(Keyboards.create_navigation_row(telegram_id, back_callback))
        else:
            keyboard.append([Keyboards.create_back_to_menu_button(telegram_id)])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_option_keyboard(telegram_id: int, options: List[Dict[str, str]], 
                             callback_prefix: str, back_callback: str = None, 
                             columns: int = 2) -> InlineKeyboardMarkup:
        """Create a keyboard for option selections (location, brand, etc.)"""
        keyboard = []
        
        # Create option buttons
        for i in range(0, len(options), columns):
            row = []
            for j in range(columns):
                if i + j < len(options):
                    option = options[i + j]
                    callback_data = f"{callback_prefix}_{option['value']}"
                    row.append(InlineKeyboardButton(option['label'], callback_data=callback_data))
            keyboard.append(row)
        
        # Add navigation
        if back_callback:
            keyboard.append(Keyboards.create_navigation_row(telegram_id, back_callback))
        else:
            keyboard.append([Keyboards.create_back_to_menu_button(telegram_id)])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    async def handle_range_selection(update, context, prefix, filter_keys, message_format, callback_func, filter_key='search_filters'):
        """Generic handler for range selections (price, year, etc.)"""
        query = update.callback_query
        range_data = query.data.replace(prefix, '').split('_')
        value_min = int(range_data[0])
        value_max = int(range_data[1])
        
        # Send confirmation message
        await query.answer(message_format.format(value_min, value_max))
        
        # Update filters
        if filter_key not in context.user_data:
            if filter_key == 'search_filters':
                from models.core.product import SearchFilters
                context.user_data[filter_key] = SearchFilters().to_dict()
            elif filter_key == 'accessory_search_filters':
                from models.core.accessory import AccessorySearchFilters
                context.user_data[filter_key] = AccessorySearchFilters().to_dict()
        
        context.user_data[filter_key][filter_keys[0]] = value_min
        context.user_data[filter_key][filter_keys[1]] = value_max
        
        # Return to search menu
        await callback_func(update, context)
    
    @staticmethod
    async def handle_option_selection(update, context, prefix, filter_field, message_format, callback_func, filter_key='search_filters'):
        """Generic handler for single option selections (location, brand, etc.)"""
        query = update.callback_query
        value = query.data.replace(prefix, '').replace('_', ' ')
        
        # Handle special cases
        if value == 'any':
            value = None
            await query.answer(f"{filter_field.title()} filter cleared")
        else:
            await query.answer(message_format.format(value))
        
        # Update filters
        if filter_key not in context.user_data:
            if filter_key == 'search_filters':
                from models.core.product import SearchFilters
                context.user_data[filter_key] = SearchFilters().to_dict()
            elif filter_key == 'accessory_search_filters':
                from models.core.accessory import AccessorySearchFilters
                context.user_data[filter_key] = AccessorySearchFilters().to_dict()
        
        context.user_data[filter_key][filter_field] = value
        
        # Return to search menu
        await callback_func(update, context)
    
    @staticmethod
    def apply_filters(items: List[Any], filters: Dict[str, Any], 
                     filter_functions: Dict[str, Callable]) -> List[Any]:
        """Generic filter application function"""
        filtered_items = items.copy()
        
        for filter_key, filter_value in filters.items():
            if filter_value and filter_key in filter_functions:
                filtered_items = filter_functions[filter_key](filtered_items, filter_value)
        
        return filtered_items