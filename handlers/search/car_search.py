from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from models.core.product import products  # Changed from cars
from utils.ui.keyboards import Keyboards
from utils.ui.language import language_handler
from utils.ui.filter_helpers import FilterHelpers
from utils.services.data_loader import car_data_loader
from typing import List, Dict, Any
import re

class SearchFilters:
    def __init__(self):
        self.price_min: float = 0
        self.price_max: float = 999999
        self.year_min: int = 1990
        self.year_max: int = 2024
        self.location: str = None
        self.brand: str = None
        self.model: str = None
        self.color: str = None
        self.category: str = None
        self.keyword: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'price_min': self.price_min,
            'price_max': self.price_max,
            'year_min': self.year_min,
            'year_max': self.year_max,
            'location': self.location,
            'brand': self.brand,
            'model': self.model,
            'color': self.color,
            'category': self.category,
            'keyword': self.keyword
        }
    
    def from_dict(self, data: Dict[str, Any]):
        self.price_min = data.get('price_min', 0)
        self.price_max = data.get('price_max', 999999)
        self.year_min = data.get('year_min', 1990)
        self.year_max = data.get('year_max', 2024)
        self.location = data.get('location')
        self.brand = data.get('brand')
        self.model = data.get('model')
        self.color = data.get('color')
        self.category = data.get('category')
        self.keyword = data.get('keyword')

async def handle_car_search_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show car search filters menu"""
    query = update.callback_query
    await query.answer()
    
    # Set search type context for car search
    context.user_data['current_search_type'] = 'car'
    
    # Initialize search filters if not exists
    if 'search_filters' not in context.user_data:
        context.user_data['search_filters'] = SearchFilters().to_dict()
    
    filters = context.user_data['search_filters']
    
    # Build current filters display
    filter_text = language_handler.get_text("current_filters", update.effective_user.id) + "\n"
    
    # Track if any filters are applied
    has_filters = False
    
    if filters['price_min'] > 0 or filters['price_max'] < 999999:
        filter_text += f"💰 ${filters['price_min']:,.0f} - ${filters['price_max']:,.0f}\n"
        has_filters = True
    
    if filters['year_min'] > 1990 or filters['year_max'] < 2024:
        filter_text += f"📅 {filters['year_min']} - {filters['year_max']}\n"
        has_filters = True
    
    if filters['location']:
        filter_text += f"📍 {filters['location']}\n"
        has_filters = True
    
    if filters['brand']:
        filter_text += f"🚗 {filters['brand']}\n"
        has_filters = True
    
    if filters['color']:
        filter_text += f"🎨 {filters['color']}\n"
        has_filters = True
    
    if filters['category']:
        filter_text += f"📂 {filters['category']}\n"
        has_filters = True
    
    if filters['keyword']:
        filter_text += f"🔤 {filters['keyword']}\n"
        has_filters = True
    
    # Add "No filters applied" only if no filters are set
    if not has_filters:
        filter_text += language_handler.get_text("no_filters_applied", update.effective_user.id) + "\n"
    
    # Build complete message
    message = language_handler.get_text("advanced_search_title", update.effective_user.id) + "\n\n" + filter_text + "\n" + language_handler.get_text("select_filter_or_apply", update.effective_user.id)
    
    # Send NEW message instead of editing
    await query.message.reply_text(
        message,
        reply_markup=Keyboards.car_search_menu(update.effective_user.id)
    )

async def handle_price_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle price range selection"""
    query = update.callback_query
    await query.answer()
    
    message = language_handler.get_text("search_by_price", update.effective_user.id) + "\n\n" + language_handler.get_text("select_price_range", update.effective_user.id)
    
    await query.edit_message_text(
        message,
        reply_markup=Keyboards.price_range_keyboard(update.effective_user.id)
    )

