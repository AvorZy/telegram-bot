from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models.core.product import products  # Changed from cars
from utils.ui.language import language_handler
from handlers.base import get_or_create_user

async def handle_contact_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = await get_or_create_user(update.effective_user)
    
    car_id = int(query.data.replace("contact_", ""))
    car = next((car for car in products if car.id == car_id), None)
    
    if not car:
        await query.message.reply_text(
            language_handler.get_text("car_not_available", user['telegram_id']),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(language_handler.get_text("view_other_cars", user['telegram_id']), callback_data="view_cars")],
                [InlineKeyboardButton(language_handler.get_text("back_to_menu", user['telegram_id']), callback_data="back_to_main")]
            ])
        )
        return
    
    # Prepare contact message with seller information
    contact_message = f"{language_handler.get_text('contact_seller_title', user['telegram_id'])}\n\n"
    contact_message += f"{language_handler.get_text('car_label', user['telegram_id'])} {car.brand} {car.model}\n"
    contact_message += f"{language_handler.get_text('price_label', user['telegram_id'])} ${car.price:,.2f}\n\n"
    
    # Add seller contact information
    if car.phone_number:
        contact_message += f"{language_handler.get_text('seller_contact_info', user['telegram_id'])}\n"
        contact_message += f"{language_handler.get_text('phone_label', user['telegram_id'])} {car.phone_number}\n\n"
        contact_message += language_handler.get_text('contact_seller_instruction', user['telegram_id'])
    else:
        contact_message += language_handler.get_text('no_contact_info', user['telegram_id'])
    
    # Create keyboard with appropriate options
    keyboard = []
    
    if car.phone_number:
        # If phone number is available, add it as a callback button
        # Note: Telegram doesn't support tel: URLs in inline keyboards
        copy_phone_text = f"{language_handler.get_text('copy_phone_button', user['telegram_id'])} {car.phone_number}"
        keyboard.append([InlineKeyboardButton(copy_phone_text, callback_data=f"copy_phone_{car_id}")])
    
    keyboard.extend([
        [InlineKeyboardButton(language_handler.get_text("contact_support", user['telegram_id']), callback_data="contact_support")],
        [InlineKeyboardButton(language_handler.get_text("back_button", user['telegram_id']), callback_data=f"brand_{car.brand}")],
        [InlineKeyboardButton(language_handler.get_text("back_to_menu", user['telegram_id']), callback_data="back_to_main")]
    ])
    
    await query.message.reply_text(
        contact_message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    
    # Store car info for potential follow-up actions
    context.user_data['selected_car_id'] = car_id
    context.user_data['seller_phone'] = car.phone_number

async def handle_copy_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle copy phone number callback"""
    query = update.callback_query
    await query.answer()
    
    user = await get_or_create_user(update.effective_user)
    
    # Extract car_id from callback data
    car_id = int(query.data.replace("copy_phone_", ""))
    car = next((car for car in products if car.id == car_id), None)
    
    if not car or not car.phone_number:
        await query.answer(language_handler.get_text('phone_not_available', user['telegram_id']), show_alert=True)
        return
    
    # Send a message with the phone number that users can easily copy
    phone_message = f"{language_handler.get_text('seller_phone_title', user['telegram_id'])}\n\n`{car.phone_number}`\n\n"
    phone_message += f"{language_handler.get_text('how_to_contact_title', user['telegram_id'])}\n"
    phone_message += f"{language_handler.get_text('copy_instruction', user['telegram_id'])}\n"
    phone_message += f"{language_handler.get_text('dialer_instruction', user['telegram_id'])}\n"
    phone_message += f"{language_handler.get_text('mention_bot_instruction', user['telegram_id'])}\n\n"
    phone_message += f"{language_handler.get_text('car_label', user['telegram_id'])} {car.brand} {car.model}\n"
    phone_message += f"{language_handler.get_text('price_label', user['telegram_id'])} ${car.price:,.2f}"
    
    await query.message.reply_text(
        phone_message,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(language_handler.get_text('back_to_car_details', user['telegram_id']), callback_data=f"contact_{car_id}")]
        ])
    )