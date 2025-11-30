class ArriendoDTO:
    def __init__(self,
                 id,
                 vehiculo_id,
                 cliente_id,
                 empleado_id,
                 fecha_inicio,
                 fecha_fin,
                 total_uf,
                 total_clp,
                 estado,
                 cliente_nombre=None,
                 cliente_apellido=None,
                 vehiculo_marca=None,
                 vehiculo_modelo=None
                 ):

        self.id = id
        self.vehiculo_id = vehiculo_id
        self.cliente_id = cliente_id
        self.empleado_id = empleado_id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.total_uf = total_uf
        self.total_clp = total_clp
        self.estado = estado
        self.cliente_nombre = cliente_nombre
        self.cliente_apellido = cliente_apellido
        self.vehiculo_marca = vehiculo_marca
        self.vehiculo_modelo = vehiculo_modelo
