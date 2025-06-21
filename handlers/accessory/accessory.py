from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, error
from telegram.ext import ContextTypes
from datetime import datetime
from typing import List
from models.core.accessory import Accessory
from utils.services.accessory_service import AccessoryService
from utils.ui.keyboards import Keyboards
from utils.ui.language import language_handler
import aiohttp

async def is_valid_image_url(url: str) -> bool:
    """Check if URL points to a valid image by attempting to download first few bytes"""
    try:
        if not url or not url.strip():
            return False
            
        # Basic URL validation
        if not (url.startswith('http://') or url.startswith('https://')):
            return False
            
        async with aiohttp.ClientSession() as session:
            # Try to get first 1024 bytes to check if it's an image
            headers = {'Range': 'bytes=0-1023'}
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status in [200, 206]:  # 206 for partial content
                    content_type = response.headers.get('content-type', '').lower()
                    # Check content type or file extension
                    if content_type.startswith('image/'):
                        return True
                    # Fallback: check file extension
                    if any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']):
                        return True
                return False
    except Exception as e:
        print(f"🔍 Image validation error for {url}: {e}")
        return False

def create_accessory_types_keyboard(types: List[str], telegram_id: int) -> InlineKeyboardMarkup:
    """Create keyboard with accessory type buttons"""
    keyboard = []
    
    # Add type buttons in rows of 2
    for i in range(0, len(types), 2):
        row = []
        for j in range(2):
            if i + j < len(types):
                accessory_type = types[i + j]
                row.append(
                    InlineKeyboardButton(
                        f"🔧 {accessory_type}",
                        callback_data=f"accessory_type_{accessory_type}"
                    )
                )
        keyboard.append(row)
    
    # Add back button
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

def create_type_accessories_keyboard(
    accessories: List[Accessory], 
    accessory_type: str, 
    telegram_id: int
) -> InlineKeyboardMarkup:
    """Create keyboard with accessory buttons for a specific type"""
    keyboard = []
    
    # Add accessory buttons
    for i, accessory in enumerate(accessories):
        keyboard.append([
            InlineKeyboardButton(
                f"🔧 {accessory.name} - ${accessory.price}",
                callback_data=f"accessory_{i}_{accessory_type}"
            )
        ])
    
    # Add back button
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("accessories_back_to_types", telegram_id),
            callback_data="view_accessories"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

def create_accessory_navigation_keyboard(
    accessories: List[Accessory], 
    telegram_id: int, 
    accessory_type: str, 
    accessory_index: int
) -> InlineKeyboardMarkup:
    """Create navigation keyboard for accessory details"""
    keyboard = []
    
    # Back buttons (removed next/previous navigation)
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("accessories_back_to_list", telegram_id),
            callback_data=f"accessory_type_{accessory_type}"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            language_handler.get_text("back_to_menu", telegram_id),
            callback_data="back_to_main"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)

