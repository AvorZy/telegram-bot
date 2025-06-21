from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.ui.language import language_handler

def create_navigation_keyboard(telegram_id, back_to_section=None, section_callback=None, include_related=None):
    """Create standardized navigation keyboard to reduce code duplication"""
    keyboard = []
    
    # Add related buttons if provided
    if include_related:
        for row in include_related:
            keyboard.append(row)
    
    # Add back navigation
    back_row = []
    if back_to_section and section_callback:
        back_text = language_handler.get_text("back_to_section", telegram_id, section=back_to_section)
        back_row.append(InlineKeyboardButton(back_text, callback_data=section_callback))
    back_row.append(InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main"))
    keyboard.append(back_row)
    
    return InlineKeyboardMarkup(keyboard)