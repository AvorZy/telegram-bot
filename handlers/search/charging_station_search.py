from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models.core.charging_station import ChargingStation
from utils.services.charging_station_service import ChargingStationService
from utils.ui.keyboards import Keyboards
from utils.ui.language import language_handler
from typing import List, Dict, Any
import re
import aiohttp

async def is_valid_image_url(url: str) -> bool:
    """Check if URL points to a valid image"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '').lower()
                    return content_type.startswith('image/')
                return False
    except Exception:
        return False

class ChargingStationSearchFilters:
    def __init__(self):
        self.price_min: float = 0
        self.price_max: float = 999999
        self.power_min: int = 0
        self.power_max: int = 500
        self.location: str = None
        self.station_type: str = None
        self.connector_type: str = None
        self.availability: bool = None
        self.keyword: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'price_min': self.price_min,
            'price_max': self.price_max,
            'power_min': self.power_min,
            'power_max': self.power_max,
            'location': self.location,
            'station_type': self.station_type,
            'connector_type': self.connector_type,
            'availability': self.availability,
            'keyword': self.keyword
        }
    
    def from_dict(self, data: Dict[str, Any]):
        self.price_min = data.get('price_min', 0)
        self.price_max = data.get('price_max', 999999)
        self.power_min = data.get('power_min', 0)
        self.power_max = data.get('power_max', 500)
        self.location = data.get('location')
        self.station_type = data.get('station_type')
        self.connector_type = data.get('connector_type')
        self.availability = data.get('availability')
        self.keyword = data.get('keyword')

async def handle_charging_station_search_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show charging station search filters menu"""
    query = update.callback_query
    await query.answer()
    
    # Initialize filters if not exists
    if 'charging_station_search_filters' not in context.user_data:
        context.user_data['charging_station_search_filters'] = ChargingStationSearchFilters().to_dict()
    
    filters = context.user_data['charging_station_search_filters']
    
    # Create filter status text
    filter_text = f"{language_handler.get_text('charging_station_search_filters', update.effective_user.id)}\n\n"
    filter_text += f"💰 {language_handler.get_text('price_range', update.effective_user.id)}: ${filters['price_min']:.2f} - ${filters['price_max']:.2f}\n"
    filter_text += f"⚡ {language_handler.get_text('power_range', update.effective_user.id)}: {filters['power_min']}kW - {filters['power_max']}kW\n"
    filter_text += f"📍 {language_handler.get_text('location', update.effective_user.id)}: {filters['location'] or language_handler.get_text('any', update.effective_user.id)}\n"
    filter_text += f"🔗 {language_handler.get_text('connector_type', update.effective_user.id)}: {filters['connector_type'] or language_handler.get_text('any', update.effective_user.id)}\n"
    
    keyboard = [
        [InlineKeyboardButton(f" {language_handler.get_text('price_filter', update.effective_user.id)}", callback_data="charging_station_price_search"),
         InlineKeyboardButton(f"⚡ {language_handler.get_text('power_filter', update.effective_user.id)}", callback_data="charging_station_power_search")],
        [InlineKeyboardButton(f" {language_handler.get_text('location_filter', update.effective_user.id)}", callback_data="charging_station_location_search"),
         InlineKeyboardButton(f"🔗 {language_handler.get_text('connector_filter', update.effective_user.id)}", callback_data="charging_station_connector_search")],
        [InlineKeyboardButton(f" {language_handler.get_text('apply_filters', update.effective_user.id)}", callback_data="apply_charging_station_filters"),
         InlineKeyboardButton(f" {language_handler.get_text('clear_filters', update.effective_user.id)}", callback_data="clear_charging_station_filters")],
        [InlineKeyboardButton(f" {language_handler.get_text('back_to_search_type', update.effective_user.id)}", callback_data="advanced_search")]
    ]
    
    await query.message.reply_text(
        filter_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_charging_price_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle charging station price filter"""
    query = update.callback_query
    await query.answer()
    
    message = f"{language_handler.get_text('select_price_range', update.effective_user.id)}\n\n"
    message += f"{language_handler.get_text('price_per_kwh', update.effective_user.id)}"
    
    keyboard = [
        [InlineKeyboardButton("$0.10 - $0.30", callback_data="charging_station_price_0.10_0.30")],
        [InlineKeyboardButton("$0.30 - $0.50", callback_data="charging_station_price_0.30_0.50")],
        [InlineKeyboardButton("$0.50 - $0.70", callback_data="charging_station_price_0.50_0.70")],
        [InlineKeyboardButton("$0.70 - $1.00", callback_data="charging_station_price_0.70_1.00")],
        [InlineKeyboardButton("$1.00+", callback_data="charging_station_price_1.00_999999")],
        [InlineKeyboardButton(f"⬅️ {language_handler.get_text('back', update.effective_user.id)}", callback_data="charging_station_search_filters")]
    ]
    
    await query.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_charging_power_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle charging station power filter"""
    query = update.callback_query
    await query.answer()
    
    message = f"{language_handler.get_text('select_power_range', update.effective_user.id)}\n\n"
    message += f"{language_handler.get_text('charging_power', update.effective_user.id)}"
    
    keyboard = [
        [InlineKeyboardButton("⚡ 0-50kW (Slow)", callback_data="charging_station_power_0_50")],
        [InlineKeyboardButton("⚡ 50-150kW (Fast)", callback_data="charging_station_power_50_150")],
        [InlineKeyboardButton("⚡ 150-350kW (Ultra Fast)", callback_data="charging_station_power_150_350")],
        [InlineKeyboardButton("⚡ 350kW+ (Super Fast)", callback_data="charging_station_power_350_500")],
        [InlineKeyboardButton(f"⬅️ {language_handler.get_text('back', update.effective_user.id)}", callback_data="charging_station_search_filters")]
    ]
    
    await query.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_charging_location_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle charging station location filter"""
    query = update.callback_query
    await query.answer()
    
    message = f"{language_handler.get_text('select_location', update.effective_user.id)}\n\n"
    message += f"{language_handler.get_text('choose_location', update.effective_user.id)}"
    
    keyboard = await Keyboards.charging_location_keyboard(update.effective_user.id)
    await query.message.reply_text(
        message,
        reply_markup=keyboard
    )

async def handle_charging_connector_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle charging station connector type filter"""
    query = update.callback_query
    await query.answer()
    
    message = f"{language_handler.get_text('select_connector_type', update.effective_user.id)}\n\n"
    message += f"{language_handler.get_text('choose_connector', update.effective_user.id)}"
    
    # Get connector types from API
    charging_service = ChargingStationService()
    connector_types = await charging_service.get_unique_connector_types()
    
    keyboard = []
    # Add connector types from API
    for connector_type in connector_types:
        keyboard.append([InlineKeyboardButton(
            f"🔌 {connector_type}", 
            callback_data=f"charging_station_connector_{connector_type}"
        )])
    
    # Add back button
    keyboard.append([InlineKeyboardButton(
        f"⬅️ {language_handler.get_text('back', update.effective_user.id)}", 
        callback_data="charging_station_search_filters"
    )])
    
    await query.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



# Selection handlers
async def handle_charging_price_range_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific charging price range selection"""
    query = update.callback_query
    price_data = query.data.replace('charging_station_price_', '').split('_')
    price_min = float(price_data[0])
    price_max = float(price_data[1])
    
    await query.answer(f"Price filter: ${price_min:.2f} - ${price_max:.2f} per kWh")
    
    # Update filters
    if 'charging_station_search_filters' not in context.user_data:
        context.user_data['charging_station_search_filters'] = ChargingStationSearchFilters().to_dict()
    
    context.user_data['charging_station_search_filters']['price_min'] = price_min
    context.user_data['charging_station_search_filters']['price_max'] = price_max
    
    # Return to charging station search menu
    await handle_charging_station_search_filters(update, context)

async def handle_charging_power_range_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific charging power range selection"""
    query = update.callback_query
    power_data = query.data.replace('charging_station_power_', '').split('_')
    power_min = int(power_data[0])
    power_max = int(power_data[1])
    
    await query.answer(f"Power filter: {power_min}kW - {power_max}kW")
    
    # Update filters
    if 'charging_station_search_filters' not in context.user_data:
        context.user_data['charging_station_search_filters'] = ChargingStationSearchFilters().to_dict()
    
    context.user_data['charging_station_search_filters']['power_min'] = power_min
    context.user_data['charging_station_search_filters']['power_max'] = power_max
    
    # Return to charging station search menu
    await handle_charging_station_search_filters(update, context)

async def handle_charging_location_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific charging location selection"""
    query = update.callback_query
    location = query.data.replace('charging_search_location_', '')
    
    await query.answer(f"Location filter: {location}")
    
    # Update filters
    if 'charging_station_search_filters' not in context.user_data:
        context.user_data['charging_station_search_filters'] = ChargingStationSearchFilters().to_dict()
    
    context.user_data['charging_station_search_filters']['location'] = location
    
    # Return to charging station search menu
    await handle_charging_station_search_filters(update, context)

async def handle_charging_connector_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific charging connector selection"""
    query = update.callback_query
    connector_type = query.data.replace('charging_station_connector_', '')
    
    await query.answer(f"Connector filter: {connector_type}")
    
    # Update filters
    if 'charging_station_search_filters' not in context.user_data:
        context.user_data['charging_station_search_filters'] = ChargingStationSearchFilters().to_dict()
    
    context.user_data['charging_station_search_filters']['connector_type'] = connector_type
    
    # Return to charging station search menu
    await handle_charging_station_search_filters(update, context)



async def handle_clear_charging_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear all charging station search filters"""
    query = update.callback_query
    await query.answer(language_handler.get_text("filters_cleared", update.effective_user.id))
    
    # Reset filters
    context.user_data['charging_station_search_filters'] = ChargingStationSearchFilters().to_dict()
    
    # Return to charging station search menu
    await handle_charging_station_search_filters(update, context)

async def apply_charging_station_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Apply charging station search filters and show results"""
    query = update.callback_query
    await query.answer("Searching charging stations...")
    
    # Get filters
    filters = context.user_data.get('charging_station_search_filters', ChargingStationSearchFilters().to_dict())
    
    try:
        # Get charging stations from service
        charging_service = ChargingStationService()
        all_stations = await charging_service.fetch_all_stations()
        
        # Apply filters
        filtered_stations = []
        for station in all_stations:
            # Price filter
            if not (filters['price_min'] <= station.price_per_kwh <= filters['price_max']):
                continue
            
            # Power filter
            if not (filters['power_min'] <= station.power_value <= filters['power_max']):
                continue
            
            # Location filter
            if filters['location'] and filters['location'].lower() not in station.location.lower():
                continue
            
            # Type filter
            if filters['station_type'] and filters['station_type'].lower() not in station.type.lower():
                continue
            
            # Connector type filter
            if filters['connector_type'] and filters['connector_type'] not in station.connector_types:
                continue
            

            
            # Availability filter
            if filters['availability'] is not None and station.availability != filters['availability']:
                continue
            
            filtered_stations.append(station)
        
        # Store results and show first page
        context.user_data['charging_search_results'] = filtered_stations
        context.user_data['charging_search_offset'] = 0
        
        await show_charging_search_results_page(update, context, 0)
        
    except Exception as e:
        await query.message.reply_text(
            f"{language_handler.get_text('search_error', update.effective_user.id)}: {str(e)}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    f"⬅️ {language_handler.get_text('back', update.effective_user.id)}",
                    callback_data="charging_station_search_filters"
                )
            ]])
        )

