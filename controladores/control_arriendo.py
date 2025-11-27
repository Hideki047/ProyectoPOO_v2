from datetime import datetime
from controladores.dto.arriendo_dto import ArriendoDTO
from controladores.dao.arriendo_dao import ArriendoDAO
from controladores.dao.cliente_dao import ClienteDAO
from controladores.dao.vehiculo_dao import VehiculoDAO
from modelos.arriendo import Arriendo
from servicios.utilidades import obtener_valor_uf


class ControladorArriendos:
    def __init__(self):
        self.dao = ArriendoDAO()
        self.dao_clientes = ClienteDAO()
        self.dao_vehiculos = VehiculoDAO()

    def crear_arriendo(self, empleado, vehiculo_id, cliente_id, fecha_inicio, fecha_fin):

        if fecha_fin <= fecha_inicio:
            return {"ok": False, "mensaje": "Fecha fin debe ser posterior a fecha inicio."}

        vehiculo = self.dao_vehiculos.buscar_por_id(vehiculo_id)
        if not vehiculo:
            return {"ok": False, "mensaje": "Vehículo no existe."}

        if vehiculo.estado != "DISPONIBLE":
            return {"ok": False, "mensaje": "El vehículo NO está disponible."}

        cliente = self.dao_clientes.buscar_por_id(cliente_id)
        if not cliente:
            return {"ok": False, "mensaje": "Cliente NO existe."}

        valor_uf = obtener_valor_uf(fecha_inicio)
        dias = (fecha_fin - fecha_inicio).days or 1
        total_uf = float(vehiculo.precio_diario_uf) * dias
        total_clp = total_uf * valor_uf

        dto = ArriendoDTO(
            vehiculo_id=vehiculo.id,
            cliente_id=cliente.id,
            empleado_id=empleado.obtener_id(),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            valor_uf=valor_uf,
            total_uf=total_uf,
            total_clp=total_clp,
            estado="VIGENTE"
        )

        if not self.dao.crear(dto):
            return {"ok": False, "mensaje": "Error en la BD al crear arriendo."}

        self.dao_vehiculos.actualizar_estado(vehiculo.id, "ARRENDADO")

        return {
            "ok": True,
            "mensaje": "Arriendo creado.",
            "data": {
                "dias": dias,
                "valor_uf": valor_uf,
                "total_uf": total_uf,
                "total_clp": total_clp
            }
        }

    def listar_arriendos(self):
        datos = self.dao.listar()
        return [Arriendo(d) for d in datos]

    def cancelar_arriendo(self, arriendo_id):
        datos = self.dao.buscar_por_id(arriendo_id)
        if not datos:
            return {"ok": False, "mensaje": "Arriendo no encontrado."}

        arr = Arriendo(datos)

        if not arr.puede_cancelarse(datetime.now()):
            return {"ok": False, "mensaje": "Faltan menos de 4 hrs → No se puede cancelar."}

        self.dao.actualizar_estado(arriendo_id, "CANCELADO")
        self.dao_vehiculos.actualizar_estado(datos.vehiculo_id, "DISPONIBLE")

        return {"ok": True, "mensaje": "Arriendo cancelado correctamente."}
