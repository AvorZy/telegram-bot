import aiohttp
import math
import os
import re
import time
import aiohttp
import requests
from typing import List, Optional, Dict, Any, Tuple
from models.core.garage import Garage
from utils.config.settings import API_BASE_URL_IMG

class GarageService:
    """Service class for handling garage API operations"""
    
    def __init__(self, api_url: str = "https://inventoryapiv1-367404119922.asia-southeast1.run.app/Garage"):
        self.api_url = api_url
        self.api_timeout = int(os.getenv('API_TIMEOUT', '30'))
        self.image_base_url = API_BASE_URL_IMG
        # Remove trailing slash from R2 URL to avoid double slashes
        self.r2_image_base_url = "https://pub-133f8593b35749f28fa090bc33925b31.r2.dev"
        # Add caching
        self.garages_cache = []
        self.cache_timestamp = 0
        self.cache_duration = 300  # 5 minutes
        # Pagination support
        self.total_items = 0
        self.items_per_page = 10
    
    async def fetch_all_garages(self) -> List[Garage]:
        """Fetch all garages from API with caching"""
        current_time = time.time()
        
        # Check if cache is still valid
        if (self.garages_cache and 
            current_time - self.cache_timestamp < self.cache_duration):
            return self.garages_cache
        
        # Fetch fresh data from API
        try:
            # First, get the total count
            self._update_total_count()
            
            # Since API pagination might be broken, request all items in one go
            # Use a large page size to get all garages
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_url,
                    params={'page': 1, 'pageSize': max(self.total_items, 1000)}
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        # Check if response_data is a list
                        if isinstance(response_data, list):
                            self.garages_cache = [Garage.from_api_data(garage_data) for garage_data in response_data]
                        elif isinstance(response_data, dict):
                            # If it's a dict, check for 'data' property (pagination response)
                            if 'data' in response_data and isinstance(response_data['data'], list):
                                self.garages_cache = [Garage.from_api_data(garage_data) for garage_data in response_data['data']]
                            else:
                                # Single garage object
                                self.garages_cache = [Garage.from_api_data(response_data)]
                        else:
                            print("Unexpected response format")
                            return self.garages_cache if self.garages_cache else []
                        
                        self.cache_timestamp = current_time
                        return self.garages_cache
                    else:
                        print(f"Error fetching garages: HTTP {response.status}")
                        return self.garages_cache if self.garages_cache else []
                        
        except Exception as e:
            print(f"Error fetching all garages: {e}")
            # Fallback: try without pagination parameters
            try:
                print("Falling back to simple API call...")
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.api_url) as response:
                        if response.status == 200:
                            response_data = await response.json()
                            
                            # Check if response_data is a list
                            if isinstance(response_data, list):
                                self.garages_cache = [Garage.from_api_data(garage_data) for garage_data in response_data]
                            elif isinstance(response_data, dict):
                                # If it's a dict, check for 'data' property (pagination response)
                                if 'data' in response_data and isinstance(response_data['data'], list):
                                    self.garages_cache = [Garage.from_api_data(garage_data) for garage_data in response_data['data']]
                                else:
                                    # Single garage object
                                    self.garages_cache = [Garage.from_api_data(response_data)]
                            
                            self.cache_timestamp = current_time
                            return self.garages_cache
                            
            except Exception as fallback_error:
                print(f"Fallback also failed: {fallback_error}")
            
            return self.garages_cache if self.garages_cache else []
    
    async def fetch_page(self, page: int, page_size: int = None) -> List[Garage]:
        """Fetch a specific page of garages"""
        if page_size is None:
            page_size = self.items_per_page
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_url,
                    params={'page': page, 'pageSize': page_size}
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        # Check if response_data is a list
                        if isinstance(response_data, list):
                            return [Garage.from_api_data(garage_data) for garage_data in response_data]
                        elif isinstance(response_data, dict):
                            # If it's a dict, check for 'data' property (pagination response)
                            if 'data' in response_data and isinstance(response_data['data'], list):
                                return [Garage.from_api_data(garage_data) for garage_data in response_data['data']]
                            else:
                                # Single garage object
                                return [Garage.from_api_data(response_data)]
                        else:
                            return []
                    else:
                        print(f"Error fetching garage page {page}: HTTP {response.status}")
                        return []
        except Exception as e:
            print(f"Error fetching garage page {page}: {e}")
            return []
    
    def _update_total_count(self) -> None:
        """Update the total count of garages"""
        try:
            # Use synchronous request for initialization
            response = requests.get(
                self.api_url,
                params={'page': 1, 'pageSize': 1},
                timeout=self.api_timeout
            )
            response.raise_for_status()
            
            data = response.json()
            self.total_items = data.get('totalItems', 0)
            print(f"Total garages: {self.total_items}")
            
        except Exception as e:
            print(f"Error getting total garage count: {e}")
            # Keep previous count if available
            if not self.total_items:
                self.total_items = 0
    
    def get_total_count(self) -> int:
        """Get the total number of garages"""
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
    
    async def get_unique_locations(self) -> List[str]:
        """Get list of unique locations from all garages"""
        garages = await self.fetch_all_garages()
        locations = list(set(garage.location for garage in garages if garage.location))
        return sorted(locations)
    
    async def get_unique_services(self) -> List[str]:
        """Get list of unique service types from all garages"""
        garages = await self.fetch_all_garages()
        services = list(set(garage.garage_service for garage in garages if garage.garage_service and garage.garage_service != 'Unknown'))
        return sorted(services)
    
    async def get_garages_by_location(self, location: str) -> List[Garage]:
        """Get garages filtered by location"""
        garages = await self.fetch_all_garages()
        return [garage for garage in garages if garage.location.lower() == location.lower()]
    
    async def get_garages_by_service(self, service: str) -> List[Garage]:
        """Get garages filtered by service type"""
        garages = await self.fetch_all_garages()
        return [garage for garage in garages if garage.garage_service.lower() == service.lower()]
    
    async def get_garage_by_id(self, garage_id: int) -> Optional[Garage]:
        """Get a specific garage by ID"""
        garages = await self.fetch_all_garages()
        for garage in garages:
            if garage.id == garage_id:
                return garage
        return None
    
    def extract_coordinates_from_map_link(self, map_link: str) -> Optional[Tuple[float, float]]:
        """Extract latitude and longitude from Google Maps link"""
        if not map_link:
            return None
        
        try:
            # Clean the map link by removing extra spaces, backticks, and quotes
            cleaned_link = map_link.strip()
            # Remove various types of backticks and quotes
            cleaned_link = cleaned_link.replace('`', '').replace('`', '').replace('´', '').replace(''', '').replace(''', '')
            cleaned_link = cleaned_link.replace('"', '').replace("'", '').strip()
            pass
            
            # Handle shortened Google Maps links by trying to expand them
            if 'maps.app.goo.gl' in cleaned_link:
                pass
                try:
                    import requests
                    response = requests.head(cleaned_link, allow_redirects=True, timeout=5)
                    expanded_url = response.url
                    pass
                    cleaned_link = expanded_url
                except Exception as e:
                    pass
                    return None
            
            # Pattern for Google Maps coordinates in various formats
            patterns = [
                r'@(-?\d+\.\d+),(-?\d+\.\d+)',  # @lat,lng
                r'q=(-?\d+\.\d+),(-?\d+\.\d+)',  # q=lat,lng
                r'll=(-?\d+\.\d+),(-?\d+\.\d+)',  # ll=lat,lng
                r'center=(-?\d+\.\d+),(-?\d+\.\d+)',  # center=lat,lng
            ]
            
            for pattern in patterns:
                match = re.search(pattern, cleaned_link)
                if match:
                    lat, lng = float(match.group(1)), float(match.group(2))
                    pass
                    return (lat, lng)
            
            pass
            return None
        except (ValueError, AttributeError) as e:
            pass
            return None
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula (in km)"""
        # Convert latitude and longitude from degrees to radians
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        return c * r
    
    async def get_nearby_garages(self, user_lat: float, user_lng: float, limit: int = 5) -> List[Garage]:
        """Get garages sorted by distance from user location"""
        garages = await self.fetch_all_garages()
        garages_with_distance = []
        
        for garage in garages:
            if garage.map_link:
                coords = self.extract_coordinates_from_map_link(garage.map_link)
                if coords:
                    garage_lat, garage_lng = coords
                    distance = self.calculate_distance(user_lat, user_lng, garage_lat, garage_lng)
                    # Update the garage's distance_in_km field
                    garage.distance_in_km = round(distance, 2)
                    garages_with_distance.append(garage)
        
        # Sort by distance and return limited results
        garages_with_distance.sort(key=lambda x: x.distance_in_km)
        return garages_with_distance[:limit]
    
    async def get_full_image_url(self, image_filename: str) -> str:
        """Get full image URL from filename with validation - supports both API and R2 storage"""
        if not image_filename:
            return ""
        
        # Clean the image filename (strip whitespace and trailing commas)
        cleaned_filename = image_filename.strip().rstrip(',')
        
        # If it's already a full URL, validate and return it
        if cleaned_filename.startswith(('http://', 'https://')):
            # Basic URL validation
            if '.' in cleaned_filename and len(cleaned_filename) > 10:
                # Test if the URL is accessible
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.head(cleaned_filename, timeout=aiohttp.ClientTimeout(total=3)) as response:
                            if response.status == 200:
                                return cleaned_filename
                except Exception:
                    pass
            return ""
        
        # Try R2 storage first (newer images) and validate
        r2_url = f"{self.r2_image_base_url}/{cleaned_filename}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(r2_url, timeout=aiohttp.ClientTimeout(total=3)) as response:
                    if response.status == 200:
                        return r2_url
        except Exception:
            pass
        
        # Try API storage as fallback and validate
        api_url = f"{self.image_base_url}{cleaned_filename}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(api_url, timeout=aiohttp.ClientTimeout(total=3)) as response:
                    if response.status == 200:
                        return api_url
        except Exception:
            pass
        
        # Return empty string if no valid image found
        return ""
    
    def get_fallback_image_url(self, image_filename: str) -> str:
        """Get fallback image URL from original API storage"""
        if not image_filename:
            return ""
        
        if image_filename.startswith(('http://', 'https://')):
            return image_filename
            
        return f"{self.image_base_url}{image_filename}"
    
    async def get_r2_image_url(self, image_filename: str) -> str:
        """Get R2 storage image URL (as fallback) with validation"""
        if not image_filename:
            return ""
        
        # Clean the image filename (strip whitespace and trailing commas)
        cleaned_filename = image_filename.strip().rstrip(',')
        
        # If it's already a full URL, validate and return it
        if cleaned_filename.startswith(('http://', 'https://')):
            # Basic URL validation
            if '.' in cleaned_filename and len(cleaned_filename) > 10:
                # Test if the URL is accessible
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.head(cleaned_filename, timeout=aiohttp.ClientTimeout(total=3)) as response:
                            if response.status == 200:
                                return cleaned_filename
                except Exception:
                    pass
            return ""
        
        # Construct R2 storage URL and validate
        r2_url = f"{self.r2_image_base_url}/{cleaned_filename}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(r2_url, timeout=aiohttp.ClientTimeout(total=3)) as response:
                    if response.status == 200:
                        return r2_url
        except Exception:
            pass
            
        return ""
    
    def get_fallback_image_url(self, image_filename: str) -> str:
        """Get fallback image URL from original API storage"""
        if not image_filename:
            return ""
        
        if image_filename.startswith(('http://', 'https://')):
            return image_filename
            
        return f"{self.image_base_url}{image_filename}"