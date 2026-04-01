from queue import Queue
import threading
from logRegistro import registrar_log
import time
import random
from cliente import Cliente
class SistemaRestaurante:
    def __init__(self, ingredientes_disponibles):
        self.ingredientes_disponibles = ingredientes_disponibles
        self.ingredientes_iniciales = ingredientes_disponibles
        self.pedidos = Queue()

        self.mutex_ingredientes = threading.Lock()
        self.mutex_pedidos = threading.Lock()
        self.contador_pedidos = 1
        
        self.mutex_output = threading.Lock()  # Para sincronizar prints

    def agregar_pedido(self, pedido):
        # Mutex para pedidos
        with self.mutex_pedidos:
            self.pedidos.put(pedido)
            registrar_log("AGREGAR PEDIDO", pedido.producto.nombre, "ColaPedidos")

        print("Pedido agregado:", pedido.producto.nombre)
        
        
    def obtener_pedidos(self, productos_disponibles):
        pedidos = []
        
        print("\n¿Cuántos clientes desea agregar? ", end="")
        try:
            num_clientes = int(input())
            if num_clientes <= 0:
                print("Número inválido. usando 1 cliente.")
                num_clientes = 1
        except ValueError:
            print("Entrada inválida. Usando 1 cliente.")
            num_clientes = 1
        
        for i in range(num_clientes):
            print(f"\n--- Cliente {i+1} ---")
            print("Ingrese el nombre del cliente: ", end="")
            nombre_cliente = input().strip()
            if not nombre_cliente:
                nombre_cliente = f"Cliente{i+1}"
            
            cliente = Cliente(i+1, nombre_cliente)
            self.mostrar_menu_productos(productos_disponibles)
            
            while True:
                print(f"Ingrese el ID del producto para {nombre_cliente} (0 para terminar): ", end="")
                try:
                    id_producto = int(input())
                    if id_producto == 0:
                        break
                    if id_producto in productos_disponibles:
                        producto = productos_disponibles[id_producto]
                        pedido = cliente.crear_pedido(self.contador_pedidos, producto)
                        pedidos.append(pedido)
                        print(f"Pedido agregado: {producto.nombre}")
                        self.contador_pedidos += 1
                    else:
                        print("ID de producto no válido. Intente de nuevo.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
        
        return pedidos
        
    
    def mostrar_menu_productos(self, productos_disponibles):
        print("\n" + "="*40)
        print("MENÚ DE PRODUCTOS DISPONIBLES")
        print("="*40)
        for id_prod, producto in productos_disponibles.items():
            print(f"{id_prod}. {producto.nombre} (Ingredientes necesarios: {producto.ingredientes_necesarios})")
        print("="*40 + "\n")
    
    def procesar_pedido(self):
        
        nombre_cocinero = threading.current_thread().name
        
        while True:
            # Mutex de pedidos e ingredientes agregado.
            with self.mutex_pedidos:  
                if self.pedidos.empty():
                    with self.mutex_output:
                        print(f"{nombre_cocinero}: No hay más pedidos")
                        registrar_log("SIN PEDIDOS", f"{nombre_cocinero}", "ColaPedidos")
                    break
                
                pedido = self.pedidos.get()
                with self.mutex_output:
                    registrar_log("TOMAR PEDIDO", f"{nombre_cocinero} tomó Pedido {pedido.id_pedido}", "ColaPedidos")
                    print(f"{nombre_cocinero}: tomó el Pedido {pedido.id_pedido}: {pedido.producto.nombre}")

            ingredientes = pedido.producto.ingredientes_necesarios

            with self.mutex_ingredientes:
                with self.mutex_output:
                    registrar_log("ACCESO INGREDIENTES",f"{nombre_cocinero} - Disponible: {self.ingredientes_disponibles}, Necesarios: {ingredientes}","Ingredientes")

                if self.ingredientes_disponibles >= ingredientes:
                    self.ingredientes_disponibles -= ingredientes

                    with self.mutex_output:
                        registrar_log("ACTUALIZAR INGREDIENTES",f"{nombre_cocinero} - Restante: {self.ingredientes_disponibles}","Ingredientes")
                        print(f"{nombre_cocinero}: preparando {pedido.producto.nombre}...")

                    #Simula tiempo de preparación
                    tiempo = random.randint(1,7)
                    time.sleep(tiempo)

                    pedido.estado = "Preparado"
                    with self.mutex_output:
                        registrar_log("PEDIDO PREPARADO", f"{nombre_cocinero} preparó {pedido.producto.nombre}", f"Pedido {pedido.id_pedido}")
                        print(f"{nombre_cocinero}: finalizó Pedido {pedido.id_pedido}: {pedido.producto.nombre}")
                else:
                    with self.mutex_output:
                        print(f"{nombre_cocinero}: No hay ingredientes suficientes para {pedido.producto.nombre}")
                        registrar_log("FALTA INGREDIENTES", f"{nombre_cocinero} - {pedido.producto.nombre}", f"Pedido {pedido.id_pedido}")
            print("\n")
        
        """
                
        nombre_cocinero = threading.current_thread().name

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
        
        """
