from enum import Enum

class Unit(Enum):

    def __init__(self, description):
        self.description = description
    
    CELSIUS = "metric"
    FAHRENHEIT = "imperial"
    KELVIN = ""