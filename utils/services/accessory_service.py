import asyncio
import aiohttp
import os
import time
import requests
from typing import List, Optional, Dict, Any
from models.core.accessory import Accessory
from utils.config.settings import API_BASE_URL, API_BASE_URL_IMG

class AccessoryService:
    """Service for handling accessory data from API"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.api_timeout = int(os.getenv('API_TIMEOUT', '30'))
        # Use environment variables like data_loader
        self.image_base_url = API_BASE_URL_IMG
        self.r2_image_base_url = API_BASE_URL_IMG if API_BASE_URL_IMG.endswith('/') else f"{API_BASE_URL_IMG}/"
        self.accessories_cache = []
        self.cache_timestamp = 0
        self.cache_duration = 300  # 5 minutes
        # Image URL validation cache
        self.image_url_cache = {}
        self.image_cache_duration = 1800  # 30 minutes
        # Pagination support
        self.total_items = 0
        self.items_per_page = 10
        
    async def fetch_all_accessories(self) -> List[Accessory]:
        """Fetch all accessories from API with caching"""
        current_time = time.time()
        
        # Check if cache is still valid
        if (self.accessories_cache and 
            current_time - self.cache_timestamp < self.cache_duration):
            return self.accessories_cache
        
        # Fetch fresh data from API
        try:
            # First, get the total count
            self._update_total_count()
            
            # Since API pagination might be broken, request all items in one go
            # Use a large page size to get all accessories
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/Accessory",
                    params={'page': 1, 'pageSize': max(self.total_items, 1000)}
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        # Handle different response formats
                        if isinstance(response_data, dict) and 'data' in response_data:
                            accessories_data = response_data['data']
                        elif isinstance(response_data, list):
                            accessories_data = response_data
                        else:
                            print("Unexpected response format")
                            return self.accessories_cache if self.accessories_cache else []
                        
                        # Convert to Accessory objects
                        self.accessories_cache = [Accessory.from_api_data(acc_data) for acc_data in accessories_data]
                        self.cache_timestamp = current_time
                        return self.accessories_cache
                    else:
                        print(f"Error fetching accessories: HTTP {response.status}")
                        return self.accessories_cache if self.accessories_cache else []
                        
        except Exception as e:
            print(f"Error fetching all accessories: {e}")
            # Fallback: try without pagination parameters
            try:
                print("Falling back to simple API call...")
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/Accessory") as response:
                        if response.status == 200:
                            response_data = await response.json()
                            
                            # Handle different response formats
                            if isinstance(response_data, dict) and 'data' in response_data:
                                accessories_data = response_data['data']
                            elif isinstance(response_data, list):
                                accessories_data = response_data
                            else:
                                accessories_data = []
                            
                            # Convert to Accessory objects
                            self.accessories_cache = [Accessory.from_api_data(acc_data) for acc_data in accessories_data]
                            self.cache_timestamp = current_time
                            return self.accessories_cache
                            
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
            
            return self.accessories_cache if self.accessories_cache else []
    
    async def fetch_page(self, page: int, page_size: int = None) -> List[Accessory]:
        """Fetch a specific page of accessories"""
        if page_size is None:
            page_size = self.items_per_page
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/Accessory",
                    params={'page': page, 'pageSize': page_size}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        accessories_data = data.get('data', [])
                        return [Accessory.from_api_data(acc_data) for acc_data in accessories_data]
                    else:
                        print(f"Error fetching page {page}: HTTP {response.status}")
                        return []
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            return []
    
    def _update_total_count(self) -> None:
        """Update the total count of accessories"""
        try:
            # Use synchronous request for initialization
            response = requests.get(
                f"{self.base_url}/Accessory",
                params={'page': 1, 'pageSize': 1},
                timeout=self.api_timeout
            )
            response.raise_for_status()
            
            data = response.json()
            self.total_items = data.get('totalItems', 0)
            print(f"Total accessories: {self.total_items}")
            
        except Exception as e:
            print(f"Error getting total accessory count: {e}")
            # Keep previous count if available
            if not self.total_items:
                self.total_items = 0
    
    def get_total_count(self) -> int:
        """Get the total number of accessories"""
        if not self.total_items:
            self._update_total_count()
        return self.total_items
    
    def get_total_pages(self, page_size: int = None) -> int:
        """Get the total number of pages"""
        if page_size is None:
            page_size = self.items_per_page
            
        total_count = self.get_total_count()
        if total_count == 0 or page_size == 0:
            return 0
            
        return (total_count + page_size - 1) // page_size  # Ceiling division
    
    async def get_unique_types(self) -> List[str]:
        """Get unique accessory categories"""
        accessories = await self.fetch_all_accessories()
        categories = list(set(acc.category for acc in accessories if acc.category))
        return sorted(categories)
    
    async def get_unique_brands(self) -> List[str]:
        """Get unique accessory brands"""
        accessories = await self.fetch_all_accessories()
        brands = list(set(acc.brand for acc in accessories if acc.brand))
        return sorted(brands)
    
    async def get_unique_colors(self) -> List[str]:
        """Get unique accessory colors"""
        accessories = await self.fetch_all_accessories()
        colors = list(set(acc.color for acc in accessories if acc.color))
        return sorted(colors)
    
    async def get_unique_locations(self) -> List[str]:
        """Get unique accessory locations"""
        accessories = await self.fetch_all_accessories()
        locations = list(set(acc.location for acc in accessories if acc.location))
        return sorted(locations)
    
    async def get_accessories_by_type(self, accessory_type: str) -> List[Accessory]:
        """Get accessories filtered by category"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if acc.category == accessory_type]
    
    async def get_accessories_by_brand(self, brand: str) -> List[Accessory]:
        """Get accessories filtered by brand"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if acc.brand == brand]
    
    async def get_accessories_by_color(self, color: str) -> List[Accessory]:
        """Get accessories filtered by color"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if acc.color == color]
    
    async def get_accessories_by_price_range(self, min_price: float, max_price: float) -> List[Accessory]:
        """Get accessories filtered by price range"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if min_price <= acc.price <= max_price]
    
    async def get_accessories_by_location(self, location: str) -> List[Accessory]:
        """Get accessories filtered by location"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if acc.location == location]
    
    async def fetch_accessory_by_id(self, accessory_id: int) -> Optional[Accessory]:
        """Get specific accessory by ID from API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/Accessory/{accessory_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        return Accessory.from_api_data(data)
                    else:
                        print(f"Error fetching accessory {accessory_id}: HTTP {response.status}")
                        return None
        except Exception as e:
            print(f"Error fetching accessory {accessory_id}: {e}")
            return None
    
    async def get_accessory_by_id(self, accessory_id: int) -> Optional[Accessory]:
        """Get specific accessory by ID (fallback to list search)"""
        # Try direct API call first
        accessory = await self.fetch_accessory_by_id(accessory_id)
        if accessory:
            return accessory
        
        # Fallback to searching in the full list
        accessories = await self.fetch_all_accessories()
        for acc in accessories:
            if acc.id == accessory_id:
                return acc
        return None
    
    async def search_accessories(self, query: str = None, category: str = None, brand: str = None, 
                                color: str = None, min_price: float = None, max_price: float = None) -> List[Accessory]:
        """Search accessories with multiple filters"""
        accessories = await self.fetch_all_accessories()
        
        # Apply text search filter
        if query:
            query_lower = query.lower()
            accessories = [
                acc for acc in accessories 
                if query_lower in acc.name.lower() or query_lower in acc.description.lower()
            ]
        
        # Apply category filter
        if category:
            accessories = [acc for acc in accessories if acc.category == category]
        
        # Apply brand filter
        if brand:
            accessories = [acc for acc in accessories if acc.brand == brand]
        
        # Apply color filter
        if color:
            accessories = [acc for acc in accessories if acc.color == color]
        
        # Apply price range filter
        if min_price is not None:
            accessories = [acc for acc in accessories if acc.price >= min_price]
        
        if max_price is not None:
            accessories = [acc for acc in accessories if acc.price <= max_price]
        
        return accessories
    
    async def get_full_image_url(self, image_filename: str) -> str:
        """Get full image URL from filename with cached validation - supports both API and R2 storage"""
        if not image_filename:
            return ""
        
        # Clean the image filename (strip whitespace and trailing commas)
        cleaned_filename = image_filename.strip().rstrip(',')
        
        # Check cache first
        current_time = time.time()
        cache_key = cleaned_filename
        if cache_key in self.image_url_cache:
            cached_result, cached_time = self.image_url_cache[cache_key]
            if current_time - cached_time < self.image_cache_duration:
                return cached_result
        
        # If already a full URL, do basic validation and return it
        if cleaned_filename.startswith(('http://', 'https://')):
            if '.' in cleaned_filename and len(cleaned_filename) > 10:
                self.image_url_cache[cache_key] = (cleaned_filename, current_time)
                return cleaned_filename
            self.image_url_cache[cache_key] = ("", current_time)
            return ""
        
        # Try R2 storage first (newer images) - assume it works to avoid HTTP calls
        r2_url = f"{self.r2_image_base_url}{cleaned_filename}"
        # Cache and return R2 URL without validation for performance
        self.image_url_cache[cache_key] = (r2_url, current_time)
        return r2_url
    
    def get_fallback_image_url(self, image_filename: str) -> str:
        """Get fallback image URL from original API storage"""
        if not image_filename:
            return ""
        
        if image_filename.startswith(('http://', 'https://')):
            return image_filename
            
        return f"{self.image_base_url}{image_filename}"