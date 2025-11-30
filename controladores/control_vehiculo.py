from controladores.dao import VehiculoDAO
from controladores.dto import VehiculoDTO
from modelos.vehiculo import Vehiculo


class ControladorVehiculos:
    def __init__(self):
        self.dao = VehiculoDAO()

    def crear_vehiculo(self, patente: str, marca: str, modelo: str,
                       anio: int, precio_diario_uf: float):
        patente = patente.strip().upper()
        if self.dao.buscar_por_patente(patente):
            return {"ok": False, "mensaje": "La patente ya existe."}
        if not isinstance(anio, int) or anio < 1900 or anio > 2100:
            return {"ok": False, "mensaje": "Año inválido."}
        try:
            precio = float(precio_diario_uf)
            if precio <= 0:
                return {"ok": False, "mensaje": "El precio debe ser mayor a 0."}
        except ValueError:
            return {"ok": False, "mensaje": "Precio inválido."}

        dto = VehiculoDTO(
            patente=patente,
            marca=marca,
            modelo=modelo,
            anio=anio,
            precio_diario_uf=precio,
            estado="DISPONIBLE"
        )

        if self.dao.crear(dto):
            return {"ok": True, "mensaje": "Vehículo creado correctamente."}
        return {"ok": False, "mensaje": "Error al crear vehículo."}

    def listar_vehiculos(self, disponibles: bool | None = None):
        return [Vehiculo(datos) for datos in self.dao.listar(disponibles)]
    
    def editar_vehiculo(self, vehiculo_id, marca, modelo, anio, precio):
        if not self.dao.buscar_por_id(vehiculo_id):
            return {"ok": False, "mensaje": "Vehículo no encontrado."}

        if self.dao.editar(vehiculo_id, marca, modelo, anio, precio):
            return {"ok": True, "mensaje": "Vehículo actualizado correctamente."}
        else:
            return {"ok": False, "mensaje": "Error al actualizar el vehículo."}

    def buscar_por_id(self, vehiculo_id):
        datos = self.dao.buscar_por_id(vehiculo_id)
        if not datos:
            return None
        return Vehiculo(datos)