async def handle_year_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle year range selection"""
    query = update.callback_query
    await query.answer()
    
    message = language_handler.get_text("search_by_year", update.effective_user.id) + "\n\n" + language_handler.get_text("select_year_range", update.effective_user.id)
    
    await query.edit_message_text(
        message,
        reply_markup=Keyboards.year_range_keyboard(update.effective_user.id)
    )

async def handle_location_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle location selection"""
    query = update.callback_query
    await query.answer()
    
    message = language_handler.get_text("search_by_location", update.effective_user.id) + "\n\n" + language_handler.get_text("select_location", update.effective_user.id)
    
    await query.edit_message_text(
        message,
        reply_markup=Keyboards.location_keyboard(update.effective_user.id)
    )

async def handle_year_range_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific year range selection"""
    await FilterHelpers.handle_range_selection(
        update, context, 'year_', 
        ['year_min', 'year_max'], 
        'Year filter: {0} - {1}',
        handle_car_search_filters
    )

async def handle_price_range_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific price range selection - routes to appropriate handler based on search context"""
    # Check current search type and route to appropriate handler
    current_search_type = context.user_data.get('current_search_type', 'car')
    
    if current_search_type == 'accessory':
        # Import and call accessory price range handler
        from handlers.search.accessory_search import handle_accessory_price_range_selection
        await handle_accessory_price_range_selection(update, context)
        return
    
    # Default to car search handling
    query = update.callback_query
    price_data = query.data.replace('price_', '').split('_')
    price_min = int(price_data[0])
    price_max = int(price_data[1])
    
    await query.answer(f"Price filter: ${price_min:,} - ${price_max:,}")
    
    # Update car filters
    if 'search_filters' not in context.user_data:
        context.user_data['search_filters'] = SearchFilters().to_dict()
    
    context.user_data['search_filters']['price_min'] = price_min
    context.user_data['search_filters']['price_max'] = price_max
    
    # Return to car search menu
    await handle_car_search_filters(update, context)

async def handle_location_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific location selection"""
    await FilterHelpers.handle_option_selection(
        update, context, 'location_',
        'location', 'Location filter: {0}',
        handle_car_search_filters
    )

async def handle_brand_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle brand selection"""
    query = update.callback_query
    await query.answer()
    
    # Get brands with emojis from data_loader
    brand_emojis = car_data_loader.get_brands_with_emojis()
    brands = list(brand_emojis.keys())
    
    if not brands:
        # Fallback to existing logic if no data available
        available_brands = set()
        for product in products:
            if hasattr(product, 'brand') and product.brand:
                available_brands.add(product.brand)
        brands = sorted(list(available_brands))
        brand_emojis = {
            'Tesla': '⚡',
            'BMW': '🔷', 
            'Mercedes': '⭐',
            'Audi': '🔴',
            'Nissan': '🔵',
            'Toyota': '🟡',
            'Honda': '🔶',
            'Ford': '🔷',
            'Chevrolet': '🟨',
            'Hyundai': '🔸'
        }
    
    message = (f"{language_handler.get_text('search_by_brand', update.effective_user.id)}\n\n"
              f"{language_handler.get_text('select_brand', update.effective_user.id)}")
    
    await query.edit_message_text(
        message,
        reply_markup=Keyboards.brand_selection_keyboard(update.effective_user.id, language_handler, brands, brand_emojis)
    )

async def handle_brand_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific brand selection"""
    await FilterHelpers.handle_option_selection(
        update, context, 'brand_search_',
        'brand', 'Brand filter: {0}',
        handle_car_search_filters
    )

async def handle_color_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle color selection"""
    query = update.callback_query
    await query.answer()
    
    # Get colors with emojis from data_loader
    color_emojis = car_data_loader.get_colors_with_emojis()
    colors = list(color_emojis.keys())
    
    if not colors:
        # Fallback to existing logic if no data available
        available_colors = set()
        for product in products:
            if hasattr(product, 'color') and product.color:
                available_colors.add(product.color)
        colors = sorted(list(available_colors))
        color_emojis = {
            'Red': '🔴',
            'Blue': '🔵', 
            'Black': '⚫',
            'White': '⚪',
            'Silver': '⚪',
            'Gray': '🔘',
            'Green': '🟢',
            'Yellow': '🟡',
            'Orange': '🟠',
            'Purple': '🟣'
        }
    
    message = (f"{language_handler.get_text('search_by_color', update.effective_user.id)}\n\n"
              f"{language_handler.get_text('select_color', update.effective_user.id)}")
    
    await query.edit_message_text(
        message,
        reply_markup=Keyboards.color_selection_keyboard(update.effective_user.id, language_handler, colors, color_emojis)
    )

