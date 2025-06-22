import os
import re
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
from decimal import Decimal
from utils.config.settings import API_BASE_URL, API_BASE_URL_IMG

class CarDataLoader:
    """Handles loading car data from API with dynamic images"""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
        self.api_timeout = int(os.getenv('API_TIMEOUT', '30'))
        self.image_base_url = API_BASE_URL_IMG
        self.loaded_cars = []
        self.categories_cache = {}
        self.brands_cache = {}
        
        if not self.api_base_url:
            raise ValueError("API_BASE_URL must be set in .env file")
    
    def load_all_data(self) -> List[Dict]:
        """Load data from API only"""
        # Load categories and brands first
        self._load_categories()
        self._load_brands()
        
        # Load cars from API
        api_cars = self._load_from_api()
        self.loaded_cars = api_cars
        return api_cars
    
    def _load_from_api(self) -> List[Dict]:
        """Load and process data from API with pagination workaround"""
        all_products = []
        
        try:
            # First, try to get total count with a small request
            print("Getting total product count...")
            response = requests.get(
                f"{self.api_base_url}/Product",
                params={'page': 1, 'pageSize': 1},
                timeout=self.api_timeout
            )
            response.raise_for_status()
            api_data = response.json()
            total_items = api_data.get('totalItems', 0)
            
            if total_items == 0:
                print("No products found in API")
                return []
            
            # Load all products in single request
            
            # Since API pagination is broken, request all items in one go
            # Use a large page size to get all products
            response = requests.get(
                f"{self.api_base_url}/Product",
                params={'page': 1, 'pageSize': total_items},
                timeout=self.api_timeout
            )
            response.raise_for_status()
            
            api_data = response.json()
            products_data = api_data.get('data', [])
            
            # Successfully loaded products from API
            
            if products_data:
                # Convert and add products
                converted_products = [self._convert_product_to_car(product) for product in products_data]
                all_products.extend(converted_products)
            
        except Exception as e:
            print(f"Error loading from API: {e}")
            # Fallback: try with standard pagination (first page only)
            try:
                print("Falling back to single page load...")
                response = requests.get(
                    f"{self.api_base_url}/Product",
                    params={'page': 1, 'pageSize': 50},
                    timeout=self.api_timeout
                )
                response.raise_for_status()
                api_data = response.json()
                products_data = api_data.get('data', [])
                
                if products_data:
                    converted_products = [self._convert_product_to_car(product) for product in products_data]
                    all_products.extend(converted_products)
                    # Fallback: loaded products from first page
                    
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
        
        # Total products loaded successfully
        return all_products
    
    def _load_categories(self) -> None:
        """Load categories from separate API endpoint"""
        try:
            response = requests.get(
                f"{self.api_base_url}/Category",
                timeout=self.api_timeout
            )
            response.raise_for_status()
            
            categories_data = response.json()
            categories = categories_data.get('data', []) if isinstance(categories_data, dict) else categories_data
            
            # Cache categories by ID
            for category in categories:
                if isinstance(category, dict) and 'id' in category:
                    self.categories_cache[category['id']] = category.get('name', 'Unknown Category')
                    
        except Exception as e:
            # Fallback categories
            self.categories_cache = {
                1: 'Sedan',
                2: 'SUV', 
                3: 'Hatchback',
                4: 'Coupe',
                5: 'Convertible',
                6: 'Truck'
            }
    
    def _load_brands(self) -> None:
        """Load brands from separate API endpoint"""
        try:
            response = requests.get(
                f"{self.api_base_url}/Brand",
                timeout=self.api_timeout
            )
            response.raise_for_status()
            
            brands_data = response.json()
            brands = brands_data.get('data', []) if isinstance(brands_data, dict) else brands_data
            
            # Cache brands by ID
            for brand in brands:
                if isinstance(brand, dict) and 'id' in brand:
                    self.brands_cache[brand['id']] = brand.get('name', 'Unknown Brand')
                    
        except Exception as e:
            # Fallback brands
            self.brands_cache = {
                1: 'Toyota',
                2: 'Honda',
                3: 'BMW',
                4: 'Mercedes-Benz',
                5: 'Audi',
                6: 'Ford',
                7: 'Chevrolet',
                8: 'Nissan'
            }
    
    def _convert_product_to_car(self, product: Dict) -> Dict:
        """Convert API product to standardized car format"""
        # Get brand name from cache using brand_id
        brand_id = product.get('brandId') or product.get('brand_id')
        brand_name = self.brands_cache.get(brand_id, product.get('brand', 'Unknown'))
        
        # Get category name from cache using category_id
        category_id = product.get('categoryId') or product.get('category_id')
        category_name = self.categories_cache.get(category_id, product.get('category', 'Sedan'))
        
        return {
            'id': product.get('id', hash(str(product)) % 100000),
            'user_id': None,
            'brand': brand_name,
            'model': product.get('model', product.get('title', 'Unknown Model')),
            'year': self._extract_year(product.get('model', '')),
            'price': float(product.get('price', 0)),
            'currency': product.get('eCurrencyType', 'USD'),
            'description': self._get_description(product),
            'image_url': self._get_dynamic_image_url(product.get('image')),
            'gallery': self._process_gallery(product.get('gallery')),
            'location': product.get('location', 'Phnom Penh'),
            'color': product.get('color', 'Unknown'),
            'condition': product.get('condition', 'Good'),
            'phone_number': product.get('phoneNumber', '097 80 24 246'),
            'category': category_name,
            'is_featured': product.get('isFeatured', False),
            'sku': product.get('sku', ''),
            'status': 'available',
            'created_at': datetime.now().isoformat(),
            'source': 'api',
            'brand_id': brand_id,
            'category_id': category_id
        }
    
    def _get_dynamic_image_url(self, image_filename: str) -> str:
        """Get dynamic image URL from R2 bucket or API data"""
        if not image_filename:
            return ""
        
        # Clean up malformed URLs with trailing commas and spaces
        clean_filename = image_filename.strip().rstrip(',')
        
        if clean_filename.startswith('http'):
            # Validate and clean the URL
            if '.' in clean_filename:  # Basic URL validation
                return clean_filename
            else:
                return ""
        
        # Construct dynamic image URL from R2 bucket
        dynamic_url = f"{self.image_base_url}/{clean_filename}"
        
        # Test if the dynamic image exists (simplified)
        try:
            response = requests.head(dynamic_url, timeout=3)
            if response.status_code == 200:
                return dynamic_url
        except Exception:
            pass
        
        # Return empty string if no valid image found
        return ""
    

    

    
    def _process_gallery(self, gallery_data) -> List[str]:
        """Process gallery images from API using dynamic URLs"""
        if not gallery_data:
            return []
        
        gallery_list = []
        
        if isinstance(gallery_data, str):
            # Handle malformed gallery strings with commas and spaces
            gallery_list = [img.strip().rstrip(',') for img in gallery_data.split(',') if img.strip().rstrip(',')]
        elif isinstance(gallery_data, list):
            # Handle array of gallery items (each might be a string with commas)
            for item in gallery_data:
                if isinstance(item, str):
                    # Split each item by comma and clean up
                    sub_items = [img.strip().rstrip(',') for img in item.split(',') if img.strip().rstrip(',')]
                    gallery_list.extend(sub_items)
                else:
                    gallery_list.append(str(item))
        else:
            return []
        
        processed_images = []
        for img in gallery_list:
            if img and img.startswith('http'):
                # Validate URL format and remove any trailing commas
                clean_url = img.strip().rstrip(',')
                if clean_url and '.' in clean_url:  # Basic URL validation
                    processed_images.append(clean_url)
            elif img:
                # Handle relative paths
                dynamic_gallery_url = f"{self.image_base_url}/{img}"
                processed_images.append(dynamic_gallery_url)
        
        return processed_images
    
    def _extract_year(self, text: str) -> int:
        """Extract year from text, default to 2020"""
        match = re.search(r'\b(19|20)\d{2}\b', text)
        return int(match.group()) if match else 2020
    
    def _get_description(self, product: Dict) -> str:
        """Get description or generate default"""
        description = product.get('description', '').strip()
        if description:
            return description
        
        brand = product.get('brand', 'Unknown')
        model = product.get('model', product.get('title', 'Unknown Model'))
        return f"Quality {brand} {model} in excellent condition. Contact seller for more details."
    

    
    def get_brands_list(self) -> List[str]:
        """Get sorted list of available brands"""
        # First try to get from cache
        if self.brands_cache:
            return sorted(list(self.brands_cache.values()))
        
        # Fallback to loaded cars data
        if not self.loaded_cars:
            return []
        
        brands = {car.get('brand') for car in self.loaded_cars if car.get('brand')}
        return sorted(list(brands))
    
    def get_unique_locations(self) -> List[str]:
        """Get list of unique locations from loaded car data"""
        if not self.loaded_cars:
            return ['Phnom Penh', 'Siem Reap', 'Battambang', 'Sihanoukville']
        
        locations = set()
        for car in self.loaded_cars:
            location = car.get('location', '').strip()
            if location:
                locations.add(location)
        
        unique_locations = sorted(list(locations))
        
        if not unique_locations:
            return ['Phnom Penh', 'Siem Reap', 'Battambang', 'Sihanoukville']
        
        return unique_locations
    
    def get_categories_list(self) -> List[str]:
        """Get sorted list of available categories"""
        # First try to get from cache
        if self.categories_cache:
            return sorted(list(self.categories_cache.values()))
        
        # Fallback to loaded cars data
        if not self.loaded_cars:
            return ['Sedan', 'SUV', 'Hatchback', 'Coupe', 'Convertible', 'Truck']
        
        categories = {car.get('category') for car in self.loaded_cars if car.get('category')}
        return sorted(list(categories))
    
    def get_colors_list(self) -> List[str]:
        """Get sorted list of available colors"""
        if not self.loaded_cars:
            return ['Red', 'Blue', 'Black', 'White', 'Silver', 'Gray']
        
        colors = {car.get('color') for car in self.loaded_cars if car.get('color')}
        return sorted(list(colors))
    
    def get_brands_with_emojis(self) -> Dict[str, str]:
        """Get brands with emoji mappings"""
        brand_emojis = {
            'Toyota': '🚗',
            'Honda': '🏎️',
            'BMW': '🚙',
            'Mercedes-Benz': '🚐',
            'Audi': '🚕',
            'Ford': '🚓',
            'Chevrolet': '🚒',
            'Nissan': '🚑',
            'Hyundai': '🚌',
            'Kia': '🚎',
            'Volkswagen': '🚍',
            'Mazda': '🚘',
            'Subaru': '🚖',
            'Mitsubishi': '🚔',
            'Lexus': '🚗',
            'Infiniti': '🏎️',
            'Acura': '🚙',
            'Volvo': '🚐',
            'Jaguar': '🚕',
            'Land Rover': '🚓'
        }
        
        brands = self.get_brands_list()
        return {brand: brand_emojis.get(brand, '🚗') for brand in brands}
    
    def get_categories_with_emojis(self) -> Dict[str, str]:
        """Get categories with emoji mappings"""
        category_emojis = {
            'Sedan': '🚗',
            'SUV': '🚙',
            'Hatchback': '🚘',
            'Coupe': '🏎️',
            'Convertible': '🚗',
            'Truck': '🚚',
            'Van': '🚐',
            'Wagon': '🚗',
            'Crossover': '🚙',
            'Pickup': '🚚',
            'Minivan': '🚐',
            'Sports Car': '🏎️',
            'Luxury': '🚕',
            'Electric': '⚡',
            'Hybrid': '🔋'
        }
        
        categories = self.get_categories_list()
        return {category: category_emojis.get(category, '🚗') for category in categories}
    
    def get_colors_with_emojis(self) -> Dict[str, str]:
        """Get colors with emoji mappings"""
        color_emojis = {
            'Red': '🔴',
            'Blue': '🔵',
            'Black': '⚫',
            'White': '⚪',
            'Silver': '⚪',
            'Gray': '⚫',
            'Grey': '⚫',
            'Green': '🟢',
            'Yellow': '🟡',
            'Orange': '🟠',
            'Purple': '🟣',
            'Brown': '🟤',
            'Gold': '🟡',
            'Pink': '🩷',
            'Maroon': '🔴',
            'Navy': '🔵',
            'Beige': '🟤'
        }
        
        colors = self.get_colors_list()
        return {color: color_emojis.get(color, '🎨') for color in colors}

# Global instance
car_data_loader = CarDataLoader()