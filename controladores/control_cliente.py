from modelos.cliente import Cliente
from controladores.dto.cliente_dto import ClienteDTO
from controladores.dao.cliente_dao import ClienteDAO
from servicios import validar_run_chileno, validar_telefono

class ControladorClientes:
    def __init__(self):
        self.dao = ClienteDAO()

    def crear_cliente(self, run: str, nombre: str, apellido: str,
                      direccion: str, telefono: str):  

        if not validar_run_chileno(run):
            return {"ok": False, "mensaje": "RUN inválido. Use formato 12345678-9."}
        if self.dao.buscar_por_run(run):
            return {"ok": False, "mensaje": "El RUN ya existe."}
        if not validar_telefono(telefono):
            return {"ok": False, "mensaje": "Teléfono inválido. Use solo números y prefijo + (opcional)."}

        dto = ClienteDTO(
            run=run,
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono
        )

        if self.dao.crear(dto):
            return {"ok": True, "mensaje": "Cliente creado correctamente."}
        return {"ok": False, "mensaje": "Error al crear cliente."}

    def listar_clientes(self):
        return [Cliente(datos) for datos in self.dao.listar()]

    def editar_cliente(self, cliente_id: int, nombre: str | None,
                       apellido: str | None, direccion: str | None,
                       telefono: str | None):
        
        datos = self.dao.buscar_por_id(cliente_id)
        if not datos:
            return {"ok": False, "mensaje": "Cliente no encontrado."}
        nuevo_nombre = nombre if nombre else datos.nombre
        nuevo_apellido = apellido if apellido else datos.apellido
        nueva_direccion = direccion if direccion else datos.direccion
        if telefono:
            if not validar_telefono(telefono):
                return {"ok": False, "mensaje": "Teléfono inválido."}
            nuevo_telefono = telefono
        else:
            nuevo_telefono = datos.telefono
        datos.nombre = nuevo_nombre
        datos.apellido = nuevo_apellido
        datos.direccion = nueva_direccion
        datos.telefono = nuevo_telefono
        if self.dao.actualizar(datos):
            return {"ok": True, "mensaje": "Cliente actualizado correctamente."}
        return {"ok": False, "mensaje": "Error al actualizar cliente."}

    def eliminar_cliente(self, cliente_id: int):
        if self.dao.eliminar(cliente_id):
            return {"ok": True, "mensaje": "Cliente eliminado."}
        return {"ok": False, "mensaje": "Cliente no encontrado."}

    def buscar_por_id(self, cliente_id):
        return self.dao.buscar_por_id(cliente_id)
