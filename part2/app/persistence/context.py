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
        """Initialize test data if needed"""
        if not self.facade.get_user("test_user"):
            self.facade.create_user({
                "id": "test_user",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com"
            })
        
        if not self.facade.get_amenity("wifi"):
            self.facade.create_amenity({
                "id": "wifi",
                "name": "WiFi"
            })

# Global access point
data_context = DataContext()
facade = data_context.facade