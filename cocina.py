import threading
class Cocina:
    def __init__(self, num_utensilios=2):
        self.num_utensilios = num_utensilios
        self.utensilios_disponibles = num_utensilios
        self.mutex_cocina = threading.Lock()
    
    