import asyncio
from telegram import Update, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.ui.language import language_handler
from utils.services.charging_station_service import charging_station_service
from models.core.charging_station import ChargingStation
from typing import List
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

def create_locations_keyboard(locations: List[str], telegram_id: int) -> InlineKeyboardMarkup:
    """Create keyboard with location buttons"""
    keyboard = []
    
    # Add location buttons (2 per row)
    for i in range(0, len(locations), 2):
        row = []
        for j in range(2):
            if i + j < len(locations):
                location = locations[i + j]
                row.append(InlineKeyboardButton(
                    f"📍 {location}",
                    callback_data=f"charging_location_{location}"
                ))
        keyboard.append(row)
    
    # Add back button
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

def create_station_navigation_keyboard(
    stations: List[ChargingStation], 
    current_index: int, 
    location: str, 
    telegram_id: int
) -> InlineKeyboardMarkup:
    """Create navigation keyboard for browsing stations"""
    keyboard = []
    
    # Navigation buttons
    nav_row = []
    if current_index > 0:
        nav_row.append(InlineKeyboardButton(
            "⬅️ Previous",
            callback_data=f"station_{current_index - 1}_{location}"
        ))
    
    if current_index < len(stations) - 1:
        nav_row.append(InlineKeyboardButton(
            "➡️ Next",
            callback_data=f"station_{current_index + 1}_{location}"
        ))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Map link button
    current_station = stations[current_index]
    if current_station.map_link:
        keyboard.append([
            InlineKeyboardButton(
                language_handler.get_text("charging_view_on_map", telegram_id),
                url=current_station.map_link
            )
        ])
    
    # Back buttons
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("charging_back_to_locations", telegram_id),
            callback_data="charging_stations"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

def create_location_stations_keyboard(
    stations: List[ChargingStation], 
    location: str, 
    telegram_id: int
) -> InlineKeyboardMarkup:
    """Create keyboard with station buttons for a specific location"""
    keyboard = []
    
    # Add station buttons
    for i, station in enumerate(stations):
        keyboard.append([
            InlineKeyboardButton(
                f"⚡ {station.name}",
                callback_data=f"station_{i}_{location}"
            )
        ])
    
    # Add back button
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("charging_back_to_locations", telegram_id),
            callback_data="charging_stations"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

async def view_charging_stations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle viewing charging stations - show main options"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    
    # Show main charging station options
    message = language_handler.get_text("charging_station_options", telegram_id)
    
    keyboard = [
        [InlineKeyboardButton(
            language_handler.get_text("show_by_location", telegram_id),
            callback_data="charging_show_by_location"
        )],
        [InlineKeyboardButton(
            language_handler.get_text("show_nearby", telegram_id),
            callback_data="charging_show_nearby"
        )],
        [InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )]
    ]
    
    await query.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
async def handle_show_by_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle showing charging stations by location"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    # Using global charging station service instance
    
    # Show loading message
    loading_message = language_handler.get_text("charging_loading", telegram_id)
    await query.message.reply_text(loading_message)
    
    try:
        # Get unique locations
        locations = await charging_station_service.get_unique_locations()
        
        if not locations:
            no_stations_message = language_handler.get_text("charging_no_stations", telegram_id)
            keyboard = create_locations_keyboard([], telegram_id)
            await query.message.reply_text(no_stations_message, reply_markup=keyboard)
            return
        
        # Show locations list
        header_message = language_handler.get_text("charging_locations_header", telegram_id)
        keyboard = create_locations_keyboard(locations, telegram_id)
        await query.message.reply_text(header_message, reply_markup=keyboard, parse_mode='Markdown')
        
    except Exception as e:
        error_message = language_handler.get_text("charging_error", telegram_id)
        keyboard = create_locations_keyboard([], telegram_id)
        await query.message.reply_text(error_message, reply_markup=keyboard)

