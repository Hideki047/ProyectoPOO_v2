from controladores.dto.empleado_dto import EmpleadoDTO
from modelos.persona import Persona

class Empleado(Persona):
    def __init__(self, dto: EmpleadoDTO):
        super().__init__(dto.run, dto.nombre, dto.apellido)
        self._datos = dto

    def obtener_cargo(self):
        return self._datos.cargo

    def asignar_cargo(self, cargo):
        self._datos.cargo = cargo

    def obtener_id(self):
        return self._datos.id

    def asignar_id(self, nuevo_id):
        self._datos.id = nuevo_id

    def obtener_datos(self):
        return self._datos

    def puede_gestionar_empleados(self):
        return self._datos.cargo == "Gerente"
