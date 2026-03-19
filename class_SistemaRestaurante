from queue import Queue
import threading
from logRegistro import registrar_log
import time
import random

class SistemaRestaurante:
    def __init__(self, ingredientes_disponibles):
        self.ingredientes_disponibles = ingredientes_disponibles
        self.pedidos = Queue()

        self.mutex_ingredientes = threading.Lock()
        self.mutex_pedidos = threading.Lock()

    def agregar_pedido(self, pedido):
        # Mutex para pedidos
        with self.mutex_pedidos:
            self.pedidos.put(pedido)
            registrar_log("AGREGAR PEDIDO", pedido.producto.nombre, "ColaPedidos")

        print("Pedido agregado:", pedido.producto.nombre)
    
    def procesar_pedido(self):
        while True:
            # Mutex de pedidos e ingredientes agregado.
            with self.mutex_pedidos:  
                if self.pedidos.empty():
                    print("No hay pedidos")
                    registrar_log("SIN PEDIDOS", "Cola vacia", "ColaPedidos")
                    break
                
                pedido = self.pedidos.get()
                registrar_log("TOMAR PEDIDO", f"Pedido {pedido.id_pedido}", "ColaPedidos")

            ingredientes = pedido.producto.ingredientes_necesarios

            with self.mutex_ingredientes:
                registrar_log("ACCESO INGREDIENTES",f"Disponible: {self.ingredientes_disponibles}, Necesarios: {ingredientes}","Ingredientes")

                if self.ingredientes_disponibles >= ingredientes:
                    self.ingredientes_disponibles -= ingredientes

                    registrar_log("ACTUALIZAR INGREDIENTES",f"Restante: {self.ingredientes_disponibles}","Ingredientes")

                    #Simula tiempo de preparación
                    tiempo = random.randint(1,5)
                    time.sleep(tiempo)

                    pedido.estado = "Preparado"
                    registrar_log("PEDIDO PREPARADO", pedido.producto.nombre, f"Pedido {pedido.id_pedido}")
                    print("Pedido preparado:", pedido.producto.nombre)
                else:
                    print("No hay ingredientes suficientes")
                    registrar_log("FALTA INGREDIENTES", pedido.producto.nombre, f"Pedido {pedido.id_pedido}")