async def handle_show_nearby(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle showing nearby charging stations with real-time location"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    
    # Request real-time location for accurate nearby results
    from telegram import KeyboardButton, ReplyKeyboardMarkup
    location_button = KeyboardButton(
        text=language_handler.get_text('share_location_button', telegram_id),
        request_location=True
    )
    
    keyboard = ReplyKeyboardMarkup(
        [[location_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    # Store that user wants to see charging stations after sharing real-time location
    context.user_data['pending_action'] = 'show_nearby_charging'
    
    await query.message.reply_text(
        language_handler.get_text('location_request_realtime', telegram_id) or 
        "📍 Please share your current location to find nearby charging stations",
        reply_markup=keyboard
    )

async def show_stations_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int, display_type: str):
    """Display a page of charging stations in card format"""
    query = update.callback_query if update.callback_query else None
    telegram_id = update.effective_user.id
    # Using global charging station service instance
    
    stations = context.user_data.get('nearby_stations', [])
    
    # Calculate pagination - show 5 stations per page
    stations_per_page = 5
    start_idx = offset
    end_idx = min(start_idx + stations_per_page, len(stations))
    page_stations = stations[start_idx:end_idx]
    
    # Update offset in context
    context.user_data['stations_offset'] = offset
    
    # Skip summary message - user doesn't need it
    
    for i, station in enumerate(page_stations, start_idx + 1):
        # Create station details in card format
        details = f"🔌 **{station.name}**\n"
        details += f"📍 {station.location}\n"
        
        # Add distance information for nearby stations
        if display_type == "nearby" and station.distance_in_km > 0:
            details += f"📏 {station.distance_in_km:.1f} km away\n"
        
        details += f"⚡ {station.power_value}kW\n"
        details += f"💰 ${station.price_per_kwh:.2f}/kWh\n"
        
        if station.connector_types:
            connector_list = ", ".join(station.connector_types)
            details += f"🔗 {connector_list}\n"
        
        if station.availability:
            details += f"✅ {language_handler.get_text('available', telegram_id)}\n"
        else:
            details += f"❌ {language_handler.get_text('occupied', telegram_id)}\n"
        
        # Note: description attribute not available in ChargingStation model
        
        details += f"\n📊 {language_handler.get_text('station_count', telegram_id, current=i, total=len(stations))}"
        
        # Create keyboard with action buttons
        keyboard_buttons = []
        
        # Add map link if available
        if station.map_link:
            keyboard_buttons.append([
                InlineKeyboardButton(
                    language_handler.get_text("view_on_map", telegram_id),
                    url=station.map_link
                )
            ])
        
        # Add navigation buttons for individual station
        keyboard_buttons.extend([
            [InlineKeyboardButton(
                language_handler.get_text("back_to_charging_options", telegram_id),
                callback_data="charging_stations"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_menu", telegram_id),
                callback_data="back_to_main"
            )]
        ])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        
        # Send station with image if available
        try:
            # Try to send photo
            image_urls = []
            
            # Add R2 storage URL if available
            if station.image_url:
                r2_url = await charging_station_service.get_full_image_url(station.image_url)
                image_urls.append((r2_url, "R2 storage"))
            
            # Add API storage URL if available
            if station.image_url:
                api_url = charging_station_service.get_fallback_image_url(station.image_url)
                image_urls.append((api_url, "API storage"))
            
            # Add default R2 image as fallback
            default_r2_url = f"{charging_station_service.r2_image_base_url}charging_station_default.jpg"
            image_urls.append((default_r2_url, "Default R2 image"))
            
            photo_sent = False
            
            # Try each URL until one works
            for image_url, source_name in image_urls:
                try:
                    print(f"🔍 Trying {source_name}: {image_url}")
                    
                    # Validate image URL first
                    if not await is_valid_image_url(image_url):
                        print(f"❌ Invalid image URL from {source_name}: {image_url}")
                        continue
                    
                    # For R2 URLs, try downloading first then fallback to direct URL
                    if "r2.dev" in image_url or "cloudflare" in image_url:
                        try:
                            import aiohttp
                            async with aiohttp.ClientSession() as session:
                                async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                                    if response.status == 200:
                                        image_data = await response.read()
                                        print(f"🔍 Downloaded {len(image_data)} bytes from {source_name}")
                                        
                                        # Send as bytes instead of URL
                                        message_obj = query.message if query else update.message
                                        if message_obj:
                                            await message_obj.reply_photo(
                                                photo=image_data,
                                                caption=details,
                                                parse_mode='Markdown'
                                            )
                                            
                                            # Send action buttons as separate message
                                            await message_obj.reply_text(
                                                language_handler.get_text("actions", telegram_id),
                                                reply_markup=keyboard
                                            )
                                        photo_sent = True
                                        print(f"✅ Successfully sent photo data from {source_name}")
                                        break
                        except Exception as download_e:
                            print(f"❌ Failed to download from {source_name}: {download_e}")
                            # Continue to try direct URL sending
                    
                    # Try direct URL sending (for non-R2 or if download failed)
                    if not photo_sent:
                        message_obj = query.message if query else update.message
                        if message_obj:
                            await message_obj.reply_photo(
                                photo=image_url,
                                caption=details,
                                parse_mode='Markdown'
                            )
                            
                            # Send action buttons as separate message
                            await message_obj.reply_text(
                                language_handler.get_text("actions", telegram_id),
                                reply_markup=keyboard
                            )
                        
                        photo_sent = True
                        print(f"✅ Successfully sent photo from {source_name}")
                        break
                    
                except Exception as e:
                    print(f"❌ Failed to send photo from {source_name}: {e}")
                    continue
            
            # If no image could be sent, send text message
            if not photo_sent:
                message_obj = query.message if query else update.message
                if message_obj:
                    await message_obj.reply_text(
                        text=details,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                print("📝 Sent text message (no image available)")
        except Exception as e:
            print(f"❌ Error sending charging station card: {e}")
            # Final fallback to text message
            fallback_message = f"🔌 {details}\n\n⚠️ Error loading images"
            message_obj = query.message if query else update.message
            if message_obj:
                await message_obj.reply_text(
                    fallback_message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
    
    # After displaying all stations on this page, show "View More" button if there are more stations
    if end_idx < len(stations):
        remaining_stations = len(stations) - end_idx
        view_more_text = f"📋 **Page {(offset // stations_per_page) + 1}** completed\n"
        view_more_text += f"🔍 {remaining_stations} more stations available\n\n"
        view_more_text += "Click 'View More' to see additional charging stations sorted by distance."
        
        view_more_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                f"🔍 View More Stations ({remaining_stations} remaining)",
                callback_data=f"more_stations_{display_type}_{end_idx}"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_charging_options", telegram_id),
                callback_data="charging_stations"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_menu", telegram_id),
                callback_data="back_to_main"
            )]
        ])
        
        message_obj = query.message if query else update.message
        if message_obj:
            await message_obj.reply_text(
                view_more_text,
                reply_markup=view_more_keyboard,
                parse_mode='Markdown'
            )
    # Skip completion message - user doesn't need it

async def handle_more_stations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Stations' button click"""
    query = update.callback_query
    
    # Parse callback data: more_stations_{display_type}_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 4:
        display_type = callback_parts[2]
        offset = int(callback_parts[3])
        
        await query.answer("Loading more stations...")
        
        # Show next page of results
        await show_stations_page(update, context, offset, display_type)
    else:
        await query.answer("Error loading more stations")

async def show_location_stations_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int):
    """Display a page of location-based charging stations in card format"""
    query = update.callback_query if update.callback_query else None
    telegram_id = update.effective_user.id
    # Using global charging station service instance
    
    stations = context.user_data.get('location_stations', [])
    location = context.user_data.get('current_location', '')
    
    # Calculate pagination - show 5 stations per page
    stations_per_page = 5
    start_idx = offset
    end_idx = min(start_idx + stations_per_page, len(stations))
    page_stations = stations[start_idx:end_idx]
    
    # Update offset in context
    context.user_data['location_stations_offset'] = offset
    
    # Skip summary message - user doesn't need it
    
    for i, station in enumerate(page_stations, start_idx + 1):
        # Create station details in card format
        details = f"🔌 **{station.name}**\n"
        details += f"📍 {station.location}\n"
        details += f"⚡ {station.power_value}kW\n"
        details += f"💰 ${station.price_per_kwh:.2f}/kWh\n"
        
        if station.connector_types:
            connector_list = ", ".join(station.connector_types)
            details += f"🔗 {connector_list}\n"
        
        if station.availability:
            details += f"✅ {language_handler.get_text('available', telegram_id)}\n"
        else:
            details += f"❌ {language_handler.get_text('occupied', telegram_id)}\n"
        
        details += f"\n📊 {language_handler.get_text('station_count', telegram_id, current=i, total=len(stations))}"
        
        # Create keyboard with action buttons (no separate actions message)
        keyboard_buttons = []
        
        # Add map link if available
        if station.map_link:
            keyboard_buttons.append([
                InlineKeyboardButton(
                    language_handler.get_text("view_on_map", telegram_id),
                    url=station.map_link
                )
            ])
        
        # Add navigation buttons
        keyboard_buttons.extend([
            [InlineKeyboardButton(
                language_handler.get_text("back_to_charging_options", telegram_id),
                callback_data="charging_stations"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_menu", telegram_id),
                callback_data="back_to_main"
            )]
        ])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        
        # Send station with image if available
        try:
            # Try to send photo
            image_urls = []
            
            # Add R2 storage URL if available
            if station.image_url:
                r2_url = await charging_station_service.get_full_image_url(station.image_url)
                image_urls.append((r2_url, "R2 storage"))
            
            # Add API storage URL if available
            if station.image_url:
                api_url = charging_station_service.get_fallback_image_url(station.image_url)
                image_urls.append((api_url, "API storage"))
            
            # Add default R2 image as fallback
            default_r2_url = f"{charging_station_service.r2_image_base_url}charging_station_default.jpg"
            image_urls.append((default_r2_url, "Default R2 image"))
            
            photo_sent = False
            
            # Try each URL until one works
            for image_url, source_name in image_urls:
                try:
                    print(f"🔍 Trying {source_name}: {image_url}")
                    
                    # Validate image URL first
                    if not await is_valid_image_url(image_url):
                        print(f"❌ Invalid image URL from {source_name}: {image_url}")
                        continue
                    
                    # For R2 URLs, try downloading first then fallback to direct URL
                    if "r2.dev" in image_url or "cloudflare" in image_url:
                        try:
                            import aiohttp
                            async with aiohttp.ClientSession() as session:
                                async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                                    if response.status == 200:
                                        image_data = await response.read()
                                        print(f"🔍 Downloaded {len(image_data)} bytes from {source_name}")
                                        
                                        # Send as bytes instead of URL
                                        if query:
                                            await query.message.reply_photo(
                                                photo=image_data,
                                                caption=details,
                                                parse_mode='Markdown'
                                            )
                                            
                                            # Send action buttons as separate message
                                            await query.message.reply_text(
                                                language_handler.get_text("actions", telegram_id),
                                                reply_markup=keyboard
                                            )
                                        photo_sent = True
                                        print(f"✅ Successfully sent photo data from {source_name}")
                                        break
                        except Exception as download_e:
                            print(f"❌ Failed to download from {source_name}: {download_e}")
                            # Continue to try direct URL sending
                    
                    # Try direct URL sending (for non-R2 or if download failed)
                    if not photo_sent:
                        if query:
                            await query.message.reply_photo(
                                photo=image_url,
                                caption=details,
                                parse_mode='Markdown'
                            )
                            
                            # Send action buttons as separate message
                            await query.message.reply_text(
                                language_handler.get_text("actions", telegram_id),
                                reply_markup=keyboard
                            )
                        
                        photo_sent = True
                        print(f"✅ Successfully sent photo from {source_name}")
                        break
                    
                except Exception as e:
                    print(f"❌ Failed to send photo from {source_name}: {e}")
                    continue
            
            # If no image could be sent, send text message
            if not photo_sent:
                if query:
                    await query.message.reply_text(
                        text=details,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                print("📝 Sent text message (no image available)")
        except Exception as e:
            print(f"❌ Error sending charging station card: {e}")
            # Final fallback to text message
            fallback_message = f"🔌 {details}\n\n⚠️ Error loading images"
            if query:
                await query.message.reply_text(
                    fallback_message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
    
    # After displaying all stations on this page, show "View More" button if there are more stations
    if end_idx < len(stations):
        remaining_stations = len(stations) - end_idx
        view_more_text = f"📋 **Page {(offset // stations_per_page) + 1}** completed\n"
        view_more_text += f"🔍 {remaining_stations} more stations available in {location}\n\n"
        view_more_text += "Click 'View More' to see additional charging stations."
        
        view_more_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                f"🔍 View More Stations ({remaining_stations} remaining)",
                callback_data=f"more_location_stations_{location}_{end_idx}"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_charging_options", telegram_id),
                callback_data="charging_stations"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_menu", telegram_id),
                callback_data="back_to_main"
            )]
        ])
        
        if query:
            await query.message.reply_text(
                view_more_text,
                reply_markup=view_more_keyboard,
                parse_mode='Markdown'
            )

