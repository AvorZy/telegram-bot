from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from utils.services.user_api_service import user_api_service
from utils.services.charging_station_service import charging_station_service
from utils.services.garage_service import GarageService
from utils.ui.language import language_handler
from utils.ui.keyboards import Keyboards
from datetime import datetime

def create_back_button(telegram_id: int) -> InlineKeyboardMarkup:
    """Create a back button keyboard"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(language_handler.get_text('back_button', telegram_id), callback_data='back')]
    ])

async def request_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Request user's location for nearby searches"""
    user = update.effective_user
    user_data = await user_api_service.get_or_create_user(user)
    lang = user_data.get('language', 'en')
    
    # Create location request keyboard
    location_button = KeyboardButton(
        text=language_handler.get_text('share_location_button', user.id),
        request_location=True
    )
    
    keyboard = ReplyKeyboardMarkup(
        [[location_button], [language_handler.get_text('cancel_button', user.id)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    # Handle both message and callback query
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            language_handler.get_text('location_request_message', user.id),
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            language_handler.get_text('location_request_message', user.id),
            reply_markup=keyboard
        )

async def handle_location_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle when user shares their location"""
    user = update.effective_user
    user_data = await user_api_service.get_or_create_user(user)
    lang = user_data.get('language', 'en')
    
    if update.message.location:
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        
        # Update user's location in the database
        print(f"DEBUG: Attempting to update location for user {user.id} with lat: {latitude}, lng: {longitude}")
        success = await user_api_service.update_user_location(
            user.id, latitude, longitude
        )
        print(f"DEBUG: Location update result for user {user.id}: {success}")
        
        if success:
            await update.message.reply_text(
                language_handler.get_text('location_saved_success', user.id),
                reply_markup=ReplyKeyboardRemove()
            )
            
            # Check if there's a pending action to execute
            pending_action = context.user_data.get('pending_action')
            
            if pending_action == 'show_nearby_charging':
                # Clear the pending action
                context.user_data.pop('pending_action', None)
                
                # Automatically show nearby charging stations
                from handlers.charging_station.charging_station import show_stations_page
                from utils.services.charging_station_service import charging_station_service
                
                stations = await charging_station_service.get_nearby_stations(latitude, longitude, limit=50)
                
                if stations:
                    context.user_data['nearby_stations'] = stations
                    await show_stations_page(update, context, 0, "nearby")
                else:
                    await update.message.reply_text(
                        language_handler.get_text('no_nearby_charging_stations', user.id)
                    )
                    
            elif pending_action == 'show_nearby_garage':
                # Clear the pending action
                context.user_data.pop('pending_action', None)
                
                # Automatically show nearby garages
                from handlers.garage.garage import show_garages_page
                from utils.services.garage_service import GarageService
                
                service = GarageService()
                garages = await service.get_nearby_garages(latitude, longitude, limit=50)
                
                if garages:
                    context.user_data['nearby_garages'] = garages
                    await show_garages_page(update, context, 0, "nearby")
                else:
                    await update.message.reply_text(
                        language_handler.get_text('no_nearby_garages', user.id)
                    )
            else:
                # Show nearby options if no specific action was pending
                from utils.helpers.keyboard import create_inline_keyboard
                keyboard = create_inline_keyboard([
                    [(language_handler.get_text('nearby_charging_stations', user.id), 'nearby_charging_stations')],
                    [(language_handler.get_text('nearby_garages', user.id), 'nearby_garages')],
                    [(language_handler.get_text('back_to_main_menu', user.id), 'main_menu')]
                ])
                
                await update.message.reply_text(
                    language_handler.get_text('location_nearby_options', user.id),
                    reply_markup=keyboard
                )
        else:
            await update.message.reply_text(
                language_handler.get_text('location_save_error', user.id),
                reply_markup=ReplyKeyboardRemove()
            )
    else:
        await update.message.reply_text(
            language_handler.get_text('location_not_received', user.id),
            reply_markup=ReplyKeyboardRemove()
        )

async def handle_nearby_charging_stations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show nearby charging stations using user's location"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    user_data = await user_api_service.get_or_create_user(user)
    lang = user_data.get('language', 'en')
    
    # Get user's location
    location = await user_api_service.get_user_location(user.id)
    
    if location:
        latitude, longitude = location
        
        # Import and use the existing charging station service
        from utils.services.charging_station_service import charging_station_service
        
        try:
            stations = await charging_station_service.get_nearby_stations(
                user_lat=latitude,
                user_lng=longitude,
                limit=10
            )
            
            if stations:
                message = language_handler.get_text('nearby_charging_stations_found', user.id).format(
                    count=len(stations)
                )
                
                for i, station in enumerate(stations[:5], 1):
                    distance = station.get('distance', 0)
                    message += f"\n\n{i}. **{station.get('name', 'Unknown')}**\n"
                    message += f"📍 {station.get('address', 'No address')}\n"
                    message += f"📏 {distance:.1f} km away\n"
                    
                    if station.get('price'):
                        message += f"💰 ${station.get('price')}/kWh\n"
                    
                    if station.get('power'):
                        message += f"⚡ {station.get('power')} kW\n"
                
                keyboard = create_back_button(user.id)
                await query.edit_message_text(
                    message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(
                    language_handler.get_text('no_nearby_charging_stations', user.id),
                    reply_markup=create_back_button(user.id)
                )
                
        except Exception as e:
            print(f"Error fetching nearby charging stations: {e}")
            await query.edit_message_text(
                language_handler.get_text('error_fetching_stations', user.id),
                reply_markup=create_back_button(user.id)
            )
    else:
        await query.edit_message_text(
             language_handler.get_text('location_not_available', user.id),
             reply_markup=create_back_button(user.id)
         )

async def handle_nearby_garages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show nearby garages using user's location"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    user_data = await user_api_service.get_or_create_user(user)
    lang = user_data.get('language', 'en')
    
    # Get user's location
    location = await user_api_service.get_user_location(user.id)
    
    if location:
        latitude, longitude = location
        
        # Import and use the existing garage service
        from utils.services.garage_service import garage_service
        
        try:
            garages = await garage_service.get_nearby_garages(
                user_lat=latitude,
                user_lng=longitude,
                limit=10
            )
            
            if garages:
                message = language_handler.get_text('nearby_garages_found', user.id).format(
                    count=len(garages)
                )
                
                for i, garage in enumerate(garages[:5], 1):
                    distance = garage.get('distance', 0)
                    message += f"\n\n{i}. **{garage.get('name', 'Unknown')}**\n"
                    message += f"📍 {garage.get('address', 'No address')}\n"
                    message += f"📏 {distance:.1f} km away\n"
                    
                    if garage.get('services'):
                        services = garage.get('services', [])
                        if isinstance(services, list) and services:
                            message += f"🔧 Services: {', '.join(services[:3])}\n"
                        elif isinstance(services, str):
                            message += f"🔧 Services: {services}\n"
                
                keyboard = create_back_button(user.id)
                await query.edit_message_text(
                    message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(
                    language_handler.get_text('no_nearby_garages', user.id),
                    reply_markup=create_back_button(user.id)
                )
                
        except Exception as e:
            print(f"Error fetching nearby garages: {e}")
            await query.edit_message_text(
                language_handler.get_text('error_fetching_garages', user.id),
                reply_markup=create_back_button(user.id)
            )
    else:
        await query.edit_message_text(
             language_handler.get_text('location_not_available', user.id),
             reply_markup=create_back_button(user.id)
         )

async def show_location_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show location settings and current status"""
    query = update.callback_query
    if query:
        await query.answer()
        user = update.effective_user
        message_func = query.edit_message_text
    else:
        user = update.effective_user
        message_func = update.message.reply_text
    
    user_data = await user_api_service.get_or_create_user(user)
    lang = user_data.get('language', 'en')
    
    # Check if user has location stored
    location = await user_api_service.get_user_location(user.id)
    
    if location:
        latitude, longitude = location
        message = language_handler.get_text('location_current_status', user.id).format(
            lat=latitude, lng=longitude
        )
        
        from utils.helpers.keyboard import create_inline_keyboard
        keyboard = create_inline_keyboard([
            [(language_handler.get_text('update_location', user.id), 'update_location')],
        [(language_handler.get_text('clear_location', user.id), 'clear_location')],
        [(language_handler.get_text('nearby_options', user.id), 'nearby_options')],
        [(language_handler.get_text('back_button', user.id), 'settings')]
        ])
    else:
        message = language_handler.get_text('location_not_set', user.id)
        
        from utils.helpers.keyboard import create_inline_keyboard
        keyboard = create_inline_keyboard([
            [(language_handler.get_text('set_location', user.id), 'set_location')],
        [(language_handler.get_text('back_button', user.id), 'settings')]
        ])
    
    await message_func(message, reply_markup=keyboard)

async def handle_clear_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear user's stored location"""
    query = update.callback_query
    await query.answer()
    
    user = update.effective_user
    user_data = await user_api_service.get_or_create_user(user)
    lang = user_data.get('language', 'en')
    
    # Clear location by setting to None
    success = await user_api_service.update_user(
        user.id, 
        {'latitude': None, 'longitude': None, 'locationUpdatedAt': None}
    )
    
    if success:
        await query.edit_message_text(
             language_handler.get_text('location_cleared_success', user.id),
             reply_markup=create_back_button(user.id)
         )
    else:
        await query.edit_message_text(
             language_handler.get_text('location_clear_error', user.id),
             reply_markup=create_back_button(user.id)
         )