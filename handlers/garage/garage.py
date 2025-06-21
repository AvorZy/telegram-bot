from typing import List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from telegram.error import BadRequest

from utils.services.garage_service import GarageService
from models.core.garage import Garage
from utils.ui.language import LanguageHandler
import aiohttp

language_handler = LanguageHandler()

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
                    callback_data=f"garage_location_{location}"
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

def create_garage_navigation_keyboard(
    garages: List[Garage], 
    telegram_id: int,
    location: str, 
    current_index: int
) -> InlineKeyboardMarkup:
    """Create navigation keyboard for browsing garages"""
    keyboard = []
    
    # Navigation buttons
    nav_row = []
    if current_index > 0:
        nav_row.append(InlineKeyboardButton(
            "⬅️ Previous",
            callback_data=f"garage_{current_index - 1}_{location}"
        ))
    
    if current_index < len(garages) - 1:
        nav_row.append(InlineKeyboardButton(
            "➡️ Next",
            callback_data=f"garage_{current_index + 1}_{location}"
        ))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Map link button
    current_garage = garages[current_index]
    if current_garage.map_link:
        keyboard.append([
            InlineKeyboardButton(
                language_handler.get_text("garage_view_on_map", telegram_id),
                url=current_garage.map_link
            )
        ])
    
    # Back buttons
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("garage_back_to_locations", telegram_id),
            callback_data="garages"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

def create_location_garages_keyboard(
    garages: List[Garage], 
    location: str, 
    telegram_id: int
) -> InlineKeyboardMarkup:
    """Create keyboard with garage buttons for a specific location"""
    keyboard = []
    
    # Add garage buttons
    for i, garage in enumerate(garages):
        keyboard.append([
            InlineKeyboardButton(
                f"🔧 {garage.garage_name}",
                callback_data=f"garage_{i}_{location}"
            )
        ])
    
    # Add back button
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("garage_back_to_locations", telegram_id),
            callback_data="garages"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