async def show_charging_search_results_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int):
    """Display charging station search results with pagination - same flow as car search"""
    search_results = context.user_data.get('charging_search_results', [])
    
    if not search_results:
        query = update.callback_query
        message = f"{language_handler.get_text('no_charging_stations_found', update.effective_user.id)}\n\n"
        message += f"{language_handler.get_text('try_different_filters', update.effective_user.id)}"
        
        keyboard = [[
            InlineKeyboardButton(
                f"⬅️ {language_handler.get_text('back_to_filters', update.effective_user.id)}",
                callback_data="charging_station_search_filters"
            )
        ]]
        
        await query.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    stations_per_page = 5  # Show 5 stations per page like car search
    start_idx = offset
    end_idx = min(start_idx + stations_per_page, len(search_results))
    
    if start_idx >= len(search_results):
        start_idx = 0
        end_idx = min(stations_per_page, len(search_results))
    
    # Update offset in context
    context.user_data['charging_search_offset'] = offset
    
    # Get charging station service for image handling
    charging_service = ChargingStationService()
    
    # Display each station as a separate message (like car search flow)
    for i, station in enumerate(search_results[start_idx:end_idx], start_idx + 1):
        # Get user language for formatting
        user_language = language_handler.get_user_language(update.effective_user.id)
        
        # Use the same detailed formatting as charging station display
        details = station.get_formatted_details(user_language)
        
        # Add search result counter
        details += f"\n\n📊 Search Result {i}/{len(search_results)}"
        
        # Create keyboard with same structure as car search
        keyboard_buttons = []
        
        # Map link button if available
        if station.map_link:
            keyboard_buttons.append([
                InlineKeyboardButton(
                    language_handler.get_text("charging_view_on_map", update.effective_user.id),
                    url=station.map_link
                )
            ])
        
        # Add "View More Results" button if there are more stations to show
        if end_idx < len(search_results):
            remaining = len(search_results) - end_idx
            keyboard_buttons.append([
                InlineKeyboardButton(
                    f"📋 View More Charging Stations ({remaining} more)",
                    callback_data=f"more_charging_search_results_{end_idx}"
                )
            ])
        
        # Add navigation buttons
        keyboard_buttons.extend([
            [InlineKeyboardButton(
                f"{language_handler.get_text('modify_filters', update.effective_user.id)}",
                callback_data="charging_station_search_filters"
            )],
            [InlineKeyboardButton(
                f"{language_handler.get_text('back_to_search', update.effective_user.id)}",
                callback_data="advanced_search"
            )]
        ])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        
        try:
            # Get image URL with fallback mechanism (same as charging station display)
            image_url = None
            if station.image_url:
                # Try R2 storage first
                image_url = await charging_service.get_full_image_url(station.image_url)
            else:
                # Use default charging station image from R2
                image_url = f"{charging_service.r2_image_base_url}charging_station_default.jpg"
            
            # Try to send photo with caption (same logic as charging station display)
            if image_url:
                photo_sent = False
                
                # Validate R2 image URL first
                if await is_valid_image_url(image_url):
                    try:
                        await update.callback_query.message.reply_photo(
                            photo=image_url,
                            caption=details,
                            parse_mode='Markdown'
                        )
                        # Send action buttons as separate message
                        await update.callback_query.message.reply_text(
                            language_handler.get_text("actions", update.effective_user.id),
                            reply_markup=keyboard
                        )
                        photo_sent = True
                    except Exception as e:
                        pass
        except Exception as e:
            pass
        
        # Try fallback to original API storage if R2 failed and station has image
        if not photo_sent and station.image_url:
            try:
                fallback_url = charging_service.get_fallback_image_url(station.image_url)
                
                # Validate fallback image URL
                if await is_valid_image_url(fallback_url):
                    await update.callback_query.message.reply_photo(
                        photo=fallback_url,
                        caption=details,
                        parse_mode='Markdown'
                    )
                    # Send action buttons as separate message
                    await update.callback_query.message.reply_text(
                        language_handler.get_text("actions", update.effective_user.id),
                        reply_markup=keyboard
                    )
                    photo_sent = True
            except Exception as fallback_e:
                pass
        
        # If both image attempts failed, send text message
        if not photo_sent:
            fallback_message = f"🔌 {details}\n\n⚠️ Image not available"
            await update.callback_query.message.reply_text(
                fallback_message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        else:
            # Send text message if no image
            await update.callback_query.message.reply_text(
                text=details,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )

async def handle_more_charging_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Results' button click"""
    query = update.callback_query
    
    # Parse callback data: charging_results_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 3:
        offset = int(callback_parts[-1])
        
        await query.answer("Loading more charging stations...")
        
        # Show next page of results
        await show_charging_search_results_page(update, context, offset)
    else:
        await query.answer("Error loading more results")

# Add new handler for "View More Results" button with new callback format
async def handle_more_charging_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Charging Search Results' button click"""
    query = update.callback_query
    
    # Parse callback data: more_charging_search_results_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 5:
        offset = int(callback_parts[-1])
        
        await query.answer("Loading more charging stations...")
        
        # Show next page of search results
        await show_charging_search_results_page(update, context, offset)
    else:
        await query.answer("Error loading more results")