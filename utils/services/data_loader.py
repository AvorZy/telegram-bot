import requests
import os
import random
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
        """Load data from API with fallback to sample data"""
        try:
            # Load categories and brands first
            self._load_categories()
            self._load_brands()
            
            api_cars = self._load_from_api()
            if api_cars:
                self.loaded_cars = api_cars
                return api_cars
        except Exception as e:
            pass  # Silent fallback
        
        # Fallback to sample data
        fallback_cars = self._generate_sample_data()
        self.loaded_cars = fallback_cars
        return fallback_cars
    
    def _load_from_api(self) -> List[Dict]:
        """Load and process data from API"""
        response = requests.get(
            f"{self.api_base_url}/Product",
            timeout=self.api_timeout
        )
        response.raise_for_status()
        
        api_data = response.json()
        products = api_data.get('data', []) if isinstance(api_data, dict) else api_data
        
        if not products:
            return []
        
        return [self._convert_product_to_car(product) for product in products]
    
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
            'id': product.get('id', random.randint(10000, 99999)),
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
        """Get dynamic image URL from R2 bucket"""
        if not image_filename:
            return self._get_fallback_car_image()
        
        # Clean up malformed URLs with trailing commas and spaces
        clean_filename = image_filename.strip().rstrip(',')
        
        if clean_filename.startswith('http'):
            # Validate and clean the URL
            if '.' in clean_filename:  # Basic URL validation
                return clean_filename
            else:
                return self._get_fallback_car_image()
        
        # Construct dynamic image URL from R2 bucket
        dynamic_url = f"{self.image_base_url}/{clean_filename}"
        
        # Test if the dynamic image exists (simplified)
        try:
            response = requests.head(dynamic_url, timeout=3)
            if response.status_code == 200:
                return dynamic_url
        except Exception:
            pass
        
        # If dynamic image fails, use fallback
        return self._get_fallback_car_image()
    
    def _get_fallback_car_image(self) -> str:
        """Get a fallback car image URL"""
        fallback_images = [
            "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1583121274602-3e2820c69888?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1550355291-bbee04a92027?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        ]
        return random.choice(fallback_images)
    
    def _generate_sample_gallery(self) -> List[str]:
        """Generate sample gallery images for cars"""
        gallery_images = [
            "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1583121274602-3e2820c69888?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1550355291-bbee04a92027?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1502877338535-766e1452684a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
        ]
        # Return 2-4 random gallery images for each car
        num_images = random.randint(2, 4)
        return random.sample(gallery_images, num_images)
    
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
    
    def _generate_sample_data(self) -> List[Dict]:
        """Generate sample car data for fallback"""
        brands = ['Toyota', 'Honda', 'BMW', 'Mercedes-Benz', 'Audi', 'Ford', 'Chevrolet', 'Nissan']
        models = ['Sedan', 'SUV', 'Hatchback', 'Coupe', 'Convertible', 'Truck']
        locations = ['Phnom Penh', 'Siem Reap', 'Battambang', 'Sihanoukville']
        colors = ['Red', 'Blue', 'Black', 'White', 'Silver', 'Gray']
        
        cars = []
        for i in range(10):
            brand = random.choice(brands)
            model_type = random.choice(models)
            
            cars.append({
                'id': i + 1,
                'user_id': None,
                'brand': brand,
                'model': f"{brand} {model_type}",
                'year': random.randint(2015, 2024),
                'price': random.randint(15000, 80000),
                'currency': 'USD',
                'description': f"Quality {brand} {model_type} in excellent condition. Well-maintained vehicle with low mileage.",
                'image_url': self._get_fallback_car_image(),
                'gallery': self._generate_sample_gallery(),
                'location': random.choice(locations),
                'color': random.choice(colors),
                'condition': 'Good',
                'phone_number': '097 80 24 246',
                'category': 'Sedan',
                'is_featured': False,
                'sku': f'SKU-{i+1}',
                'status': 'available',
                'created_at': datetime.now().isoformat(),
                'source': 'fallback'
            })
        
        return cars
    
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