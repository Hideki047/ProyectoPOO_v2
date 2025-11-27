class ArriendoDTO:
    def __init__(
        self,
        id=None,
        vehiculo_id=None,
        cliente_id=None,
        empleado_id=None,
        fecha_inicio=None,
        fecha_fin=None,
        valor_uf=None,
        total_uf=None,
        total_clp=None,
        estado="VIGENTE"
    ):
        self.id = id
        self.vehiculo_id = vehiculo_id
        self.cliente_id = cliente_id
        self.empleado_id = empleado_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.valor_uf = valor_uf
        self.total_uf = total_uf
        self.total_clp = total_clp
        self.estado = estado
