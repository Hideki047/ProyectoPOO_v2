class VehiculoDTO:
    def __init__(self, id=None, patente=None, marca=None, modelo=None,
                 anio=None, precio_diario_uf=None, estado=None):
        self.id = id
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.precio_diario_uf = precio_diario_uf
        self.estado = estado  
