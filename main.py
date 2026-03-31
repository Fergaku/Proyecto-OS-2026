import threading
from sistemaRestaurante import SistemaRestaurante
from cliente import Cliente
from pedido import Pedido
from producto import Producto

PRODUCTOS_DISPONIBLES = {
    1: Producto(1, "Pizza", 3),
    2: Producto(2, "Hamburguesa", 2),
    3: Producto(3, "Pasta", 4),
    4: Producto(4, "Ensalada", 1),
    5: Producto(5, "Postre", 1)
}

def mostrar_menu_productos():
    
    print("\n" + "="*40)
    print("MENÚ DE PRODUCTOS DISPONIBLES")
    print("="*40)
    for id_prod, producto in PRODUCTOS_DISPONIBLES.items():
        print(f"{id_prod}. {producto.nombre} (Ingredientes necesarios: {producto.ingredientes_necesarios})")
    print("="*40 + "\n")

def main():
    print("\n" + "="*40)
    print("SISTEMA DE RESTAURANTE")
    print("="*40)
    
    print("\nIngrese la cantidad inicial de ingredientes disponibles: ", end="")
    try:
        ingredientes = int(input())
        if (ingredientes < 0):
            ingredientes = 10
            print("usando valor por defecto de ingredientes disponibles: 10")
    except ValueError:
        ingredientes = 10
        print("usando valor por defecto de ingredientes disponibles: 10")
    
    sistema = SistemaRestaurante(ingredientes)

    pedidos = sistema.obtener_pedidos(PRODUCTOS_DISPONIBLES)
    if not pedidos: print("Pedidos vacios. Finalizando"); return
    
    print(f"Procesando {len(pedidos)} pedidos...")
    for pedido in pedidos: sistema.agregar_pedido(pedido)
    
    try:
        num_cocineros = int(input("Ingrese la cantidad de cocineros (1-5, default 3): "))
        if num_cocineros < 1 or num_cocineros > 5:
            num_cocineros = 3
    except ValueError:
        num_cocineros = 3
        
    hilos = []
    print(f"Iniciando {num_cocineros} cocineros...")
    
    for i in range(num_cocineros):
        hilo = threading.Thread(
            target=sistema.procesar_pedido,
            name = f"Cocinero {i+1}"
        )
        hilos.append(hilo)
        hilo.start()
    
    for hilo in hilos: hilo.join()
    
    """
    
    cliente = Cliente(1, "Jose")

    pizza = Producto(1, "Pizza", 3)

    pedido1 = cliente.crear_pedido(1, pizza)
    pedido2 = cliente.crear_pedido(2, pizza)
    pedido3 = cliente.crear_pedido(3, pizza)

    sistema.agregar_pedido(pedido1)
    sistema.agregar_pedido(pedido2)
    sistema.agregar_pedido(pedido3)

    hilo1 = threading.Thread(target=sistema.procesar_pedido, name="COCINERO 1")
    hilo2 = threading.Thread(target=sistema.procesar_pedido, name="COCINERO 2")
    hilo3 = threading.Thread(target=sistema.procesar_pedido, name="COCINERO 3")

    hilo1.start()
    hilo2.start()
    hilo3.start()
    
    hilo1.join()
    hilo2.join()
    hilo3.join()
    """

    
    print("\n" + "="*40)
    print("Simulación finalizada.")
    print("="*40 + "\n")

if __name__ == "__main__":
    
    main()