async def handle_more_location_stations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Stations' button click for location-based stations"""
    query = update.callback_query
    
    # Parse callback data: more_location_stations_{location}_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 4:
        # Reconstruct location (might contain underscores)
        location = '_'.join(callback_parts[3:-1])
        offset = int(callback_parts[-1])
        
        await query.answer("Loading more stations...")
        
        # Show next page of results
        await show_location_stations_page(update, context, offset)
    else:
        await query.answer("Error loading more stations")

async def view_location_stations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle viewing stations in a specific location with card format"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    # Using global charging station service instance
    
    # Extract location from callback data
    callback_data = query.data
    location = callback_data.replace('charging_location_', '')
    
    # Show loading message
    loading_message = language_handler.get_text("charging_loading", telegram_id)
    await query.message.reply_text(loading_message)
    
    try:
        # Get stations for this location
        stations = await charging_station_service.get_stations_by_location(location)
        
        if not stations:
            no_stations_message = language_handler.get_text("charging_no_stations_in_location", telegram_id).format(location=location)
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    language_handler.get_text("back_to_menu", telegram_id),
                    callback_data="back_to_main"
                )
            ]])
            await query.message.reply_text(no_stations_message, reply_markup=keyboard)
            return
        
        # Store stations and location in context for pagination
        context.user_data['location_stations'] = stations
        context.user_data['current_location'] = location
        context.user_data['location_stations_offset'] = 0
        
        # Show first page of stations in card format
        await show_location_stations_page(update, context, 0)
        
    except Exception as e:
        error_message = language_handler.get_text("charging_error", telegram_id)
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                language_handler.get_text("back_to_menu", telegram_id),
                callback_data="back_to_main"
            )
        ]])
        await query.message.reply_text(error_message, reply_markup=keyboard)
        print(f"Error in view_location_stations: {e}")

