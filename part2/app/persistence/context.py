# persistence/context.py
from app.services.facade import HBnBFacade

class DataContext:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.facade = HBnBFacade()
            cls._instance.init_test_data()
        return cls._instance
    
    def init_test_data(self):
        """Initialize test data using existing methods"""
        # Para User - usando get_user_by_email
        if not self.facade.get_user_by_email("test@example.com"):
            test_user = self.facade.create_user({
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com"
            })
            self.test_user_id = test_user.id
            print(f"Test user created with ID: {test_user.id}")
        
        # Para Amenity - implementación temporal
        if not self._amenity_exists("WiFi"):
            test_amenity = self.facade.create_amenity({
                "name": "WiFi"
            })
            self.test_amenity_id = test_amenity.id
            print(f"Test amenity created with ID: {test_amenity.id}")

    def _amenity_exists(self, name):
        """Helper method to check amenity by name"""
        # Implementación temporal usando get_all_amenities
        # (puedes reemplazarla con get_amenity_by_name si lo implementas)
        amenities = self.facade.get_all_amenities()
        return any(a.name == name for a in amenities)

# Global access point
data_context = DataContext()
facade = data_context.facade