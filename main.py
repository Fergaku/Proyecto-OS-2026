import threading
from sistemaRestaurante import SistemaRestaurante
from cliente import Cliente
from pedido import Pedido
from producto import Producto

def main():
    sistema = SistemaRestaurante(10)

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

    print("Simulación finalizada.")

if __name__ == "__main__":
    main()