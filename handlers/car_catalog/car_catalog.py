# Add this import at the top
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, error
from telegram.ext import ContextTypes
from datetime import datetime
from models.core.product import Product, products  # Changed from Car, cars
from utils.ui.keyboards import Keyboards
from utils.ui.language import language_handler
# Add this import

async def view_cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(language_handler.get_text("loading_cars", update.effective_user.id))
    
    # Check available cars first
    available_cars = [car for car in products if car.status == "available"]
    
    if not available_cars:
        # No cars available - show no cars keyboard
        message = language_handler.get_text("no_cars_available", update.effective_user.id)
        keyboard = Keyboards.get_no_cars_keyboard(update.effective_user.id)
    else:
        # Cars available - show brand selection
        message = language_handler.get_text("select_car_brand", update.effective_user.id)
        keyboard = Keyboards.car_brands(available_cars, update.effective_user.id, False)
    
    # Send NEW message instead of editing
    await query.message.reply_text(
        message,
        reply_markup=keyboard
    )
    
async def handle_brand_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    brand = query.data.replace("brand_", "")
    await query.answer(language_handler.get_text("loading_brand_cars", update.effective_user.id, brand=brand))
    
    brand_cars = [car for car in products if car.brand == brand and car.status == "available"]
    
    if not brand_cars:
        await query.message.reply_text(
            language_handler.get_text("no_brand_cars", update.effective_user.id, brand=brand),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(language_handler.get_text("check_other_brands", update.effective_user.id), callback_data="view_cars")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
            ])
        )
        return
    
    # Store brand cars in context for pagination
    context.user_data['current_brand'] = brand
    context.user_data['brand_cars'] = brand_cars
    context.user_data['cars_offset'] = 0
    
    # Show first 5 cars
    await show_brand_cars_page(update, context, 0)

