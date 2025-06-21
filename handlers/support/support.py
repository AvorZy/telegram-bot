from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime
from models.data.message import Message, messages
from models.core.user import users
from utils.ui.language import language_handler

async def contact_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = next((user for user in users if user.telegram_id == update.effective_user.id), None)
    if not user:
        # If user not found, create a default user_id or handle gracefully
        user_id = update.effective_user.id  # Use telegram_id as fallback
    else:
        user_id = user.id
    message = Message(
        id=len(messages) + 1,
        user_id=user_id,
        message="Support request initiated",
        direction="outbound",
        timestamp=datetime.now()
    )
    messages.append(message)
    
    # Change from edit_text to reply_text for conversational flow
    await query.message.reply_text(
        language_handler.get_text("contact_support_message", update.effective_user.id),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
        ])
    )
    context.user_data['awaiting_support_message'] = True