async def view_garages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle viewing garages - show main options"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    
    # Show main garage options
    message = language_handler.get_text("garage_options", telegram_id)
    
    keyboard = [
        [InlineKeyboardButton(
            language_handler.get_text("show_by_location", telegram_id),
            callback_data="garage_show_by_location"
        )],
        [InlineKeyboardButton(
            language_handler.get_text("show_nearby", telegram_id),
            callback_data="garage_show_nearby"
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
    """Handle showing garages by location"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    service = GarageService()
    
    # Show loading message
    loading_message = language_handler.get_text("garage_loading", telegram_id)
    await query.message.reply_text(loading_message)
    
    try:
        # Get unique locations
        locations = await service.get_unique_locations()
        
        if not locations:
            no_garages_message = language_handler.get_text("garage_no_garages", telegram_id)
            keyboard = create_locations_keyboard([], telegram_id)
            await query.message.reply_text(no_garages_message, reply_markup=keyboard)
            return
        
        # Show locations list
        header_message = language_handler.get_text("garage_locations_header", telegram_id)
        keyboard = create_locations_keyboard(locations, telegram_id)
        await query.message.reply_text(header_message, reply_markup=keyboard, parse_mode='Markdown')
        
    except Exception as e:
        error_message = language_handler.get_text("garage_error", telegram_id)
        keyboard = create_locations_keyboard([], telegram_id)
        await query.message.reply_text(error_message, reply_markup=keyboard)

async def handle_show_nearby(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle showing nearby garages with real-time location"""
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
    
    # Store that user wants to see garages after sharing real-time location
    context.user_data['pending_action'] = 'show_nearby_garage'
    
    await query.message.reply_text(
        language_handler.get_text('location_request_realtime', telegram_id) or 
        "📍 Please share your current location to find nearby garages",
        reply_markup=keyboard
    )

async def show_garages_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int, display_type: str):
    """Display a page of garages in card format"""
    query = update.callback_query if update.callback_query else None
    telegram_id = update.effective_user.id
    service = GarageService()
    
    # Get garages based on display type
    if display_type == "nearby":
        garages = context.user_data.get('nearby_garages', [])
    else:  # location
        garages = context.user_data.get('location_garages', [])
    
    # Calculate pagination - show 5 garages per page
    garages_per_page = 5
    start_idx = offset
    end_idx = min(start_idx + garages_per_page, len(garages))
    page_garages = garages[start_idx:end_idx]
    
    # Update offset in context
    context.user_data['garages_offset'] = offset
    
    # Skip summary message - user doesn't need it
    
    for i, garage in enumerate(page_garages, start_idx + 1):
        # Create garage details in card format
        details = f"🔧 **{garage.garage_name}**\n"
        details += f"📍 {garage.location}\n"
        
        # Add distance information for nearby garages
        if display_type == "nearby" and garage.distance_in_km and garage.distance_in_km > 0:
            details += f"📏 {garage.distance_in_km:.1f} km away\n"
        
        if garage.garage_service:
            details += f"🛠️ {garage.garage_service}\n"
        
        if garage.rating:
            details += f"⭐ {garage.rating}/5\n"
        
        if garage.phone_number:
            details += f"📞 {garage.phone_number}\n"
        
        if garage.operating_hours:
            details += f"🕒 {garage.operating_hours}\n"
        
        details += f"\n📊 {language_handler.get_text('garage_count', telegram_id, current=i, total=len(garages))}"
        
        # Send garage with image if available
        try:
            # Try to send photo
            image_urls = []
            
            # Add R2 storage URL if available
            if garage.image_url:
                r2_url = await service.get_full_image_url(garage.image_url)
                image_urls.append((r2_url, "R2 storage"))
            
            # Add API storage URL if available
            if garage.image_url:
                api_url = service.get_fallback_image_url(garage.image_url)
                image_urls.append((api_url, "API storage"))
            
            # Add default R2 image as fallback
            default_r2_url = f"{service.r2_image_base_url}garage_default.jpg"
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
                        
                        photo_sent = True
                        print(f"✅ Successfully sent photo from {source_name}")
                        break
                    
                except Exception as e:
                    print(f"❌ Failed to send photo from {source_name}: {e}")
                    continue
            
            # If no image could be sent, send text message
            if not photo_sent:
                fallback_message = f"🔧 {details}\n\n⚠️ Image not available"
                message_obj = query.message if query else update.message
                if message_obj:
                    await message_obj.reply_text(
                        fallback_message,
                        parse_mode='Markdown'
                    )
        except Exception as e:
            print(f"❌ Error sending garage card: {e}")
            # Final fallback to text message
            fallback_message = f"🔧 {details}\n\n⚠️ Error loading images"
            message_obj = query.message if query else update.message
            if message_obj:
                await message_obj.reply_text(
                    fallback_message,
                    parse_mode='Markdown'
                )
        
        # Send action buttons as separate message after the photo/details
        action_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                language_handler.get_text("garage_view_on_map", telegram_id),
                url=garage.map_link if garage.map_link else "https://maps.google.com"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_garage_options", telegram_id),
                callback_data="view_garages"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_menu", telegram_id),
                callback_data="back_to_main"
            )]
        ])
        
        message_obj = query.message if query else update.message
        if message_obj:
            await message_obj.reply_text(
                language_handler.get_text("actions", telegram_id),
                reply_markup=action_keyboard
            )
    
    # After displaying all garages on this page, show "View More" button if there are more garages
    if end_idx < len(garages):
        remaining_garages = len(garages) - end_idx
        view_more_text = f"📋 **Page {(offset // garages_per_page) + 1}** completed\n"
        view_more_text += f"🔍 {remaining_garages} more garages available\n\n"
        view_more_text += "Click 'View More' to see additional garages sorted by distance."
        
        view_more_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                f"🔍 View More Garages ({remaining_garages} remaining)",
                callback_data=f"more_garages_{display_type}_{end_idx}"
            )],
            [InlineKeyboardButton(
                language_handler.get_text("back_to_garage_options", telegram_id),
                callback_data="view_garages"
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

async def handle_more_garages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Garages' button click"""
    query = update.callback_query
    
    # Parse callback data: more_garages_{display_type}_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 4:
        display_type = callback_parts[2]
        offset = int(callback_parts[3])
        
        await query.answer("Loading more garages...")
        
        # Show next page of results
        await show_garages_page(update, context, offset, display_type)
    else:
        await query.answer("Error loading more garages")

async def view_location_garages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle viewing garages in a specific location"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    service = GarageService()
    
    # Extract location from callback data
    callback_data = query.data
    location = callback_data.replace('garage_location_', '')
    
    # Show loading message
    loading_message = language_handler.get_text("garage_loading", telegram_id)
    await query.message.reply_text(loading_message)
    
    try:
        # Get garages for this location
        garages = await service.get_garages_by_location(location)
        
        if not garages:
            no_garages_message = language_handler.get_text("garage_no_garages_in_location", telegram_id).format(location=location)
            keyboard = create_locations_keyboard([], telegram_id)
            await query.message.reply_text(no_garages_message, reply_markup=keyboard)
            return
        
        # Show first garage details directly
        # Show garages in card format like charging stations
        context.user_data['location_garages'] = garages
        context.user_data['garages_offset'] = 0
        await show_garages_page(update, context, 0, "location")
        
    except Exception as e:
        print(f"Error in view_location_garages: {e}")
        error_message = language_handler.get_text("garage_error", telegram_id)
        keyboard = create_locations_keyboard([], telegram_id)
        await query.message.reply_text(error_message, reply_markup=keyboard)