async def show_brand_cars_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int):
    """Display a page of cars for the selected brand"""
    query = update.callback_query if update.callback_query else None
    
    brand = context.user_data.get('current_brand')
    brand_cars = context.user_data.get('brand_cars', [])
    
    # Calculate pagination
    cars_per_page = 5
    start_idx = offset
    end_idx = min(start_idx + cars_per_page, len(brand_cars))
    page_cars = brand_cars[start_idx:end_idx]
    
    # Update offset in context
    context.user_data['cars_offset'] = offset
    
    for i, car in enumerate(page_cars, start_idx + 1):
        details = f"🚗 {car.brand} {car.model}\n"
        details += language_handler.get_text("car_price", update.effective_user.id, price=f"${car.price:,.2f}") + "\n"
        details += language_handler.get_text("car_location", update.effective_user.id, location=car.location) + "\n"
        if car.description:
            details += f"\n📝 {car.description}"
        details += language_handler.get_text("car_count", update.effective_user.id, current=i, total=len(brand_cars))
        
        # Create keyboard with pagination buttons
        keyboard_buttons = [
            [InlineKeyboardButton(language_handler.get_text("contact_seller", update.effective_user.id), callback_data=f"contact_{car.id}"),
             InlineKeyboardButton(language_handler.get_text("add_to_favourites", update.effective_user.id), callback_data=f"favourite_{car.id}")]
        ]
        
        # Add "View More Cars" button if there are more cars to show (with translation)
        if end_idx < len(brand_cars):
            keyboard_buttons.append([InlineKeyboardButton(language_handler.get_text("view_more_cars", update.effective_user.id), callback_data=f"more_cars_{brand}_{end_idx}")])
        
        # Add navigation buttons
        keyboard_buttons.extend([
            [InlineKeyboardButton(language_handler.get_text("check_other_brands", update.effective_user.id), callback_data="view_cars")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
        ])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        
        # Send images first (without buttons)
        message_sent = False
        
        if car.gallery and len(car.gallery) > 0:
            # Create media group with main image and gallery images
            media_group = []
            
            # Validate and add main image with caption
            if car.image_url and car.image_url.strip():
                try:
                    media_group.append(InputMediaPhoto(media=car.image_url.strip(), caption=details))
                    print(f"✅ Added main image: {car.image_url[:50]}...")
                except Exception as e:
                    print(f"❌ Failed to add main image {car.image_url}: {e}")
            
            # Validate and add gallery images (up to 9 more images, total 10 max for Telegram)
            valid_gallery_count = 0
            for i, gallery_img in enumerate(car.gallery[:9]):
                if gallery_img and gallery_img.strip():
                    try:
                        clean_url = gallery_img.strip().rstrip(',')
                        if clean_url.startswith('http') and '.' in clean_url:
                            media_group.append(InputMediaPhoto(media=clean_url))
                            valid_gallery_count += 1
                            print(f"✅ Added gallery image {i+1}: {clean_url[:50]}...")
                        else:
                            print(f"⚠️ Skipped invalid gallery URL {i+1}: {gallery_img}")
                    except Exception as e:
                        print(f"❌ Failed to add gallery image {i+1} ({gallery_img}): {e}")
            
            # Only send media group if we have valid images
            if len(media_group) > 0:
                try:
                    if query:
                        sent_messages = await query.message.reply_media_group(media=media_group)
                        print(f"📱 Media group sent with {len(sent_messages)} messages (1 main + {valid_gallery_count} gallery)")
                    else:
                        sent_messages = await update.message.reply_media_group(media=media_group)
                        print(f"📱 Media group sent with {len(sent_messages)} messages (1 main + {valid_gallery_count} gallery)")
                    message_sent = True
                except Exception as e:
                    print(f"❌ Failed to send media group with {len(media_group)} images: {e}")
                    # Log individual URLs for debugging
                    for idx, media in enumerate(media_group):
                        print(f"   Image {idx+1}: {media.media[:100]}...")
                    message_sent = False
            else:
                print(f"⚠️ No valid images found in media group for car {car.id}")
                message_sent = False
        else:
            # Send single image with product details (without buttons)
            if car.image_url and car.image_url.strip():
                clean_image_url = car.image_url.strip().rstrip(',')
                if clean_image_url.startswith('http') and '.' in clean_image_url:
                    try:
                        if query:
                            await query.message.reply_photo(
                                photo=clean_image_url,
                                caption=details
                            )
                        else:
                            await update.message.reply_photo(
                                photo=clean_image_url,
                                caption=details
                            )
                        message_sent = True
                    except Exception as e:
                        pass
                        message_sent = False
                else:
                    pass
                    message_sent = False
            else:
                pass
                message_sent = False
        
        # Always send action buttons as a separate message with translated label
        try:
            actions_text = language_handler.get_text("actions", update.effective_user.id)
            if query:
                await query.message.reply_text(
                    f"{actions_text}:",
                    reply_markup=keyboard
                )
            else:
                await update.message.reply_text(
                    f"{actions_text}:",
                    reply_markup=keyboard
                )
            pass
        except Exception as e:
            pass
        
        # Send fallback text message only if media group wasn't sent successfully
        if not message_sent:
            fallback_message = f"🚗 {details}\n\n⚠️ Image not available"
            if query:
                await query.message.reply_text(
                    fallback_message,
                    reply_markup=keyboard
                )
            else:
                await update.message.reply_text(
                    fallback_message,
                    reply_markup=keyboard
                )

async def handle_more_cars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Cars' button click"""
    query = update.callback_query
    
    # Parse callback data: more_cars_{brand}_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 3:
        brand = '_'.join(callback_parts[2:-1])  # Handle brands with underscores
        offset = int(callback_parts[-1])
        
        await query.answer(f"Loading more {brand} cars...")
        
        # Show next page of cars
        await show_brand_cars_page(update, context, offset)
    else:
        await query.answer("Error loading more cars")

# Gallery functionality removed for cleaner interface