async def view_accessories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle viewing accessories - show types first"""
    query = update.callback_query
    await query.answer(language_handler.get_text("loading_accessories", update.effective_user.id))
    
    service = AccessoryService()
    
    try:
        # Get all unique accessory types
        types = await service.get_unique_types()
        
        if not types:
            # No accessories available
            message = language_handler.get_text("no_accessories_available", update.effective_user.id)
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    language_handler.get_text("back_to_menu", update.effective_user.id),
                    callback_data="back_to_main"
                )
            ]])
        else:
            # Accessories available - show type selection
            message = language_handler.get_text("select_accessory_type", update.effective_user.id)
            keyboard = create_accessory_types_keyboard(types, update.effective_user.id)
        
        # Send NEW message instead of editing
        await query.message.reply_text(
            message,
            reply_markup=keyboard
        )
        
    except Exception as e:
        print(f"Error in view_accessories: {e}")
        await query.message.reply_text(
            language_handler.get_text("accessories_error", update.effective_user.id),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    language_handler.get_text("back_to_menu", update.effective_user.id),
                    callback_data="back_to_main"
                )
            ]])
        )

async def handle_accessory_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle accessory type selection and show accessories of that type"""
    query = update.callback_query
    accessory_type = query.data.replace("accessory_type_", "")
    await query.answer(language_handler.get_text("loading_type_accessories", update.effective_user.id, type=accessory_type))
    
    service = AccessoryService()
    
    try:
        # Get accessories for this type
        type_accessories = await service.get_accessories_by_type(accessory_type)
        
        if not type_accessories:
            await query.message.reply_text(
                language_handler.get_text("no_type_accessories", update.effective_user.id, type=accessory_type),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(language_handler.get_text("check_other_types", update.effective_user.id), callback_data="view_accessories")],
                    [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
                ])
            )
            return
        
        # Store type accessories in context for pagination
        context.user_data['current_accessory_type'] = accessory_type
        context.user_data['type_accessories'] = type_accessories
        context.user_data['accessories_offset'] = 0
        
        # Show first 3 accessories
        await show_type_accessories_page(update, context, 0)
        
    except Exception as e:
        print(f"Error in handle_accessory_type_selection: {e}")
        await query.message.reply_text(
            language_handler.get_text("accessories_error", update.effective_user.id),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(language_handler.get_text("check_other_types", update.effective_user.id), callback_data="view_accessories")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
            ])
        )

