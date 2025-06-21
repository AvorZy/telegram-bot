from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models.core.garage import Garage
from utils.services.garage_service import GarageService
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

class GarageSearchFilters:
    def __init__(self):
        self.location: str = None
        self.service_type: str = None
        self.keyword: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'location': self.location,
            'service_type': self.service_type,
            'keyword': self.keyword
        }
    
    def from_dict(self, data: Dict[str, Any]):
        self.location = data.get('location')
        self.service_type = data.get('service_type')
        self.keyword = data.get('keyword')

async def handle_garage_search_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show garage search filters menu"""
    query = update.callback_query
    await query.answer()
    
    # Initialize filters if not exists
    if 'garage_search_filters' not in context.user_data:
        context.user_data['garage_search_filters'] = GarageSearchFilters().to_dict()
    
    filters = context.user_data['garage_search_filters']
    
    # Create filter status text
    filter_text = f"{language_handler.get_text('garage_search_filters', update.effective_user.id)}\n\n"
    filter_text += f"📍 {language_handler.get_text('location', update.effective_user.id)}: {filters['location'] or language_handler.get_text('any', update.effective_user.id)}\n"
    filter_text += f"🔧 {language_handler.get_text('service_type', update.effective_user.id)}: {filters['service_type'] or language_handler.get_text('any', update.effective_user.id)}\n"
    
    keyboard = [
        [InlineKeyboardButton(f" {language_handler.get_text('location_filter', update.effective_user.id)}", callback_data="garage_location_search"),
         InlineKeyboardButton(f"🔧 {language_handler.get_text('service_filter', update.effective_user.id)}", callback_data="garage_service_search")],
        [InlineKeyboardButton(f" {language_handler.get_text('apply_filters', update.effective_user.id)}", callback_data="apply_garage_filters"),
         InlineKeyboardButton(f" {language_handler.get_text('clear_filters', update.effective_user.id)}", callback_data="clear_garage_filters")],
        [InlineKeyboardButton(f" {language_handler.get_text('back_to_search_type', update.effective_user.id)}", callback_data="advanced_search")]
    ]
    
    await update.effective_message.reply_text(
        filter_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_garage_location_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle garage location filter"""
    query = update.callback_query
    await query.answer()
    
    try:
        # Show loading message first
        await query.edit_message_text(
            language_handler.get_text('loading_locations', update.effective_user.id)
        )
        
        # Fetch unique locations from garage service
        garage_service = GarageService()
        locations = await garage_service.get_unique_locations()
        
        if not locations:
            await query.edit_message_text(
                language_handler.get_text('no_locations_available', update.effective_user.id),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"⬅️ {language_handler.get_text('back', update.effective_user.id)}", callback_data="garage_search_filters")]
                ])
            )
            return
        
        message = f"{language_handler.get_text('select_garage_location', update.effective_user.id)}\n\n"
        message += f"{language_handler.get_text('choose_garage_location', update.effective_user.id)}"
        
        keyboard = []
        for location in locations:
            keyboard.append([InlineKeyboardButton(f"📍 {location}", callback_data=f"search_garage_location_{location}")])
        
        keyboard.append([InlineKeyboardButton(f"⬅️ {language_handler.get_text('back', update.effective_user.id)}", callback_data="garage_search_filters")])
        
        await update.effective_message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
        
    except Exception as e:
        await update.effective_message.reply_text(
            language_handler.get_text('location_error', update.effective_user.id),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"⬅️ {language_handler.get_text('back', update.effective_user.id)}", callback_data="garage_search_filters")]
            ])
        )

async def handle_garage_service_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle garage service type filter"""
    query = update.callback_query
    await query.answer()
    
    # Fetch available services from API
    garage_service = GarageService()
    services = await garage_service.get_unique_services()
    
    message = f"{language_handler.get_text('select_service_type', update.effective_user.id)}\n\n"
    message += f"{language_handler.get_text('choose_service', update.effective_user.id)}"
    
    # Create keyboard with dynamic services from API
    keyboard = []
    service_icons = {
        'General Repair': '🔧',
        'Battery Service': '🔋', 
        'Electrical Repair': '⚡',
        'Tire Service': '🛞',
        'Car Wash': '🧽',
        'Inspection': '🔍',
        'Maintenance': '🛠️'
    }
    
    for service in services:
        icon = service_icons.get(service, '🔧')  # Default icon if not found
        keyboard.append([InlineKeyboardButton(
            f"{icon} {service}", 
            callback_data=f"garage_service_{service}"
        )])
    
    # Add back button
    keyboard.append([InlineKeyboardButton(
        f"⬅️ {language_handler.get_text('back', update.effective_user.id)}", 
        callback_data="garage_search_filters"
    )])
    
    await update.effective_message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )




# Selection handlers
async def handle_garage_location_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific garage location selection"""
    query = update.callback_query
    location = query.data.replace('search_garage_location_', '')
    
    await query.answer(f"Location filter: {location}")
    
    # Update filters
    if 'garage_search_filters' not in context.user_data:
        context.user_data['garage_search_filters'] = GarageSearchFilters().to_dict()
    
    context.user_data['garage_search_filters']['location'] = location
    
    # Return to garage search menu
    await handle_garage_search_filters(update, context)

