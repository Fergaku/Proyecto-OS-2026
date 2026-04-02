from queue import Queue
import threading
from logRegistro import registrar_log
import time
import random
from cliente import Cliente
from cocina import Cocina
class SistemaRestaurante:
    def __init__(self, ingredientes_disponibles, num_utensilios=2):
        self.ingredientes_disponibles = ingredientes_disponibles
        self.ingredientes_iniciales = ingredientes_disponibles
        self.pedidos = Queue()
        self.cocina = Cocina(num_utensilios)

        self.mutex_ingredientes = threading.Lock()
        self.mutex_pedidos = threading.Lock()
        self.contador_pedidos = 1
        
        self.mutex_cocina = threading.Lock()
        self.utensilios_disponibles = num_utensilios
        
        self.mutex_output = threading.Lock()  # Para sincronizar prints

    def agregar_pedido(self, pedido):
        # Mutex para pedidos
        with self.mutex_pedidos:
            self.pedidos.put(pedido)
            registrar_log("AGREGAR PEDIDO", pedido.producto.nombre, "ColaPedidos")

        print("Pedido agregado:", pedido.producto.nombre)
        
    # ===== METODOS PARA ACCEDER A RECURSO COMPARTIDO: COCINA =====
    def solicitar_cocina(self, nCocinero):
        with self.mutex_cocina:
            while self.utensilios_disponibles <= 0:
                pass
            self.utensilios_disponibles -= 1
            print(f"{nCocinero} esta usando la cocina (Utensilios disponibles) : {self.utensilios_disponibles}")
            
    def liberar_cocina(self, nCocinero):
        with self.mutex_cocina:
            self.utensilios_disponibles += 1
            print(f"{nCocinero} libero la cocina (Utensilios disponibles) {self.utensilios_disponibles}")        
    
       
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
            # Obtener pedido de la cola
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

            # Verificar disponibilidad de ingredientes
            with self.mutex_ingredientes:
                with self.mutex_output:
                    registrar_log("ACCESO INGREDIENTES", 
                                 f"{nombre_cocinero} - Disponible: {self.ingredientes_disponibles}, Necesarios: {ingredientes}",
                                 "Ingredientes")

                if self.ingredientes_disponibles >= ingredientes:
                    self.ingredientes_disponibles -= ingredientes

                    with self.mutex_output:
                        registrar_log("ACTUALIZAR INGREDIENTES",
                                     f"{nombre_cocinero} - Restante: {self.ingredientes_disponibles}",
                                     "Ingredientes")
                        print(f"{nombre_cocinero}: esperando acceso a la cocina...")
                    
                    # ===== RECURSO COMPARTIDO: COCINA =====
                    self.solicitar_cocina(nombre_cocinero)
                    
                    try:
                        with self.mutex_output:
                            print(f"{nombre_cocinero}: USANDO COCINA - preparando {pedido.producto.nombre}...")
                            registrar_log("USANDO COCINA", 
                                         f"{nombre_cocinero} está usando la cocina para {pedido.producto.nombre}",
                                         "Cocina")
                        
                        # Simula tiempo de preparación en la cocina
                        tiempo = random.randint(2, 4)
                        time.sleep(tiempo)

                        pedido.estado = "Preparado"
                        with self.mutex_output:
                            registrar_log("PEDIDO PREPARADO", 
                                         f"{nombre_cocinero} preparó {pedido.producto.nombre}",
                                         f"Pedido {pedido.id_pedido}")
                            print(f"{nombre_cocinero}: finalizó Pedido {pedido.id_pedido}: {pedido.producto.nombre}")
                    
                    finally:
                        # Siempre liberar la cocina, incluso si hay error
                        self.liberar_cocina(nombre_cocinero)
                    
                    # ===== FIN RECURSO COMPARTIDO =====
                    
                else:
                    with self.mutex_output:
                        print(f"{nombre_cocinero}: No hay ingredientes suficientes para {pedido.producto.nombre}")
                        registrar_log("FALTA INGREDIENTES", 
                                     f"{nombre_cocinero} - {pedido.producto.nombre}",
                                     f"Pedido {pedido.id_pedido}")
            print("\n")
 
