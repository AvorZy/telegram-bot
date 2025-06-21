from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from utils.ui.language import language_handler
from utils.ui.keyboards import Keyboards
from utils.ui.filter_helpers import FilterHelpers
from utils.services.accessory_service import AccessoryService
from typing import List, Dict, Any

class AccessorySearchFilters:
    """Accessory search filters data structure"""
    def __init__(self):
        self.price_min: float = 0
        self.price_max: float = 999999
        self.location: str = None
        self.brand: str = None
        self.accessory_type: str = None
        self.keyword: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'price_min': self.price_min,
            'price_max': self.price_max,
            'location': self.location,
            'brand': self.brand,
            'accessory_type': self.accessory_type,
            'keyword': self.keyword
        }
    
    def from_dict(self, data: Dict[str, Any]):
        self.price_min = data.get('price_min', 0)
        self.price_max = data.get('price_max', 999999)
        self.location = data.get('location')
        self.brand = data.get('brand')
        self.accessory_type = data.get('accessory_type')
        self.keyword = data.get('keyword')

async def handle_accessory_search_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show accessory search filters menu"""
    query = update.callback_query
    await query.answer()
    
    # Set search type context for accessory search
    context.user_data['current_search_type'] = 'accessory'
    
    # Initialize accessory search filters if not exists
    if 'accessory_search_filters' not in context.user_data:
        context.user_data['accessory_search_filters'] = AccessorySearchFilters().to_dict()
    
    filters = context.user_data['accessory_search_filters']
    
    # Build current filters display
    filter_text = language_handler.get_text("current_filters", update.effective_user.id) + "\n"
    
    # Track if any filters are applied
    has_filters = False
    
    if filters['price_min'] > 0 or filters['price_max'] < 999999:
        filter_text += f"💰 ${filters['price_min']:,.0f} - ${filters['price_max']:,.0f}\n"
        has_filters = True
    
    if filters['location']:
        filter_text += f"📍 {filters['location']}\n"
        has_filters = True
    
    if filters['brand']:
        filter_text += f"🏷️ {filters['brand']}\n"
        has_filters = True
    
    if filters['accessory_type']:
        filter_text += f"🔧 {filters['accessory_type']}\n"
        has_filters = True
    
    if filters['keyword']:
        filter_text += f"🔤 {filters['keyword']}\n"
        has_filters = True
    
    # Add "No filters applied" only if no filters are set
    if not has_filters:
        filter_text += language_handler.get_text("no_filters_applied", update.effective_user.id) + "\n"
    
    # Build complete message
    message = language_handler.get_text("accessory_search_title", update.effective_user.id) + "\n\n" + filter_text + "\n" + language_handler.get_text("select_filter_or_apply", update.effective_user.id)
    
    # Send NEW message instead of editing
    await query.message.reply_text(
        message,
        reply_markup=Keyboards.accessory_search_menu(update.effective_user.id)
    )

async def handle_accessory_price_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle accessory price range selection"""
    query = update.callback_query
    await query.answer()
    
    # Set search type context for accessory search
    context.user_data['current_search_type'] = 'accessory'
    
    message = language_handler.get_text("search_by_price", update.effective_user.id) + "\n\n" + language_handler.get_text("select_price_range", update.effective_user.id)
    
    await query.edit_message_text(
        message,
        reply_markup=Keyboards.price_range_keyboard(update.effective_user.id)
    )

