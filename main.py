def main():
    sistema = SistemaRestaurante(10)

    cliente = Cliente(1, "Jose")

    pizza = Producto(1, "Pizza", 3)

    pedido = cliente.crear_pedido(1, pizza)

    sistema.agregar_pedido(pedido)

    sistema.procesar_pedido()

main()