async def handle_color_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific color selection"""
    await FilterHelpers.handle_option_selection(
        update, context, 'color_search_',
        'color', 'Color filter: {0}',
        handle_car_search_filters
    )

async def handle_category_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category selection"""
    query = update.callback_query
    await query.answer()
    
    # Get categories with emojis from data_loader
    category_emojis = car_data_loader.get_categories_with_emojis()
    categories = list(category_emojis.keys())
    
    if not categories:
        # Fallback to existing logic if no data available
        available_categories = set()
        for product in products:
            if hasattr(product, 'category') and product.category:
                available_categories.add(product.category)
        categories = sorted(list(available_categories))
        category_emojis = {
            'Electric Vehicles': '⚡',
            'Sedan': '🚗',
            'SUV': '🚙',
            'Hatchback': '🚘',
            'Truck': '🚚',
            'Convertible': '🏎️',
            'Coupe': '🚗',
            'Wagon': '🚐'
        }
    
    message = (f"{language_handler.get_text('search_by_category', update.effective_user.id)}\n\n"
              f"{language_handler.get_text('select_category', update.effective_user.id)}")
    
    await query.edit_message_text(
        message,
        reply_markup=Keyboards.category_selection_keyboard(update.effective_user.id, language_handler, categories, category_emojis)
    )

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle specific category selection"""
    await FilterHelpers.handle_option_selection(
        update, context, 'category_search_',
        'category', 'Category filter: {0}',
        handle_car_search_filters
    )

async def handle_clear_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear all search filters"""
    query = update.callback_query
    await query.answer("All filters cleared!")
    
    # Reset filters
    context.user_data['search_filters'] = SearchFilters().to_dict()
    
    # Return to car search menu
    await handle_car_search_filters(update, context)
    
