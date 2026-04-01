import threading
from sistemaRestaurante import SistemaRestaurante
from cliente import Cliente
from pedido import Pedido
from producto import Producto
from info_estudiantes import nombres_estudiantes
from info_proyecto import descripcion_proyecto
from time import sleep

PRODUCTOS_DISPONIBLES = {
    1: Producto(1, "Pizza", 3),
    2: Producto(2, "Hamburguesa", 2),
    3: Producto(3, "Pasta", 4),
    4: Producto(4, "Ensalada", 1),
    5: Producto(5, "Postre", 1),
    6: Producto(6, "Sopa", 2),
    7: Producto(7, "Sandwich", 2),
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
    
    while True:
        try:
            
            opcion_intro = int(input("Ingrese la opción que quiere mostrar \n1. Nombres de estudiantes  \n2. Info del proyecto\nOtro valor para seguir.\nSeleccione: "))
            sleep(0.5)
            match opcion_intro:
                case 1:
                    print("="*30)
                    nombres_estudiantes()
                    print("="*30)
                case 2:
                    print("="*30)
                    descripcion_proyecto()
                    print("="*30)
                case _:
                    print("Continuando a sistema...")
                    sleep(1)
                    break
            opcion_intro = int(input("Ingrese la opción que quiere mostrar \n1. Nombres de estudiantes  \n2. Info del proyecto\nOtro valor para seguir.\nSeleccione: "))
        except ValueError:
            print("Valor equivocado.")
            opcion_intro = int(input("Ingrese un número. \n1. Nombres de estudiantes  \n2. Info del proyecto\nOtro valor para seguir.\nSeleccione: "))
    
    
    
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
    sleep(1)
    print(f"Procesando {len(pedidos)} pedidos...")
    for pedido in pedidos: sistema.agregar_pedido(pedido)
    sleep(1)
    try:
        num_cocineros = int(input("Ingrese la cantidad de cocineros (1-5, default 3): "))
        if num_cocineros < 1 or num_cocineros > 5:
            num_cocineros = 3
    except ValueError:
        num_cocineros = 3
    sleep(1)
    hilos = []
    print(f"Iniciando {num_cocineros} cocineros...")
    sleep(1)
    for i in range(num_cocineros):
        hilo = threading.Thread(
            target=sistema.procesar_pedido,
            name = f"Cocinero {i+1}"
        )
        hilos.append(hilo)
        hilo.start()
    
        
    for hilo in hilos: print(f"Cocinero {i+1}: listo para procesar pedidos.") ; hilo.join()
    
    
    print("\n" + "="*40)
    print("Simulación finalizada.")
    print("="*40 + "\n")

if __name__ == "__main__":
    
    main()