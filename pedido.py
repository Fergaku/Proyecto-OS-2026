class Pedido:

    def _init_(self, id_pedido, cliente, producto):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.producto = producto
        self.estado = "Pendiente"
    