async def apply_search_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Apply current filters and show results"""
    query = update.callback_query
    await query.answer("Searching...")
    
    filters = context.user_data.get('search_filters', SearchFilters().to_dict())
    
    # Filter products based on criteria
    filtered_cars = []
    for car in products:  # Changed from cars to products
        if car.status != "available":
            continue
            
        # Price filter
        if not (filters['price_min'] <= float(car.price) <= filters['price_max']):
            continue
            
        # Year filter (extract from model or use default)
        car_year = extract_year_from_model(car.model)
        if not (filters['year_min'] <= car_year <= filters['year_max']):
            continue
            
        # Location filter
        if filters['location'] and filters['location'].lower() not in car.location.lower():
            continue
            
        # Brand filter
        if filters['brand'] and filters['brand'].lower() != car.brand.lower():
            continue
        
        # Color filter
        if filters['color'] and filters['color'].lower() != car.color.lower():
            continue
        
        # Category filter
        if filters['category'] and filters['category'].lower() != car.category.lower():
            continue
            
        # Keyword filter
        if filters['keyword']:
            keyword_lower = filters['keyword'].lower()
            if not any(keyword_lower in text.lower() for text in [
                car.brand, car.model, car.description or "", car.location
            ]):
                continue
        
        filtered_cars.append(car)
    
    if not filtered_cars:
        message = language_handler.get_text("no_search_results", update.effective_user.id)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(language_handler.get_text("modify_filters", update.effective_user.id), callback_data="car_search_filters")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
        ])
        await query.edit_message_text(message, reply_markup=keyboard)
    else:
        # Store filtered results
        context.user_data['search_results'] = filtered_cars
        context.user_data['search_offset'] = 0
        
        # Show results count message first
        count_message = language_handler.get_text("search_results", update.effective_user.id, count=len(filtered_cars))
        await query.edit_message_text(count_message)
        
        # Show first result
        await show_search_results_page(update, context, 0)

def extract_year_from_model(model: str) -> int:
    """Extract year from car model string"""
    year_match = re.search(r'(19|20)\d{2}', model)
    return int(year_match.group()) if year_match else 2020

async def show_search_results_page(update: Update, context: ContextTypes.DEFAULT_TYPE, offset: int):
    """Display search results with pagination - same flow as view_cars"""
    search_results = context.user_data.get('search_results', [])
    
    if not search_results:
        return
    
    cars_per_page = 5  # Show 5 cars per page like view_cars
    start_idx = offset
    end_idx = min(start_idx + cars_per_page, len(search_results))
    
    if start_idx >= len(search_results):
        start_idx = 0
        end_idx = min(cars_per_page, len(search_results))
    
    # Update offset in context
    context.user_data['search_offset'] = offset
    
    # Display each car as a separate message (like view_cars flow)
    for i, car in enumerate(search_results[start_idx:end_idx], start_idx + 1):
        details = f"🚗 {car.brand} {car.model}\n"
        details += language_handler.get_text("car_price", update.effective_user.id, price=f"${car.price:,.2f}") + "\n"
        details += language_handler.get_text("car_location", update.effective_user.id, location=car.location) + "\n"
        if car.description:
            details += f"\n📝 {car.description}"
        details += language_handler.get_text("car_count", update.effective_user.id, current=i, total=len(search_results))
        
        # Create keyboard with same structure as view_cars
        keyboard_buttons = [
            [InlineKeyboardButton(language_handler.get_text("contact_seller", update.effective_user.id), callback_data=f"contact_{car.id}"),
             InlineKeyboardButton(language_handler.get_text("add_to_favourites", update.effective_user.id), callback_data=f"favourite_{car.id}")]
        ]
        
        # Add "View More Results" button if there are more cars to show
        if end_idx < len(search_results):
            keyboard_buttons.append([InlineKeyboardButton(language_handler.get_text("view_more_cars", update.effective_user.id), callback_data=f"more_search_results_{end_idx}")])
        
        # Add navigation buttons
        keyboard_buttons.extend([
            [InlineKeyboardButton(language_handler.get_text("modify_filters", update.effective_user.id), callback_data="car_search_filters")],
            [InlineKeyboardButton(language_handler.get_text("back_to_menu", update.effective_user.id), callback_data="back_to_main")]
        ])
        
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        
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
                    await update.callback_query.message.reply_media_group(media=media_group)
                    
                    # Send action buttons as separate message
                    await update.callback_query.message.reply_text(
                        language_handler.get_text("actions", update.effective_user.id),
                        reply_markup=keyboard
                    )
                else:
                    # Fallback to text if no valid images
                    await update.callback_query.message.reply_text(
                        text=details,
                        reply_markup=keyboard
                    )
            else:
                # Single image or text message
                if car.image_url and car.image_url.startswith(('http://', 'https://')) and car.image_url != '🚗':
                    try:
                        await update.callback_query.message.reply_photo(
                            photo=car.image_url,
                            caption=details
                        )
                        # Send action buttons as separate message
                        await update.callback_query.message.reply_text(
                            language_handler.get_text("actions", update.effective_user.id),
                            reply_markup=keyboard
                        )
                    except Exception as e:
                        # Fallback to text if image fails
                        fallback_message = f"🚗 {details}\n\n⚠️ Image not available"
                        await update.callback_query.message.reply_text(
                            fallback_message,
                            reply_markup=keyboard
                        )
                else:
                    # Text message for invalid/missing image
                    await update.callback_query.message.reply_text(
                        text=details,
                        reply_markup=keyboard
                    )
        except Exception as e:
            print(f"❌ Error sending search result: {e}")
            # Final fallback to text message
            fallback_message = f"🚗 {details}\n\n⚠️ Error loading images"
            await update.callback_query.message.reply_text(
                fallback_message,
                reply_markup=keyboard
            )

# Add new handler for "View More Results" button
async def handle_more_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'View More Results' button click"""
    query = update.callback_query
    
    # Parse callback data: more_search_results_{offset}
    callback_parts = query.data.split('_')
    if len(callback_parts) >= 4:
        offset = int(callback_parts[-1])
        
        await query.answer("Loading more search results...")
        
        # Show next page of search results
        await show_search_results_page(update, context, offset)
    else:
        await query.answer("Error loading more results")