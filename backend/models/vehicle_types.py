"""
Vehicle types and configurations for the courier system.
"""

from enum import Enum

class VehicleType(Enum):
    BICYCLE = 'bicycle'
    MOTORCYCLE = 'motorcycle'
    CAR = 'car'
    SCOOTER = 'scooter'
    E_BIKE = 'e_bike'
    WALKING = 'walking'  # For very close deliveries

# Vehicle type configurations with their specific attributes
VEHICLE_CONFIGS = {
    VehicleType.BICYCLE: {
        'name': 'Bicycle',
        'icon': '🚲',
        'max_radius': 5.0,  # km
        'max_weight': 10.0,  # kg
        'requires_license': False,
        'requires_insurance': False,
        'speed_factor': 0.7  # relative to base delivery time
    },
    VehicleType.MOTORCYCLE: {
        'name': 'Motorcycle',
        'icon': '🏍️',
        'max_radius': 15.0,
        'max_weight': 20.0,
        'requires_license': True,
        'requires_insurance': True,
        'speed_factor': 1.2
    },
    VehicleType.CAR: {
        'name': 'Car',
        'icon': '🚗',
        'max_radius': 25.0,
        'max_weight': 50.0,
        'requires_license': True,
        'requires_insurance': True,
        'speed_factor': 1.0
    },
    VehicleType.SCOOTER: {
        'name': 'Scooter',
        'icon': '🛵',
        'max_radius': 10.0,
        'max_weight': 15.0,
        'requires_license': True,
        'requires_insurance': True,
        'speed_factor': 1.1
    },
    VehicleType.E_BIKE: {
        'name': 'E-Bike',
        'icon': '⚡🚲',
        'max_radius': 8.0,
        'max_weight': 15.0,
        'requires_license': False,
        'requires_insurance': False,
        'speed_factor': 0.9
    },
    VehicleType.WALKING: {
        'name': 'Walking',
        'icon': '🚶',
        'max_radius': 2.0,
        'max_weight': 5.0,
        'requires_license': False,
        'requires_insurance': False,
        'speed_factor': 0.4
    }
}