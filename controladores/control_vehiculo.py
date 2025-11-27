from controladores.dao import VehiculoDAO
from controladores.dto import VehiculoDTO
from modelos.vehiculo import Vehiculo


class ControladorVehiculos:
    def __init__(self):
        self.dao = VehiculoDAO()


    # CREAR VEHÍCULO
    def crear_vehiculo(self, patente: str, marca: str, modelo: str,
                       anio: int, precio_diario_uf: float):

        patente = patente.strip().upper()

        # Validar patente duplicada
        if self.dao.buscar_por_patente(patente):
            return {"ok": False, "mensaje": "La patente ya existe."}

        # Validar año
        if not isinstance(anio, int) or anio < 1900 or anio > 2100:
            return {"ok": False, "mensaje": "Año inválido."}

        # Validar precio UF
        try:
            precio = float(precio_diario_uf)
            if precio <= 0:
                return {"ok": False, "mensaje": "El precio debe ser mayor a 0."}
        except ValueError:
            return {"ok": False, "mensaje": "Precio inválido."}

        # Crear DTO
        dto = VehiculoDTO(
            patente=patente,
            marca=marca,
            modelo=modelo,
            anio=anio,
            precio_diario_uf=precio,
            estado="DISPONIBLE"
        )

        # Guardar en la BD
        if self.dao.crear(dto):
            return {"ok": True, "mensaje": "Vehículo creado correctamente."}

        return {"ok": False, "mensaje": "Error al crear vehículo."}


    # LISTAR VEHÍCULOS

    def listar_vehiculos(self, disponibles: bool | None = None):
        return [Vehiculo(datos) for datos in self.dao.listar(disponibles)]
