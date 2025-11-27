from controladores.dto.cliente_dto import ClienteDTO
from modelos.persona import Persona

class Cliente(Persona):
    def __init__(self, dto: ClienteDTO):
        super().__init__(dto.run, dto.nombre, dto.apellido)
        self._datos = dto

    def obtener_id(self):
        return self._datos.id

    def asignar_id(self, nuevo_id):
        self._datos.id = nuevo_id

    def obtener_datos(self):
        return self._datos