async def handle_accessory_location_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle accessory location selection"""
    query = update.callback_query
    await query.answer()
    
    # Set search type context for accessory search
    context.user_data['current_search_type'] = 'accessory'
    
    message = language_handler.get_text("search_by_location", update.effective_user.id) + "\n\n" + language_handler.get_text("select_location", update.effective_user.id)
    
    # Use the new API-based accessory location keyboard
    keyboard = await Keyboards.accessory_location_keyboard(update.effective_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=keyboard
    )

async def handle_accessory_brand_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle accessory brand selection"""
    query = update.callback_query
    await query.answer()
    
    # Set search type context for accessory search
    context.user_data['current_search_type'] = 'accessory'
    
    # Get available accessory brands
    available_brands = set()
    service = AccessoryService()
    accessories = await service.fetch_all_accessories()
    for accessory in accessories:
        if hasattr(accessory, 'brand') and accessory.brand:
            available_brands.add(accessory.brand)
    
    # Create brand selection keyboard
    keyboard = []
    brands_list = sorted(list(available_brands))
    
    for i in range(0, len(brands_list), 2):
        row = []
        row.append(InlineKeyboardButton(brands_list[i], callback_data=f"accessory_brand_{brands_list[i]}"))
        if i + 1 < len(brands_list):
            row.append(InlineKeyboardButton(brands_list[i + 1], callback_data=f"accessory_brand_{brands_list[i + 1]}"))
        keyboard.append(row)
    
    # Add back button
    keyboard.append([InlineKeyboardButton(language_handler.get_text("back_to_search_type", update.effective_user.id), callback_data="accessory_search")])
    
    message = language_handler.get_text("search_by_brand", update.effective_user.id) + "\n\n" + language_handler.get_text("select_brand", update.effective_user.id)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_accessory_category_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle accessory category selection"""
    query = update.callback_query
    await query.answer()
    
    # Set search type context for accessory search
    context.user_data['current_search_type'] = 'accessory'
    
    message = language_handler.get_text("search_by_category", update.effective_user.id) + "\n\n" + language_handler.get_text("select_category", update.effective_user.id)
    
    # Use the new API-based accessory category keyboard
    keyboard = await Keyboards.accessory_category_keyboard(update.effective_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=keyboard
    )

async def handle_accessory_price_range_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific accessory price range selection"""
    await FilterHelpers.handle_range_selection(
        update, context, 'price_',
        ['price_min', 'price_max'],
        'Price filter: ${0:,} - ${1:,}',
        handle_accessory_search_filters,
        filter_key='accessory_search_filters'
    )

async def handle_accessory_location_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific accessory location selection"""
    await FilterHelpers.handle_option_selection(
        update, context, 'location_',
        'location', 'Location filter: {0}',
        handle_accessory_search_filters,
        filter_key='accessory_search_filters'
    )

async def handle_accessory_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific accessory category selection"""
    await FilterHelpers.handle_option_selection(
        update, context, 'accessory_category_',
        'accessory_type', 'Category filter: {0}',
        handle_accessory_search_filters,
        filter_key='accessory_search_filters'
    )



async def handle_apply_accessory_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Apply accessory search filters and show results"""
    query = update.callback_query
    await query.answer("Searching...")
    
    # Get current accessory filters from context
    accessory_filters = context.user_data.get('accessory_search_filters', {})
    
    # Filter accessories based on applied filters
    service = AccessoryService()
    accessories = await service.fetch_all_accessories()
    filtered_accessories = []
    
    for accessory in accessories:
        # Apply price filter
        if 'price_min' in accessory_filters and accessory_filters['price_min']:
            if not hasattr(accessory, 'price') or accessory.price < accessory_filters['price_min']:
                continue
        
        if 'price_max' in accessory_filters and accessory_filters['price_max']:
            if not hasattr(accessory, 'price') or accessory.price > accessory_filters['price_max']:
                continue
        
        # Apply location filter
        if 'location' in accessory_filters and accessory_filters['location']:
            if not hasattr(accessory, 'location') or accessory_filters['location'].lower() not in accessory.location.lower():
                continue
        
        filtered_accessories.append(accessory)
    
    if not filtered_accessories:
        message = language_handler.get_text("no_accessory_search_results", update.effective_user.id)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(language_handler.get_text("modify_filters", update.effective_user.id), callback_data="accessory_search_filters")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
        ])
        await query.edit_message_text(message, reply_markup=keyboard)
    else:
        # Store filtered results
        context.user_data['accessory_search_results'] = filtered_accessories
        context.user_data['accessory_search_offset'] = 0
        
        # Show results count message first
        count_message = language_handler.get_text("accessory_search_results", update.effective_user.id).format(count=len(filtered_accessories))
        await query.edit_message_text(count_message)
        
        # Show first result
        await show_accessory_search_results_page(update, context, 0)

async def handle_clear_accessory_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear all accessory search filters"""
    query = update.callback_query
    await query.answer(language_handler.get_text("accessory_filters_cleared", update.effective_user.id))
    
    # Clear accessory filters from context
    context.user_data['accessory_search_filters'] = AccessorySearchFilters().to_dict()
    
    # Show updated accessory search filters menu
    await handle_accessory_search_filters(update, context)

