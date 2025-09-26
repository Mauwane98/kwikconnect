"""
Vendor Types and Categories

This file defines the various types of vendors supported by the platform.
"""

from enum import Enum

class VendorType(Enum):
    SPAZA = "spaza"
    SUPERMARKET = "supermarket"
    BUTCHERY = "butchery"
    PHARMACY = "pharmacy"
    FAST_FOOD = "fast_food"
    STREET_FOOD = "street_food"
    TAVERN = "tavern"
    HARDWARE = "hardware"
    CLOTHING = "clothing"
    SALON = "salon"
    ELECTRONICS = "electronics"
    STATIONERY = "stationery"
    FRUIT_VEG = "fruit_and_vegetables"
    BAKERY = "bakery"
    TUCKSHOP = "tuckshop"
    CELL_PHONE = "cell_phone_shop"
    CAR_WASH = "car_wash"
    LAUNDRY = "laundry"
    RESTAURANT = "restaurant"
    OTHER = "other"

# Vendor categories with their specific requirements and features
VENDOR_CATEGORIES = {
    VendorType.SPAZA: {
        "name": "Spaza Shop",
        "description": "Local convenience store",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "🏠"
    },
    VendorType.SUPERMARKET: {
        "name": "Supermarket",
        "description": "Larger retail store",
        "requires_license": True,
        "allows_delivery": True,
        "icon": "🛒"
    },
    VendorType.BUTCHERY: {
        "name": "Butchery",
        "description": "Meat and poultry shop",
        "requires_license": True,
        "requires_cold_chain": True,
        "allows_delivery": True,
        "icon": "🥩"
    },
    VendorType.PHARMACY: {
        "name": "Pharmacy",
        "description": "Medicine and healthcare products",
        "requires_license": True,
        "requires_pharmacist": True,
        "allows_delivery": True,
        "icon": "💊"
    },
    VendorType.FAST_FOOD: {
        "name": "Fast Food",
        "description": "Quick service food",
        "requires_license": True,
        "requires_food_cert": True,
        "allows_delivery": True,
        "icon": "🍟"
    },
    VendorType.STREET_FOOD: {
        "name": "Street Food",
        "description": "Local food stands and kota spots",
        "requires_license": False,
        "requires_food_cert": True,
        "allows_delivery": True,
        "icon": "🥘"
    },
    VendorType.TAVERN: {
        "name": "Tavern",
        "description": "Local pub/bar",
        "requires_license": True,
        "requires_liquor_license": True,
        "allows_delivery": True,
        "age_restricted": True,
        "icon": "🍻"
    },
    VendorType.HARDWARE: {
        "name": "Hardware Store",
        "description": "Building and home improvement supplies",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "🔨"
    },
    VendorType.CLOTHING: {
        "name": "Clothing Store",
        "description": "Apparel and accessories",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "👕"
    },
    VendorType.SALON: {
        "name": "Beauty Salon",
        "description": "Hair and beauty services",
        "requires_license": True,
        "allows_delivery": False,
        "icon": "💇"
    },
    VendorType.ELECTRONICS: {
        "name": "Electronics Shop",
        "description": "Electronics and accessories",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "📱"
    },
    VendorType.STATIONERY: {
        "name": "Stationery Shop",
        "description": "School and office supplies",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "📚"
    },
    VendorType.FRUIT_VEG: {
        "name": "Fruit and Veg",
        "description": "Fresh produce",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "🥬"
    },
    VendorType.BAKERY: {
        "name": "Bakery",
        "description": "Fresh bread and baked goods",
        "requires_license": True,
        "requires_food_cert": True,
        "allows_delivery": True,
        "icon": "🥖"
    },
    VendorType.TUCKSHOP: {
        "name": "Tuck Shop",
        "description": "Small convenience store",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "🏪"
    },
    VendorType.CELL_PHONE: {
        "name": "Cell Phone Shop",
        "description": "Mobile phones and airtime",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "📱"
    },
    VendorType.CAR_WASH: {
        "name": "Car Wash",
        "description": "Vehicle cleaning services",
        "requires_license": False,
        "allows_delivery": False,
        "icon": "🚗"
    },
    VendorType.LAUNDRY: {
        "name": "Laundry",
        "description": "Laundry and dry cleaning services",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "👕"
    },
    VendorType.RESTAURANT: {
        "name": "Restaurant",
        "description": "Sit-down dining",
        "requires_license": True,
        "requires_food_cert": True,
        "allows_delivery": True,
        "icon": "🍽️"
    },
    VendorType.OTHER: {
        "name": "Other",
        "description": "Other type of business",
        "requires_license": False,
        "allows_delivery": True,
        "icon": "🏢"
    }
}