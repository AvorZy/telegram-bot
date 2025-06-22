from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

class Brand(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: Optional[datetime] = None

class Product(BaseModel):
    id: int
    user_id: Optional[int]
    brand: str
    model: str
    year: Optional[int] = None
    price: Decimal
    currency: str = "USD"
    description: Optional[str]
    image_url: Optional[str]
    gallery: List[str] = []
    location: Optional[str]
    color: Optional[str] = None
    condition: Optional[str] = None
    phone_number: Optional[str] = None
    category: Optional[str] = None
    brand_id: Optional[int] = None
    category_id: Optional[int] = None
    is_featured: bool = False
    sku: Optional[str] = None
    status: str = "available"
    created_at: datetime
    source: Optional[str] = None

class SellRequest(BaseModel):
    id: int
    user_id: int
    step: int
    car_data: str
    status: str
    created_at: datetime

class Review(BaseModel):
    id: int
    user_id: int
    car_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

class Transaction(BaseModel):
    id: int
    buyer_id: int
    seller_id: int
    car_id: int
    price: Decimal
    status: str
    created_at: datetime

# Initialize empty lists to store data
products = []
sell_requests = []
reviews = []
transactions = []

# Initialize product data from external files
def initialize_product_data():
    """Load product data from external CSV/JSON files"""
    global products, product_listings
    
    try:
        # Import here to avoid circular imports
        from utils.services.data_loader import car_data_loader
        
        # Load data from external files
        product_listings = car_data_loader.load_all_data()
        
        # Clear existing products and convert to Product objects
        products.clear()
        
        for listing in product_listings:
            try:
                product = Product(
                    id=listing["id"],
                    user_id=listing.get("user_id"),
                    brand=listing["brand"],
                    model=listing["model"],
                    year=listing.get("year"),
                    price=Decimal(str(listing["price"])),
                    currency=listing.get("currency", "USD"),
                    description=listing.get("description"),
                    image_url=listing.get("image_url"),
                    gallery=listing.get("gallery", []),
                    location=listing.get("location"),
                    color=listing.get("color"),
                    condition=listing.get("condition"),
                    phone_number=listing.get("phone_number"),
                    category=listing.get("category"),
                    is_featured=listing.get("is_featured", False),
                    sku=listing.get("sku"),
                    status=listing.get("status", "available"),
                    created_at=datetime.fromisoformat(listing["created_at"]),
                    source=listing.get("source")
                )
                products.append(product)
            except Exception as e:
                pass
        
        pass
        
    except Exception as e:
        pass
        # Fallback to empty list
        products.clear()
        product_listings = []

# Global product listings (will be populated by initialize_product_data)
product_listings = []