async def show_accessory_search_results_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int):
    """Display accessory search results with pagination - same flow as car search"""
    search_results = context.user_data.get('accessory_search_results', [])
    
    if not search_results:
        return
    
    accessories_per_page = 5  # Show 5 accessories per page like car search
    start_idx = offset
    end_idx = min(start_idx + accessories_per_page, len(search_results))
    
    if start_idx >= len(search_results):
        start_idx = 0
        end_idx = min(accessories_per_page, len(search_results))
    
    # Update offset in context
    context.user_data['accessory_search_offset'] = offset
    
    # Display each accessory as a separate message (matching original accessory view format)
    for i, accessory in enumerate(search_results[start_idx:end_idx], start_idx + 1):
        # Format accessory details like original accessory view
        details = f"🔧 {accessory.name}\n"
        details += language_handler.get_text("accessory_price", update.effective_user.id, price=f"${accessory.price:,.2f}") + "\n"
        details += language_handler.get_text("accessory_location", update.effective_user.id, location=accessory.location) + "\n"
        details += language_handler.get_text("accessory_type", update.effective_user.id, type=accessory.type) + "\n"
        
        # Add rating with stars
        stars = "⭐" * int(accessory.rating)
        if accessory.rating % 1 >= 0.5:
            stars += "⭐"
        details += language_handler.get_text("accessory_rating", update.effective_user.id, rating=accessory.rating, stars=stars) + "\n"
        
        if hasattr(accessory, 'warranty') and accessory.warranty:
            details += language_handler.get_text("accessory_warranty", update.effective_user.id, warranty=accessory.warranty) + "\n"
        
        if hasattr(accessory, 'voltage') and accessory.voltage and accessory.voltage != "N/A":
            details += language_handler.get_text("accessory_voltage", update.effective_user.id, voltage=accessory.voltage) + "\n"
            
        if hasattr(accessory, 'capacity') and accessory.capacity and accessory.capacity != "N/A":
            details += language_handler.get_text("accessory_capacity", update.effective_user.id, capacity=accessory.capacity) + "\n"
        
        if accessory.description:
            details += f"\n📝 {accessory.description[:100]}{'...' if len(accessory.description) > 100 else ''}\n"
        
        details += language_handler.get_text("accessory_count", update.effective_user.id, current=i, total=len(search_results))
        
        # Create keyboard with action buttons (matching original accessory view)
        keyboard_buttons = [
            [InlineKeyboardButton(language_handler.get_text("contact_seller", update.effective_user.id), callback_data=f"contact_accessory_{accessory.id}"),
             InlineKeyboardButton(language_handler.get_text("add_to_favourites", update.effective_user.id), callback_data=f"favourite_accessory_{accessory.id}")]
        ]
        
        # Add "View More Results" button if there are more accessories to show
        if end_idx < len(search_results):
            keyboard_buttons.append([InlineKeyboardButton(language_handler.get_text("view_more_accessories", update.effective_user.id), callback_data=f"more_accessory_results_{end_idx}")])
        
        # Add navigation buttons
        keyboard_buttons.extend([
            [InlineKeyboardButton(language_handler.get_text("modify_filters", update.effective_user.id), callback_data="accessory_search_filters")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
        ])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        
        # Send images using the same robust approach as regular accessory view
        try:
            chat_id = update.effective_chat.id
            bot = context.bot
            service = AccessoryService()
            
            photo_sent = False
            
            # Try to send image if available
            if accessory.image and accessory.image.strip():
                # List of image URLs to try in order
                image_urls = []
                
                # Add R2 URL
                try:
                    r2_url = await service.get_full_image_url(accessory.image)
                    if r2_url and r2_url.strip():
                        image_urls.append((r2_url, "R2 storage"))
                except Exception as e:
                    print(f"🔍 Error getting R2 URL: {e}")
                
                # Add fallback URL
                try:
                    fallback_url = service.get_fallback_image_url(accessory.image)
                    if fallback_url and fallback_url.strip():
                        image_urls.append((fallback_url, "API storage"))
                except Exception as e:
                    print(f"🔍 Error getting fallback URL: {e}")
                
                # Try each URL until one works
                for image_url, source_name in image_urls:
                    try:
                        print(f"🔍 Trying {source_name}: {image_url}")
                        
                        # For R2 URLs, try different approaches
                        if "r2.dev" in image_url:
                            # Try with different user agent or headers
                            import aiohttp
                            try:
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                                        if response.status == 200:
                                            image_data = await response.read()
                                            print(f"🔍 Downloaded {len(image_data)} bytes from R2")
                                            
                                            # Send as bytes instead of URL
                                            await bot.send_photo(
                                                chat_id=chat_id,
                                                photo=image_data,
                                                caption=details,
                                                parse_mode='Markdown'
                                            )
                                            
                                            # Send action buttons as separate message
                                            await bot.send_message(
                                                chat_id=chat_id,
                                                text=language_handler.get_text("actions", update.effective_user.id),
                                                reply_markup=keyboard
                                            )
                                            photo_sent = True
                                            print(f"✅ Successfully sent photo data from {source_name}")
                                            break
                            except Exception as download_e:
                                print(f"❌ Failed to download from R2: {download_e}")
                                # Fallback to direct URL
                                pass
                        
                        # Try direct URL sending (for non-R2 or if download failed)
                        if not photo_sent:
                            await bot.send_photo(
                                chat_id=chat_id,
                                photo=image_url,
                                caption=details,
                                parse_mode='Markdown'
                            )
                            
                            # Send action buttons as separate message
                            await bot.send_message(
                                chat_id=chat_id,
                                text=language_handler.get_text("choose_action", update.effective_user.id),
                                reply_markup=keyboard
                            )
                            photo_sent = True
                            print(f"✅ Successfully sent photo URL from {source_name}")
                            break
                            
                    except Exception as e:
                        print(f"❌ Failed to send photo from {source_name}: {e}")
                        continue
            
            # If no image was sent, send text message
            if not photo_sent:
                fallback_message = f"🔧 {details}"
                if accessory.image:
                    fallback_message += "\n\n" + language_handler.get_text("image_not_available", update.effective_user.id)
                
                await bot.send_message(
                    chat_id=chat_id,
                    text=fallback_message,
                    parse_mode='Markdown'
                )
                
                # Send action buttons as separate message
                await bot.send_message(
                    chat_id=chat_id,
                    text=language_handler.get_text("choose_action", update.effective_user.id),
                    reply_markup=keyboard
                )
                print(f"📝 Sent text message as fallback")
                
        except Exception as e:
            print(f"❌ Error sending accessory card: {e}")
            # Final fallback to text message
            try:
                fallback_message = f"🔧 {details}\n\n" + language_handler.get_text("error_loading_content", update.effective_user.id)
                if chat_id and bot:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=fallback_message,
                        parse_mode='Markdown'
                    )
                    
                    # Send action buttons as separate message
                    await bot.send_message(
                        chat_id=chat_id,
                        text=language_handler.get_text("choose_action", update.effective_user.id),
                        reply_markup=keyboard
                    )
            except Exception as final_e:
                print(f"❌ Final fallback failed: {final_e}")

async def handle_more_accessory_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Results' button for accessory search"""
    query = update.callback_query
    offset = int(query.data.replace('more_accessory_results_', ''))
    
    await query.answer()
    await show_accessory_search_results_page(update, context, offset)