async def show_type_accessories_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int):
    """Display a page of accessories for the selected type"""
    query = update.callback_query if update.callback_query else None
    
    service = AccessoryService()
    
    accessory_type = context.user_data.get('current_accessory_type')
    type_accessories = context.user_data.get('type_accessories', [])
    
    # Calculate pagination
    accessories_per_page = 3
    start_idx = offset
    end_idx = min(start_idx + accessories_per_page, len(type_accessories))
    page_accessories = type_accessories[start_idx:end_idx]
    
    # Update offset in context
    context.user_data['accessories_offset'] = offset
    
    for i, accessory in enumerate(page_accessories, start_idx + 1):
        # Format accessory details
        details = language_handler.get_text("accessory_name", update.effective_user.id, name=accessory.name) + "\n"
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
        
        details += language_handler.get_text("accessory_count", update.effective_user.id, current=i, total=len(type_accessories))
        
        # Create keyboard with action buttons
        keyboard_buttons = [
            [InlineKeyboardButton(language_handler.get_text("contact_seller", update.effective_user.id), callback_data=f"contact_accessory_{accessory.id}"),
             InlineKeyboardButton(language_handler.get_text("add_to_favourites", update.effective_user.id), callback_data=f"favourite_accessory_{accessory.id}")]
        ]
        
        # Add "View More Accessories" button if there are more accessories to show
        if end_idx < len(type_accessories):
            keyboard_buttons.append([InlineKeyboardButton(language_handler.get_text("view_more_accessories", update.effective_user.id), callback_data=f"more_accessories_{accessory_type}_{end_idx}")])
        
        # Add navigation buttons
        keyboard_buttons.extend([
            [InlineKeyboardButton(language_handler.get_text("check_other_types", update.effective_user.id), callback_data="view_accessories")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
        ])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        
        # Send accessory with image - simplified robust approach
        try:
            # Get the appropriate chat context
            chat_id = update.effective_chat.id if update.effective_chat else None
            bot = context.bot if context and context.bot else None
            
            if not chat_id or not bot:
                print(f"❌ Missing chat context for accessory {accessory.name}")
                continue
            
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
                        
                        # Validate image URL first
                        if not await is_valid_image_url(image_url):
                            print(f"❌ Invalid image URL from {source_name}: {image_url}")
                            continue
                        
                        # For R2 URLs, try downloading first then fallback to direct URL
                        if "r2.dev" in image_url or "cloudflare" in image_url:
                            try:
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                                        if response.status == 200:
                                            image_data = await response.read()
                                            print(f"🔍 Downloaded {len(image_data)} bytes from {source_name}")
                                            
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
                                print(f"❌ Failed to download from {source_name}: {download_e}")
                                # Continue to try direct URL sending
                        
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
                print(f"❌ Final fallback also failed: {final_e}")

async def handle_more_accessories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Accessories' button click"""
    query = update.callback_query
    
    # Parse callback data: more_accessories_{type}_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 3:
        accessory_type = '_'.join(callback_parts[2:-1])  # Handle types with underscores
        offset = int(callback_parts[-1])
        
        await query.answer(f"Loading more {accessory_type} accessories...")
        
        # Show next page of accessories
        await show_type_accessories_page(update, context, offset)
    else:
        await query.answer("Error loading more accessories")

async def handle_contact_accessory_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle contact seller for accessories"""
    query = update.callback_query
    accessory_id = int(query.data.replace("contact_accessory_", ""))
    
    service = AccessoryService()
    
    try:
        # Get accessory details
        accessory = await service.get_accessory_by_id(accessory_id)
        
        if accessory and hasattr(accessory, 'phone_number') and accessory.phone_number:
            # Create contact message with accessory details
            contact_message = language_handler.get_text("contact_seller_header", update.effective_user.id) + "\n\n"
            contact_message += language_handler.get_text("contact_accessory_name", update.effective_user.id, name=accessory.name) + "\n"
            contact_message += language_handler.get_text("contact_accessory_price", update.effective_user.id, price=f"${accessory.price:,.2f}") + "\n"
            contact_message += language_handler.get_text("contact_accessory_location", update.effective_user.id, location=accessory.location) + "\n\n"
            contact_message += language_handler.get_text("contact_phone", update.effective_user.id, phone=accessory.phone_number) + "\n\n"
            contact_message += language_handler.get_text("contact_tap_to_copy", update.effective_user.id)
            
            # Create keyboard with copy phone and back buttons
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(language_handler.get_text("copy_phone_number", update.effective_user.id), callback_data=f"copy_accessory_phone_{accessory.id}")],
                [InlineKeyboardButton(language_handler.get_text("back_to_accessories", update.effective_user.id), callback_data="view_accessories")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
            ])
            
            await query.answer(language_handler.get_text("contact_info_loaded", update.effective_user.id))
            await query.message.reply_text(
                contact_message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
        else:
            await query.answer(language_handler.get_text("contact_info_not_available", update.effective_user.id), show_alert=True)
            
    except Exception as e:
        print(f"Error in handle_contact_accessory_seller: {e}")
        await query.answer(language_handler.get_text("contact_info_error", update.effective_user.id), show_alert=True)

async def handle_copy_accessory_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle copying accessory seller's phone number"""
    query = update.callback_query
    accessory_id = int(query.data.replace("copy_accessory_phone_", ""))
    
    service = AccessoryService()
    
    try:
        # Get accessory details
        accessory = await service.get_accessory_by_id(accessory_id)
        
        if accessory and hasattr(accessory, 'phone_number') and accessory.phone_number:
            # Send phone number as a copyable message
            phone_message = language_handler.get_text("seller_phone_header", update.effective_user.id) + "\n\n"
            phone_message += f"`{accessory.phone_number}`\n\n"
            phone_message += language_handler.get_text("phone_accessory_name", update.effective_user.id, name=accessory.name) + "\n"
            phone_message += language_handler.get_text("phone_copy_instruction", update.effective_user.id)
            
            await query.answer(language_handler.get_text("phone_ready_to_copy", update.effective_user.id))
            await query.message.reply_text(
                phone_message,
                parse_mode='Markdown'
            )
        else:
            await query.answer(language_handler.get_text("phone_not_available", update.effective_user.id), show_alert=True)
            
    except Exception as e:
        print(f"Error in handle_copy_accessory_phone: {e}")
        await query.answer(language_handler.get_text("phone_error", update.effective_user.id), show_alert=True)