async def view_station_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle station navigation (previous/next)"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    # Using global charging station service instance
    
    # Extract station index and location from callback data
    callback_data = query.data
    parts = callback_data.split('_')
    station_index = int(parts[1])
    location = '_'.join(parts[2:]) if len(parts) > 2 else ''
    
    try:
        # Get stations for this location
        stations = await charging_station_service.get_stations_by_location(location)
        
        if not stations or station_index >= len(stations):
            error_message = language_handler.get_text("charging_error", telegram_id)
            keyboard = create_locations_keyboard([], telegram_id)
            await query.message.reply_text(error_message, reply_markup=keyboard)
            return
        
        # Show station details
        await _show_station_details(query, stations, station_index, location, telegram_id, charging_station_service)
        
    except Exception as e:
        error_message = language_handler.get_text("charging_error", telegram_id)
        keyboard = create_locations_keyboard([], telegram_id)
        await query.message.reply_text(error_message, reply_markup=keyboard)
        print(f"Error in view_station_navigation: {e}")

async def _show_station_details(query, stations, station_index, location, telegram_id, charging_service):
    """Helper function to show station details with image"""
    station = stations[station_index]
    
    # Get formatted details
    user_language = language_handler.get_user_language(telegram_id)
    caption = station.get_formatted_details(user_language)
    
    # Create navigation keyboard
    keyboard = create_station_navigation_keyboard(stations, station_index, location, telegram_id)
    
    # Get image URL with fallback mechanism
    image_url = None
    if station.image_url:
        # Try R2 storage first
        image_url = await charging_service.get_full_image_url(station.image_url)
    else:
        # Use default charging station image from R2
        image_url = f"{charging_service.r2_image_base_url}charging_station_default.jpg"
    
    # Try to send photo with caption
    if image_url:
        # Try to send photo
        image_urls = []
        
        # Add R2 storage URL if available
        if station.image_url:
            r2_url = await charging_service.get_full_image_url(station.image_url)
            image_urls.append((r2_url, "R2 storage"))
        
        # Add API storage URL if available
        if station.image_url:
            api_url = charging_service.get_fallback_image_url(station.image_url)
            image_urls.append((api_url, "API storage"))
        
        # Add default R2 image as fallback
        default_r2_url = f"{charging_service.r2_image_base_url}charging_station_default.jpg"
        image_urls.append((default_r2_url, "Default R2 image"))
        
        photo_sent = False
        
        # Try each URL until one works
        for image_url, source_name in image_urls:
            try:
                print(f"🔍 Trying {source_name}: {image_url}")
                
                # Validate image URL first
                if not await is_valid_image_url(image_url):
                    print(f"❌ Invalid image URL from {source_name}: {image_url}")
                    continue
                
                # For R2 URLs, try downloading first then fallback to direct URL
                if "r2.dev" in image_url or "cloudflare" in image_url:
                    try:
                        import aiohttp
                        async with aiohttp.ClientSession() as session:
                            async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                                if response.status == 200:
                                    image_data = await response.read()
                                    print(f"🔍 Downloaded {len(image_data)} bytes from {source_name}")
                                    
                                    # Send as bytes instead of URL
                                    await query.message.reply_photo(
                                        photo=image_data,
                                        caption=caption,
                                        reply_markup=keyboard,
                                        parse_mode='Markdown'
                                    )
                                    photo_sent = True
                                    print(f"✅ Successfully sent photo data from {source_name}")
                                    break
                    except Exception as download_e:
                        print(f"❌ Failed to download from {source_name}: {download_e}")
                        # Continue to try direct URL sending
                
                # Try direct URL sending (for non-R2 or if download failed)
                if not photo_sent:
                    await query.message.reply_photo(
                        photo=image_url,
                        caption=caption,
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                    
                    photo_sent = True
                    print(f"✅ Successfully sent photo from {source_name}")
                    break
                
            except Exception as e:
                print(f"❌ Failed to send photo from {source_name}: {e}")
                continue
        
        # If no image could be sent, send text message
        if not photo_sent:
            await query.message.reply_text(caption, reply_markup=keyboard, parse_mode='Markdown')
            print("📝 Sent text message (no image available)")
    else:
        # Send text message if no image
        await query.message.reply_text(caption, reply_markup=keyboard, parse_mode='Markdown')