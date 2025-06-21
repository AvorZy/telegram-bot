from typing import Dict, Any

class LanguageHandler:
    def __init__(self):
        self.user_languages = {}
        self.translations = {
            "en": {
                # Main Menu
                "welcome_message": "👋 Welcome {name}!\n\n🚗 Discover amazing electric vehicles with our comprehensive platform! Explore cars, find charging stations, locate trusted garages, browse accessories, and save your favorites - all at your fingertips.\n\nPlease select an option to continue:",
                "main_menu_message": "🏠 Main Menu\n\nHello {name}! What would you like to do today?",
                "view_cars": "🔎 View Cars",
                "sell_car": "📝 Sell a Car",
                "my_favourites": "❤️ My Favourites",
                "contact_support": "📞 Contact Support",
                "notifications": "🔔 Notifications",
                "settings": "⚙️ Settings",
                "charging_stations": "🔌 Charging Stations",
                "view_charging_stations": "🔌 View Charging Stations",
                "view_garages": "🔧 View Garages",
                "explore_cars": "🚗 Explore Cars",
                "view_favourites": "❤️ View Favourites",
                "view_help": "❓ View Help",
                "help": "❓ Help",
                
                # Charging Station Messages
                "charging_loading": "🔌 Loading charging stations...",
                "charging_no_stations": "⚠️ No charging stations available at the moment.",
                "charging_no_stations_in_location": "⚠️ No charging stations found in {location}.",
                "charging_locations_header": "🔌 Charging Station Locations\n\nSelect a location to view available charging stations:",
                "charging_stations_header": "🔌 Available Charging Stations\n\nSelect a station to view details:",
                "charging_error": "❌ Error loading charging stations. Please try again later.",
                "charging_back_to_locations": "🔙 Back to Locations",
                "charging_view_on_map": "🗺️ View on Map",
                
                # Charging Station Search Filters
                "charging_station_search_filters": "🔌 Charging Station Search Filters",
                "search_charging_stations": "🔌 Search Charging Stations",
                "no_charging_stations_found": "⚠️ No charging stations found matching your criteria.",
                "price_filter": "Price Filter",
                "power_filter": "Power Filter",
                "location_filter": "Location Filter",
                "type_filter": "Type Filter",
                "connector_filter": "Connector Filter",
                "apply_filters": "Apply Filters",
                "clear_filters": "Clear Filters",
                "price_range": "Price Range",
                "power_range": "Power Range",
                "location": "Location",
                "station_type": "Station Type",
                "connector_type": "Connector Type",
                "any": "Any",
                "choose_location": "Choose a location:",
                "select_connector_type": "Select Connector Type",
                "choose_connector": "Choose a connector type:",
                
                # New Charging Station Options
                "charging_station_options": "🔌 Charging Station Options\n\nChoose how you want to view charging stations:",
                "show_by_location": "📍 Show by Location",
                "show_nearby": "📍 Show Nearby",
                "view_more_stations": "📋 View More Stations",
                "station_count": "Station {current} of {total}",
                "available": "Available",
                "unavailable": "Unavailable",
                "view_on_map": "🗺️ View on Map",
                "back_to_charging_options": "🔙 Back to Options",
                
                # Garage Messages
                "garages": "🔧 Garages",
                "garage_loading": "🔧 Loading garages...",
                "garage_no_garages": "⚠️ No garages available at the moment.",
                "garage_no_garages_in_location": "⚠️ No garages found in {location}.",
                "garage_locations_header": "🔧 Garage Locations\n\nSelect a location to view available garages:",
                "garage_location": "📍 Location: {location}",
                "garage_rating": "⭐ Rating: {rating}/5.0",
                "garage_service": "🔧 Service: {service}",
                "garage_price_range": "💰 Price Range: {price_range}",
                "garage_phone": "📞 Phone: {phone}",
                "garage_contact": "📧 Contact: {contact}",
                "garage_hours": "🕐 Hours: {hours}",
                "garage_garages_header": "🔧 Available Garages\n\nSelect a garage to view details:",
                "garage_error": "❌ Error loading garages. Please try again later.",
                "garage_back_to_locations": "🔙 Back to Locations",
                "garage_view_on_map": "🗺️ View on Map",
                "garage_map_link": "🗺️ View on Google Maps",
                
                # New Garage Options
                "garage_options": "🔧 Garage Options\n\nChoose how you want to view garages:",
                "garage_count": "Garage {current} of {total}",
                "back_to_garage_options": "🔙 Back to Options",
                
                # Garage Search Filters
                "service_type":"Service Type",
                "garage_search_filters": "🔧 Garage Search Filters",
                "service_filter": "Service Filter",
                "choose_price_range": "Choose a price range:",
                "select_service_type": "Select Service Type",
                "choose_service": "Choose a service type:",
                "select_garage_location": "Select Garage Location",
                "choose_garage_location": "Choose a location:",
                "loading_locations": "Loading locations...",
                "no_locations_available": "No locations available at the moment.",
                "location_error": "Error loading locations. Please try again.",
                "garage_search_results": "Garage Search Results",
                "no_garages_found": "No garages found matching your criteria.",
                "try_different_filters": "Try adjusting your search filters.",
                "back_to_filters": "Back to Filters",
                "refine_search": "Refine Search",
                "back_to_search": "Back to Search",
                "page": "Page",
                "filters_cleared": "All filters cleared!",
                "search_error": "Search error",
                
                # Accessory Messages
                "view_accessories": "🔧 View Accessories",
                "accessory_loading": "🔧 Loading accessories...",
                "accessory_no_accessories": "⚠️ No accessories available at the moment.",
                "accessory_no_type_accessories": "⚠️ No {type} accessories available.",
                "accessory_types_header": "🔧 Select Accessory Type\n\nChoose an accessory type to view available accessories:",
                "accessory_list_header": "🔧 {type} Accessories\n\nSelect an accessory to view details:",
                "accessory_error": "❌ Error loading accessories. Please try again later.",
                "accessory_back_to_types": "← Back to Types",
                "accessory_phone": "📞 Phone: {phone}",
                "accessory_contact": "📞 Contact: {contact}",
                "accessory_rating": "⭐ Rating: {rating}/5",
                "accessory_sku": "🏷️ SKU: {sku}",
                "accessory_warranty": "🛡️ Warranty: {warranty}",
                "accessory_voltage": "⚡ Voltage: {voltage}V",
                "accessory_capacity": "🔋 Capacity: {capacity}",
                "accessory_compatible": "🚗 Compatible: {vehicles}",
                "accessory_location": "📍 Location: {location}",
                "accessory_price": "💰 Price: {price}",
                "accessory_type": "🏷️ Type: {type}",
                "accessory_count": "📊 Accessory {current} of {total}",
                
                # Accessory Messages
                "view_accessories": "⚙️ View Accessories",
                "accessory_loading": "⚙️ Loading accessories...",
                "accessory_no_accessories": "⚠️ No accessories available at the moment.",
                "accessory_no_category_accessories": "⚠️ No {category} accessories available.",
                "accessory_categories_header": "⚙️ Select Accessory Category\n\nChoose a category to view available accessories:",
                "accessory_list_header": "⚙️ {category} Accessories\n\nSelect an accessory to view details:",
                "accessory_error": "❌ Error loading accessories. Please try again later.",
                "accessory_back_to_categories": "🔙 Back to Categories",
                "accessory_phone": "📞 Phone: {phone}",
                "accessory_contact": "📞 Contact: {contact}",
                "accessory_rating": "⭐ Rating: {rating}/5",
                "accessory_sku": "🏷️ SKU: {sku}",
                "accessory_weight": "⚖️ Weight: {weight}kg",
                "accessory_color": "🎨 Color: {color}",
                "accessory_brand": "🏷️ Brand: {brand}",
                "accessory_category": "📦 Category: {category}",
                "accessory_location": "📍 Location: {location}",
                "accessory_price": "💰 Price: {price}",
                "accessory_compatible": "🚗 Compatible: {models}",
                "accessory_count": "📊 Accessory {current} of {total}",
                
                # Accessory Loading and Navigation
                "loading_accessories": "⚙️ Loading accessories...",
                "no_accessories_available": "⚠️ No accessories available at the moment.",
                "select_accessory_category": "⚙️ Select Accessory Category\n\nChoose a category to view available accessories:",
                "no_category_accessories": "⚠️ No {category} accessories available.",
                "check_other_categories": "🔍 Check Other Categories",
                "loading_category_accessories": "⚙️ Loading {category} accessories...",
                "accessories_back_to_categories": "🔙 Back to Categories",
                "accessories_back_to_list": "🔙 Back to List",
                "view_more_accessories": "👀 View More Accessories",
                "back_to_accessories": "🔙 Back to Accessories",
                
                # Accessory Contact
                "contact_accessory_name": "⚙️ Accessory: {name}",
                "contact_accessory_price": "💰 Price: {price}",
                "contact_accessory_location": "📍 Location: {location}",
                "phone_accessory_name": "📱 Accessory: {name}",
                
                # Accessory Details Header
                "accessory_details_header": "⚙️ Accessory Details",
                "accessory_name": "📦 Name: {name}",
                "accessory_description": "📝 Description: {description}",
                "accessory_reviews": "📊 Reviews: {count}",
                
                # Browse More Accessories
                "browse_more_accessory": "⚙️ Browse More Accessories",
                
                # Accessory Loading and Navigation
                "loading_accessories": "🔧 Loading accessories...",
                "no_accessories_available": "⚠️ No accessories available at the moment.",
                "select_accessory_type": "🔧 Select Accessory Type\n\nChoose an accessory type to view available accessories:",
                "no_type_accessories": "⚠️ No {type} accessories available.",
                "check_other_types": "🔍 Check Other Types",
                "loading_type_accessories": "🔧 Loading {type} accessories...",
                "accessories_back_to_types": "🔙 Back to Types",
                "accessories_back_to_list": "🔙 Back to List",
                "view_more_accessories": "👀 View More Accessories",
                "back_to_accessories": "🔙 Back to Accessories",
                
                # Accessory Contact
                "contact_accessory_name": "🔧 Accessory: {name}",
                "contact_accessory_price": "💰 Price: {price}",
                "contact_accessory_location": "📍 Location: {location}",
                "phone_accessory_name": "📱 Accessory: {name}",
                
                # Accessory Details Header
                "accessory_details_header": "🔧 Accessory Details",
                
                # Browse More Accessories
                "browse_more_accessory": "🔧 Browse More Accessories",
                
                # Accessory Contact Seller
                "contact_seller_header": "📞 Contact Accessory Seller",
                "contact_phone": "📞 Phone: {phone}",
                "contact_tap_to_copy": "💡 Tap the button below to copy the phone number",
                "copy_phone_number": "📞 Copy Phone Number",
                "contact_info_loaded": "Contact information loaded",
                "contact_info_not_available": "Contact information not available",
                "contact_info_error": "Error loading contact information",
                
                # Seller Phone Header and Instructions
                "seller_phone_header": "📞 Seller Contact Information",
                "phone_copy_instruction": "💡 Tap the button below to copy the phone number",
                
                # Car Selling Flow
                "sell_car_start": "🚗 Let's list your car for sale!",
                "ask_car_model": "Step 1/5: What's the model of your car?\n(Example: Camry, Civic)",
                "ask_car_brand": "Step 2/5: What's the brand of your car?\n(Example: Toyota, Honda)",
                "ask_car_description": "Step 3/5: Please provide a description of your car:\n- Year\n- Condition\n- Mileage\n- Additional features",
                "ask_car_price": "Step 4/5: What's the price of your car? (in USD)",
                "ask_car_location": "Step 5/5: Where is the car located?",
                
                # Settings
                "settings_title": "⚙️ Settings\n\nWhat would you like to modify?",
                "change_language": "🌐 Change Language",
                "update_contact": "📱 Update Contact",
                "notification_settings": "⚙️ Notification Settings",
                "select_language": "🌐 Please select your preferred language:",
                
                "back_to_menu": "🔙 Back to Menu",
                "back_to_settings": "🔙 Back to Settings",
                "language_changed": "✅ Language changed to English!",
                
                # Help Section
                "help_center": "❓ Help Center\n\nWelcome to the help section! Here you can find information about how to use our car marketplace bot.\n\nWhat would you like help with?",
                "help_browse_cars": "❓Help 🔍 Browse Cars",
                "help_explore": "❓Help 🚗 Explore Cars",
                "help_search": "❓Help 🔍 Search",
                "help_favourites": "❓Help ❤️ Favourites",
                "help_contact": "❓Help 📞 Contact",
                "help_settings": "❓Help ⚙️ Settings",
                "help_charging_stations": "❓Help ⚡ Charging Stations",
                "help_garage": "🔧 Garage",
                "back_to_help": "🔙 Back to Help",
                
                # Help Content
                "help_browse_cars_content": "🔍 How to Explore Cars\n\n📋 Browse by Categories:\n1. Click 'View Cars' from the main menu\n2. Select a car brand you're interested in\n3. Browse through available cars by category\n\n🔍 Explore Car Details:\n4. View comprehensive car information:\n   • Model, year, and specifications\n   • Price and financing options\n   • Location and seller details\n   • High-quality photos\n\n⚡ Quick Actions:\n5. Contact the seller directly\n6. Add cars to your favourites\n7. Share car details with friends\n\n💡 Pro Tips:\n• Use navigation buttons to explore more cars\n• Filter by price range for better results\n• Save interesting cars to compare later\n• Check car history and condition details",
                "help_favourites_content": "❤️ Managing Favourites\n\n1. While viewing a car, click 'Add to Favourites'\n2. Access your favourites from the main menu\n3. View saved cars anytime\n4. Remove cars you're no longer interested in\n\nNote: You can save up to 5 cars in your favourites!",
                "help_search_content": "🔍 Search Help\n\n1. Use 'Search' from the main menu\n2. Filter by brand, price range, or location\n3. Browse through search results\n4. Use 'More Results' to see additional cars\n5. Add interesting cars to your favourites\n\nTip: Try different search criteria to find your perfect car!",
                "help_explore_content": "🚗 Explore Cars Feature\n\n🎯 Your Complete Car Knowledge Hub\n\nDiscover everything about cars through our comprehensive explorer!\n\n📚 What You Can Explore:\n• 🚗 Car Types & Models - Learn about different vehicle categories\n• ⚡ Benefits & Advantages - Understand car ownership benefits\n• 🔧 Features & Technology - Discover modern car features\n• 🛡️ Safety & Maintenance - Learn about car safety and care\n• 🌱 Eco-Friendly Options - Explore environmentally friendly vehicles\n\n💡 How to Use:\n1. Click 'Explore Car' from the main menu\n2. Choose a topic you're interested in\n3. Read detailed information and guides\n4. Use navigation buttons to explore more topics\n\n🎯 Perfect for both beginners and car enthusiasts!",
                "help_contact_content": "📞 Contact Information\n\n• Telegram Support: @sim_senchamrong\n• Phone: +855 96 554 5454\n\nFeel free to reach out if you have any questions or need assistance with buying or selling cars!",
                "help_settings_content": "⚙️ Settings Help\n\n1. Change Language: Switch between English and Khmer\n2. Notifications: Manage your notification preferences\n\nYour settings are automatically saved!",
                "help_charging_stations_content": "⚡ Charging Stations Help\n\n🔌 Find Charging Stations:\n1. Click 'Charging Stations' from the main menu\n2. Browse available charging stations in your area\n3. View station details including:\n   • Location and address\n   • Charging types available (AC/DC)\n   • Power output and connector types\n   • Operating hours and availability\n   • Pricing information\n\n💡 Features:\n• Real-time availability status\n• Navigation assistance\n• Station reviews and ratings\n• Booking capabilities (where available)\n\n🎯 Perfect for planning your EV charging stops!",
                "help_garage_content": "🔧 Garage Services Help\n\n🛠️ Find Garage Services:\n1. Click 'Garages' from the main menu\n2. Browse certified garages and service centers\n3. View garage information including:\n   • Service types offered\n   • Location and contact details\n   • Operating hours\n   • Specializations (EV, hybrid, traditional)\n   • Customer ratings and reviews\n\n🔧 Services Available:\n• Regular maintenance and servicing\n• Repairs and diagnostics\n• EV-specific services\n• Emergency roadside assistance\n• Parts replacement\n\n💡 Tips:\n• Check garage specializations for your vehicle type\n• Read customer reviews before booking\n• Compare prices and services offered",
                        

                
                # Command Details
                "cmd_start_detail": "🚀 /start Command\n\nDescription: Initializes the bot and shows the main menu\n\nUsage: Simply type `/start` or click the start button\n\nWhat it does:\n• Welcomes you to the bot\n• Displays the main navigation menu\n• Sets up your user preferences\n• Shows available options",
                "cmd_help_detail": "❓ /help Command\n\nDescription: Access the comprehensive help center\n\nUsage: Type `/help` or click the Help button\n\nWhat it provides:\n• Detailed guides for all features\n• Step-by-step instructions\n• Tips and tricks\n• Troubleshooting information",
                "cmd_cars_detail": "🚗 /cars Command\n\nDescription: Browse available cars by brand\n\nUsage: Type `/cars` or click 'View Cars'\n\nFeatures:\n• Browse cars by brand\n• View detailed car information\n• See prices and locations\n• Contact sellers directly\n• Add cars to favorites",
                "cmd_search_detail": "🔍 /search Command\n\nDescription: Advanced search with multiple filters\n\nUsage: Type `/search` or click 'Search by Filter'\n\nFilter Options:\n• Price range\n• Car brand\n• Year range\n• Location\n• Keywords\n• Multiple filter combinations",
                "cmd_favorites_detail": "❤️ /favorites Command\n\nDescription: Manage your saved favorite cars\n\nUsage: Type `/favorites` or click 'My Favorites'\n\nFeatures:\n• View all saved cars\n• Remove unwanted favorites\n• Quick access to car details\n• Contact sellers\n• Save up to 5 cars",
                "cmd_settings_detail": "⚙️ /settings Command\n\nDescription: Customize your bot experience\n\nUsage: Type `/settings` or click 'Settings'\n\nOptions:\n• Change language (English/Khmer)\n• Update contact information\n• Notification preferences\n• Auto-save settings",
                "cmd_contact_detail": "📞 /contact Command\n\nDescription: Get support and assistance\n\nUsage: Type `/contact` or click 'Contact Support'\n\nSupport Channels:\n• Telegram: @sim_senchamrong\n• Phone: +855 96 554 5454\n• Direct messaging\n• Technical assistance",
                "cmd_explore_detail": "🚗 /explore Command\n\nDescription: Learn about cars and automotive knowledge\n\nUsage: Type `/explore` or click 'Explore Cars'\n\nTopics:\n• Car types and models\n• Benefits and advantages\n• Features and technology\n• Safety and maintenance\n• Eco-friendly options",
                
                # Help Action Buttons
                "try_browsing_now": "🔍 Try Browsing Now",
                "view_my_favourites": "❤️ View My Favourites",
                "open_settings": "⚙️ Open Settings",
                
                # Favourites
                "browse_more_accessory": "🔧 Browse More Accessories",
                "no_favourites": "You haven't saved any cars to your favourites yet.",
                "browse_more_cars": "🔍 Browse Cars",
                "added_to_favourites": "✅ Added to favourites!",
                "already_favourited_message": "⚠️ This car is already in your favourites!",
                "favourites_limit": "⚠️ You can only add up to 5 cars to favourites!",
                "removed_from_favourites": "✅ Removed from favourites!",
                "contact_seller": "📞 Contact Seller",
                "your_favourites": "❤️🚗 Your Favourites Cars & Accessories",
                "add_to_favourites": "❤️ Add to Favourites",
                "remove_from_favourites": "❌ Remove from Favourites",
                "view_more_cars": "🔍 View More Cars",
                
                # Car-related translations
                "loading_cars": "Loading available cars... 🚗",
                "no_cars_available": "No cars available at the moment. We'll notify you when new cars are added! 🔔",
                "select_car_brand": "Select a car brand to view available cars:",
                "loading_brand_cars": "Loading {brand} cars... 🚗",
                "no_brand_cars": "No {brand} cars available at the moment. 😔\n\nWe'll notify you when new cars are added!",
                "check_other_brands": "🔄 Check Other Brands",
                "car_name": "📦 Name: {name}",
                "car_price": "💰 Price: {price}",
                "car_location": "📍 Location: {location}",
                "car_type": "🏷️ Type: {type}",
                "car_rating": "⭐️ Rating: {rating}/5",
                "car_count": "\n\nCar {current} of {total}",
                "accessory_name": "📦 Name: {name}",
                "accessory_price": "💰 Price: {price}",
                "accessory_location": "📍 Location: {location}",
                "accessory_type": "🏷️ Type: {type}",
                "accessory_rating": "⭐️ Rating: {rating}/5",
                "actions": "🔽 Actions",
                
                # Notifications
                "no_notifications": "🔔 No new notifications\n\nYou'll be notified here about:\n• New cars matching your interests\n• Price drops on favourited cars\n• Updates on your transactions",
                "refresh": "🔄 Refresh",
                "your_notifications": "🔔 Your Notifications\n\n",
                
                # API Integration Messages
                "favorite_added": "✅ Car added to favorites!",
                "favorite_add_failed": "❌ Failed to add car to favorites. Please try again.",
                "favorite_add_error": "⚠️ Error adding car to favorites. Please check your connection.",
                "favorite_removed": "✅ Car removed from favorites!",
                "favorite_remove_failed": "❌ Failed to remove car from favorites. Please try again.",
                "favorite_remove_error": "⚠️ Error removing car from favorites. Please check your connection.",
                "favorites_load_error": "⚠️ Error loading favorites. Please check your connection and try again.",
                "user_data_sync_error": "⚠️ Unable to sync user data. Operating in offline mode.",
                "api_connection_error": "⚠️ Connection error. Some features may be limited.",
                "new_notifications_header": "📫 New Notifications:\n",
                
                # Support
                "contact_support_message": "📞 Contact Support\n\n📱 telegram-supporter: @sim_senchamrong\n📱 Phone: +855 96 554 5454\nHow can we help you?.",
                
                # Add these to the English section:
                "notification_settings_message": "🔔 Notification Settings\n\nManage your notification preferences:",
                "new_cars_notification": "🚗 New Cars Notification",
                "price_drops_notification": "💰 Price Drops Notification", 
                "transaction_updates_notification": "📋 Transaction Updates Notification",
                "notifications_enabled": "✅ Enabled",
                "notifications_disabled": "❌ Disabled",
                "notification_updated": "✅ Notification setting updated!",
                
                
                # Contact Seller
                "contact_seller_message": "📞 Contact Seller\n\n Information regarding this contact, please share with the seller or admin.",
                "view_other_cars": "🔍 View Other Cars",
                "share_contact_button": "📱 Share Contact Button",   
                "back_button": "⬅️ Back",
                "contact_seller_title": "📞 Contact Seller",
                "seller_contact_info": "📱 Seller Contact:",
                "phone_label": "Phone:",
                
                # Location Services
                "share_location_button": "📍 Share My Location",
                "cancel_button": "❌ Cancel",
                "location_request_message": "📍 Location Request\n\nTo show you nearby charging stations and garages, please share your current location by clicking the button below.",
                "location_request_realtime": "📍 Please share your current location to find nearby services.",
                "location_saved_success": "✅ Location saved successfully! You can now view nearby services.",
                "location_save_error": "❌ Failed to save your location. Please try again.",
                "location_not_received": "❌ Location not received. Please try sharing your location again.",
                "location_nearby_options": "📍 Location Saved!\n\nWhat would you like to find nearby?",
                "nearby_charging_stations": "🔌 Nearby Charging Stations",
                "nearby_garages": "🔧 Nearby Garages",
                "back_to_main_menu": "🏠 Back to Main Menu",
                "nearby_charging_stations_found": "🔌 Found {count} nearby charging stations:",
                "no_nearby_charging_stations": "⚠️ No charging stations found nearby. Try expanding your search area.",
                "error_fetching_stations": "❌ Error fetching charging stations. Please try again.",
                "nearby_garages_found": "🔧 Found {count} nearby garages:",
                "no_nearby_garages": "⚠️ No garages found nearby. Try expanding your search area.",
                "error_fetching_garages": "❌ Error fetching garages. Please try again.",
                "location_not_available": "📍 Location not available. Please share your location first.",
                "location_not_found": "❌ Location not found. Please share your location first.",
                "location_current_status": "📍 Current Location\n\nLatitude: {lat:.6f}\nLongitude: {lng:.6f}\n\nYour location is saved and being used for nearby searches.",
                "location_not_set": "📍 Location Not Set\n\nYou haven't shared your location yet. Share your location to find nearby services.",
                "update_location": "📍 Update Location",
                "clear_location": "🗑️ Clear Location",
                "nearby_options": "🔍 Find Nearby",
                "set_location": "📍 Set Location",
                "location_cleared_success": "✅ Location cleared successfully.",
                "location_clear_error": "❌ Failed to clear location. Please try again.",
                "contact_seller_instruction": "💡 You can contact the seller directly using the phone number above.\nPlease mention that you found this car through our bot!",
                "no_contact_info": "⚠️ No contact information available\nPlease contact support for assistance with this listing.",
                "copy_phone_button": "📞 Copy Phone:",
                "phone_not_available": "Phone number not available",
                "seller_phone_title": "📞 Seller Phone Number:",
                "how_to_contact_title": "💡 How to contact:",
                "copy_instruction": "• Tap and hold the number above to copy",
                "dialer_instruction": "• Use your phone's dialer to call",
                "mention_bot_instruction": "• Mention you found this car through our bot",
                "back_to_car_details": "🔙 Back to Car Details",
                "car_label": "🚗 Car:",
                "price_label": "💰 Price:",
                
                
                # Add to the "en" section:
                "advanced_search": "🔍Search​ by filter",
                "advanced_search_title": "🔍Search​ by filter",
                "search_cars": "🚗​ ​Search Cars",
                "search_filter": "🔍 Search",
                "search_accessories": "🔧 Search Accessories",
                "search_type_selection": "🔍 Select Search Type",
                "search_type_message": "What would you like to search for?",
                "back_to_search_type": "🔙 Back to Search Type",
                "search_by_accessory_type": "🔧 Search by Accessory Type",
                "apply_accessory_filters": "✅ Apply Accessory Filters",
                "clear_accessory_filters": "🗑️ Clear Accessory Filters",
                "accessory_search_title": "🔧 Accessory Search Filters",
                "accessory_search_results": "🔍 Accessory Search Results ({count} accessories found)",
                "no_accessory_search_results": "❌ No accessories found matching your criteria. Try adjusting your filters.",
                "accessory_price_filter": "Accessory price filter: ${price_min:,} - ${price_max:,}",
                "accessory_location_filter": "Accessory location filter: {location}",
                "accessory_type_filter": "Accessory type filter: {type}",
                "accessory_filters_cleared": "Accessory filters cleared!",
                "found_accessories_matching": "Found {count} accessories matching your filters!",
                "no_accessories_found_filters": "No accessories found matching your filters.",
                "warranty": "Warranty",
                "voltage": "Voltage",
                "capacity": "Capacity",
                "contact_seller": "📞 Contact Seller",
                "add_to_favourites": "❤️ Add to Favourites",
                "view_more_accessories": "➡️ View More Accessories",
                "modify_filters": "🔍 Modify Filters",
                "back_to_menu": "🏠 Back to Menu",
                "accessory_of_total": "Accessory {current} of {total}",
                "apply_filters": "✅ Apply Filters",

                "no_filters_applied": "❌ No filters applied",
                "select_filter_or_apply": "Please select a filter to modify or apply current filters to search.",
                "search_by_price": "💰 Search by Price Range",
                "search_by_year": "📅 Search by Year",
                "search_by_location": "📍 Search by Location",
                "search_by_brand": "🚗 Search by Brand ",
                "search_by_type": "🔧 Search by Type",
                "keyword_search": "🔤 Keyword Search",
                "clear_filters": "🗑️ Clear All Filters",
                "back_to_search": "🔙 Back to Search",
                "search_results": "🔍 Search Results ({count} cars found)",
                "search_completed": "Search Completed",
                "car_search_results": "🔍 Car Search Results ({count} cars found)",
                "accessory_search_results": "Accessory Search Results ({count} accessories found)",
                "no_search_results": "❌ No cars found matching your criteria. Try adjusting your filters.",
                "current_filters": "📋 Current Filters:",
                "price_filter": "💰 Price: ${min} - ${max}",
                "year_filter": "📅 Year: {min} - {max}",
                "location_filter": "📍 Location: {location}",
                "brand_filter": "🚗 Brand: {brand}",
                "model_filter": "🚗 Model: {model}",
                "apply_filters": "✅ Apply Filters",
                "modify_filters": "✏️ Modify Filters",
                
                
                # Explore Section en
                "explore_car": "🚗 Explore Car",
                "explore_welcome": "🚗 Welcome to Car Explorer!\n\n🎯 Your Complete Car Knowledge Hub\n\nDiscover everything about cars - from types and features to buying guides and maintenance tips. Whether you're a first-time buyer or car enthusiast, we've got you covered!\n\n📚 What would you like to explore today?",
                "explore_car_types": "🚗 Car Types & Models",
                "explore_benefits": "⚡ Benefits & Advantages",
                "explore_features": "🔧 Features & Technology",
                "explore_safety": "🛡️ Safety & Maintenance",
                "explore_eco": "🌱 Eco-Friendly Options",
                "back_to_explorer": "🔙 Back to Explorer",
                
                # Car Types
                "car_types_title": "🚗 Car Types & Categories\n\n🎯 Find Your Perfect Match!\n\nEvery car type serves different needs and lifestyles. From fuel-efficient compacts to powerful sports cars, discover which type suits you best!\n\nChoose a category to explore:",
                "sports_cars": "🏎️ Sports Cars",
                "suvs_crossovers": "🚙 SUVs & Crossovers",
                "sedans_saloons": "🚗 Sedans & Saloons",
                "hatchbacks_compacts": "🚐 Hatchbacks & Compacts",
                "trucks_pickups": "🚚 Trucks & Pickups",
                "convertibles": "🏎️ Convertibles",
                "wagons_estates": "🚐 Wagons & Estates",
                "minivans_mpvs": "🚌 Minivans & MPVs",
                
                
                  # Car Types Section
                "car_types_section": "Car Types",
                "type_sports_content": "🏎️ Sports Cars\n\n🚀 Pure Performance & Excitement!\n\nKey Characteristics:\n• High-performance engines (300+ HP)\n• Superior handling and acceleration\n• Aerodynamic design\n• Premium materials and craftsmanship\n• Advanced suspension systems\n\nPopular Models:\n• Porsche 911, BMW M3, Audi R8\n• Chevrolet Corvette, Ford Mustang\n• Ferrari, Lamborghini, McLaren\n\nPrice Range: $30,000 - $500,000+\n\nPerfect For:\n• Driving enthusiasts\n• Weekend adventures\n• Track day experiences\n• Making a statement\n\n🏁 Feel the thrill of the road!",
                "type_suv_content": "🚙 SUVs & Crossovers\n\n🎯 Space, Versatility & Capability!\n\nKey Features:\n• Higher seating position\n• All-wheel drive capability\n• Generous cargo space\n• Towing capacity\n• Advanced safety features\n\nPopular Models:\n• Toyota RAV4, Honda CR-V\n• BMW X5, Mercedes GLE\n• Jeep Wrangler, Ford Explorer\n• Tesla Model Y, Audi Q7\n\nPrice Range: $25,000 - $100,000+\n\nPerfect For:\n• Families with children\n• Outdoor enthusiasts\n• Long road trips\n• All-weather driving\n\n🚙 Adventure awaits!",
                "type_sedan_content": "🚗 Sedans & Saloons\n\n✨ Elegance Meets Practicality!\n\nKey Features:\n• Four doors with separate trunk\n• Comfortable seating for 5\n• Smooth and quiet ride\n• Excellent fuel economy\n• Professional appearance\n\nPopular Models:\n• Toyota Camry, Honda Accord\n• BMW 3 Series, Mercedes C-Class\n• Audi A4, Lexus ES\n• Tesla Model S, Genesis G90\n\nPrice Range: $20,000 - $150,000+\n\nPerfect For:\n• Daily commuting\n• Business professionals\n• Comfortable family transport\n• Fuel-efficient travel\n\n🚗 Classic sophistication!",
                "type_hatchback_content": "🚐 Hatchbacks & Compacts\n\n🎯 Efficiency & Urban Agility!\n\nKey Features:\n• Compact size for easy parking\n• Rear hatch for cargo access\n• Excellent fuel economy\n• Affordable pricing\n• Nimble city driving\n\nPopular Models:\n• Honda Civic, Toyota Corolla\n• Volkswagen Golf, Ford Focus\n• MINI Cooper, Mazda3\n• Hyundai Elantra GT\n\nPrice Range: $18,000 - $45,000\n\nPerfect For:\n• First-time buyers\n• City dwellers\n• Budget-conscious drivers\n• Easy parking situations\n\n🚐 Smart and efficient!",
                "type_truck_content": "🚚 Trucks & Pickups\n\n💪 Power, Capability & Utility!\n\nKey Features:\n• Open cargo bed\n• High towing capacity\n• 4WD capability\n• Rugged construction\n• High ground clearance\n\nPopular Models:\n• Ford F-150, Chevrolet Silverado\n• Ram 1500, Toyota Tacoma\n• GMC Sierra, Nissan Titan\n• Ford Ranger, Honda Ridgeline\n\nPrice Range: $25,000 - $80,000+\n\nPerfect For:\n• Work and construction\n• Hauling and towing\n• Off-road adventures\n• Outdoor activities\n\n🚚 Built tough for any job!",
                "type_convertible_content": "🏎️ Convertibles\n\n☀️ Open-Air Freedom & Style!\n\nKey Features:\n• Retractable roof (soft or hard top)\n• Enhanced structural reinforcement\n• Premium interior materials\n• Advanced wind management\n• Stylish design\n\nPopular Models:\n• BMW Z4, Mercedes SL-Class\n• Porsche 911 Cabriolet\n• Mazda MX-5 Miata\n• Ford Mustang Convertible\n\nPrice Range: $30,000 - $200,000+\n\nPerfect For:\n• Scenic drives\n• Weekend getaways\n• Warm weather enjoyment\n• Making a statement\n\n🏎️ Feel the wind in your hair!",
                "type_wagon_content": "🚐 Wagons & Estates\n\n🎯 Maximum Space & Versatility!\n\nKey Features:\n• Extended cargo area\n• Low loading height\n• Fold-flat rear seats\n• Car-like handling\n• Fuel efficiency\n\nPopular Models:\n• Subaru Outback, Volvo V90\n• Audi A4 Allroad\n• Mercedes E-Class Wagon\n• Volkswagen Golf SportWagen\n\nPrice Range: $25,000 - $70,000+\n\nPerfect For:\n• Active families\n• Cargo hauling needs\n• Road trips with gear\n• Dog owners\n\n🚐 Space without compromise!",
                "type_minivan_content": "🚌 Minivans & MPVs\n\n👨‍👩‍👧‍👦 Ultimate Family Transportation!\n\nKey Features:\n• Seating for 7-8 passengers\n• Sliding doors for easy access\n• Flexible seating configurations\n• Abundant storage space\n• Family-friendly features\n\nPopular Models:\n• Honda Odyssey, Toyota Sienna\n• Chrysler Pacifica\n• Kia Carnival, Volkswagen Atlas\n\nPrice Range: $30,000 - $50,000+\n\nPerfect For:\n• Large families\n• Carpooling\n• Group travel\n• Maximum passenger comfort\n\n🚌 Family adventures made easy!",
                
              
                
                # Benefits & Advantages
                "benefits_title": "⚡ Car Ownership Benefits\n\n🌟 Transform Your Lifestyle!\n\nOwning a car opens up countless opportunities and conveniences. From career advancement to family adventures, discover how a car can enhance every aspect of your life!\n\nExplore the benefits:",
                "work_career": "💼 Work & Career",
                "financial_benefits": "💸 Financial Benefits",
                "family_lifestyle": "👨‍👩‍👧‍👦 Family & Lifestyle", 
                "social_freedom": "🌍 Social & Environmental",
                "cost_comparison": "🚗 vs 🚌 Car vs Public Transport",
                "independence": "🗽 Independence",
                "safety_features": "🛡️ Safety Features",
                "tech_features": "📱 Technology",
                "comfort_features": "🛋️ Comfort Features",
                "performance_features": "⚡ Performance",
                "electric_features": "🔋 Electric Features",
                "entertainment_features": "🎵 Entertainment",
                
                # Features & Technology
                "features_title": "🔧 Car Features & Technology\n\n🚀 Discover Advanced Automotive Technology!\n\n🛡️ Safety Features:\n• Advanced driver assistance\n• Collision prevention systems\n• Smart braking technology\n\n📱 Technology Features:\n• Infotainment systems\n• Smartphone integration\n• Voice control\n\n🛋️ Comfort Features:\n• Climate control\n• Premium seating\n• Noise reduction\n\n💡 Which feature category interests you most?",
                
                # Safety & Maintenance
                "safety_title": "🛡️ Safety & Maintenance Hub\n\n🎯 Keep Your Car Safe & Reliable!\n\n🔧 Essential Maintenance:\n• Oil changes every 5,000-7,500 miles\n• Tire rotation every 6,000-8,000 miles\n• Brake inspection annually\n• Battery check seasonally\n\n⚠️ Watch for Warning Signs:\n• Strange noises or vibrations\n• Dashboard warning lights\n• Fluid leaks or unusual smells\n\n💡 What safety topic interests you?",
                "personal_freedom": "🎯 Personal Freedom",
                "maintenance_schedule": "🔧 Maintenance Schedule",
                "driving_safety_tips": "🛡️ Driving Safety Tips",
                "warning_signs": "⚠️ Warning Signs",
                "emergency_preparedness": "🆘 Emergency Preparedness",
                "seasonal_care": "❄️ Seasonal Care",
                "diy_checks": "🔍 DIY Checks",
                "maintenance_guide": "🔧 Maintenance Guide",
                "safety_tips": "⚠️ Safety Tips",
                "emergency_procedures": "🆘 Emergency Procedures",
                "diy_maintenance": "🛠️ DIY Maintenance",
                
                # Eco-Friendly Options
                "eco_title": "🌱 Eco-Friendly Car Options\n\n🌍 Drive Green, Save Money!\n\n🔋 Electric Vehicles (EVs):\n• Zero emissions\n• Lower operating costs\n• Instant torque\n• Quiet operation\n\n🌿 Hybrid Benefits:\n• Best of both worlds\n• Excellent fuel economy\n• Reduced emissions\n• No range anxiety\n\n💡 Ready to go green? Which option interests you?",
                "electric_vehicles": "⚡ Electric Vehicles",
                "hybrid_technology": "🌿 Hybrid Technology",
                "fuel_efficiency": "⛽ Fuel Efficiency Tips",
                "environmental_impact": "🌍 Environmental Impact",
                "cost_savings": "💰 Cost Savings",
                "charging_infrastructure": "🔌 Charging Infrastructure",
                
                # Add to English translations:
                "benefits_work_content": "💼 Professional & Work Benefits\n\n🚀 Boost Your Career Success!\n\nProfessional Advantages:\n• Reliable transportation to work\n• Professional image and credibility\n• Ability to attend meetings anywhere\n• Client visits and business travel\n• Emergency work response capability\n\nCareer Benefits:\n• Expanded job opportunities\n• Punctuality and reliability\n• Mobile office capability\n• Flexible work arrangements\n\n💡 Your car is an investment in your career!",
                "benefits_family_content": "👨‍👩‍👧‍👦 Family & Lifestyle Benefits\n\n❤️ Enhance Your Family Life!\n\nFamily Convenience:\n• School drop-offs and pick-ups\n• Family outings and vacations\n• Emergency medical transport\n• Grocery shopping with ease\n• Sports and activity transportation\n\nLifestyle Enhancement:\n• Weekend adventures\n• Date nights and entertainment\n• Hobby and recreation access\n• Social event participation\n\nSafety & Security:\n• Protected travel in bad weather\n• Safe late-night transportation\n• Emergency evacuation capability\n\n💡 Creating memories, one journey at a time!",
                "benefits_freedom_content": "🎯 Personal Freedom Benefits\n\n🗽 True Independence & Flexibility!\n\nFreedom of Movement:\n• Go anywhere, anytime\n• No schedule restrictions\n• Spontaneous trips and adventures\n• Door-to-door convenience\n• Privacy during travel\n\nTime Freedom:\n• No waiting for public transport\n• Direct routes to destinations\n• Multiple errands in one trip\n• Flexible departure times\n\nLifestyle Freedom:\n• Choose your music and environment\n• Travel with pets and belongings\n• Stop whenever you want\n• Explore new places easily\n\n🗽 Your schedule, your way!",
                "benefits_financial_content": "💰 Financial Benefits\n\n📈 Smart Money Moves!\n\nLong-term Savings:\n• No daily transport costs\n• Bulk shopping savings\n• Reduced delivery fees\n• Tax deductions (business use)\n• Asset building (car value)\n\nIncome Opportunities:\n• Rideshare driving (Uber/Lyft)\n• Delivery services\n• Mobile business opportunities\n• Expanded job market access\n\nCost Comparisons:\n• Public transport: $100-200/month\n• Car ownership: $300-500/month\n• Added value: Convenience + Freedom\n\n💡 Your car can pay for itself!",
                "benefits_social_content": "🌍 Social & Environmental Benefits\n\n🤝 Connect & Contribute!\n\nSocial Advantages:\n• Help friends and family\n• Community event participation\n• Volunteer work accessibility\n• Emergency assistance to others\n• Carpooling opportunities\n\nEnvironmental Responsibility:\n• Choose eco-friendly vehicles\n• Reduce multiple trips\n• Efficient route planning\n• Support green technology\n\nCommunity Impact:\n• Local business support\n• Economic contribution\n• Emergency response capability\n• Neighborhood participation\n\n💡 Drive positive change in your community!",
                "benefits_comparison_content": "🚗 vs 🚌 Car vs Public Transport\n\n⚖️ The Complete Comparison!\n\n🚗 Car Ownership Advantages:\n• Door-to-door convenience\n• Travel on your schedule\n• Privacy and comfort\n• Carry unlimited luggage\n• Weather protection\n• Emergency transportation\n\n🚌 Public Transport Advantages:\n• Lower monthly costs\n• No parking hassles\n• Environmental benefits\n• No maintenance worries\n• Can read/work during travel\n\n💰 Cost Comparison (Monthly):\n• Public Transport: $100-200\n• Car Ownership: $300-600\n• Car Benefits: Priceless convenience\n\n🎯 Best Choice Depends On:\n• Your lifestyle needs\n• Budget considerations\n• Location and infrastructure\n• Family size and requirements\n\n⚖️ Choose what works for you!",
    
                # Add these missing keys to English translations
                "benefits_section": "Benefits & Advantages",
                "professional_work": "💼 Professional & Work",
                "social_environmental": "🌍 Social & Environmental",
                
                
                
                # Features & Technology Section
                "features_section": "Features & Technology",
                "features_safety_content": "🛡️ Advanced Safety Systems\n\n🚗 Your Guardian Angel on Wheels!\n\nActive Safety Features:\n• Automatic Emergency Braking (AEB)\n• Blind Spot Monitoring (BSM)\n• Lane Departure Warning (LDW)\n• Adaptive Cruise Control (ACC)\n• Forward Collision Warning (FCW)\n\nPassive Safety Features:\n• Multiple airbags\n• Reinforced safety cage\n• Anti-lock Braking System (ABS)\n• Electronic Stability Control (ESC)\n\nBenefits:\n• Accident prevention\n• Reduced injury severity\n• Lower insurance premiums\n• Peace of mind driving\n\n🛡️ Safety first, always!",
                "features_tech_content": "📱 Smart Technology Features\n\n🚀 Connected Car Revolution!\n\nConnectivity Features:\n• Apple CarPlay & Android Auto\n• Wireless smartphone integration\n• Bluetooth connectivity\n• Wi-Fi hotspot capability\n• Voice recognition systems\n\nAI & Automation:\n• Intelligent voice assistants\n• Predictive maintenance alerts\n• Smart climate control\n• Automated parking systems\n\nSmart Controls:\n• Digital instrument clusters\n• Heads-up display (HUD)\n• Touch-sensitive surfaces\n\n📱 Stay connected, stay smart!",
                "features_comfort_content": "❄️ Comfort & Luxury Features\n\n🌟 Premium Driving Experience!\n\nSeating Comfort:\n• Heated and ventilated seats\n• Memory seat positions\n• Premium leather upholstery\n• Power-adjustable seats\n• Lumbar support systems\n\nClimate Control:\n• Dual/tri-zone automatic climate\n• Air purification systems\n• Heated steering wheel\n• Remote climate pre-conditioning\n\nLuxury Touches:\n• Ambient lighting\n• Premium interior materials\n• Panoramic sunroof\n• Wireless device charging\n\n❄️ Luxury redefined!",
                "features_performance_content": "⚡ Performance Features\n\n🏁 Unleash the Power!\n\nEngine Performance:\n• Turbocharged engines\n• Variable valve timing\n• Direct fuel injection\n• Performance tuning modes\n• Launch control systems\n\nTransmission & Drivetrain:\n• Advanced automatic transmissions\n• All-wheel drive (AWD) systems\n• Limited-slip differentials\n• Drive mode selection\n\nChassis & Handling:\n• Adaptive suspension systems\n• Performance braking systems\n• Aerodynamic enhancements\n\n⚡ Performance unleashed!",
                "features_electric_content": "🔋 Electric & Hybrid Features\n\n⚡ Future of Automotive Technology!\n\nBattery & Charging:\n• High-capacity lithium-ion batteries\n• Fast charging capabilities\n• Home charging solutions\n• Battery thermal management\n• Regenerative braking systems\n\nElectric Drivetrain:\n• Instant torque delivery\n• Silent electric operation\n• Multiple electric motors\n• Precise power control\n\nEfficiency Features:\n• Eco driving modes\n• Energy consumption monitoring\n• Route optimization\n• Smart charging scheduling\n\n🔋 Electric excellence!",
                "features_entertainment_content": "🎵 Entertainment Systems\n\n🎶 Premium Audio & Entertainment!\n\nAudio Systems:\n• Premium brand audio (Bose, Harman Kardon)\n• Surround sound systems\n• Multiple speakers (8-20+ speakers)\n• Customizable audio settings\n\nDisplay & Media:\n• Large touchscreen displays\n• Rear seat entertainment screens\n• Digital instrument clusters\n• High-resolution graphics\n\nEntertainment Features:\n• Streaming services integration\n• Gaming capabilities (while parked)\n• Video playback support\n• Multiple USB ports\n\nConnectivity Options:\n• Bluetooth audio streaming\n• Apple CarPlay & Android Auto\n• Spotify, Apple Music integration\n• Internet radio streaming\n\n🎵 Entertainment redefined!",
                "smart_technology": "📱 Smart Technology",
                "comfort_luxury": "❄️ Comfort & Luxury",
                "safety_systems": "🛡️ Safety Systems",
                "entertainment_systems": "🎵 Entertainment Systems",
                
                # Safety & Maintenance Section - Content
                "safety_section": "Safety",
                "safety_maintenance_content": "🔧 Maintenance Schedule\n\n📅 Keep Your Car Running Smoothly!\n\nEvery 3,000-5,000 Miles:\n• Oil and filter change\n• Fluid level checks\n• Tire pressure inspection\n• Battery terminals cleaning\n\nEvery 6,000-10,000 Miles:\n• Tire rotation\n• Air filter replacement\n• Brake inspection\n• Belts and hoses check\n\nEvery 12,000-15,000 Miles:\n• Transmission service\n• Coolant system flush\n• Spark plug replacement\n• Timing belt inspection\n\nAnnually:\n• Comprehensive inspection\n• Emissions testing\n• Insurance review\n• Registration renewal\n\n🔧 Prevention is better than repair!",
                "safety_tips_content": "🛡️ Driving Safety Tips\n\n🎯 Stay Safe on the Road!\n\nBefore Driving:\n• Adjust mirrors and seat\n• Check fuel and fluids\n• Plan your route\n• Ensure seatbelt fits properly\n• Remove distractions\n\nWhile Driving:\n• Maintain safe following distance\n• Use turn signals early\n• Check blind spots\n• Avoid aggressive driving\n• Stay focused on the road\n\nWeather Conditions:\n• Reduce speed in rain/snow\n• Use headlights in low visibility\n• Increase following distance\n• Avoid sudden movements\n\nNight Driving:\n• Clean windshield and lights\n• Dim dashboard lights\n• Look away from oncoming lights\n• Take breaks on long trips\n\n🛡️ Safe driving saves lives!",
                "safety_warnings_content": "⚠️ Warning Signs\n\n🚨 Don't Ignore These Signals!\n\nEngine Issues:\n• Check engine light\n• Unusual noises or vibrations\n• Smoke from exhaust\n• Loss of power\n• Overheating\n\nBrake Problems:\n• Squealing or grinding sounds\n• Soft or spongy brake pedal\n• Car pulls to one side\n• Brake warning light\n\nTire Issues:\n• Uneven wear patterns\n• Low tire pressure warning\n• Vibration while driving\n• Bulges or cracks\n\nElectrical Problems:\n• Dim or flickering lights\n• Battery warning light\n• Difficulty starting\n• Electrical accessories failing\n\nWhen to Stop Immediately:\n• Steam from engine\n• Oil pressure warning\n• Brake failure\n• Steering problems\n\n⚠️ When in doubt, get it checked!",
                "safety_emergency_content": "🆘 Emergency Preparedness\n\n🎯 Be Ready for Anything!\n\nEmergency Kit Essentials:\n• First aid kit\n• Flashlight and batteries\n• Emergency flares or reflectors\n• Jumper cables\n• Tire pressure gauge\n• Multi-tool or basic tools\n• Emergency blanket\n• Water and snacks\n\nRoadside Emergency Steps:\n1. Pull over safely\n2. Turn on hazard lights\n3. Set up warning triangles\n4. Call for help\n5. Stay visible and safe\n\nImportant Numbers:\n• Emergency services: 911\n• Roadside assistance\n• Insurance company\n• Trusted mechanic\n\nWinter Additions:\n• Ice scraper and snow brush\n• Sand or cat litter\n• Warm clothing\n• Extra blankets\n\n🆘 Preparation prevents panic!",
                "safety_seasonal_content": "❄️ Seasonal Care\n\n🌍 Year-Round Vehicle Care!\n\nWinter Preparation:\n• Switch to winter tires\n• Check antifreeze levels\n• Test battery and charging system\n• Keep gas tank full\n• Pack emergency winter kit\n\nSpring Maintenance:\n• Inspect for winter damage\n• Change to all-season tires\n• Check air conditioning\n• Clean salt residue\n• Replace worn wiper blades\n\nSummer Care:\n• Check cooling system\n• Inspect belts and hoses\n• Monitor tire pressure\n• Use sunshades for interior\n• Keep extra water\n\nFall Preparation:\n• Test heating system\n• Check lights and visibility\n• Inspect tires for winter\n• Clean and wax exterior\n• Prepare for time change\n\n❄️ Every season has its needs!",
                "safety_diy_content": "🔍 DIY Checks\n\n🛠️ Simple Checks You Can Do!\n\nWeekly Checks:\n• Tire pressure and tread\n• Fluid levels (oil, coolant, brake)\n• Lights and signals\n• Windshield washer fluid\n• Battery terminals\n\nMonthly Checks:\n• Air filter condition\n• Belt tension and wear\n• Hose condition\n• Exhaust system\n• Suspension components\n\nEasy DIY Tasks:\n• Changing air filter\n• Replacing wiper blades\n• Checking tire pressure\n• Topping off fluids\n• Cleaning battery terminals\n\nWhen to Call a Professional:\n• Engine problems\n• Brake issues\n• Transmission problems\n• Electrical faults\n• Safety system warnings\n\nSafety First:\n• Use proper tools\n• Work on level ground\n• Engage parking brake\n• Let engine cool down\n\n🔍 Knowledge is power!",
                                
                # Add these to the English section (around line 203, after the existing eco keys):
                "eco_section": "Eco-Friendly Options",
                "fuel_efficiency_tips": "⛽ Fuel Efficiency Tips",
                "eco_electric_content": "⚡ Electric Vehicles\n\n🔋 The Future of Transportation!\n\nKey Benefits:\n• Zero direct emissions\n• Lower operating costs (electricity vs gas)\n• Instant torque and smooth acceleration\n• Quiet operation\n• Minimal maintenance required\n\nPopular Models:\n• Tesla Model 3, Model Y, Model S\n• Nissan Leaf, Chevrolet Bolt\n• BMW i3, Audi e-tron\n• Ford Mustang Mach-E\n\nCharging Options:\n• Home charging (Level 1 & 2)\n• Public fast charging (DC)\n• Workplace charging\n• Destination charging\n\nRange Considerations:\n• Most EVs: 200-400+ miles\n• Improving battery technology\n• Growing charging infrastructure\n\n⚡ Ready for the electric revolution?",
                "eco_hybrid_content": "🌿 Hybrid Technology\n\n🔄 Best of Both Worlds!\n\nHow Hybrids Work:\n• Combines gas engine + electric motor\n• Automatic switching between power sources\n• Regenerative braking captures energy\n• Battery charges while driving\n\nTypes of Hybrids:\n• Traditional Hybrid: Gas engine primary\n• Plug-in Hybrid: Larger battery, can charge\n• Mild Hybrid: Electric assist only\n\nPopular Models:\n• Toyota Prius, Camry Hybrid\n• Honda Accord Hybrid, Insight\n• Ford Escape Hybrid\n• Lexus RX Hybrid\n\nBenefits:\n• 40-60+ MPG fuel economy\n• Reduced emissions\n• No range anxiety\n• Lower fuel costs\n\n🌿 Efficiency without compromise!",
                "eco_fuel_content": "⛽ Fuel Efficiency Tips\n\n💡 Maximize Your MPG!\n\nDriving Techniques:\n• Maintain steady speeds (55-65 mph optimal)\n• Gradual acceleration and braking\n• Use cruise control on highways\n• Anticipate traffic flow\n• Remove excess weight from car\n\nVehicle Maintenance:\n• Keep tires properly inflated\n• Regular oil changes\n• Clean air filter\n• Tune-ups as scheduled\n• Use recommended fuel grade\n\nTrip Planning:\n• Combine errands into one trip\n• Avoid peak traffic hours\n• Use GPS for efficient routes\n• Consider carpooling\n\nTechnology Helpers:\n• Eco driving modes\n• Real-time fuel economy displays\n• Trip computers\n• Mobile apps for gas prices\n\n⛽ Every drop counts!",
                "eco_impact_content": "🌍 Environmental Impact\n\n🌱 Your Car's Carbon Footprint\n\nTraditional Vehicles:\n• Average car: 4.6 tons CO2/year\n• 1 gallon gas = 19.6 lbs CO2\n• Tailpipe emissions\n• Oil consumption impact\n\nElectric Vehicles:\n• Zero direct emissions\n• Electricity source matters\n• 50-70% less lifetime emissions\n• Improving as grid gets cleaner\n\nHybrid Benefits:\n• 30-50% less emissions than gas cars\n• Reduced fuel consumption\n• Lower air pollution\n• Bridge to full electric future\n\nMaking a Difference:\n• Choose efficient vehicles\n• Drive less, combine trips\n• Maintain your vehicle\n• Consider alternative transport\n\nGlobal Impact:\n• Transportation: 29% of US emissions\n• Every efficient car helps\n• Supporting clean technology\n\n🌍 Drive toward a cleaner future!",
                "eco_savings_content": "💰 Cost Savings\n\n📊 Calculate Your Savings!\n\nElectric Vehicle Savings:\n• Electricity vs Gas: $0.04 vs $0.12 per mile\n• Annual savings: $1,000-2,000\n• Lower maintenance costs\n• Federal tax credits up to $7,500\n• State/local incentives available\n\nHybrid Savings:\n• 40-60 MPG vs 25 MPG average\n• Save $500-1,500/year on fuel\n• Longer engine life\n• Reduced brake wear\n\nFuel Efficiency Savings:\n• Improving 25 to 35 MPG saves $600/year\n• Proper maintenance saves 10-15%\n• Efficient driving saves 20-40%\n\nAdditional Benefits:\n• HOV lane access\n• Reduced parking fees\n• Lower insurance (some companies)\n• Increased resale value\n\nPayback Period:\n• Hybrids: 3-5 years\n• EVs: 5-8 years (with incentives)\n• Fuel efficiency: Immediate\n\n💰 Green driving = green savings!",
                "eco_charging_content": "🔌 Charging Infrastructure\n\n⚡ Power Up Anywhere!\n\nHome Charging:\n• Level 1: Standard 120V outlet (slow)\n• Level 2: 240V outlet (recommended)\n• Installation: $500-2,000\n• Overnight charging convenience\n• Lowest cost electricity rates\n\nPublic Charging:\n• Level 2: 4-8 hours full charge\n• DC Fast: 30-60 minutes to 80%\n• Networks: ChargePoint, EVgo, Electrify America\n• Apps help locate stations\n\nWorkplace Charging:\n• Growing employer benefit\n• Charge while you work\n• Often free or low cost\n• Reduces range anxiety\n\nCharging Costs:\n• Home: $0.10-0.20 per kWh\n• Public Level 2: $0.20-0.30 per kWh\n• DC Fast: $0.30-0.50 per kWh\n• Still cheaper than gasoline\n\nFuture Growth:\n• 500,000+ public chargers by 2030\n• Faster charging technology\n• More convenient locations\n• Lower costs\n\n🔌 The network is growing fast!",
                
                # Add to English translations section
                "back_to_section": "🔙 Back to {section}",
                "search_garages":"🔍 Search Garages",
                "search_by_color": "🎨 Search by Color",
                "search_by_category": "📂 Search by Category",
                "select_price_range": "💰 Select a price range:",
                "select_year_range": "📅 Select a year range:",
                "select_location": "📍 Select a location:",
                "select_brand": "🚗 Select a brand:",
                "select_color": "🎨 Select a color:",
                "select_category": "📂 Select a category:",
                "any_brand": "🌈 Any Brand",
                "any_color": "🌈 Any Color",
                "any_category": "📂 Any Category",
                "red": "Red",
                "blue": "Blue",
                "white": "White",
                "black": "Black",
                "silver": "Silver",
                "gray": "Gray",
                "green": "Green",
                "yellow": "Yellow",
                "sedan": "Sedan",
                "suv": "SUV",
                "hatchback": "Hatchback",
                "truck": "Truck",
                "convertible": "Convertible",
                "refine_search":"Refine Search",
                
                # Error Messages
                "unknown_command": "I don't understand that command. Please use the menu options below:",
                "car_not_available": "Sorry, this car is no longer available.",

            },
            "kh": {
                # Main Menu
                "welcome_message": "👋 សូមស្វាគមន៍ {name}!\n\n🚗 ស្វែងរកយានយន្តអគ្គិសនីដ៏អស្ចារ្យជាមួយនឹងវេទិកាទូលំទូលាយរបស់យើង! ស្វែងរកយានយន្ត រកស្ថានីយ៍បញ្ចូលថាមពល ស្វែងរកហាងជួសជុលដែលអាចទុកចិត្តបាន រកមើលគ្រឿងបរិក្ខារ និងរក្សាទុកចំណូលចិត្តរបស់អ្នក - ទាំងអស់នេះនៅក្នុងដៃរបស់អ្នក។\n\nសូមជ្រើសរើសតម្រង ឬអនុវត្តតម្រងបច្ចុប្បន្ន:",
                "main_menu_message": "🏠 ម៉ឺនុយមេ\n\nជំរាបសួរ {name}! តើអ្នកចង់ធ្វើអ្វីនៅថ្ងៃនេះ?",
                "view_cars": "🔎 មើលរថយន្ត",
                "sell_car": "📝 លក់រថយន្ត",
                "my_favourites": "❤️ ចំណូលចិត្តរបស់ខ្ញុំ",
                "contact_support": "📞 ទំនាក់ទំនងជំនួយ",
                "notifications": "🔔 ការជូនដំណឹង",
                "settings": "⚙️ ការកំណត់",
                "charging_stations": "🔌 ស្ថានីយ៍បញ្ចូលថាមពល",
                "view_charging_stations": "🔌 មើលស្ថានីយ៍បញ្ចូលថាមពល",
                "view_garages": "🔧 មើលហាងជួសជុល",
                "explore_cars": "🚗 ស្វែងយល់ពីរថយន្ត",
                "view_favourites": "❤️ មើលចំណូលចិត្ត",
                "view_help": "❓ មើលជំនួយ",
                "help": "❓ ជំនួយ",
                
                # Charging Station Messages
                "charging_loading": "🔌 កំពុងផ្ទុកស្ថានីយ៍បញ្ចូលថាមពល...",
                "charging_no_stations": "⚠️ មិនមានស្ថានីយ៍បញ្ចូលថាមពលនៅពេលនេះទេ។",
                "charging_no_stations_in_location": "⚠️ រកមិនឃើញស្ថានីយ៍បញ្ចូលថាមពលនៅ {location} ទេ។",
                "charging_locations_header": "🔌 ទីតាំងស្ថានីយ៍បញ្ចូលថាមពល\n\nជ្រើសរើសទីតាំងដើម្បីមើលស្ថានីយ៍បញ្ចូលថាមពលដែលមាន:",
                "charging_stations_header": "🔌 ស្ថានីយ៍បញ្ចូលថាមពលដែលមាន\n\nជ្រើសរើសស្ថានីយ៍ដើម្បីមើលព័ត៌មានលម្អិត:",
                "charging_error": "❌ មានបញ្ហាក្នុងការផ្ទុកស្ថានីយ៍បញ្ចូលថាមពល។ សូមព្យាយាមម្តងទៀតនៅពេលក្រោយ។",
                "charging_back_to_locations": "🔙 ត្រលប់ទីតាំង",
                "charging_view_on_map": "🗺️ មើលលើផែនទី",
                
                # Charging Station Search Filters
                "charging_station_search_filters": "🔌 តម្រងស្វែងរកស្ថានីយ៍បញ្ចូលថាមពល",
                "search_charging_stations": "🔌 ស្វែងរកស្ថានីយ៍បញ្ចូលថាមពល",
                "no_charging_stations_found": "⚠️ រកមិនឃើញស្ថានីយ៍បញ្ចូលថាមពលដែលត្រូវនឹងលក្ខខណ្ឌរបស់អ្នកទេ។",
                "price_filter": "តម្រងតម្លៃ",
                "power_filter": "តម្រងថាមពល",
                "location_filter": "តម្រងទីតាំង",
                "type_filter": "តម្រងប្រភេទ",
                "connector_filter": "តម្រងឆ្នាំង",
                "apply_filters": "អនុវត្តតម្រង",
                "clear_filters": "សម្អាតតម្រង",
                "price_range": "ចន្លោះតម្លៃ",
                "power_range": "ចន្លោះថាមពល",
                "location": "ទីតាំង",
                "station_type": "ប្រភេទស្ថានីយ៍",
                "connector_type": "ប្រភេទឆ្នាំង",
                "any": "ណាមួយ",
                "choose_location": "ជ្រើសរើសទីតាំង:",
                "select_connector_type": "ជ្រើសរើសប្រភេទឆ្នាំង",
                "choose_connector": "ជ្រើសរើសប្រភេទឆ្នាំង:",
                
                # New Charging Station Options
                "charging_station_options": "🔌 ជម្រើសស្ថានីយ៍បញ្ចូលថ្ម\n\nជ្រើសរើសរបៀបដែលអ្នកចង់មើលស្ថានីយ៍បញ្ចូលថ្ម:",
                "show_by_location": "📍 បង្ហាញតាមទីតាំង",
                "show_nearby": "📍 បង្ហាញនៅជិត",
                "view_more_stations": "📋 មើលស្ថានីយ៍បន្ថែម",
                "station_count": "ស្ថានីយ៍ {current} នៃ {total}",
                "available": "មាន",
                "unavailable": "អត់មាន",
                "view_on_map": "🗺️ មើលលើផែនទី",
                "back_to_charging_options": "🔙 ត្រលប់ទៅជម្រើស",
                
                # Garage Messages
                "service_type":"ប្រភេទសេវាកម្ម",
                "garages": "🔧 ហាងជួសជុល",
                "garage_loading": "🔧 កំពុងផ្ទុកហាងជួសជុល...",
                "garage_no_garages": "⚠️ មិនមានហាងជួសជុលនៅពេលនេះទេ។",
                "garage_no_garages_in_location": "⚠️ រកមិនឃើញហាងជួសជុលនៅ {location} ទេ។",
                "garage_locations_header": "🔧 ទីតាំងហាងជួសជុល\n\nជ្រើសរើសទីតាំងដើម្បីមើលហាងជួសជុលដែលមាន:",
                "garage_location": "📍 ទីតាំង: {location}",
                "garage_rating": "⭐ ការវាយតម្លៃ: {rating}/5.0",
                "garage_service": "🔧 សេវាកម្ម: {service}",
                "garage_price_range": "💰 ជួរតម្លៃ: {price_range}",
                
                # Accessory Messages
                "view_accessories": "⚙️ មើលគ្រឿងបន្លាស់",
                "accessory_loading": "⚙️ កំពុងផ្ទុកគ្រឿងបន្លាស់...",
                "accessory_no_accessories": "⚠️ មិនមានគ្រឿងបន្លាស់នៅពេលនេះទេ។",
                "accessory_no_category_accessories": "⚠️ មិនមានគ្រឿងបន្លាស់ {category} ទេ។",
                "accessory_categories_header": "⚙️ ជ្រើសរើសប្រភេទគ្រឿងបន្លាស់\n\nជ្រើសរើសប្រភេទដើម្បីមើលគ្រឿងបន្លាស់ដែលមាន:",
                "accessory_list_header": "⚙️ គ្រឿងបន្លាស់ {category}\n\nជ្រើសរើសគ្រឿងបន្លាស់ដើម្បីមើលព័ត៌មានលម្អិត:",
                "accessory_error": "❌ មានបញ្ហាក្នុងការផ្ទុកគ្រឿងបន្លាស់។ សូមព្យាយាមម្តងទៀតនៅពេលក្រោយ។",
                "accessory_back_to_categories": "🔙 ត្រលប់ទៅប្រភេទ",
                "accessory_phone": "📞 ទូរស័ព្ទ: {phone}",
                "accessory_contact": "📞 ទំនាក់ទំនង: {contact}",
                "accessory_rating": "⭐ ការវាយតម្លៃ: {rating}/5",
                "accessory_sku": "🏷️ លេខកូដ: {sku}",
                "accessory_weight": "⚖️ ទម្ងន់: {weight}kg",
                "accessory_color": "🎨 ពណ៌: {color}",
                "accessory_brand": "🏷️ ម៉ាក: {brand}",
                "accessory_category": "📦 ប្រភេទ: {category}",
                "accessory_location": "📍 ទីតាំង: {location}",
                "accessory_price": "💰 តម្លៃ: {price}",
                "accessory_compatible": "🚗 ត្រូវគ្នា: {models}",
                "accessory_count": "📊 គ្រឿងបន្លាស់ {current} នៃ {total}",
                
                # Accessory Loading and Navigation
                "loading_accessories": "⚙️ កំពុងផ្ទុកគ្រឿងបន្លាស់...",
                "no_accessories_available": "⚠️ មិនមានគ្រឿងបន្លាស់នៅពេលនេះទេ។",
                "select_accessory_category": "⚙️ ជ្រើសរើសប្រភេទគ្រឿងបន្លាស់\n\nជ្រើសរើសប្រភេទដើម្បីមើលគ្រឿងបន្លាស់ដែលមាន:",
                "no_category_accessories": "⚠️ មិនមានគ្រឿងបន្លាស់ {category} ទេ។",
                "check_other_categories": "🔍 ពិនិត្យប្រភេទផ្សេង",
                "loading_category_accessories": "⚙️ កំពុងផ្ទុកគ្រឿងបន្លាស់ {category}...",
                "accessories_back_to_categories": "🔙 ត្រលប់ទៅប្រភេទ",
                "accessories_back_to_list": "🔙 ត្រលប់ទៅបញ្ជី",
                "view_more_accessories": "👀 មើលគ្រឿងបន្លាស់បន្ថែម",
                "back_to_accessories": "🔙 ត្រលប់ទៅគ្រឿងបន្លាស់",
                
                # Accessory Contact
                "contact_accessory_name": "⚙️ គ្រឿងបន្លាស់: {name}",
                "contact_accessory_price": "💰 តម្លៃ: {price}",
                "contact_accessory_location": "📍 ទីតាំង: {location}",
                "phone_accessory_name": "📱 គ្រឿងបន្លាស់: {name}",
                
                # Accessory Details Header
                "accessory_details_header": "⚙️ ព័ត៌មានលម្អិតគ្រឿងបន្លាស់",
                "accessory_name": "📦 ឈ្មោះ: {name}",
                "accessory_description": "📝 ការពិពណ៌នា: {description}",
                "accessory_reviews": "📊 ការវាយតម្លៃ: {count}",
                
                # Browse More Accessories
                "browse_more_accessory": "⚙️ រកមើលគ្រឿងបន្លាស់បន្ថែម",
                "garage_phone": "📞 លេខទូរស័ព្ទ: {phone}",
                "garage_contact": "📧 ព័ត៌មានទំនាក់ទំនង: {contact}",
                
                # New Garage Options
                "garage_options": "🔧 ជម្រើសហាងជួសជុល\n\nជ្រើសរើសរបៀបដែលអ្នកចង់មើលហាងជួសជុល:",
                "garage_count": "ហាងជួសជុល {current} នៃ {total}",
                "back_to_garage_options": "🔙 ត្រលប់ទៅជម្រើស",
                "garage_hours": "🕐 ម៉ោងបើកបិទ: {hours}",
                "garage_garages_header": "🔧 ហាងជួសជុលដែលមាន\n\nជ្រើសរើសហាងដើម្បីមើលព័ត៌មានលម្អិត:",
                
                # Garage Search Filters
                "garage_search_filters": "🔧 តម្រងស្វែងរកហាងជួសជុល",
                "service_filter": "តម្រងសេវាកម្ម",
                "choose_price_range": "ជ្រើសរើសជួរតម្លៃ:",
                "select_service_type": "ជ្រើសរើសប្រភេទសេវាកម្ម",
                "choose_service": "ជ្រើសរើសប្រភេទសេវាកម្ម:",
                "select_garage_location": "ជ្រើសរើសទីតាំងហាងជួសជុល",
                "choose_garage_location": "ជ្រើសរើសទីតាំង:",
                "loading_locations": "កំពុងផ្ទុកទីតាំង...",
                "no_locations_available": "មិនមានទីតាំងនៅពេលនេះទេ។",
                "location_error": "កំហុសក្នុងការផ្ទុកទីតាំង។ សូមព្យាយាមម្តងទៀត។",
                "garage_search_results": "លទ្ធផលស្វែងរកហាងជួសជុល",
                "no_garages_found": "រកមិនឃើញហាងជួសជុលដែលត្រូវនឹងលក្ខខណ្ឌរបស់អ្នកទេ។",
                "try_different_filters": "សូមព្យាយាមកែប្រែតម្រងស្វែងរករបស់អ្នក។",
                "back_to_filters": "ត្រលប់ទៅតម្រង",
                "refine_search": "កែលម្អការស្វែងរក",
                "back_to_search": "ត្រលប់ទៅការស្វែងរក",
                "page": "ទំព័រ",
                "filters_cleared": "តម្រងទាំងអស់ត្រូវបានសម្អាត!",
                "search_error": "កំហុសស្វែងរក",
                
                # Accessory Messages
                "view_accessories": "🔧 មើលគ្រឿងបន្លាស់",
                "accessories_loading": "🔧 កំពុងផ្ទុកគ្រឿងបន្លាស់...",
                "accessories_no_accessories": "⚠️ មិនមានគ្រឿងបន្លាស់នៅពេលនេះទេ។",
                "accessories_types_header": "🔧 ប្រភេទគ្រឿងបន្លាស់\n\nជ្រើសរើសប្រភេទដើម្បីមើលគ្រឿងបន្លាស់ដែលមាន:",
                "accessories_list_header": "🔧 គ្រឿងបន្លាស់ {type}\n\nជ្រើសរើសគ្រឿងបន្លាស់ដើម្បីមើលព័ត៌មានលម្អិត:",
                "accessory_details_header": "🔧 ព័ត៌មានលម្អិតគ្រឿងបន្លាស់",
                "accessory_name": "📝 ឈ្មោះ: {name}",
                "accessory_type": "🏷️ ប្រភេទ: {type}",
                "accessory_description": "📄 ការពិពណ៌នា: {description}",
                "accessory_price": "💰 តម្លៃ: ${price}",
                "accessory_location": "📍 ទីតាំង: {location}",
                "accessory_availability": "✅ ភាពអាចរកបាន: {availability}",
                "accessory_manufacturer": "🏭 អ្នកផលិត: {manufacturer}",
                "accessory_warranty": "🛡️ ការធានា: {warranty}",
                "accessory_installation": "🔧 ការដំឡើង: {installation}",
                "accessory_compatibility": "🔗 ភាពឆបគ្នា: {compatibility}",
                "accessory_phone": "📞 ទូរស័ព្ទ: {phone}",
                "accessory_contact": "📞 ទំនាក់ទំនង: {contact}",
                "accessory_rating": "⭐ ការវាយតម្លៃ: {rating}/5",
                "accessory_sku": "🏷️ SKU: {sku}",
                "accessory_voltage": "⚡ វ៉ុល: {voltage}V",
                "accessory_capacity": "🔋 ចំណុះ: {capacity}",
                "accessory_compatible": "🚗 ឆបគ្នា: {vehicles}",
                "accessory_count": "📊 គ្រឿងបន្លាស់ {current} នៃ {total}",
                
                # Accessory Loading and Navigation
                "loading_accessories": "🔧 កំពុងផ្ទុកគ្រឿងបន្លាស់...",
                "no_accessories_available": "⚠️ មិនមានគ្រឿងបន្លាស់នៅពេលនេះទេ។",
                "select_accessory_type": "🔧 ជ្រើសរើសប្រភេទគ្រឿងបន្លាស់\n\nជ្រើសរើសប្រភេទគ្រឿងបន្លាស់ដើម្បីមើល:",
                "no_type_accessories": "⚠️ មិនមានគ្រឿងបន្លាស់ {type} ទេ។",
                "check_other_types": "🔍 ពិនិត្យប្រភេទផ្សេង",
                "loading_type_accessories": "🔧 កំពុងផ្ទុកគ្រឿងបន្លាស់ {type}...",
                "accessories_back_to_types": "🔙 ត្រលប់ប្រភេទ",
                "accessories_back_to_list": "🔙 ត្រលប់បញ្ជី",
                "view_more_accessories": "👀 មើលគ្រឿងបន្លាស់បន្ថែម",
                "back_to_accessories": "🔙 ត្រលប់គ្រឿងបន្លាស់",
                
                # Accessory Contact
                "contact_accessory_name": "🔧 គ្រឿងបន្លាស់: {name}",
                "contact_accessory_price": "💰 តម្លៃ: {price}",
                "contact_accessory_location": "📍 ទីតាំង: {location}",
                "phone_accessory_name": "📱 គ្រឿងបន្លាស់: {name}",
                
                # Browse More Accessories
                "browse_more_accessory": "🔧 រកមើលគ្រឿងបន្លាស់បន្ថែម",
                
                # Accessory Contact Seller
                "contact_seller_header": "📞 ទំនាក់ទំនងអ្នកលក់គ្រឿងបន្លាស់",
                "contact_phone": "📞 ទូរស័ព្ទ: {phone}",
                "contact_tap_to_copy": "💡 ចុចប៊ូតុងខាងក្រោមដើម្បីចម្លងលេខទូរស័ព្ទ",
                "copy_phone_number": "📞 ចម្លងលេខទូរស័ព្ទ",
                "contact_info_loaded": "ព័ត៌មានទំនាក់ទំនងត្រូវបានផ្ទុក",
                "contact_info_not_available": "ព័ត៌មានទំនាក់ទំនងមិនមាន",
                "contact_info_error": "មានបញ្ហាក្នុងការផ្ទុកព័ត៌មានទំនាក់ទំនង",
                
                # Seller Phone Header and Instructions
                "seller_phone_header": "📞 ព័ត៌មានទំនាក់ទំនងអ្នកលក់",
                "phone_copy_instruction": "💡 ចុចប៊ូតុងខាងក្រោមដើម្បីចម្លងលេខទូរស័ព្ទ",
                
                "accessories_error": "❌ មានបញ្ហាក្នុងការផ្ទុកគ្រឿងបន្លាស់។ សូមព្យាយាមម្តងទៀតនៅពេលក្រោយ។",
                "accessories_back_to_list": "🔙 ត្រលប់បញ្ជី",
                "garage_error": "❌ មានបញ្ហាក្នុងការផ្ទុកហាងជួសជុល។ សូមព្យាយាមម្តងទៀតនៅពេលក្រោយ។",
                "garage_back_to_locations": "🔙 ត្រលប់ទីតាំង",
                "garage_view_on_map": "🗺️ មើលលើផែនទី",
                "garage_map_link": "🗺️ មើលលើ Google Maps",
                
                # Car Selling Flow
                "sell_car_start": "🚗 ចូរយើងដាក់លក់រថយន្តរបស់អ្នក!",
                "ask_car_model": "ជំហានទី 1/5: តើម៉ូដែលរថយន្តរបស់អ្នកជាអ្វី?\n(ឧទាហរណ៍៖ Camry, Civic)",
                "ask_car_brand": "ជំហានទី 2/5: តើម៉ាករថយន្តរបស់អ្នកជាអ្វី?\n(ឧទាហរណ៍៖ Toyota, Honda)",
                "ask_car_description": "ជំហានទី 3/5: សូមផ្តល់ការពិពណ៌នាអំពីរថយន្តរបស់អ្នក៖\n- ឆ្នាំ\n- ស្ថានភាព\n- ចំនួនគីឡូម៉ែត្រ\n- មុខងារន្ថែម",
                "ask_car_price": "ជំហានទី 4/5: តើតម្លៃរថយន្តរបស់អ្នកប៉ុន្មាន? (គិតជា USD)",
                "ask_car_location": "ជំហានទី 5/5: តើរថយន្តស្ថិតនៅទីណា?",
                
                # Settings
                "settings_title": "⚙️ ការកំណត់\n\nតើអ្នកចង់កែប្រែអ្វី?",
                "change_language": "🌐 ប្តូរភាសា",
                "update_contact": "📱 ធ្វើបច្ចុប្បន្នភាពទំនាក់ទំនង",
                "notification_settings": "🔔 ការកំណត់ការជូនដំណឹង",
                "select_language": "🌐 សូមជ្រើសរើសភាសាដែលអ្នកចង់បាន:",
                "back_to_menu": "⬅️ ត្រឡប់ទៅម៉ឺនុយ",
                "back_to_settings": "⬅️ ត្រឡប់ទៅការកំណត់",
                "language_changed": "✅ ភាសាត្រូវបានប្តូរទៅជាខ្មែរ!",
                
                # Help Section - NEW ADDITIONS
                "help_center": "❓ ជំនួយ\n\nសូមស្វាគមន៍មកកាន្នួយ! នៅទីនេះអ្នកអាចកឃើញព័ត៌មានអំពីរបៀបប្រើប្រាស់បូតទីផ្សាររថយន្តរបស់យើង។\n\nតើអ្នកចង់បានជំនួយអំពីអ្វី?",
                "help_browse_cars": "🔍 រកមើលរថយន្ត",
                "help_explore": "🚗 ស្វែងយល់អំពីរថយន្ត",
                "help_search": "🔍 ស្វែករក",
                "help_favourites": "❤️ ចំណូលចិត្ត",
                "help_contact": "📞 ទំនាក់ទំនង",
                "help_settings": "⚙️ ការកំណត់",
                "help_charging_stations": "⚡ ស្ថានីយ៍បញ្ចូលថាមពល",
                "help_garage": "🔧 ហាងជួសជុល",
                "back_to_help": "⬅️ ត្រឡប់ទៅជំនួយ",
                
                # Help Content
                "help_browse_cars_content": "🔍 របៀបស្វែងយល់រថយន្ត\n\n📋 រកមើលតាមប្រភេទ:\n1. ចុច 'មើលរថយន្ត' ពីម៉ឺនុយដើម\n2. ជ្រើសរើសម៉ាករថយន្តដែលអ្នកចាប់អារម្មណ៍\n3. រកមើលរថយន្តដែលមានតាមប្រភេទ\n\n🔍 ស្វែងយល់ព័ត៌មានលម្អិតរថយន្ត:\n4. មើលព័ត៌មានរថយន្តពេញលេញ:\n   • ម៉ូដែល ឆ្នាំ និងលក្ខណៈពិសេស\n   • តម្លៃ និងជម្រើសហិរញ្ញវត្ថុ\n   • ទីតាំង និងព័ត៌មានអ្នកលក់\n   • រូបភាពគុណភាពខ្ពស់\n\n⚡ សកម្មភាពរហ័ស:\n5. ទំនាក់ទំនងអ្នកលក់ដោយផ្ទាល់\n6. បន្ថែមរថយន្តទៅចំណូលចិត្ត\n7. ចែករំលែកព័ត៌មានរថយន្តជាមួយមិត្តភក្តិ\n\n💡 គន្លឹះអ្នកជំនាញ:\n• ប្រើប៊ូតុងរុករកដើម្បីស្វែងយល់រថយន្តបន្ថែម\n• ច្រោះតាមចន្លោះតម្លៃសម្រាប់លទ្ធផលប្រសើរ\n• រក្សាទុករថយន្តដែលចាប់អារម្មណ៍ដើម្បីប្រៀបធៀបក្រោយ\n• ពិនិត្យប្រវត្តិរថយន្ត និងព័ត៌មានលម្អិតអំពីស្ថានភាព",
                "help_favourites_content": "❤️ គ្រប់គ្រងចំណូលចិត្ត\n\n1. ពេលកំពុងមើលរថយន្ត ចុច 'បន្ថែមទៅចំណូលចិត្ត'\n2. ចូលទៅកាន់ចំណូលចិត្តរបស់អ្នកពីម៉ឺនុយដើម\n3. មើលរថយន្តដែលបានកកាទុកគ្រប់ពេល\n4. ដកចេញរថយន្តដែលអ្នកលែងចាប់អារម្មណ៍\n\nចំណាំ: អ្នកអាចរក្សាទុករថយន្តបានរហូតដល់ 5 គ្រឿង!",
                "help_search_content": "🔍 ជំនួយស្វែករក\n\n1. ប្រើ 'ស្វែងរក' ពីម៉ឺនុយដើម\n2. ច្រោះតាមម៉ាក ចន្លោះតម្លៃ ឬទីតាំង\n3. រកមើលលទ្ធផលស្វែងរក\n4. ប្រើ 'លទ្ធផលបន្ថែម' ដើម្បីមើលរថយន្តបន្ថែម\n5. បន្ថែមរថយន្តដែលចាប់អារម្មណ៍ទៅចំណូលចិត្ត\n\nគន្លឹះ: សាកល្បងលក្ខខណ្ឌស្វែងរកផ្សេងៗដើម្បីរកឃើញរថយន្តដ៏ល្អឥតខ្ចោះរបស់អ្នក!",
                "help_explore_content": "🚗 លក្ខណៈពិសេសស្វែងយល់អំពីរថយន្ត\n\n🎯 មជ្ឈមណ្ឌលចំណេះដឹងរថយន្តពេញលេញរបស់អ្នក\n\nស្វែងយល់អំពីរថយន្តគ្រប់ផ្នែកតាមរយៈការស្វែងយល់ដ៏ទូលំទូលាយរបស់យើង!\n\n📚 អ្វីដែលអ្នកអាចស្វែងយល់:\n• 🚗 ប្រភេទ និងម៉ូដែលរថយន្ត - រៀនអំពីប្រភេទយានយន្តផ្សេងៗ\n• ⚡ អត្ថប្រយោជន៍ និងការប្រៀបធៀប - យល់ដឹងអំពីអត្ថប្រយោជន៍នៃការមានរថយន្ត\n• 🔧 លក្ខណៈពិសេស និងបច្ចេកវិទ្យា - ស្វែងយល់លក្ខណៈពិសេសរថយន្តទំនើប\n• 🛡️ សុវត្ថិភាព និងការថែទាំ - រៀនអំពីសុវត្ថិភាព និងការថែទាំរថយន្ត\n• 🌱 ជម្រើសនៃការសន្សំសម្ចៃថាមពល - ស្វែងយល់យានយន្តដែលមិនបំពុលបរិស្ថាន\n\n💡 របៀបប្រើប្រាស់:\n1. ចុច 'ស្វែងយល់អំពីរថយន្ត' ពីម៉ឺនុយដើម\n2. ជ្រើសរើសប្រធានបទដែលអ្នកចាប់អារម្មណ៍\n3. អានព័ត៌មានលម្អិត និងមគ្គុទេសក៍\n4. ប្រើប៊ូតុងរុករកដើម្បីស្វែងយល់ប្រធានបទបន្ថែម\n\n🎯 ល្អឥតខ្ចោះសម្រាប់ទាំងអ្នកចាប់ផ្តើម និងអ្នកចូលចិត្តរថយន្ត!",              "help_contact_content": "📞 ព័ត៌មានទំនាក់ទំនង\n\n• ជំនួយតេឡេក្រាម: @sim_senchamrong\n• ទូរស័ព្ទ: +855 96 554 5454\n\nFeel free to reach out if you have any questions or need assistance with buying or selling cars!",
                

                "commands_title": "📋 ពាក្យបញ្ជាដែលមាន\n\nនេះគឺជាបញ្ជីពាក្យបញ្ជាដែលអ្នកអាចប្រើបាន:",
                "commands_list": "🤖 ពាក្យបញ្ជាមូលដ្ឋាន:\n/start - ចាប់ផ្តើមបូត\n/help - បង្ហាញជំនួយ\n\n🚗 ពាក្យបញ្ជារថយន្ត:\n/cars - មើលរថយន្តដែលមាន\n/search - ស្វែងរករថយន្ត\n/favorites - មើលចំណូលចិត្តរបស់អ្នក\n\n⚙️ ពាក្យបញ្ជាការកំណត់:\n/settings - បើកការកំណត់\n/contact - ទំនាក់ទំនងជំនួយ\n/explore - ស្វែងយល់អំពីរថយន្ត",
                "command_start_desc": "🤖 /start\n\nចាប់ផ្តើមបូត និងបង្ហាញម៉ឺនុយដើម។ ប្រើពាក្យបញ្ជានេះដើម្បីចាប់ផ្តើមការសន្ទនាជាមួយបូត ឬត្រឡប់ទៅម៉ឺនុយដើម។",
                "command_help_desc": "❓ /help\n\nបង្ហាញមជ្ឈមណ្ឌលជំនួយជាមួយនឹងព័ត៌មានលម្អិតអំពីរបៀបប្រើប្រាស់បូត។ រួមបញ្ចូលមគ្គុទេសក៍ និងគន្លឹះសម្រាប់លក្ខណៈពិសេសទាំងអស់។",
                "command_cars_desc": "🚗 /cars\n\nមើលរថយន្តដែលមានទាំងអស់។ រកមើលតាមម៉ាក ឬមើលរថយន្តទាំងអស់ដែលមានលក់។",
                "command_search_desc": "🔍 /search\n\nស្វែងរករថយន្តដោយប្រើលក្ខខណ្ឌជាក់លាក់។ ច្រោះតាមម៉ាក ចន្លោះតម្លៃ ឬទីតាំង។",
                "command_favorites_desc": "❤️ /favorites\n\nមើលរថយន្តដែលអ្នកបានរក្សាទុកក្នុងចំណូលចិត្តរបស់អ្នក។ គ្រប់គ្រងបញ្ជីរថយន្តដែលអ្នកចាប់អារម្មណ៍។",
                "command_settings_desc": "⚙️ /settings\n\nបើកម៉ឺនុយការកំណត់។ ប្តូរភាសា ធ្វើបច្ចុប្បន្នភាពព័ត៌មានទំនាក់ទំនង ឬកែប្រែការកំណត់ការជូនដំណឹង។",
                "command_contact_desc": "📞 /contact\n\nទំនាក់ទំនងជំនួយ។ ទទួលបានព័ត៌មានទំនាក់ទំនងសម្រាប់ជំនួយ ឬសំណួរ។",
                "command_explore_desc": "🚗 /explore\n\nស្វែងយល់អំពីរថយន្ត។ រៀនអំពីប្រភេទរថយន្តផ្សេងៗ លក្ខណៈពិសេស និងព័ត៌មានមានប្រយោជន៍ផ្សេងៗ។",
                "help_settings_content": "⚙️ ជំនួយការកំណត់\n\n1. ប្តូរភាសា: ប្តូររវាងភាសាអង់គ្លេស និងខ្មែរ\n2. ការជូនដំណឹង: គ្រប់គ្រងចំណូលចិត្តការជូនដំណឹងរបស់អ្នក\n\nការកំណត់របស់អ្នកត្រូវបានរក្សាទុកដោយស្វ័យប្រវត្តិ!",
                "help_charging_stations_content": "⚡ ជំនួយស្ថានីយ៍បញ្ចូលថាមពល\n\n🔌 រកស្ថានីយ៍បញ្ចូលថាមពល:\n1. ចុច 'ស្ថានីយ៍បញ្ចូលថាមពល' ពីម៉ឺនុយដើម\n2. រកមើលស្ថានីយ៍បញ្ចូលថាមពលដែលមាននៅក្នុងតំបន់របស់អ្នក\n3. មើលព័ត៌មានលម្អិតស្ថានីយ៍រួមទាំង:\n   • ទីតាំង និងអាសយដ្ឋាន\n   • ប្រភេទការបញ្ចូលថាមពលដែលមាន (AC/DC)\n   • កម្លាំងថាមពលចេញ និងប្រភេទឆ្នាំង\n   • ម៉ោងធ្វើការ និងភាពអាចប្រើបាន\n   • ព័ត៌មានតម្លៃ\n\n💡 លក្ខណៈពិសេស:\n• ស្ថានភាពអាចប្រើបានក្នុងពេលវេលាជាក់ស្តែង\n• ជំនួយការណែនាំផ្លូវ\n• ការវាយតម្លៃ និងការដាក់ពិន្ទុស្ថានីយ៍\n• សមត្ថភាពកក់ទុក (នៅកន្លែងដែលមាន)\n\n🎯 ល្អឥតខ្ចោះសម្រាប់ការរៀបចំការបញ្ចូលថាមពលរថយន្តអគ្គិសនីរបស់អ្នក!",
                "help_garage_content": "🔧 ជំនួយសេវាកម្មហាងជួសជុល\n\n🛠️ រកសេវាកម្មហាងជួសជុល:\n1. ចុច 'ហាងជួសជុល' ពីម៉ឺនុយដើម\n2. រកមើលហាងជួសជុល និងមជ្ឈមណ្ឌលសេវាកម្មដែលមានវិញ្ញាបនបត្រ\n3. មើលព័ត៌មានហាងជួសជុលរួមទាំង:\n   • ប្រភេទសេវាកម្មដែលផ្តល់\n   • ទីតាំង និងព័ត៌មានទំនាក់ទំនង\n   • ម៉ោងធ្វើការ\n   • ការឯកទេស (រថយន្តអគ្គិសនី ហាយប្រីត ប្រពៃណី)\n   • ការវាយតម្លៃ និងការពិនិត្យឡើងវិញរបស់អតិថិជន\n\n🔧 សេវាកម្មដែលមាន:\n• ការថែទាំ និងសេវាកម្មទៀងទាត់\n• ការជួសជុល និងការវិនិច្ឆ័យ\n• សេវាកម្មជាក់លាក់សម្រាប់រថយន្តអគ្គិសនី\n• ជំនួយបន្ទាន់នៅផ្លូវ\n• ការជំនួសគ្រឿងបន្លាស់\n\n💡 គន្លឹះ:\n• ពិនិត្យការឯកទេសហាងជួសជុលសម្រាប់ប្រភេទរថយន្តរបស់អ្នក\n• អានការពិនិត្យឡើងវិញរបស់អតិថិជនមុនពេលកក់\n• ប្រៀបធៀបតម្លៃ និងសេវាកម្មដែលផ្តល់",
                
                # Help Action Buttons
                "try_browsing_now": "🔍 សាកល្បងរកមើលឥឡូវនេះ",
                "view_my_favourites": "❤️ មើលចំណូលចិត្តរបស់ខ្ញុំ",
                "open_settings": "⚙️ បើកការកំណត់",
                
                # Favourites
                "no_favourites": "អ្នកមិនទាន់បានរក្សាទុករថយន្តណាមួយក្នុងចំណូលចិត្តរបស់អ្នកនៅឡើយទេ។",
                "browse_more_cars": "🔍 រកមើលរថយន្ត",
                "added_to_favourites": "✅ បានបន្ថែមទៅចំណូលចិត្ត!",
                "already_favourited_message": "⚠️ រថយន្តនេះមានក្នុងចំណូលចិត្តរបស់អ្នករួចហើយ!",
                "favourites_limit": "⚠️ អ្នកអាចបន្ថែមរថយន្តបានតែ 5 គ្រឿងប៉ុណ្ណោះ!",
                "removed_from_favourites": "✅ បានដកចេញពីចំណូលចិត្ត!",
                "your_favourites": "❤️🚗 រថយន្ត និងផ្នែកដែលអ្នកចូលចិត្ត",
                "contact_seller": "📞 ទំនាក់ទំនងអ្នកលក់",
                "add_to_favourites": "❤️ បន្ថែមទៅចំណូលចិត្ត",
                "remove_from_favourites": "❌ ដកចេញពីចំណូលចិត្ត",
                "view_more_cars": "🔍 មើលរថយន្តបន្ថែម",
                
                # Car-related translations
                "loading_cars": "កំពុងផ្ទុករថយន្តដែលមាន... 🚗",
                "no_cars_available": "មិនមានរថយន្តនៅពេលនេះទេ។ យើងនឹងជូនដំណឹងអ្នកនៅពេលមានរថយន្តថ្មី! 🔔",
                "select_car_brand": "ជ្រើសរើសម៉ាករថយន្តដើម្បីមើលរថយន្តដែលមាន:",
                "loading_brand_cars": "កំពុងផ្ទុករថយន្ត {brand}... 🚗",
                "no_brand_cars": "មិនមានរថយន្ត {brand} នៅពេលនេះទេ។ 😔\n\nយើងនឹងជូនដំណឹងអ្នកនៅពេលមានរថយន្តថ្មី!",
                "check_other_brands": "🔄 ពិនិត្យម៉ាកផ្សេងទៀត",
                "car_name": "📦 ឈ្មោះ: {name}",
                "car_price": "💰 តម្លៃ: {price}",
                "car_location": "📍 ទីតាំង: {location}",
                "car_type": "🏷️ ប្រភេទ: {type}",
                "car_rating": "⭐️ ការវាយតម្លៃ: {rating}/5",
                "car_count": "\n\nរថយន្ត {current} នៃ {total}",
                "accessory_name": "📦 ឈ្មោះ: {name}",
                "accessory_price": "💰 តម្លៃ: {price}",
                "accessory_location": "📍 ទីតាំង: {location}",
                "accessory_type": "🏷️ ប្រភេទ: {type}",
                "accessory_rating": "⭐️ ការវាយតម្លៃ: {rating}/5",
                "actions": "🔽 សកម្មភាព",
                "choose_action": "ជ្រើសរើសសកម្មភាព:",
                "image_not_available": "⚠️ រូបភាពមិនអាចប្រើបាន",
                "error_loading_content": "⚠️ កំហុសក្នុងការផ្ទុកមាតិកា",
                
                # Navigation
                "previous": "⬅️ មុន",
                "next": "➡️ បន្ទាប់",
                "back": "⬅️ ត្រឡប់",
                "refresh": "🔄 ផ្សេងទៀត",
                "your_notifications": "🔔 ការជូនដំណឹងរបស់អ្នក\n\n",
                "new_notifications_header": "📫 ការជូនដំណឹងថ្មី:\n",
                
                # Support
                "contact_support_message": "📞 ទំនាក់ទំនងជំនួយ\n\n📱 អ្នកជំនួយតេឡេក្រាម: @sim_senchamrong\n📱 ទូរស័ព្ទ: +855 96 554 5454\nតើយើងអាចជួយអ្នកយ៉ាងណា? សូមវាយសារអ្នកខាងក្រោម។",
                
                # Notification Settings
                "notification_settings_message": "🔔 ការកំណត់ការជូនដំណឹង\n\nគ្រប់គ្រងចំណូលចិត្តការជូនដំណឹងរបស់អ្នក:",
                "new_cars_notification": "🚗 ការជូនដំណឹងរថយន្តថ្មី",
                "price_drops_notification": "💰 ការជូនដំណឹងការធ្លាក់ចុះតម្លៃ",
                "transaction_updates_notification": "📋 ការជូនដំណឹងការធ្វើបច្ចុប្បន្នភាពលើប្រតិបត្តិការ",
                "notifications_enabled": "✅ បានបើក",
                "notifications_disabled": "❌ បានបិទ",
                "notification_updated": "✅ ការកំណត់ការជូនដំណឹងត្រូវបានធ្វើបច្ចុប្បន្នភាព!",
                
                # Contact Seller
                "search_garages":"🔍 ស្វែងរកការាស់ឡាន",
                "contact_seller_message": "📞 ទំនាក់ទំនងអ្នកលក់\n\nដើម្បីទំនាក់ទំនងអ្នកលក់អំពីរថយន្តនេះ សូមចែករំលែកព័ត៌មានទំនាក់ទំនងរបស់អ្នក ឬផ្ញើសារដោយផ្ទាល់។",
                "view_other_cars": "🔍 មើលរថយន្តផ្សេងទៀត",
                "share_contact_button": "📱 ចែករំលែកទំនាក់ទំនង",
                "back_button": "⬅️ ត្រឡប់",
                "contact_seller_title": "📞 ទំនាក់ទំនងអ្នកលក់",
                "seller_contact_info": "📱 ព័ត៌មានទំនាក់ទំនងអ្នកលក់:",
                "phone_label": "ទូរស័ព្ទ:",
                
                # Location Service
                "location_request_message": "📍 ចែករំលែកទីតាំងរបស់អ្នក\n\nដើម្បីរកឃើញស្ថានីយ៍បញ្ចូលថាមពលនិងហាងជួសជុលនៅជិតអ្នក សូមចែករំលែកទីតាំងបច្ចុប្បន្នរបស់អ្នក។",
                "location_request_realtime": "📍 សូមចែករំលែកទីតាំងបច្ចុប្បន្នរបស់អ្នកដើម្បីរកសេវាកម្មនៅជិត។",
                "share_location_button": "📍 ចែករំលែកទីតាំង",
                "location_saved": "✅ ទីតាំងរបស់អ្នកត្រូវបានរក្សាទុក!",
                "location_updated": "🔄 ទីតាំងរបស់អ្នកត្រូវបានកែប្រែ!",
                "location_cleared": "🗑️ ទីតាំងរបស់អ្នកត្រូវបានលុប!",
                "location_error": "❌ មានបញ្ហាក្នុងការរក្សាទុកទីតាំង។ សូមព្យាយាមម្តងទៀត។",
                "location_not_found": "❌ រកមិនឃើញទីតាំងរបស់អ្នក។ សូមចែករំលែកទីតាំងរបស់អ្នកជាមុនសិន។",
                "location_options_message": "📍 ជម្រើសទីតាំង\n\nតើអ្នកចង់ធ្វើអ្វី?",
                "view_nearby_charging": "🔌 មើលស្ថានីយ៍បញ្ចូលថាមពលនៅជិត",
                "view_nearby_garages": "🔧 មើលហាងជួសជុលនៅជិត",
                "update_location": "🔄 កែប្រែទីតាំង",
                "clear_location": "🗑️ លុបទីតាំង",
                "location_settings": "⚙️ ការកំណត់ទីតាំង",
                "current_location": "📍 ទីតាំងបច្ចុប្បន្ន: {lat}, {lng}",
                "no_current_location": "📍 មិនមានទីតាំងដែលបានរក្សាទុក",
                "location_last_updated": "🕐 កែប្រែចុងក្រោយ: {time}",
                "nearby_charging_results": "🔌 ស្ថានីយ៍បញ្ចូលថាមពលនៅជិតអ្នក\n\nរកឃើញ {count} ស្ថានីយ៍:",
                "nearby_garages_results": "🔧 ហាងជួសជុលនៅជិតអ្នក\n\nរកឃើញ {count} ហាង:",
                "distance_away": "📏 ចម្ងាយ: {distance} គីឡូម៉ែត្រ",
                "no_nearby_charging": "⚠️ រកមិនឃើញស្ថានីយ៍បញ្ចូលថាមពលនៅជិតអ្នកទេ។",
                "no_nearby_garages": "⚠️ រកមិនឃើញហាងជួសជុលនៅជិតអ្នកទេ។",
                "back_to_location_options": "🔙 ត្រលប់ទៅជម្រើសទីតាំង",
                
                "contact_seller_instruction": "💡 អ្នកអាចទំនាក់ទំនងអ្នកលក់ដោយផ្ទាល់តាមរយៈលេខទូរស័ព្ទខាងលើ។\nសូមរំលឹកថាអ្នកបានរកឃើញរថយន្តនេះតាមរយៈបូតរបស់យើង!",
                "no_contact_info": "⚠️ មិនមានព័ត៌មានទំនាក់ទំនង\nសូមទំនាក់ទំនងជំនួយសម្រាប់ការជួយអំពីបញ្ជីនេះ។",
                "copy_phone_button": "📞 ចម្លងទូរស័ព្ទ:",
                "phone_not_available": "លេខទូរស័ព្ទមិនមាន",
                "seller_phone_title": "📞 លេខទូរស័ព្ទអ្នកលក់:",
                "how_to_contact_title": "💡 របៀបទំនាក់ទំនង:",
                "copy_instruction": "• ចុចនិងកាន់លេខខាងលើដើម្បីចម្លង",
                "dialer_instruction": "• ប្រើកម្មវិធីហៅទូរស័ព្ទរបស់អ្នកដើម្បីហៅ",
                "mention_bot_instruction": "• រំលឹកថាអ្នកបានរកឃើញរថយន្តនេះតាមរយៈបូតរបស់យើង",
                "back_to_car_details": "🔙 ត្រលប់ទៅព័ត៌មានរថយន្ត",
                "car_label": "🚗 រថយន្ត:",
                "price_label": "💰 តម្លៃ:",
                "advanced_search": "🔍ស្វែងរកតាមតម្រង",
                "advanced_search_title": "🔍ស្វែងរកតាមតម្រង",
                "search_cars": "🚗 ស្វែងរករថយន្ត",
                "search_filter": "🔍 ស្វែងរក",
                "search_accessories": "🔧 ស្វែងរកគ្រឿងបន្លាស់",
                "search_type_selection": "🔍 ជ្រើសរើសប្រភេទស្វែងរក",
                "search_type_message": "តើអ្នកចង់ស្វែងរកអ្វី?",
                "back_to_search_type": "🔙 ត្រឡប់ទៅប្រភេទស្វែងរក",
                "search_by_accessory_type": "🔧 ស្វែងរកតាមប្រភេទគ្រឿងបន្លាស់",
                "apply_accessory_filters": "✅ អនុវត្តតម្រងគ្រឿងបន្លាស់",
                "clear_accessory_filters": "🗑️ លុបតម្រងគ្រឿងបន្លាស់",
                "accessory_search_title": "🔧 តម្រងស្វែងរកគ្រឿងបន្លាស់",
                "accessory_search_results": "🔍 លទ្ធផលស្វែងរកគ្រឿងបន្លាស់ ({count} គ្រឿងបន្លាស់បានរកឃើញ)",
                "no_accessory_search_results": "❌ មិនមានគ្រឿងបន្លាស់ដែលផ្គូផ្គងនឹងលក្ខណៈស្វែងរកទេ។ សូមបំពេញតម្រងរបស់អ្នក។",
                "accessory_price_filter": "តម្រងតម្លៃគ្រឿងបន្លាស់៖ ${price_min:,} - ${price_max:,}",
                "accessory_location_filter": "តម្រងទីតាំងគ្រឿងបន្លាស់៖ {location}",
                "accessory_type_filter": "តម្រងប្រភេទគ្រឿងបន្លាស់៖ {type}",
                "accessory_filters_cleared": "តម្រងគ្រឿងបន្លាស់ត្រូវបានលុបចេញ!",
                "found_accessories_matching": "រកឃើញ {count} គ្រឿងបន្លាស់ដែលផ្គូផ្គងនឹងតម្រងរបស់អ្នក!",
                "no_accessories_found_filters": "មិនមានគ្រឿងបន្លាស់ដែលផ្គូផ្គងនឹងតម្រងរបស់អ្នកទេ។",
                "warranty": "ការធានា",
                "voltage": "វ៉ុល",
                "capacity": "ចំណុះ",
                "contact_seller": "📞 ទាក់ទងអ្នកលក់",
                "add_to_favourites": "❤️ បន្ថែមទៅចំណូលចិត្ត",
                "view_more_accessories": "➡️ មើលគ្រឿងបន្លាស់បន្ថែម",
                "modify_filters": "🔍 កែប្រែតម្រង",
                "back_to_menu": "🏠 ត្រឡប់ទៅម៉ឺនុយ",
                "accessory_of_total": "គ្រឿងបន្លាស់ {current} នៃ {total}",
                "search_by_price": "💰 ស្វែងរកតាមជួរថ្លៃ",
                "no_filters_applied": "❌ មិនមានតម្រងត្រូវបានអនុវត្ត",
                "select_filter_or_apply": "សូមជ្រើសរើសតម្រងដើម្បីកែប្រែ ឬអនុវត្តតម្រងបច្ចុប្បន្នដើម្បីស្វែងរក។",
                "search_by_year": "📅 ស្វែងរកតាមឆ្នាំ",
                "search_by_location": "📍 ស្វែងរកតាមទីតាំង",
                "search_by_brand": "🚗 ស្វែងរកតាមម៉ាក",
                "search_by_type": "🔧 ស្វែងរកតាមប្រភេទ",
                "keyword_search": "🔤 ស្វែងរកតាមពាក្យគន្លឹះ",
                "clear_filters": "🗑️ លុបតម្រងទាំងអស់",
                "back_to_search": "🔙 ត្រឡប់ទៅការស្វែងរក",
                "search_results": "🔍 លទ្ធផលស្វែងរក ({count} គ្រឿងរថយន្តបានរកឃើញ)",
                "car_search_results": "🔍 លទ្ធផលស្វែងរករថយន្ត ({count} គ្រឿងរថយន្តបានរកឃើញ)",
                "search_completed": "ការស្វែងរកបានបញ្ចប់",
                "accessory_search_results": "លទ្ធផលស្វែងរកគ្រឿងបន្លាស់ ({count} គ្រឿងបន្លាស់បានរកឃើញ)",
                "no_search_results": "❌ មិនមានរថយន្តដែលផ្គូផ្គងនឹងលក្ខណៈស្វែងរកទេ។ សូមបំពេញតម្រងរបស់អ្នក។",
                "current_filters": "📋 តម្រងបច្ចុប្បន្ន:",
                "price_filter": "💰 តម្លៃ: ${min} - ${max}",
                "year_filter": "📅 ឆ្នាំ: {min} - {max}",
                "location_filter": "📍 ទីតាំង: {location}",
                "brand_filter": "🚗 ម៉ាក: {brand}",
                "model_filter": "🚗 ម៉ូដែល: {model}",
                "apply_filters": "✅ អនុវត្តតម្រង",

                "modify_filters": "✏️ កែប្រែតម្រង",
                
                
                # Explore Section Translations
                "explore_car": "🚗 ការស្វែងយល់អំពីរថយន្ត",
                "explore_welcome": "🚗 សូមស្វាគមន៍មកកាន់ ការស្វែងយល់ពីរថយន្ត!\n\n🎯 មជ្ឈមណ្ឌលចំណេះដឹងរថយន្តពេញលេញរបស់អ្នក\n\nស្វែងយល់អំពីរថយន្តគ្រប់ផ្នែក — ចាប់ពីប្រភេទ និងម៉ូដែល ដល់មគ្គុទេសក៍ទិញ និងគន្លឹះថែទាំ។ មិនថាអ្នកជាអ្នកទិញជាលើកដំបូងឬអ្នកចូលចិត្តរថយន្ត — យើងមានអ្វីៗគ្រប់យ៉ាងសម្រាប់អ្នក!\n\n📚 តើអ្នកចង់ស្វែងយល់អ្វីថ្ងៃនេះ?",
                "explore_car_types": "🚗 ប្រភេទ និងម៉ូដែលរថយន្ត",
                "explore_benefits": "⚡ អត្ថប្រយោជន៍ និងការប្រៀបធៀប",
                "explore_features": "🔧 លក្ខណៈពិសេស និងបច្ចេកវិទ្យា",
                "explore_safety": "🛡️ សុវត្ថិភាព និងការថែទាំ",
                "explore_eco": "🌱 ជម្រើសនៃការសន្សំសម្ចៃថាមពល",
                "back_to_explorer": "🔙 ត្រលប់ទៅ ការស្វែងយល់រថយន្ត",
                
                 # Add these to the "km" section:
                "work_career": "💼 ការងារ និងអាជីព",
                "family_lifestyle": "👨‍👩‍👧‍👦 គ្រួសារ និងរបៀបរស់នៅ",
                "social_freedom": "🌍 សង្គម និងបរិស្ថាន",
                "cost_comparison": "🚗 vs 🚌 រថយន្ត ទល់នឹង ការដឹកជញ្ជូនសាធារណៈ",
                "independence": "🗽 ឯករាជ្យភាព",
                "safety_features": "🛡️ លក្ខណៈពិសេសសុវត្ថិភាព",
                "tech_features": "📱 បច្ចេកវិទ្យាឆ្លាតវៃ",
                "comfort_features": "🛋️ លក្ខណៈពិសេសផាសុកភាព",
                "performance_features": "⚡ ការអនុវត្ត",
                "electric_features": "🔋 លក្ខណៈពិសេសអគ្គិសនី",
                
                # API Integration Messages
                "browse_more_accessory": "🔧 រកមើលគ្រឿងបន្លាស់បន្ថែម",
                "favorite_added": "✅ រថយន្តត្រូវបានបន្ថែមទៅចំណូលចិត្ត!",
                "favorite_add_failed": "❌ បរាជ័យក្នុងការបន្ថែមរថយន្តទៅចំណូលចិត្ត។ សូមព្យាយាមម្តងទៀត។",
                "favorite_add_error": "⚠️ កំហុសក្នុងការបន្ថែមរថយន្តទៅចំណូលចិត្ត។ សូមពិនិត្យការតភ្ជាប់របស់អ្នក។",
                "favorite_removed": "✅ រថយន្តត្រូវបានដកចេញពីចំណូលចិត្ត!",
                "favorite_remove_failed": "❌ បរាជ័យក្នុងការដកចេញរថយន្តពីចំណូលចិត្ត។ សូមព្យាយាមម្តងទៀត។",
                "favorite_remove_error": "⚠️ កំហុសក្នុងការដកចេញរថយន្តពីចំណូលចិត្ត។ សូមពិនិត្យការតភ្ជាប់របស់អ្នក។",
                "favorites_load_error": "⚠️ កំហុសក្នុងការផ្ទុកចំណូលចិត្ត។ សូមពិនិត្យការតភ្ជាប់របស់អ្នកហើយព្យាយាមម្តងទៀត។",
                "user_data_sync_error": "⚠️ មិនអាចធ្វើសមកាលកម្មទិន្នន័យអ្នកប្រើប្រាស់បានទេ។ កំពុងដំណើរការក្នុងរបៀបក្រៅបណ្តាញ។",
                "api_connection_error": "⚠️ កំហុសការតភ្ជាប់។ លក្ខណៈពិសេសមួយចំនួនអាចមានកំណត់។",
                "entertainment_features": "🎵 ការកម្សាន្ត",
                
                                
                "benefits_title": "⚡ អត្ថប្រយោជន៍នៃការកាន់កាប់រថយន្ត\n\n🌟 ផ្លាស់ប្តូររបៀបរស់នៅរបស់អ្នក!\n\nការកាន់កាប់រថយន្តបើកចំហឱកាសនិងភាពងាយស្រួលជាច្រើន។ ពីការរីកចម្រើនផ្នែកអាជីពដល់ការផ្សងព្រេងជាមួយគ្រួសារ សូមស្វែងយល់ពីរបៀបដែលរថយន្តអាចបង្កើនគុណភាពជីវិតរបស់អ្នកបាន!\n\n<>ស្វែងយល់អត្ថប្រយោជន៍:",
                "work_career": "💼 ការងារ និងអាជីព",
                "family_lifestyle": "👨‍👩‍👧‍👦 គ្រួសារ និងរបៀបរស់នៅ",
                "social_freedom": "🌍 សង្គម និងបរិស្ថាន",
                "financial_benefits": "💸 អត្ថប្រយោជន៍ហិរញ្ញវត្ថុ",
                "cost_comparison": "🚗 vs 🚌 ប្រៀបធៀបរវាងរថយន្តនិងប្រាក់ចំណាយសាធារណៈ",
                "independence": "🗽 ឯករាជ្យភាព",
                "safety_features": "🛡️ លក្ខណៈសុវត្ថិភាព",
                "tech_features": "📱 បច្ចេកវិទ្យាឆ្លាតវៃ",
                "comfort_features": "🛋️ ភាពស្រួលស្រាត",
                "performance_features": "⚡ លក្ខណៈប្រសិទ្ធភាព",
                "electric_features": "🔋 លក្ខណៈរថយន្តអគ្គិសនី",
                "entertainment_features": "🎵 លក្ខណៈកម្សាន្ត",

                # Features & Technology
                "features_title": "🔧 លក្ខណៈពិសេស និងបច្ចេកវិទ្យារថយន្ត\n\n🚀 ស្វែងយល់បច្ចេកវិទ្យាកម្រិតខ្ពស់របស់រថយន្ត!\n\n🛡️ លក្ខណៈពិសេសសុវត្ថិភាព:\n• ប្រព័ន្ធជំនួយអ្នកបើកបរកម្រិតខ្ពស់\n• ប្រព័ន្ធការពារការប៉ះទង្គិច\n• បច្ចេកវិទ្យាហ្វ្រាំងឆ្លាតវៃ\n\n📱 លក្ខណៈពិសេសបច្ចេកវិទ្យា:\n• ប្រព័ន្ធព័ត៌មាន និងកម្សាន្ត\n• ការភ្ជាប់ទូរស័ព្ទឆ្លាតវៃ\n• ការគ្រប់គ្រងដោយសំឡេង\n\n🛋️ លក្ខណៈពិសេសផាសុកភាព:\n• ការគ្រប់គ្រងអាកាសធាតុ\n• កៅអីកម្រិតខ្ពស់\n• ការកាត់បន្ថយសំឡេង\n\n💡 អ្នកចាប់អារម្មណ៍លើប្រភេទលក្ខណៈពិសេសណាមួយ?",
                
                # Car Types
                "car_types_title": "🚗 ប្រភេទ និងប្រភេទរថយន្ត\n\n🎯 រកឃើញការផ្គូផ្គងដ៏ល្អឥតខ្ចោះរបស់អ្នក!\n\nរថយន្តគ្រប់ប្រភេទបម្រើតម្រូវការ និងរបៀបរស់នៅផ្សេងៗ។ ពីរថយន្តតូចសន្សំប្រេងទៅដល់រថយន្តកីឡាដ៏មានថាមពល ស្វែងយល់ថាតើប្រភេទណាសមស្របនឹងអ្នកបំផុត!\n\nជ្រើសរើសប្រភេទមួយដើម្បីស្វែងរក:",
                "sports_cars": "🏎️ រថយន្តកីឡា",
                "suvs_crossovers": "🚙 SUV និង Crossover",
                "sedans_saloons": "🚗 Sedan និង Saloon",
                "hatchbacks_compacts": "🚐 Hatchback និងតូច",
                "trucks_pickups": "🚚 ឡានដឹកទំនិញ និង Pickup",
                "convertibles": "🏎️ Convertible",
                "wagons_estates": "🚐 Wagon និង Estate",
                "minivans_mpvs": "🚌 Minivan និង MPV",
                       
                # Car Types Section
                "car_types_section": "ប្រភេទរថយន្ត",
                "type_sports_content": "🏎️ រថយន្តកីឡា\n\n🚀 ការអនុវត្តន៍ និងភាពរំភើបសុទ្ធ!\n\nលក្ខណៈពិសេសសំខាន់ៗ:\n• ម៉ាស៊ីនដែលមានកម្រិតខ្ពស់ (300+ HP)\n• ការគ្រប់គ្រង និងការបង្កើនល្បឿនល្អឥតខ្ចោះ\n• ការរចនាអាកាសយានិក\n• វត្ថុធាតុដើម និងសិប្បកម្មកម្រិតខ្ពស់\n• ប្រព័ន្ធព្យួរកម្រិតខ្ពស់\n\nម៉ូដែលពេញនិយម:\n• Porsche 911, BMW M3, Audi R8\n• Chevrolet Corvette, Ford Mustang\n• Ferrari, Lamborghini, McLaren\n\nជួរតម្លៃ: $30,000 - $500,000+\n\nល្អឥតខ្ចោះសម្រាប់:\n• អ្នកចូលចិត្តបើកបរ\n• ការផ្សងព្រេងចុងសប្តាហ៍\n• បទពិសោធន៍ផ្លូវប្រណាំង\n• ការបង្ហាញអត្តសញ្ញាណ\n\n🏁 អនុភវនូវភាពរំភើបនៃផ្លូវ!",
                "type_suv_content": "🚙 SUV និង Crossover\n\n🎯 ទំហំ, ភាពបត់បែន និងសមត្ថភាព!\n\nលក្ខណៈពិសេសសំខាន់ៗ:\n• ទីតាំងអង្គុយខ្ពស់\n• សមត្ថភាពបើកបរគ្រប់កង់\n• ទំហំដឹកទំនិញធំទូលាយ\n• សមត្ថភាពអូស\n• លក្ខណៈពិសេសសុវត្ថិភាពកម្រិតខ្ពស់\n\nម៉ូដែលពេញនិយម:\n• Toyota RAV4, Honda CR-V\n• BMW X5, Mercedes GLE\n• Jeep Wrangler, Ford Explorer\n• Tesla Model Y, Audi Q7\n\nជួរតម្លៃ: $25,000 - $100,000+\n\nល្អឥតខ្ចោះសម្រាប់:\n• គ្រួសារដែលមានកូន\n• អ្នកចូលចិត្តធម្មជាតិ\n• ការធ្វើដំណើរឆ្ងាយ\n• ការបើកបរគ្រប់អាកាសធាតុ\n\n🚙 ការផ្សងព្រេងកំពុងរង់ចាំ!",
                "type_sedan_content": "🚗 Sedan និង Saloon\n\n✨ ភាពឆើតឆាយជួបនឹងភាពជាក់ស្តែង!\n\nលក្ខណៈពិសេសសំខាន់ៗ:\n• ទ្វារបួនជាមួយនឹងកន្ទុយដាច់ដោយឡែក\n• កៅអីស្រួលសម្រាប់ 5 នាក់\n• ការបើកបររលូន និងស្ងាត់\n• សន្សំប្រេងល្អឥតខ្ចោះ\n• រូបរាងវិជ្ជាជីវៈ\n\nម៉ូដែលពេញនិយម:\n• Toyota Camry, Honda Accord\n• BMW 3 Series, Mercedes C-Class\n• Audi A4, Lexus ES\n• Tesla Model S, Genesis G90\n\nជួរតម្លៃ: $20,000 - $150,000+\n\nល្អឥតខ្ចោះសម្រាប់:\n• ការធ្វើដំណើរប្រចាំថ្ងៃ\n• អ្នកជំនួញវិជ្ជាជីវៈ\n• ការដឹកជញ្ជូនគ្រួសារស្រួល\n• ការធ្វើដំណើរសន្សំប្រេង\n\n🚗 ភាពទាន់សម័យបុរាណ!",
                "type_hatchback_content": "🚐 Hatchback និងតូច\n\n🎯 ប្រសិទ្ធភាព និងភាពរហ័សរហួនក្នុងទីក្រុង!\n\nលក្ខណៈពិសេសសំខាន់ៗ:\n• ទំហំតូចសម្រាប់ការចតងាយ\n• ទ្វារក្រោយសម្រាប់ការចូលដំណើរការ\n• សន្សំប្រេងល្អឥតខ្ចោះ\n• តម្លៃសមរម្យ\n• ការបើកបរក្នុងទីក្រុងរហ័ស\n\nម៉ូដែលពេញនិយម:\n• Honda Civic, Toyota Corolla\n• Volkswagen Golf, Ford Focus\n• MINI Cooper, Mazda3\n• Hyundai Elantra GT\n\nជួរតម្លៃ: $18,000 - $45,000\n\nល្អឥតខ្ចោះសម្រាប់:\n• អ្នកទិញលើកដំបូង\n• អ្នករស់នៅក្នុងទីក្រុង\n• អ្នកបើកបរដែលគិតពីថវិកា\n• ស្ថានការណ៍ចតងាយ\n\n🚐 ឆ្លាតវៃ និងមានប្រសិទ្ធភាព!",
                "type_truck_content": "🚚 ឡានដឹកទំនិញ និង Pickup\n\n💪 កម្លាំង, សមត្ថភាព និងឧបករណ៍ប្រើប្រាស់!\n\nលក្ខណៈពិសេសសំខាន់ៗ:\n• គ្រែដឹកទំនិញបើកចំហ\n• សមត្ថភាពអូសខ្ពស់\n• សមត្ថភាព 4WD\n• ការសាងសង់រឹងមាំ\n• ការឆ្ងាយពីដីខ្ពស់\n\nម៉ូដែលពេញនិយម:\n• Ford F-150, Chevrolet Silverado\n• Ram 1500, Toyota Tacoma\n• GMC Sierra, Nissan Titan\n• Ford Ranger, Honda Ridgeline\n\nជួរតម្លៃ: $25,000 - $80,000+\n\nល្អឥតខ្ចោះសម្រាប់:\n• ការងារ និងការសាងសង់\n• ការដឹក និងការអូស\n• ការផ្សងព្រេងក្រៅផ្លូវ\n• សកម្មភាពក្រៅផ្ទះ\n\n🚚 សាងសង់រឹងមាំសម្រាប់ការងារណាមួយ!",
                "type_convertible_content": "🏎️ Convertible\n\n☀️ សេរីភាពខ្យល់បើកចំហ និងស្ទីល!\n\nលក្ខណៈពិសេសសំខាន់ៗ:\n• ដំបូលអាចបត់បាន (ដំបូលទន់ ឬរឹង)\n• ការពង្រឹងរចនាសម្ព័ន្ធបន្ថែម\n• វត្ថុធាតុដើមខាងក្នុងកម្រិតខ្ពស់\n• ការគ្រប់គ្រងខ្យល់កម្រិតខ្ពស់\n• ការរចនាទាន់សម័យ\n\nម៉ូដែលពេញនិយម:\n• BMW Z4, Mercedes SL-Class\n• Porsche 911 Cabriolet\n• Mazda MX-5 Miata\n• Ford Mustang Convertible\n\nជួរតម្លៃ: $30,000 - $200,000+\n\nល្អឥតខ្ចោះសម្រាប់:\n• ការបើកបរទេសភាព\n• ការចេញលេងចុងសប្តាហ៍\n• ការរីករាយអាកាសធាតុក្តៅ\n• ការបង្ហាញអត្តសញ្ញាណ\n\n🏎️ អនុភវនូវខ្យល់ក្នុងសក់របស់អ្នក!",
                "type_wagon_content": "🚐 Wagon និង Estate\n\n🎯 ទំហំអតិបរមា និងភាពបត់បែន!\n\nលក្ខណៈពិសេសសំខាន់ៗ:\n• តំបន់ដឹកទំនិញបន្ថែម\n• កម្ពស់ផ្ទុកទាប\n• កៅអីក្រោយបត់រាបស្មើ\n• ការគ្រប់គ្រងដូចរថយន្ត\n• ប្រសិទ្ធភាពប្រេង\n\nម៉ូដែលពេញនិយម:\n• Subaru Outback, Volvo V90\n• Audi A4 Allroad\n• Mercedes E-Class Wagon\n• Volkswagen Golf SportWagen\n\nជួរតម្លៃ: $25,000 - $70,000+\n\nល្អឥតខ្ចោះសម្រាប់:\n• គ្រួសារសកម្ម\n• តម្រូវការដឹកទំនិញ\n• ការធ្វើដំណើរជាមួយឧបករណ៍\n• ម្ចាស់ឆ្កែ\n\n🚐 ទំហំដោយមិនមានការសម្របសម្រួល!",
                "type_minivan_content": "🚌 Minivan និង MPV\n\n👨‍👩‍👧‍👦 ការដឹកជញ្ជូនគ្រួសារចុងក្រោយ!\n\nលក្ខណៈពិសេសសំខាន់ៗ:\n• កៅអីសម្រាប់ 7-8 នាក់\n• ទ្វាររុញសម្រាប់ការចូលងាយ\n• ការកំណត់រចនាសម្ព័ន្ធកៅអីបត់បែន\n• ទំហំផ្ទុកច្រើន\n• លក្ខណៈពិសេសស្រស់ស្អាតសម្រាប់គ្រួសារ\n\nម៉ូដែលពេញនិយម:\n• Honda Odyssey, Toyota Sienna\n• Chrysler Pacifica\n• Kia Carnival, Volkswagen Atlas\n\nជួរតម្លៃ: $30,000 - $50,000+\n\nល្អឥតខ្ចោះសម្រាប់:\n• គ្រួសារធំ\n• ការចែករំលែករថយន្ត\n• ការធ្វើដំណើរជាក្រុម\n• ភាពស្រួលអតិបរមាអ្នកដំណើរ\n\n🚌 ការផ្សងព្រេងគ្រួសារធ្វើឱ្យងាយ!",
                                                
                                
                "safety_title": "🛡️ មជ្ឈមណ្ឌលសុវត្ថិភាព និងការថែទាំ\n\n🎯 រក្សាថែរថយន្តរបស់អ្នកឱ្យមានសុវត្ថិភាព និងទុកចិត្តបាន!\n\n🔧 ការថែទាំចាំបាច់:\n• ផ្លាស់ប្តូរប្រេងរាល់ ៥,០០០-៧,៥០០ ម៉ាយ\n• បង្វិលកង់រាល់ ៦,០០០-៨,០០០ ម៉ាយ\n• ពិនិត្យហ្វ្រាំងរាល់ឆ្នាំ\n• ពិនិត្យថ្មតាមរដូវកាល\n\n⚠️ ត្រូវប្រុងប្រយ័ត្នសញ្ញាហ្វូងហែរដែលគួរឱ្យកង្វល់:\n• សម្លេង ឬការបាត់បង់ស្ថេរភាពខុសប្រក្រតី\n• ភ្លើងព្រមានលើផ្ទាំងឧបករណ៍\n• បាក់បែកទឹក ឬក្លិនមិនធម្មតា\n\n💡 តើប្រធានបទសុវត្ថិភាពណាដែលអ្នកចាប់អារម្មណ៍?",
                "personal_freedom": "🎯 សេរីភាពផ្ទាល់ខ្លួន",
                "maintenance_schedule": "🔧 កាលវិភាគថែទាំ",
                "driving_safety_tips": "🛡️ គន្លឹះសុវត្ថិភាពក្នុងការបើកបរ",
                "warning_signs": "⚠️ សញ្ញាព្រមាន",
                "emergency_preparedness": "🆘 ការត្រៀមខ្លួនសម្រាប់អាសន្ន",
                "seasonal_care": "❄️ ការថែទាំតាមរដូវកាល",
                "diy_checks": "🔍 ការត្រួតពិនិត្យដោយខ្លួនឯង",
                "maintenance_guide": "🔧 មគ្គុទេសក៍ថែទាំ",
                "safety_tips": "⚠️ គន្លឹះសុវត្ថិភាព",
                "emergency_procedures": "🆘 វិធីសាស្ត្រប្រើពេលអាសន្ន",
                "diy_maintenance": "🛠️ ការថែទាំដោយខ្លួនឯង",

                "eco_title": "🌱 ជម្រើសរថយន្តដែលស្រឡាញ់បរិស្ថាន\n\n🌍 បើកបរដោយបៃតង សន្សំប្រាក់!\n\n🔋 រថយន្តអគ្គិសនី (EV):\n• មិនបញ្ចេញឧស្ម័នពុល\n• ចំណាយក្នុងការប្រើប្រាស់ទាប\n• បញ្ជូនថាមពលភ្លាមៗ\n• ប្រតិបត្តិការជាប្រក្រតី និងស្ងៀមស្ងាត់\n\n🌿 អត្ថប្រយោជន៍នៃរថយន្តឆ្លើយបញ្ចប់ (Hybrid):\n• រួមបញ្ចូលអត្ថប្រយោជន៍ពីរប្រភេទ\n• ប្រើប្រាស់ប្រេងមានប្រសិទ្ធភាពខ្ពស់\n• ការបញ្ចេញឧស្ម័នតិច\n• គ្មានការព្រួយបារម្ភពីចម្ងាយបើកបរ\n\n💡 តើអ្នករួចរាល់សម្រាប់ការបើកបរបៃតងហើយឬនៅ? ជម្រើសមួយណាដែលអ្នកចង់ស្វែងយល់បន្ថែម?",
                "electric_vehicles": "⚡ រថយន្តអគ្គិសនី",
                "hybrid_technology": "🌿 បច្ចេកវិទ្យា Hybrid",
                "fuel_efficiency": "⛽ គន្លឹះប្រើប្រាស់ប្រេងមានប្រសិទ្ធភាព",
                "environmental_impact": "🌍 វិភាគឥទ្ធិពលលើបរិស្ថាន",
                "cost_savings": "💰 ការសន្សំប្រាក់",
                "charging_infrastructure": "🔌 ហេដ្ឋារចនាសម្ព័ន្ធសម្រាប់សាកភ្លើង",
                
                
                "benefits_work_content": "💼 អត្ថប្រយោជន៍សម្រាប់អាជីព និងការងារ\n\n🚀 ជម្រើសដ៏ឆ្លាតវៃសម្រាប់ភាពជោគជ័យក្នុងអាជីព!\n\nអត្ថប្រយោជន៍ផ្នែកអាជីព:\n• ការធានាការដឹកជញ្ជូនទៅធ្វើការ\n• បង្កើនភាពជាអ្នកជំនាញ និងឥទ្ធិពល\n• អាចចូលរួមប្រជុំគ្រប់ទីកន្លែង\n• ទស្សនកិច្ចអតិថិជន និងការធ្វើដំណើរការងារ\n• ការឆ្លើយតបអាសន្នពេលមានបញ្ហាការងារ\n\nអត្ថប្រយោជន៍ផ្នែកអាជីព:\n• ឱកាសការងារពង្រីក\n• ការមកទាន់ពេល និងទុកចិត្តបាន\n• បង្កើតការិយាល័យចល័ត\n• បត់បែនម៉ោងធ្វើការបាន\n\n💡 រថយន្តរបស់អ្នកគឺជាការវិនិយោគក្នុងអាជីព!",
                "benefits_family_content": "👨‍👩‍👧‍👦 អត្ថប្រយោជន៍សម្រាប់គ្រួសារ និងជីវិតប្រចាំថ្ងៃ\n\n❤️ បង្កើនគុណភាពជីវិតគ្រួសាររបស់អ្នក!\n\nភាពងាយស្រួលសម្រាប់គ្រួសារ:\n• ដឹកនាំកូនទៅ/មកពីសាលា\n• ដំណើរកំសាន្ត និងការធ្វើវិស្សមកាលគ្រួសារ\n• ដឹកជញ្ជូនជាបន្ទាន់ក្នុងករណីវេជ្ជសាស្ត្រ\n• ទិញឥវ៉ាន់ប្រចាំសប្ដាហ៍បានងាយស្រួល\n• ដឹកនាំក្នុងសកម្មភាពកីឡា និងស្នាក់នៅ\n\nការលើកកម្ពស់ជីវិត:\n• ដំណើរប្រចាំចុងសប្ដាហ៍\n• យប់ទៅដើរលេង និងទស្សនភាព\n• ចូលរួមសកម្មភាពចំណូលចិត្ត\n• ចូលរួមព្រឹត្តិការណ៍សង្គម\n\nសុវត្ថិភាព និងការពារ:\n• ដំណើរជាសុវត្ថិភាពពេលអាកាសធាតុអាក្រក់\n• ដំណើរពេលយប់ដោយសុវត្ថិភាព\n• អាចជួយគេចខ្លួនពេលមានអាសន្ន\n\n💡 បង្កើតអនុស្សាវរីយ៍ថ្មីៗគ្រប់ដំណើរ!",
                "benefits_freedom_content": "🎯 អត្ថប្រយោជន៍ផ្នែកសេរីភាពផ្ទាល់ខ្លួន\n\n🗽 ភាពឯករាជ្យ និងបត់បែនពិតប្រាកដ!\n\nសេរីភាពក្នុងការផ្លាស់ទី:\n• អាចទៅណាក៏បាន គ្រប់ពេលវេលា\n• គ្មានកាលវិភាគបង្ខំ\n• ដំណើរបែបចៃដន្យនិងស្វែងយល់ថ្មីៗ\n• អាចទៅដល់ផ្ទះផ្ទាល់បាន\n• មានឯកជនភាពពេលធ្វើដំណើរ\n\nសេរីភាពផ្នែកពេលវេលា:\n• មិនចាំបាច់រង់ចាំការដឹកជញ្ជូនសាធារណៈ\n• ផ្លូវផ្ទាល់ទៅកាន់គោលដៅ\n• ចូលរួមកិច្ចការច្រើនក្នុងដំណើរដូចមួយ\n• អាចចាកចេញគ្រប់ពេលវេលាតាមចិត្ត\n\nសេរីភាពក្នុងរបៀបរស់នៅ:\n• ជ្រើសរើសតន្ត្រី និងបរិយាកាសដូចចិត្ត\n• អាចដឹកសត្វចិញ្ចឹម និងអ្វីៗបាន\n• បញ្ឈប់ដំណើរដោយសេរីភាព\n• ស្វែងយល់ទីកន្លែងថ្មីៗបានងាយស្រួល\n\n🗽 ម៉ោងរបស់អ្នក ជាជម្រើសរបស់អ្នក!",
                "benefits_financial_content": "💰 អត្ថប្រយោជន៍ផ្នែកហិរញ្ញវត្ថុ\n\n📈 ជម្រើសឆ្លាតវៃក្នុងការចំណាយប្រាក់!\n\nការសន្សំរយៈពេលវែង:\n• មិនចំណាយលើដំណើរសាធារណៈប្រចាំថ្ងៃ\n• ទិញឥវ៉ាន់ដោយចំណាយតិច (ទិញទំនិញច្រើនក្នុងដង)\n• ការចំណាយដឹកជញ្ជូនតិច\n• បញ្ចុះពន្ធសម្រាប់ការប្រើប្រាស់ពាណិជ្ជកម្ម\n• ជាសម្បត្តិដែលអាចបង្កើនតម្លៃ\n\nឱកាសរកចំណូល:\n• បើករថយន្តជាប្រព័ន្ធ rideshare (Uber/Lyft)\n• សេវាដឹកជញ្ជូន\n• បង្កើតអាជីវកម្មចល័ត\n• ចូលដំណើរការទៅទីផ្សារងារជាច្រើន\n\nការប្រៀបធៀបចំណាយ:\n• ដំណើរសាធារណៈ៖ $100-200/ខែ\n• ការកាន់កាប់រថយន្ត៖ $300-500/ខែ\n• តម្លៃបន្ថែម៖ ភាពងាយស្រួល និងសេរីភាព\n\n💡 រថយន្តរបស់អ្នកអាចផ្តល់ចំណូលវិញបាន!",
                "benefits_social_content": "🌍 អត្ថប្រយោជន៍សង្គម និងបរិស្ថាន\n\n🤝 ភ្ជាប់ទំនាក់ទំនង និងចូលរួមក្នុងសង្គម!\n\nអត្ថប្រយោជន៍សង្គម:\n• ជួយមិត្តភក្តិ និងគ្រួសារ\n• ចូលរួមព្រឹត្តិការណ៍សហគមន៍\n• សមាជិកកម្មអាសន្នឬចម្រាញ់អំណោយ\n• ជួយគេក្នុងករណីអាសន្ន\n• ឱកាសរួមដំណើរការ carpool\n\nការទទួលខុសត្រូវបរិស្ថាន:\n• ជ្រើសរើសរថយន្តបៃតង\n• កាត់បន្ថយដំណើរច្រើនលើថ្ងៃ\n• បង្កើតផ្លូវប្រសើរដើម្បីសន្សំ\n• គាំទ្របច្ចេកវិទ្យាបៃតង\n\nឥទ្ធិពលសហគមន៍:\n• គាំទ្រអាជីវកម្មក្នុងស្រុក\n• រួមចំណែកសេដ្ឋកិច្ច\n• មានសមត្ថភាពឆ្លើយតបពេលអាសន្ន\n• ចូលរួមក្នុងសហគមន៍ជាប្រចាំ\n\n💡 ជំរុញការផ្លាស់ប្តូរដែលមានអត្ថន័យសម្រាប់សហគមន៍របស់អ្នក!",
                "benefits_comparison_content": "🚗 vs 🚌 ការប្រៀបធៀបរវាងរថយន្ត និងដំណើរសាធារណៈ\n\n⚖️ ការប្រៀបធៀបទាំងមូល!\n\n🚗 អត្ថប្រយោជន៍នៃការកាន់កាប់រថយន្ត:\n• ភាពងាយស្រួលពីផ្ទះទៅផ្ទះ\n• ធ្វើដំណើរតាមម៉ោងផ្ទាល់ខ្លួន\n• ឯកជនភាព និងផាសុខភាព\n• អាចដឹកសំភារៈគ្មានដែនកំណត់\n• ការការពារពេលអាកាសធាតុអាក្រក់\n• សមត្ថភាពដឹកជញ្ជូនអាសន្ន\n\n🚌 អត្ថប្រយោជន៍នៃដំណើរសាធារណៈ:\n• ចំណាយប្រចាំខែទាប\n• គ្មានបញ្ហារកទីចតឡាន\n• មានអត្ថប្រយោជន៍បរិស្ថាន\n• មិនចាំបាច់បារម្ភការថែទាំ\n• អាចអាន/ធ្វើការ ពេលធ្វើដំណើរ\n\n💰 ប្រៀបធៀបចំណាយប្រចាំខែ:\n• ដំណើរសាធារណៈ៖ $100-200\n• ការកាន់កាប់រថយន្ត៖ $300-600\n• អត្ថប្រយោជន៍រថយន្ត៖ ភាពងាយស្រួលដែលមិនអាចវាស់បាន\n\n🎯 ជម្រើសល្អបំផុតអាស្រ័យលើ:\n• តម្រូវការរបៀបរស់នៅរបស់អ្នក\n• ប្រាក់ចំណូល និងថវិកា\n• ទីតាំង និងហេដ្ឋារចនាសម្ព័ន្ធ\n• ទំហំគ្រួសារ និងតម្រូវការផ្សេងៗ\n\n⚖️ ជ្រើសរើសអ្វីដែលសមរម្យសម្រាប់អ្នក!",
                
                # Add these missing keys to Khmer translations  
                "benefits_section": "អត្ថប្រយោជន៍ និងគុណសម្បត្តិ",
                "professional_work": "💼 អាជីព និងការងារ", 
                "social_environmental": "🌍 សង្គម និងបរិស្ថាន",
                
                # Features & Technology Section
                "features_section": "លក្ខណៈពិសេស និងបច្ចេកវិទ្យា",
                "features_safety_content": "🛡️ ប្រព័ន្ធសុវត្ថិភាពកម្រិតខ្ពស់\n\n🚗 ទេវតាការពារអ្នកនៅលើផ្លូវ!\n\nលក្ខណៈពិសេសសុវត្ថិភាពសកម្ម:\n• ប្រព័ន្ធហ្វ្រាំងអាសន្នស្វ័យប្រវត្តិ (AEB)\n• ការត្រួតពិនិត្យចំណុចងងឹត (BSM)\n• ការព្រមានចាកចេញពីផ្លូវ (LDW)\n• ការគ្រប់គ្រងល្បឿនបែបសម្របតាម (ACC)\n• ការព្រមានការប៉ះទង្គិចខាងមុខ (FCW)\n\nលក្ខណៈពិសេសសុវត្ថិភាពអកម្ម:\n• ថង់ខ្យល់សុវត្ថិភាពច្រើន\n• ក្រុមការពារដែលបានពង្រឹង\n• ប្រព័ន្ធហ្វ្រាំងមិនចាក់សោ (ABS)\n• ការគ្រប់គ្រងស្ថេរភាពអេឡិចត្រូនិច (ESC)\n\nអត្ថប្រយោជន៍:\n• ការពារគ្រោះថ្នាក់\n• កាត់បន្ថយភាពធ្ងន់ធ្ងរនៃរបួស\n• ការធានារ៉ាប់រងទាប\n• ចិត្តស្ងប់ក្នុងការបើកបរ\n\n🛡️ សុវត្ថិភាពជាមុនគេ ជានិច្ច!",
                "features_tech_content": "📱 លក្ខណៈពិសេសបច្ចេកវិទ្យាឆ្លាតវៃ\n\n🚀 បដិវត្តន៍រថយន្តភ្ជាប់!\n\nលក្ខណៈពិសេសការភ្ជាប់:\n• Apple CarPlay & Android Auto\n• ការភ្ជាប់ទូរស័ព្ទឆ្លាតវៃដោយគ្មានខ្សែ\n• ការភ្ជាប់ប៊្លូធូស\n• សមត្ថភាពចំណុចភ្ជាប់ Wi-Fi\n• ប្រព័ន្ធសម្គាល់សំឡេង\n\nAI និងស្វ័យប្រវត្តិកម្ម:\n• ជំនួយការសំឡេងឆ្លាតវៃ\n• ការព្រមានថែទាំដោយព្យាករណ៍\n• ការគ្រប់គ្រងអាកាសធាតុឆ្លាតវៃ\n• ប្រព័ន្ធចតស្វ័យប្រវត្តិ\n\nការគ្រប់គ្រងឆ្លាតវៃ:\n• ផ្ទាំងឧបករណ៍ឌីជីថល\n• ការបង្ហាញលើកក្បាល (HUD)\n• ផ្ទៃប៉ះដោយការប៉ះ\n\n📱 នៅតែភ្ជាប់ នៅតែឆ្លាតវៃ!",
                "features_comfort_content": "❄️ លក្ខណៈពិសេសផាសុកភាព និងប្រណីតភាព\n\n🌟 បទពិសោធន៍បើកបរកម្រិតខ្ពស់!\n\nផាសុកភាពកៅអី:\n• កៅអីកក់ និងខ្យល់\n• ទីតាំងកៅអីចងចាំ\n• ស្បែកកម្រិតខ្ពស់\n• កៅអីកែតម្រូវដោយថាមពល\n• ប្រព័ន្ធទ្រទ្រង់ចង្កេះ\n\nការគ្រប់គ្រងអាកាសធាតុ:\n• អាកាសធាតុស្វ័យប្រវត្តិពីរ/បីតំបន់\n• ប្រព័ន្ធបន្សុទ្ធខ្យល់\n• កង់ចង្កូតកក់\n• ការកំណត់អាកាសធាតុពីចម្ងាយ\n\nការប៉ះពាល់ប្រណីតភាព:\n• ពន្លឺបរិយាកាស\n• វត្ថុធាតុខាងក្នុងកម្រិតខ្ពស់\n• ដំបូលកញ្ចក់ទូលាយ\n• ការសាកថ្មឧបករណ៍ដោយគ្មានខ្សែ\n\n❄️ ប្រណីតភាពត្រូវបានកំណត់ឡើងវិញ!",
                "features_performance_content": "⚡ លក្ខណៈពិសេសប្រសិទ្ធភាព\n\n🏁 បញ្ចេញថាមពល!\n\nប្រសិទ្ធភាពម៉ាស៊ីន:\n• ម៉ាស៊ីនទួរបូ\n• ការកំណត់ពេលវ៉ាល់បម្រែបម្រួល\n• ការបញ្ចូលប្រេងផ្ទាល់\n• របៀបកែតម្រូវប្រសិទ្ធភាព\n• ប្រព័ន្ធគ្រប់គ្រងការចាប់ផ្តើម\n\nការបញ្ជូន និងប្រព័ន្ធបើកបរ:\n• ការបញ្ជូនស្វ័យប្រវត្តិកម្រិតខ្ពស់\n• ប្រព័ន្ធបើកបរកង់ទាំងអស់ (AWD)\n• ឌីផេរ៉ង់ស្យែលកំណត់ការរអិល\n• ការជ្រើសរើសរបៀបបើកបរ\n\nតួ និងការគ្រប់គ្រង:\n• ប្រព័ន្ធព្យួរបែបសម្របតាម\n• ប្រព័ន្ធហ្វ្រាំងប្រសិទ្ធភាព\n• ការកែលម្អអាកាសធាតុ\n\n⚡ ប្រសិទ្ធភាពត្រូវបានបញ្ចេញ!",
                "features_electric_content": "🔋 លក្ខណៈពិសេសអគ្គិសនី និងកូនកាត់\n\n⚡ អនាគតនៃបច្ចេកវិទ្យាយានយន្ត!\n\nថ្ម និងការសាក:\n• ថ្មលីចូម-អ៊ីយ៉ុងសមត្ថភាពខ្ពស់\n• សមត្ថភាពសាកលឿន\n• ដំណោះស្រាយសាកនៅផ្ទះ\n• ការគ្រប់គ្រងកំដៅថ្ម\n• ប្រព័ន្ធហ្វ្រាំងបង្កើតថាមពលវិញ\n\nប្រព័ន្ធបើកបរអគ្គិសនី:\n• ការផ្តល់ម៉ូម៉ង់ភ្លាមៗ\n• ការដំណើរការអគ្គិសនីស្ងៀម\n• ម៉ូទ័រអគ្គិសនីច្រើន\n• ការគ្រប់គ្រងថាមពលច្បាស់លាស់\n\nលក្ខណៈពិសេសប្រសិទ្ធភាព:\n• របៀបបើកបរអេកូ\n• ការត្រួតពិនិត្យការប្រើប្រាស់ថាមពល\n• ការធ្វើឱ្យផ្លូវល្អប្រសើរ\n• កាលវិភាគសាកឆ្លាតវៃ\n\n🔋 ឧត្តមភាពអគ្គិសនី!",
                "features_entertainment_content": "🎵 ប្រព័ន្ធកម្សាន្ត\n\n🎶 សំឡេង និងកម្សាន្តកម្រិតខ្ពស់!\n\nប្រព័ន្ធសំឡេង:\n• សំឡេងម៉ាកល្បីល្បាញ (Bose, Harman Kardon)\n• ប្រព័ន្ធសំឡេងព័ទ្ធជុំវិញ\n• អូប៉ាល័រច្រើន (8-20+ អូប៉ាល័រ)\n• ការកំណត់សំឡេងតាមបំណង\n\nការបង្ហាញ និងមេឌៀ:\n• ការបង្ហាញអេក្រង់ប៉ះធំ\n• អេក្រង់កម្សាន្តកៅអីខាងក្រោយ\n• ផ្ទាំងឧបករណ៍ឌីជីថល\n• ក្រាហ្វិកគុណភាពខ្ពស់\n\nលក្ខណៈពិសេសកម្សាន្ត:\n• ការរួមបញ្ចូលសេវាកម្មស្ទ្រីម\n• សមត្ថភាពហ្គេម (ពេលចត)\n• ការគាំទ្រការចាក់វីដេអូ\n• ច្រកភ្ជាប់ USB ច្រើន\n\nជម្រើសការភ្ជាប់:\n• ការស្ទ្រីមសំឡេងប៊្លូធូស\n• Apple CarPlay & Android Auto\n• ការរួមបញ្ចូល Spotify, Apple Music\n• ការស្ទ្រីមវិទ្យុអ៊ីនធឺណិត\n\n🎵 កម្សាន្តត្រូវបានកំណត់ឡើងវិញ!",
                "smart_technology": "📱 បច្ចេកវិទ្យាឆ្លាតវៃ",
                "comfort_luxury": "❄️ ផាសុកភាព និងប្រណីតភាព",
                "safety_systems": "🛡️ ប្រព័ន្ធសុវត្ថិភាព",
                "entertainment_systems": "🎵 ប្រព័ន្ធកម្សាន្ត",
                     
                
                # Safety & Maintenance Section - Content
                "safety_section": "សុវត្ថិភាព",
                "safety_maintenance_content": "🔧 កាលវិភាគថែទាំ\n\n📅 រក្សាឱ្យរថយន្តរបស់អ្នកដំណើរការយ៉ាងរលូន!\n\nរាល់ 3,000-5,000 ម៉ាយ:\n• ផ្លាស់ប្តូរប្រេង និងតម្រង\n• ពិនិត្យកម្រិតទឹក\n• ពិនិត្យសម្ពាធកង់\n• សម្អាតចុងថ្ម\n\nរាល់ 6,000-10,000 ម៉ាយ:\n• បង្វិលកង់\n• ផ្លាស់ប្តូរតម្រងខ្យល់\n• ពិនិត្យហ្វ្រាំង\n• ពិនិត្យខ្សែក្រវ៉ាត់ និងបំពង់\n\nរាល់ 12,000-15,000 ម៉ាយ:\n• សេវាកម្មប្រេងឡាន\n• លាងប្រព័ន្ធត្រជាក់\n• ផ្លាស់ប្តូរស្ពាន់ភ្លើង\n• ពិនិត្យខ្សែក្រវ៉ាត់ពេលវេលា\n\nប្រចាំឆ្នាំ:\n• ការពិនិត្យទូលំទូលាយ\n• ការធ្វើតេស្តការបញ្ចេញឧស្ម័ន\n• ពិនិត្យការធានារ៉ាប់រង\n• ការបន្តចុះឈ្មោះ\n\n🔧 ការពារប្រសើរជាងការជួសជុល!",
                "safety_tips_content": "🛡️ គន្លឹះសុវត្ថិភាពក្នុងការបើកបរ\n\n🎯 រក្សាសុវត្ថិភាពនៅលើផ្លូវ!\n\nមុនពេលបើកបរ:\n• កែតម្រូវកញ្ចក់ និងកៅអី\n• ពិនិត្យប្រេង និងទឹក\n• រៀបចំផ្លូវដំណើរ\n• ធានាថាខ្សែក្រវ៉ាត់សុវត្ថិភាពត្រឹមត្រូវ\n• ដកចេញនូវអ្វីដែលរំខាន\n\nពេលកំពុងបើកបរ:\n• រក្សាចម្ងាយសុវត្ថិភាព\n• ប្រើសញ្ញាបត់មុនពេល\n• ពិនិត្យចំណុចងងឹត\n• ជៀសវាងការបើកបរឆាប់រហ័ស\n• ផ្តោតលើផ្លូវ\n\nលក្ខខណ្ឌអាកាសធាតុ:\n• កាត់បន្ថយល្បឿនពេលភ្លៀង/ព្រិល\n• ប្រើភ្លើងមុខពេលមើលមិនច្បាស់\n• បង្កើនចម្ងាយតាម\n• ជៀសវាងចលនាភ្លាមៗ\n\nការបើកបរពេលយប់:\n• សម្អាតកញ្ចក់ និងភ្លើង\n• បន្ថយភ្លើងផ្ទាំងឧបករណ៍\n• មើលចេញពីភ្លើងរថយន្តមកទល់មុខ\n• សម្រាកក្នុងដំណើរឆ្ងាយ\n\n🛡️ ការបើកបរប្រុងប្រយ័ត្នជួយសង្គ្រោះជីវិត!",
                "safety_warnings_content": "⚠️ សញ្ញាព្រមាន\n\n🚨 កុំមិនអើពើនឹងសញ្ញាទាំងនេះ!\n\nបញ្ហាម៉ាស៊ីន:\n• ភ្លើងព្រមានម៉ាស៊ីន\n• សម្លេង ឬការរញ្ជួយមិនធម្មតា\n• ផ្សែងពីបំពង់បញ្ចេញ\n• បាត់បង់កម្លាំង\n• ក្តៅពេក\n\nបញ្ហាហ្វ្រាំង:\n• សម្លេងស្រែក ឬកិន\n• ឈ្នាន់ហ្វ្រាំងទន់ ឬស្រុង\n• រថយន្តទាញទៅម្ខាង\n• ភ្លើងព្រមានហ្វ្រាំង\n\nបញ្ហាកង់:\n• លំនាំស្លៀកមិនស្មើគ្នា\n• ការព្រមានសម្ពាធកង់ទាប\n• ការរញ្ជួយពេលបើកបរ\n• ការប៉ោង ឬស្នាម\n\nបញ្ហាអគ្គិសនី:\n• ភ្លើងស្រអាប់ ឬព្រិច\n• ភ្លើងព្រមានថ្ម\n• ការលំបាកក្នុងការចាប់ផ្តើម\n• គ្រឿងបរិក្ខារអគ្គិសនីខូច\n\nពេលត្រូវឈប់ភ្លាមៗ:\n• ចំហាយពីម៉ាស៊ីន\n• ការព្រមានសម្ពាធប្រេង\n• ហ្វ្រាំងខូច\n• បញ្ហាចង្កូត\n\n⚠️ ពេលមានការសង្ស័យ សូមយកទៅពិនិត្យ!",
                "safety_emergency_content": "🆘 ការត្រៀមខ្លួនសម្រាប់ភាពអាសន្ន\n\n🎯 ត្រៀមខ្លួនសម្រាប់អ្វីៗទាំងអស់!\n\nរបស់ចាំបាច់ក្នុងកេសអាសន្ន:\n• កញ្ចប់ជំនួយបឋម\n• ភ្លើងពិល និងថ្ម\n• ភ្លើងសញ្ញា ឬកញ្ចក់ឆ្លុះ\n• ខ្សែភ្ជាប់ថ្ម\n• ឧបករណ៍វាស់សម្ពាធកង់\n• ឧបករណ៍ច្រើនមុខងារ ឬឧបករណ៍មូលដ្ឋាន\n• ភួយអាសន្ន\n• ទឹក និងអាហារស្រាល\n\nជំហានអាសន្នតាមផ្លូវ:\n1. ចតសុវត្ថិភាព\n2. បើកភ្លើងគ្រោះថ្នាក់\n3. ដាក់ត្រីកោណព្រមាន\n4. ហៅសុំជំនួយ\n5. នៅឱ្យមើលឃើញ និងសុវត្ថិភាព\n\nលេខសំខាន់ៗ:\n• សេវាកម្មអាសន្ន: 911\n• ជំនួយតាមផ្លូវ\n• ក្រុមហ៊ុនធានារ៉ាប់រង\n• ជាងម៉ាស៊ីនទុកចិត្ត\n\nបន្ថែមរដូវរងា:\n• ឧបករណ៍កោសទឹកកក និងច្រាសព្រិល\n• ខ្សាច់ ឬលាមីឆ្មា\n• សម្លៀកបំពាក់ក្តៅ\n• ភួយបន្ថែម\n\n🆘 ការត្រៀមខ្លួនការពារភាពភ័យស្លន់ស្លោ!",
                "safety_seasonal_content": "❄️ ការថែទាំតាមរដូវកាល\n\n🌍 ការថែទាំរថយន្តពេញមួយឆ្នាំ!\n\nការត្រៀមរដូវរងា:\n• ប្តូរទៅកង់រដូវរងា\n• ពិនិត្យកម្រិតទឹកកកកុំឱ្យ\n• ធ្វើតេស្តថ្ម និងប្រព័ន្ធសាក\n• រក្សាធុងប្រេងឱ្យពេញ\n• ខ្ចប់កេសអាសន្នរដូវរងា\n\nការថែទាំរដូវផ្ការីក:\n• ពិនិត្យការខូចខាតរដូវរងា\n• ប្តូរទៅកង់គ្រប់រដូវកាល\n• ពិនិត្យម៉ាស៊ីនត្រជាក់\n• សម្អាតសំណល់អំបិល\n• ផ្លាស់ប្តូរដងកន្ទុយកញ្ចក់ចាស់\n\nការថែទាំរដូវក្តៅ:\n• ពិនិត្យប្រព័ន្ធត្រជាក់\n• ពិនិត្យខ្សែក្រវ៉ាត់ និងបំពង់\n• តាមដានសម្ពាធកង់\n• ប្រើម្លប់ថ្ងៃសម្រាប់ខាងក្នុង\n• រក្សាទឹកបន្ថែម\n\nការត្រៀមរដូវស្លឹកឈើជ្រុះ:\n• ធ្វើតេស្តប្រព័ន្ធកំដៅ\n• ពិនិត្យភ្លើង និងការមើលឃើញ\n• ពិនិត្យកង់សម្រាប់រដូវរងា\n• សម្អាត និងលាបម៉ូមខាងក្រៅ\n• ត្រៀមសម្រាប់ការផ្លាស់ប្តូរពេលវេលា\n\n❄️ រដូវកាលនីមួយៗមានតម្រូវការរបស់វា!",
                "safety_diy_content": "🔍 ការពិនិត្យដោយខ្លួនឯង\n\n🛠️ ការពិនិត្យសាមញ្ញដែលអ្នកអាចធ្វើបាន!\n\nការពិនិត្យប្រចាំសប្តាហ៍:\n• សម្ពាធកង់ និងចង្អូរ\n• កម្រិតទឹក (ប្រេង, ទឹកត្រជាក់, ហ្វ្រាំង)\n• ភ្លើង និងសញ្ញា\n• ទឹកលាងកញ្ចក់\n• ចុងថ្ម\n\nការពិនិត្យប្រចាំខែ:\n• ស្ថានភាពតម្រងខ្យល់\n• ភាពតានតឹង និងការស្លៀកខ្សែក្រវ៉ាត់\n• ស្ថានភាពបំពង់\n• ប្រព័ន្ធបញ្ចេញ\n• សមាសធាតុព្យួរ\n\nកិច្ចការងាយៗដែលអាចធ្វើដោយខ្លួនឯង:\n• ផ្លាស់ប្តូរតម្រងខ្យល់\n• ផ្លាស់ប្តូរដងកន្ទុយកញ្ចក់\n• ពិនិត្យសម្ពាធកង់\n• បន្ថែមទឹក\n• សម្អាតចុងថ្ម\n\nពេលត្រូវហៅអ្នកជំនាញ:\n• បញ្ហាម៉ាស៊ីន\n• បញ្ហាហ្វ្រាំង\n• បញ្ហាប្រេងឡាន\n• កំហុសអគ្គិសនី\n• ការព្រមានប្រព័ន្ធសុវត្ថិភាព\n\nសុវត្ថិភាពជាមុនគេ:\n• ប្រើឧបករណ៍ត្រឹមត្រូវ\n• ធ្វើការនៅលើដីរាប\n• ចាក់ហ្វ្រាំងចត\n• ទុកឱ្យម៉ាស៊ីនត្រជាក់\n\n🔍 ចំណេះដឹងគឺជាកម្លាំង!",
                
                # Add these to the Khmer section (around line 452, after the existing eco keys):                                        
                "eco_section": "ជម្រើសដែលស្រឡាញ់បរិស្ថាន",
                "fuel_efficiency_tips": "⛽ គន្លឹះប្រើប្រាស់ប្រេងមានប្រសិទ្ធភាព",
                "eco_electric_content": "⚡ រថយន្តអគ្គិសនី\n\n🔋 អនាគតនៃការដឹកជញ្ជូន!\n\nអត្ថប្រយោជន៍សំខាន់ៗ:\n• មិនបញ្ចេញឧស្ម័នដោយផ្ទាល់\n• ចំណាយប្រតិបត្តិការទាប (អគ្គិសនី vs ប្រេង)\n• ម៉ូម៉ង់ភ្លាមៗ និងការបង្កើនល្បឿនរលូន\n• ប្រតិបត្តិការស្ងៀម\n• ការថែទាំតិចតួច\n\nម៉ូដែលពេញនិយម:\n• Tesla Model 3, Model Y, Model S\n• Nissan Leaf, Chevrolet Bolt\n• BMW i3, Audi e-tron\n• Ford Mustang Mach-E\n\nជម្រើសសាក:\n• សាកនៅផ្ទះ (កម្រិត 1 & 2)\n• សាកសាធារណៈលឿន (DC)\n• សាកនៅកន្លែងធ្វើការ\n• សាកនៅគោលដៅ\n\nការពិចារណាចម្ងាយ:\n• EV ភាគច្រើន: 200-400+ ម៉ាយ\n• បច្ចេកវិទ្យាថ្មកាន់តែប្រសើរ\n• ហេដ្ឋារចនាសម្ព័ន្ធសាកកាន់តែច្រើន\n\n⚡ រួចរាល់សម្រាប់បដិវត្តអគ្គិសនីហើយឬ?",
                "eco_hybrid_content": "🌿 បច្ចេកវិទ្យា Hybrid\n\n🔄 ល្អបំផុតនៃពិភពលោកទាំងពីរ!\n\nរបៀបដែល Hybrid ដំណើរការ:\n• រួមបញ្ចូលម៉ាស៊ីនប្រេង + ម៉ូទ័រអគ្គិសនី\n• ការប្តូរស្វ័យប្រវត្តិរវាងប្រភពថាមពល\n• ហ្វ្រាំងបង្កើតថាមពលវិញចាប់យកថាមពល\n• ថ្មសាកពេលបើកបរ\n\nប្រភេទ Hybrid:\n• Hybrid បុរាណ: ម៉ាស៊ីនប្រេងជាមេ\n• Plug-in Hybrid: ថ្មធំជាង អាចសាក\n• Mild Hybrid: ជំនួយអគ្គិសនីតែប៉ុណ្ណោះ\n\nម៉ូដែលពេញនិយម:\n• Toyota Prius, Camry Hybrid\n• Honda Accord Hybrid, Insight\n• Ford Escape Hybrid\n• Lexus RX Hybrid\n\nអត្ថប្រយោជន៍:\n• សន្សំប្រេង 40-60+ MPG\n• បន្ថយការបញ្ចេញឧស្ម័ន\n• គ្មានការព្រួយបារម្ភចម្ងាយ\n• ចំណាយប្រេងទាប\n\n🌿 ប្រសិទ្ធភាពដោយគ្មានការសម្របសម្រួល!",
                "eco_fuel_content": "⛽ គន្លឹះប្រើប្រាស់ប្រេងមានប្រសិទ្ធភាព\n\n💡 បង្កើនប្រសិទ្ធភាព MPG របស់អ្នក!\n\nបច្ចេកទេសបើកបរ:\n• រក្សាល្បឿនស្ថេរ (55-65 mph ល្អបំផុត)\n• បង្កើនល្បឿន និងហ្វ្រាំងបន្តិចម្តងៗ\n• ប្រើការគ្រប់គ្រងល្បឿននៅលើផ្លូវហាយវេ\n• ព្យាករណ៍លំហូរចរាចរណ៍\n• យកទម្ងន់បន្ថែមចេញពីរថយន្ត\n\nការថែទាំរថយន្ត:\n• រក្សាកង់ឱ្យមានសម្ពាធត្រឹមត្រូវ\n• ប្តូរប្រេងទៀងទាត់\n• ធ្វើអនាម័យតម្រងខ្យល់\n• ការកែសម្រួលតាមកាលវិភាគ\n• ប្រើប្រេងដែលបានណែនាំ\n\nការរៀបចំដំណើរ:\n• រួមបញ្ចូលការធ្វើធុរកិច្ចក្នុងដំណើរតែមួយ\n• ជៀសវាងម៉ោងចរាចរណ៍កកស្ទះ\n• ប្រើ GPS សម្រាប់ផ្លូវមានប្រសិទ្ធភាព\n• ពិចារណាការចែករំលែករថយន្ត\n\nជំនួយបច្ចេកវិទ្យា:\n• របៀបបើកបរអេកូ\n• ការបង្ហាញសន្សំប្រេងពេលវេលាជាក់ស្តែង\n• កុំព្យូទ័រដំណើរ\n• កម្មវិធីទូរស័ព្ទសម្រាប់តម្លៃប្រេង\n\n⛽ រាល់ដំណក់មានសារៈសំខាន់!",
                "eco_impact_content": "🌍 ឥទ្ធិពលលើបរិស្ថាន\n\n🌱 ស្នាមជើងកាបូនរបស់រថយន្តអ្នក\n\nរថយន្តបុរាណ:\n• រថយន្តមធ្យម: 4.6 តោន CO2/ឆ្នាំ\n• ប្រេង 1 ហ្គាឡុង = 19.6 ផោន CO2\n• ការបញ្ចេញឧស្ម័នពីបំពង់\n• ឥទ្ធិពលការប្រើប្រាស់ប្រេង\n\nរថយន្តអគ្គិសនី:\n• មិនបញ្ចេញឧស្ម័នដោយផ្ទាល់\n• ប្រភពអគ្គិសនីមានសារៈសំខាន់\n• បន្ថយការបញ្ចេញ 50-70% ពេញមួយជីវិត\n• ប្រសើរឡើងនៅពេលបណ្តាញស្អាត\n\nអត្ថប្រយោជន៍ Hybrid:\n• បន្ថយការបញ្ចេញ 30-50% ជាងរថយន្តប្រេង\n• បន្ថយការប្រើប្រាស់ប្រេង\n• បន្ថយការបំពុលខ្យល់\n• ស្ពានទៅអនាគតអគ្គិសនីពេញលេញ\n\nធ្វើឱ្យមានភាពខុសគ្នា:\n• ជ្រើសរើសរថយន្តមានប្រសិទ្ធភាព\n• បើកបរតិច រួមបញ្ចូលដំណើរ\n• ថែទាំរថយន្តរបស់អ្នក\n• ពិចារណាការដឹកជញ្ជូនជំនួស\n\nឥទ្ធិពលសកល:\n• ការដឹកជញ្ជូន: 29% នៃការបញ្ចេញរបស់អាមេរិក\n• រថយន្តមានប្រសិទ្ធភាពគ្រប់គ្នាជួយ\n• គាំទ្របច្ចេកវិទ្យាស្អាត\n\n🌍 បើកបរឆ្ពោះទៅអនាគតស្អាតជាង!",
                "eco_savings_content": "💰 ការសន្សំប្រាក់\n\n📊 គណនាការសន្សំរបស់អ្នក!\n\nការសន្សំរថយន្តអគ្គិសនី:\n• អគ្គិសនី vs ប្រេង: $0.04 vs $0.12 ក្នុងមួយម៉ាយ\n• ការសន្សំប្រចាំឆ្នាំ: $1,000-2,000\n• ចំណាយថែទាំទាប\n• ឥណទានពន្ធសហព័ន្ធរហូតដល់ $7,500\n• ការលើកទឹកចិត្តរដ្ឋ/មូលដ្ឋានមាន\n\nការសន្សំ Hybrid:\n• 40-60 MPG vs 25 MPG មធ្យម\n• សន្សំ $500-1,500/ឆ្នាំលើប្រេង\n• អាយុកាលម៉ាស៊ីនវែងជាង\n• បន្ថយការរលាយហ្វ្រាំង\n\nការសន្សំប្រសិទ្ធភាពប្រេង:\n• ប្រសើរពី 25 ទៅ 35 MPG សន្សំ $600/ឆ្នាំ\n• ការថែទាំត្រឹមត្រូវសន្សំ 10-15%\n• ការបើកបរមានប្រសិទ្ធភាពសន្សំ 20-40%\n\nអត្ថប្រយោជន៍បន្ថែម:\n• ការចូលដំណើរផ្លូវ HOV\n• បន្ថយថ្លៃចត\n• ការធានារ៉ាប់រងទាប (ក្រុមហ៊ុនខ្លះ)\n• បង្កើនតម្លៃលក់វិញ\n\nរយៈពេលសងវិញ:\n• Hybrid: 3-5 ឆ្នាំ\n• EV: 5-8 ឆ្នាំ (ជាមួយការលើកទឹកចិត្ត)\n• ប្រសិទ្ធភាពប្រេង: ភ្លាមៗ\n\n💰 ការបើកបរបៃតង = ការសន្សំបៃតង!",
                "eco_charging_content": "🔌 ហេដ្ឋារចនាសម្ព័ន្ធសាកភ្លើង\n\n⚡ សាកនៅគ្រប់ទីកន្លែង!\n\nការសាកនៅផ្ទះ:\n• កម្រិត 1: ដោតស្តង់ដារ 120V (យឺត)\n• កម្រិត 2: ដោត 240V (បានណែនាំ)\n• ការដំឡើង: $500-2,000\n• ភាពស្រួលសាកពេលយប់\n• អត្រាអគ្គិសនីថោកបំផុត\n\nការសាកសាធារណៈ:\n• កម្រិត 2: 4-8 ម៉ោងសាកពេញ\n• DC លឿន: 30-60 នាទីដល់ 80%\n• បណ្តាញ: ChargePoint, EVgo, Electrify America\n• កម្មវិធីជួយរកស្ថានីយ៍\n\nការសាកនៅកន្លែងធ្វើការ:\n• អត្ថប្រយោជន៍និយោជកកាន់តែច្រើន\n• សាកពេលអ្នកធ្វើការ\n• ជាញឹកញាប់ឥតគិតថ្លៃ ឬថោក\n• បន្ថយការព្រួយបារម្ភចម្ងាយ\n\nចំណាយសាក:\n• ផ្ទះ: $0.10-0.20 ក្នុងមួយ kWh\n• សាធារណៈកម្រិត 2: $0.20-0.30 ក្នុងមួយ kWh\n• DC លឿន: $0.30-0.50 ក្នុងមួយ kWh\n• នៅតែថោកជាងប្រេង\n\nការលូតលាស់អនាគត:\n• ឧបករណ៍សាកសាធារណៈ 500,000+ នៅឆ្នាំ 2030\n• បច្ចេកវិទ្យាសាកលឿនជាង\n• ទីតាំងស្រួលជាង\n• ចំណាយទាប\n\n🔌 បណ្តាញកំពុងលូតលាស់លឿន!",
                
                # Add to Khmer translations section  
                "back_to_section": "🔙 ត្រលប់ទៅ {section}",
        


                # Khmer section (around line 378)
                "search_by_brand": "🏷️ ស្វែងរកតាមម៉ាក",
                "search_by_color": "🎨 ស្វែងរកតាមពណ៌",
                "search_by_category": "📂 ស្វែងរកតាមប្រភេទ",
                "select_price_range": "💰 ជ្រើសរើសជួរតម្លៃ:",
                "select_year_range": "📅 ជ្រើសរើសជួរឆ្នាំ:",
                "select_location": "📍 ជ្រើសរើសទីតាំង:",
                "select_brand": "🚗 ជ្រើសរើសម៉ាក:",
                "select_color": "🎨 ជ្រើសរើសពណ៌:",
                "select_category": "📂 ជ្រើសរើសប្រភេទ:",
                "any_brand": "ម៉ាកណាមួយ",
                "any_color": "ពណ៌ណាមួយ",
                "any_category": "ប្រភេទណាមួយ",
                "red": "ក្រហម",
                "blue": "ខៀវ",
                "black": "ខ្មៅ",
                "white": "ស",
                "silver": "ប្រាក់",
                "gray": "ប្រផេះ",
                "green": "បៃតង",
                "yellow": "លឿង",
                "sedan": "រថយន្តសេដាន",
                "suv": "រថយន្ត SUV",
                "hatchback": "រថយន្តហាចបែក",
                "truck": "រថយន្តដឹកទំនិញ",
                "convertible": "រថយន្តបើកដំបូល",
                
                # Error Messages
                "unknown_command": "ខ្ញុំមិនយល់ពីពាក្យបញ្ជានោះទេ។ សូមប្រើជម្រើសមុខម៉ឺនុយខាងក្រោម៖",
                "car_not_available": "សូមអភ័យទោស រថយន្តនេះមិនមានទៀតទេ។"
            }
        }
    

    
    def get_user_language(self, telegram_id: int) -> str:
        """Get user's preferred language from cache, API or fallback to local data"""
        # Check if language is already cached
        if telegram_id in self.user_languages:
            return self.user_languages[telegram_id]
        
        try:
            import requests
            from utils.config.settings import API_BASE_URL
            
            api_url = f"{API_BASE_URL}/User/GetTelegramUser/{telegram_id}"
            
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                user_data = response.json()
                language = user_data.get('language', 'en')
                # Cache the language to avoid future API calls
                self.user_languages[telegram_id] = language
                return language
                
        except Exception as e:
            pass
        
        # Fallback to local data if API fails
        from models.core.user import users
        user = next((user for user in users if user.telegram_id == telegram_id), None)
        fallback_language = user.language if user else "en"
        # Cache the fallback language
        self.user_languages[telegram_id] = fallback_language
        return fallback_language
    
    def set_user_language(self, telegram_id: int, lang_code: str) -> None:
        """Set user's language preference"""
        if lang_code not in self.translations:
            return
            
        # Update the cache with new language
        self.user_languages[telegram_id] = lang_code
            
        try:
            from handlers.base import user_cache
            if telegram_id in user_cache:
                user_cache[telegram_id]['language'] = lang_code
                # Language updated in memory cache only
        except ImportError:
            pass
        
        # Also update old method for backward compatibility
        from models.core.user import users
        user = next((user for user in users if user.telegram_id == telegram_id), None)
        if user:
            user.language = lang_code
    

    
    def get_text(self, key: str, telegram_id: int, *args, **kwargs) -> str:
        """Get translated text for the given key in user's language"""
        user_lang = self.get_user_language(telegram_id)
        text = self.translations.get(user_lang, {}).get(key, key)
        
        # Handle both dictionary and keyword arguments
        format_args = {}
        if args and isinstance(args[0], dict):
            format_args = args[0]
        elif kwargs:
            format_args = kwargs
        
        # Format text with provided arguments
        if format_args:
            try:
                text = text.format(**format_args)
            except (KeyError, ValueError):
                pass  # If formatting fails, return unformatted text
        
        return text

# Create a global instance
language_handler = LanguageHandler()










