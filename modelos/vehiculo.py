from controladores.dto.vehiculo_dto import VehiculoDTO

class Vehiculo:
    def __init__(self, dto: VehiculoDTO):
        self._datos = dto

    def obtener_id(self):
        return self._datos.id

    def asignar_id(self, nuevo_id):
        self._datos.id = nuevo_id

    def obtener_patente(self):
        return self._datos.patente

    def asignar_patente(self, patente):
        self._datos.patente = patente

    def obtener_estado(self):
        return self._datos.estado

    def asignar_estado(self, nuevo_estado):
        if nuevo_estado in ("DISPONIBLE", "ARRENDADO"):
            self._datos.estado = nuevo_estado

    def obtener_datos(self):
        return self._datos
