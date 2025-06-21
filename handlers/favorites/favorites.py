from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from models.core.user import User, users
from models.core.product import products
from models.core.accessory import Accessory
from utils.services.accessory_service import AccessoryService
from models.data.favourite import Favourite, favourites
from utils.ui.keyboards import Keyboards
from utils.ui.language import language_handler
from utils.services.user_api_service import user_api_service
from utils.services.favorites_api_service import add_to_favorites_api, remove_from_favorites_api
from handlers.base import get_or_create_user
from datetime import datetime
import httpx

# Removed validate_image_url function - following car_catalog approach

async def view_favourites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    user = await get_or_create_user(update.effective_user)
    user_id = user.get('id') or user.get('telegram_id')
    # Try to get favorites from API first, fallback to local list
    try:
        api_favorites = await user_api_service.get_user_favorites(telegram_id)
        if api_favorites:
            user_favourites = api_favorites
        else:
            user_favourites = [fav for fav in favourites if fav.user_id == user_id]
    except Exception:
        # Fallback to local list if API fails
        user_favourites = [fav for fav in favourites if fav.user_id == user_id]
    
    if not user_favourites:
        # Send NEW message instead of editing
        await query.message.reply_text(
            language_handler.get_text("no_favourites", telegram_id),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(language_handler.get_text("browse_more_cars", telegram_id), callback_data="view_cars")],
                [InlineKeyboardButton(language_handler.get_text("browse_more_accessory", telegram_id), callback_data="view_accessories")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
            ])
        )
        return
    
    # Send header message
    await query.message.reply_text(
        language_handler.get_text("your_favourites", telegram_id),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
        ])
    )
    
    # Handle both API format (dict) and local format (object)
    # Get accessories from API for favorites
    accessory_service = AccessoryService()
    all_accessories = await accessory_service.fetch_all_accessories()
    
    if user_favourites and isinstance(user_favourites[0], dict):
        # API format
        favourite_cars = [car for car in products if any(fav.get('car_id') == car.id for fav in user_favourites)]
        # Support accessories in API format
        favourite_accessories = [acc for acc in all_accessories if any(fav.get('accessory_id') == acc.id for fav in user_favourites if fav.get('accessory_id'))]
    else:
        # Local format
        favourite_cars = [car for car in products if any(fav.car_id == car.id for fav in user_favourites if fav.car_id)]
        favourite_accessories = [acc for acc in all_accessories if any(fav.accessory_id == acc.id for fav in user_favourites if fav.accessory_id)]
    
    for car in favourite_cars:
        details = f"{language_handler.get_text('car_name', telegram_id, name=f'{car.brand} {car.model}')}\n"
        details += f"{language_handler.get_text('car_price', telegram_id, price=f'${car.price:,.2f}')}\n"
        details += f"{language_handler.get_text('car_location', telegram_id, location=car.location)}\n"
        if hasattr(car, 'category') and car.category:
            details += f"{language_handler.get_text('car_type', telegram_id, type=car.category)}\n"
        # Note: Rating not available in Product model, using default
        details += f"{language_handler.get_text('car_rating', telegram_id, rating='0')}\n"
        if car.description:
            details += f"\n📝 {car.description}"
        
        # Send each car with gallery support
        try:
            # Check if car has gallery images
            if hasattr(car, 'gallery') and car.gallery and len(car.gallery) > 0:
                # Create media group with main image + gallery
                media_group = []
                
                # Add main image first
                if car.image_url and car.image_url.startswith(('http://', 'https://')) and car.image_url != '🚗':
                    media_group.append(InputMediaPhoto(media=car.image_url, caption=details))
                
                # Add gallery images
                for gallery_img in car.gallery:
                    if gallery_img and gallery_img.startswith(('http://', 'https://')):
                        media_group.append(InputMediaPhoto(media=gallery_img))
                
                if media_group:
                    # Send media group
                    await query.message.reply_media_group(media=media_group)
                    
                    # Send action buttons as separate message with Actions header
                    actions_keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        "🔽 Actions",
                        reply_markup=InlineKeyboardMarkup(actions_keyboard)
                    )
                else:
                    # Fallback to text if no valid images
                    keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        text=details,
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
            else:
                # Single image or text message
                if car.image_url and car.image_url.startswith(('http://', 'https://')) and car.image_url != '🚗':
                    try:
                        await query.message.reply_photo(
                            photo=car.image_url,
                            caption=details
                        )
                        # Send action buttons as separate message with Actions header
                        actions_keyboard = [
                            [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                             InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                        ]
                        await query.message.reply_text(
                            "🔽 Actions",
                            reply_markup=InlineKeyboardMarkup(actions_keyboard)
                        )
                    except Exception:
                        keyboard = [
                            [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                             InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                        ]
                        await query.message.reply_text(
                            text=details,
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
                else:
                    keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        text=details,
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
        except Exception as e:
            print(f"❌ Error sending car details: {e}")
            # Final fallback to text message
            keyboard = [
                [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                 InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
            ]
            await query.message.reply_text(
                text=details,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    # Display favourite accessories
    for accessory in favourite_accessories:
        details = f"{language_handler.get_text('accessory_name', telegram_id, name=accessory.name)}\n"
        details += f"{language_handler.get_text('accessory_price', telegram_id, price=f'${accessory.price:,.2f}')}\n"
        details += f"{language_handler.get_text('accessory_location', telegram_id, location=accessory.location)}\n"
        if hasattr(accessory, 'category') and accessory.category:
            details += f"{language_handler.get_text('accessory_type', telegram_id, type=accessory.category)}\n"
        details += f"{language_handler.get_text('accessory_rating', telegram_id, rating=accessory.rating)}\n"
        if accessory.description:
            details += f"\n📝 {accessory.description}"
        
        # Send accessory with image support
        try:
            # Get full image URL using the accessory's method
            image_url = accessory.get_full_image_url()
            
            # Validate image URL before sending
            valid_image = False
            print(f"🔍 DEBUG: Checking image URL: {image_url}")
            if image_url and image_url.startswith(('http://', 'https://')):
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.head(image_url, timeout=5)
                        content_type = response.headers.get('content-type', '').lower()
                        print(f"🔍 DEBUG: Status: {response.status_code}, Content-Type: {content_type}")
                        if response.status_code == 200 and content_type.startswith('image/'):
                            valid_image = True
                            print(f"✅ DEBUG: Image validation passed")
                        else:
                            print(f"❌ DEBUG: Image validation failed - status: {response.status_code}, type: {content_type}")
                except Exception as e:
                    print(f"❌ DEBUG: Validation exception: {e}")
                    pass  # Silently fail validation, will fall back to text
            else:
                print(f"❌ DEBUG: Invalid URL format or empty URL")
            
            print(f"🔍 DEBUG: Final valid_image result: {valid_image}")
            
            if valid_image:
                try:
                    # Download image and send as bytes instead of URL
                    async with httpx.AsyncClient() as client:
                        img_response = await client.get(image_url, timeout=10)
                        if img_response.status_code == 200:
                            await query.message.reply_photo(
                                photo=img_response.content,
                                caption=details
                            )
                        else:
                            raise Exception(f"Failed to download image: {img_response.status_code}")
                    # Send action buttons as separate message
                    actions_keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_accessory_{accessory.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_accessory_{accessory.id}")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        "🔽 Actions",
                        reply_markup=InlineKeyboardMarkup(actions_keyboard)
                    )
                except Exception as e:
                    print(f"❌ Image failed ({str(e)[:50]}...), sending text instead")
                    # Fallback to text message
                    keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_accessory_{accessory.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_accessory_{accessory.id}")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        text=f"🖼️ Image not available\n\n{details}",
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
            else:
                keyboard = [
                    [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_accessory_{accessory.id}"),
                     InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_accessory_{accessory.id}")],
                    [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                ]
                await query.message.reply_text(
                    text=details,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        except Exception as e:
            print(f"❌ Error sending accessory details: {e}")
            keyboard = [
                [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_accessory_{accessory.id}"),
                 InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_accessory_{accessory.id}")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
            ]
            await query.message.reply_text(
                text=details,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

async def handle_favourite_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    car_id = int(query.data.replace("favourite_", ""))
    user = await get_or_create_user(update.effective_user)
    user_id = user.get('id') or user.get('telegram_id')
    
    # Try to add to favorites via API first
    try:
        api_favorites = await user_api_service.get_user_favorites(telegram_id)
        
        # Check if already favourited (API format)
        if api_favorites and any(fav.get('car_id') == car_id for fav in api_favorites):
            await query.message.reply_text(
                language_handler.get_text("already_favourited_message", telegram_id),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(language_handler.get_text("view_my_favourites", telegram_id), callback_data="view_favourites")],
                    [InlineKeyboardButton(language_handler.get_text("browse_more_cars", telegram_id), callback_data="view_cars")],
                    [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                ])
            )
            return
        
        # Check favourites limit
        if api_favorites and len(api_favorites) >= 5:
            await query.answer(language_handler.get_text("favourites_limit", telegram_id))
            return
        
        # Try to add via API
        success = await user_api_service.add_favorite(telegram_id, car_id)
        if not success:
            # Fallback to local storage
            raise Exception("API add failed")
            
    except Exception:
        # Fallback to local storage
        existing_favourite = next((f for f in favourites if f.user_id == user_id and f.car_id == car_id), None)
        if existing_favourite:
            await query.message.reply_text(
                language_handler.get_text("already_favourited_message", telegram_id),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(language_handler.get_text("view_my_favourites", telegram_id), callback_data="view_favourites")],
                    [InlineKeyboardButton(language_handler.get_text("browse_more_accessory", telegram_id), callback_data="view_cars")],
                    [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                ])
            )
            return
        
        # Check favourites limit
        user_favourites_count = len([f for f in favourites if f.user_id == user_id])
        if user_favourites_count >= 5:
            await query.answer(language_handler.get_text("favourites_limit", telegram_id))
            return
        
        # Add to local favourites
        favourite = Favourite(
            id=len(favourites) + 1,
            user_id=user_id,
            car_id=car_id,
            saved_at=datetime.now()
        )
        favourites.append(favourite)
    
    car = next((car for car in products if car.id == car_id), None)
    if car:
        details = language_handler.get_text("added_to_favourites", telegram_id) + "\n\n"
        details += f"🚗 {car.brand} {car.model}\n"
        details += language_handler.get_text("car_price", telegram_id, price=f"${car.price:,.2f}") + "\n"
        details += language_handler.get_text("car_location", telegram_id, location=car.location) + "\n"
        if car.description:
            details += f"\n📝 {car.description}"
        
        # Send car details with gallery support
        try:
            # Check if car has gallery images
            if hasattr(car, 'gallery') and car.gallery and len(car.gallery) > 0:
                # Create media group with main image + gallery
                media_group = []
                
                # Add main image first
                if car.image_url and car.image_url.startswith(('http://', 'https://')) and car.image_url != '🚗':
                    media_group.append(InputMediaPhoto(media=car.image_url, caption=details))
                
                # Add gallery images
                for gallery_img in car.gallery:
                    if gallery_img and gallery_img.startswith(('http://', 'https://')):
                        media_group.append(InputMediaPhoto(media=gallery_img))
                
                if media_group:
                    # Send media group
                    await query.message.reply_media_group(media=media_group)
                    
                    # Send action buttons as separate message with Actions header
                    actions_keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                        [InlineKeyboardButton(language_handler.get_text("view_more_cars", telegram_id), callback_data="view_cars")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        "🔽 Actions",
                        reply_markup=InlineKeyboardMarkup(actions_keyboard)
                    )
                else:
                    # Fallback to text if no valid images
                    actions_keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                        [InlineKeyboardButton(language_handler.get_text("view_more_cars", telegram_id), callback_data="view_cars")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        text=details,
                        reply_markup=InlineKeyboardMarkup(actions_keyboard)
                    )
            else:
                # Single image or text message
                if car.image_url and car.image_url.startswith(('http://', 'https://')) and car.image_url != '🚗':
                    try:
                        await query.message.reply_photo(
                            photo=car.image_url,
                            caption=details
                        )
                        # Send action buttons as separate message with Actions header
                        actions_keyboard = [
                            [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                             InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                            [InlineKeyboardButton(language_handler.get_text("view_more_cars", telegram_id), callback_data="view_cars")],
                            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                        ]
                        await query.message.reply_text(
                            "🔽 Actions",
                            reply_markup=InlineKeyboardMarkup(actions_keyboard)
                        )
                    except Exception as e:
                        print(f"❌ Failed to send photo: {e}")
                        actions_keyboard = [
                            [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                             InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                            [InlineKeyboardButton(language_handler.get_text("view_more_cars", telegram_id), callback_data="view_cars")],
                            [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                        ]
                        await query.message.reply_text(
                            text=details,
                            reply_markup=InlineKeyboardMarkup(actions_keyboard)
                        )
                else:
                    actions_keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                        [InlineKeyboardButton(language_handler.get_text("view_more_cars", telegram_id), callback_data="view_cars")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        text=details,
                        reply_markup=InlineKeyboardMarkup(actions_keyboard)
                    )
        except Exception as e:
            print(f"❌ Error sending car details: {e}")
            # Final fallback to text message
            actions_keyboard = [
                [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_{car.id}"),
                 InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_{car.id}")],
                [InlineKeyboardButton(language_handler.get_text("view_more_cars", telegram_id), callback_data="view_cars")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
            ]
            await query.message.reply_text(
                text=details,
                reply_markup=InlineKeyboardMarkup(actions_keyboard)
            )

async def handle_add_to_favourites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This function is now handled by handle_favourite_car for consistency
    # Redirect to the main handler
    await handle_favourite_car(update, context)

async def handle_unfavourite_car(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    car_id = int(query.data.replace("unfavourite_", ""))
    user = await get_or_create_user(update.effective_user)
    user_id = user.get('id') or user.get('telegram_id')
    
    # Try to remove from favorites via API first
    try:
        success = await user_api_service.remove_favorite(telegram_id, car_id)
        if not success:
            # Fallback to local storage
            raise Exception("API remove failed")
    except Exception:
        # Fallback to local storage
        favourites[:] = [f for f in favourites if not (f.user_id == user_id and f.car_id == car_id)]
    
    # Show brief confirmation and redirect to favorites view
    car = next((car for car in products if car.id == car_id), None)
    if car:
        confirmation_msg = language_handler.get_text("removed_from_favourites", telegram_id) + f" {car.brand} {car.model}"
        await query.message.reply_text(confirmation_msg)
    
    # Automatically redirect to the main favorites view
    await view_favourites(update, context)

async def handle_favourite_accessory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle adding accessories to favorites"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    accessory_id = int(query.data.replace("favourite_accessory_", ""))
    user = await get_or_create_user(update.effective_user)
    user_id = user.get('id') or user.get('telegram_id')
    
    # Check if already favourited
    existing_favourite = next((f for f in favourites if f.user_id == user_id and f.accessory_id == accessory_id), None)
    if existing_favourite:
        await query.message.reply_text(
            language_handler.get_text("already_favourited_message", telegram_id),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(language_handler.get_text("view_my_favourites", telegram_id), callback_data="view_favourites")],
                [InlineKeyboardButton(language_handler.get_text("browse_more_accessory", telegram_id), callback_data="view_accessories")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
            ])
        )
        return
    
    # Check favourites limit
    user_favourites_count = len([f for f in favourites if f.user_id == user_id])
    if user_favourites_count >= 5:
        await query.answer(language_handler.get_text("favourites_limit", telegram_id))
        return
    
    # Add to favourites
    favourite = Favourite(
        id=len(favourites) + 1,
        user_id=user_id,
        accessory_id=accessory_id,
        saved_at=datetime.now()
    )
    favourites.append(favourite)
    
    # Get accessory from API
    accessory_service = AccessoryService()
    all_accessories = await accessory_service.fetch_all_accessories()
    accessory = next((acc for acc in all_accessories if acc.id == accessory_id), None)
    if accessory:
        details = language_handler.get_text("added_to_favourites", telegram_id) + "\n\n"
        details += f"🔧 {language_handler.get_text('accessory_name', telegram_id, name=accessory.name)}\n"
        details += f"💰 {language_handler.get_text('accessory_price', telegram_id, price=f'${accessory.price:,.2f}')}\n"
        details += f"📍 {language_handler.get_text('accessory_location', telegram_id, location=accessory.location)}\n"
        details += f"⭐ {language_handler.get_text('accessory_rating', telegram_id, rating=accessory.rating)}\n"
        if accessory.description:
            details += f"\n📝 {accessory.description}"
        
        # Send accessory details with image support
        try:
            # Get full image URL using the accessory's method
            image_url = accessory.get_full_image_url()
            
            # Validate image URL before sending
            valid_image = False
            print(f"🔍 DEBUG ACCESSORY: Checking image URL: {image_url}")
            if image_url and image_url.startswith(('http://', 'https://')):
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.head(image_url, timeout=5)
                        content_type = response.headers.get('content-type', '').lower()
                        print(f"🔍 DEBUG ACCESSORY: Status: {response.status_code}, Content-Type: {content_type}")
                        if response.status_code == 200 and content_type.startswith('image/'):
                            valid_image = True
                            print(f"✅ DEBUG ACCESSORY: Image validation passed")
                        else:
                            print(f"❌ DEBUG ACCESSORY: Image validation failed - status: {response.status_code}, type: {content_type}")
                except Exception as e:
                    print(f"❌ DEBUG ACCESSORY: Validation exception: {e}")
                    pass  # Silently fail validation, will fall back to text
            else:
                print(f"❌ DEBUG ACCESSORY: Invalid URL format or empty URL")
            
            print(f"🔍 DEBUG ACCESSORY: Final valid_image result: {valid_image}")
            
            if valid_image:
                try:
                    # Download image and send as bytes instead of URL
                    async with httpx.AsyncClient() as client:
                        img_response = await client.get(image_url, timeout=10)
                        if img_response.status_code == 200:
                            await query.message.reply_photo(
                                photo=img_response.content,
                                caption=details
                            )
                        else:
                            raise Exception(f"Failed to download image: {img_response.status_code}")
                    # Send action buttons as separate message
                    actions_keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_accessory_{accessory.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_accessory_{accessory.id}")],
                        [InlineKeyboardButton(language_handler.get_text("browse_more_accessory", telegram_id), callback_data="view_accessories")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        "🔽 Actions",
                        reply_markup=InlineKeyboardMarkup(actions_keyboard)
                    )
                except Exception as e:
                    print(f"❌ Image failed ({str(e)[:50]}...), sending text instead")
                    # Fallback to text message
                    actions_keyboard = [
                        [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_accessory_{accessory.id}"),
                         InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_accessory_{accessory.id}")],
                        [InlineKeyboardButton(language_handler.get_text("browse_more_accessory", telegram_id), callback_data="view_accessories")],
                        [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                    ]
                    await query.message.reply_text(
                        text=f"🖼️ Image not available\n\n{details}",
                        reply_markup=InlineKeyboardMarkup(actions_keyboard)
                    )
            else:
                actions_keyboard = [
                    [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_accessory_{accessory.id}"),
                     InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_accessory_{accessory.id}")],
                    [InlineKeyboardButton(language_handler.get_text("browse_more_accessory", telegram_id), callback_data="view_accessories")],
                    [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
                ]
                await query.message.reply_text(
                    text=details,
                    reply_markup=InlineKeyboardMarkup(actions_keyboard)
                )
        except Exception as e:
            print(f"❌ Error sending accessory details: {e}")
            # Final fallback to text message
            actions_keyboard = [
                [InlineKeyboardButton(language_handler.get_text("contact_seller", telegram_id), callback_data=f"contact_accessory_{accessory.id}"),
                 InlineKeyboardButton(language_handler.get_text("remove_from_favourites", telegram_id), callback_data=f"unfavourite_accessory_{accessory.id}")],
                [InlineKeyboardButton(language_handler.get_text("browse_more_accessory", telegram_id), callback_data="view_accessories")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", telegram_id), callback_data="back_to_main")]
            ]
            await query.message.reply_text(
                text=details,
                reply_markup=InlineKeyboardMarkup(actions_keyboard)
            )

async def handle_unfavourite_accessory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle removing accessories from favorites"""
    query = update.callback_query
    await query.answer()
    
    telegram_id = update.effective_user.id
    accessory_id = int(query.data.replace("unfavourite_accessory_", ""))
    user = await get_or_create_user(update.effective_user)
    user_id = user.get('id') or user.get('telegram_id')
    
    # Remove from favourites
    favourites[:] = [f for f in favourites if not (f.user_id == user_id and f.accessory_id == accessory_id)]
    
    # Show brief confirmation and redirect to favorites view
    # Get accessory from API
    accessory_service = AccessoryService()
    all_accessories = await accessory_service.fetch_all_accessories()
    accessory = next((acc for acc in all_accessories if acc.id == accessory_id), None)
    if accessory:
        confirmation_msg = language_handler.get_text("removed_from_favourites", telegram_id) + f" {accessory.name}"
        await query.message.reply_text(confirmation_msg)
    
    # Automatically redirect to the main favorites view
    await view_favourites(update, context)