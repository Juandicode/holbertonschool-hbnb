#!/usr/bin/python3

class Place(BaseModel):
    """Place model"""
    def __init__(self, title: str, price: float, latitude: float, longitude: float, owner: User, description: str = ""):
        super().__init__()  # hereda id, created_at, updated_at
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