async def handle_garage_service_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific garage service selection"""
    query = update.callback_query
    service_type = query.data.replace('garage_service_', '')
    
    await query.answer(f"Service filter: {service_type}")
    
    # Update filters
    if 'garage_search_filters' not in context.user_data:
        context.user_data['garage_search_filters'] = GarageSearchFilters().to_dict()
    
    context.user_data['garage_search_filters']['service_type'] = service_type
    
    # Return to garage search menu
    await handle_garage_search_filters(update, context)





async def handle_clear_garage_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear all garage search filters"""
    query = update.callback_query
    await query.answer(language_handler.get_text("filters_cleared", update.effective_user.id))
    
    # Reset filters
    context.user_data['garage_search_filters'] = GarageSearchFilters().to_dict()
    
    # Return to garage search menu
    await handle_garage_search_filters(update, context)

async def apply_garage_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Apply garage search filters and show results"""
    query = update.callback_query
    await query.answer("Searching garages...")
    
    # Get filters
    filters = context.user_data.get('garage_search_filters', GarageSearchFilters().to_dict())
    
    try:
        # Get garages from service
        garage_service = GarageService()
        all_garages = await garage_service.fetch_all_garages()
        
        # Apply filters
        filtered_garages = []
        for garage in all_garages:
            # Location filter
            if filters['location'] and filters['location'].lower() not in garage.location.lower():
                continue
            
            # Service type filter
            if filters['service_type'] and filters['service_type'].lower() not in garage.garage_service.lower():
                continue
            
            # Rating filter (skip if not set)
            if filters.get('rating_min') and garage.rating < filters['rating_min']:
                continue
            

            
            # Operating hours filter (skip if not set)
            if filters.get('operating_hours') and garage.operating_hours and filters['operating_hours'].lower() not in garage.operating_hours.lower():
                continue
            
            filtered_garages.append(garage)
        
        # Store results and show first page
        context.user_data['garage_search_results'] = filtered_garages
        context.user_data['garage_search_offset'] = 0
        
        await show_garage_search_results_page(update, context, 0)
        
    except Exception as e:
        await update.effective_message.reply_text(
            f"{language_handler.get_text('search_error', update.effective_user.id)}: {str(e)}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    f"⬅️ {language_handler.get_text('back', update.effective_user.id)}",
                    callback_data="garage_search_filters"
                )
            ]])
        )

async def show_garage_search_results_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int):
    """Show garage search results in card format like original garage display"""
    query = update.callback_query
    
    results = context.user_data.get('garage_search_results', [])
    
    if not results:
        message = f"{language_handler.get_text('no_garages_found', update.effective_user.id)}\n\n"
        message += f"{language_handler.get_text('try_different_filters', update.effective_user.id)}"
        
        keyboard = [[
            InlineKeyboardButton(
                f"⬅️ {language_handler.get_text('back_to_filters', update.effective_user.id)}",
                callback_data="garage_search_filters"
            )
        ]]
        
        await update.effective_message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    # Display garages in card format like original garage flow
    garages_per_page = 5  # Same as original garage display
    start_idx = offset
    end_idx = min(start_idx + garages_per_page, len(results))
    page_garages = results[start_idx:end_idx]
    
    telegram_id = update.effective_user.id
    
    # Initialize garage service
    from utils.services.garage_service import GarageService
    service = GarageService()
    
    # Display each garage in card format
    for i, garage in enumerate(page_garages, start_idx + 1):
        # Create garage details in card format (same as original)
        details = f"🔧 **{garage.garage_name}**\n"
        details += f"📍 {garage.location}\n"
        
        if garage.garage_service:
            details += f"🛠️ {garage.garage_service}\n"
        
        if garage.rating:
            details += f"⭐ {garage.rating}/5\n"
        
        if garage.phone_number:
            details += f"📞 {garage.phone_number}\n"
        
        if garage.operating_hours:
            details += f"🕒 {garage.operating_hours}\n"
        
        details += f"\n📊 {language_handler.get_text('garage_count', telegram_id, current=i, total=len(results))}"
        
        # Send garage with image if available (same logic as original)
        try:
            if garage.image_url:
                # Try R2 storage first
                image_url = await service.get_full_image_url(garage.image_url)
            else:
                # Use default garage image from R2
                image_url = f"{service.r2_image_base_url}garage_default.jpg"
            
            # Try to send photo with caption
            if image_url:
                photo_sent = False
                
                # Validate R2 image URL first
                if await is_valid_image_url(image_url):
                    try:
                        await query.message.reply_photo(
                            photo=image_url,
                            caption=details,
                            parse_mode='Markdown'
                        )
                        photo_sent = True
                    except Exception as e:
                        print(f"❌ Failed to send photo from R2: {e}")
                else:
                    print(f"❌ R2 image URL is invalid or not an image: {image_url}")
                
                # Try fallback to original API storage if R2 failed and garage has image
                if not photo_sent and garage.image_url:
                    try:
                        fallback_url = service.get_fallback_image_url(garage.image_url)
                        
                        # Validate fallback image URL
                        if await is_valid_image_url(fallback_url):
                            await query.message.reply_photo(
                                photo=fallback_url,
                                caption=details,
                                parse_mode='Markdown'
                            )
                            photo_sent = True
                            print(f"✅ Successfully sent photo from fallback API storage")
                        else:
                            print(f"❌ Fallback image URL is invalid or not an image: {fallback_url}")
                    except Exception as fallback_e:
                        print(f"❌ Failed to send photo from fallback API: {fallback_e}")
                
                # If both image attempts failed, send text message
                if not photo_sent:
                    fallback_message = f"🔧 {details}\n\n⚠️ Image not available"
                    await query.message.reply_text(
                        fallback_message,
                        parse_mode='Markdown'
                    )
            else:
                # Send text message if no image
                await query.message.reply_text(
                    text=details,
                    parse_mode='Markdown'
                )
        except Exception as e:
            print(f"❌ Error sending garage card: {e}")
            # Final fallback to text message
            fallback_message = f"🔧 {details}\n\n⚠️ Error loading images"
            await query.message.reply_text(
                fallback_message,
                parse_mode='Markdown'
            )
        
        # Send action buttons as separate message after the photo/details (same as original)
        # Debug: Log map_link value to help with debugging
        print(f"DEBUG: Garage '{garage.garage_name}' map_link value: '{garage.map_link}' (type: {type(garage.map_link)})")
        print(f"DEBUG: map_link truthiness: {bool(garage.map_link)}")
        
        # Determine which URL will be used
        map_url = garage.map_link if garage.map_link else "https://maps.google.com"
        print(f"DEBUG: Final map URL used: '{map_url}'")
        
        action_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                language_handler.get_text("garage_view_on_map", telegram_id),
                url=map_url
            )],
            [InlineKeyboardButton(
                f" {language_handler.get_text('modify_filters', telegram_id)}",
                callback_data="garage_search_filters"
            )],
            [InlineKeyboardButton(
                f" {language_handler.get_text('back_to_search', telegram_id)}",
                callback_data="advanced_search"
            )]
        ])
        
        await query.message.reply_text(
            language_handler.get_text("actions", telegram_id),
            reply_markup=action_keyboard
        )
    
    # After displaying all garages on this page, show "View More" button if there are more garages
    if end_idx < len(results):
        remaining_garages = len(results) - end_idx
        view_more_text = f"📋 **Search Results Page {(offset // garages_per_page) + 1}** completed\n"
        view_more_text += f"🔍 {remaining_garages} more garages found\n\n"
        view_more_text += "Click 'View More' to see additional search results."
        
        view_more_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                f"🔍 View More Results ({remaining_garages} remaining)",
                callback_data=f"more_garage_search_results_{end_idx}"
            )],
            [InlineKeyboardButton(
                f"🔍 {language_handler.get_text('modify_filters', telegram_id)}",
                callback_data="garage_search_filters"
            )],
            [InlineKeyboardButton(
                f"⬅️ {language_handler.get_text('back_to_search', telegram_id)}",
                callback_data="advanced_search"
            )]
        ])
        
        await query.message.reply_text(
            view_more_text,
            reply_markup=view_more_keyboard,
            parse_mode='Markdown'
        )

async def handle_more_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Results' button click for garage search"""
    query = update.callback_query
    
    # Parse callback data: more_garage_search_results_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 5:
        offset = int(callback_parts[4])
        
        await query.answer("Loading more search results...")
        await show_garage_search_results_page(update, context, offset)
    else:
        await query.answer("Error loading more results")