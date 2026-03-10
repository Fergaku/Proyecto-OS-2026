class Cliente:

    def __init__(self, id_cliente, nombre):
        self.id_cliente = id_cliente
        self.nombre = nombre

    def crear_pedido(self, id_pedido, producto):
        return Pedido(id_pedido, self, producto)