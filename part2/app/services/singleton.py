# singleton.py para persistencia entre solicitudes
from app.facade import HBnBFacade

class SingletonFacade:
    _instance = None  # Almacena la única instancia

    def __new__(cls):
        if cls._instance is None:
            cls._instance = HBnBFacade()  # Crea la instancia solo una vez
        return cls._instance

# Instancia global accesible desde cualquier módulo
facade = SingletonFacade()