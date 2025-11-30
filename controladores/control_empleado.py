import pwinput
from controladores.dto.empleado_dto import EmpleadoDTO
from controladores.dao.empleado_dao import EmpleadoDAO
from modelos.empleado import Empleado
from servicios.utilidades import (
    calcular_hash_contrasena,
    validar_run_chileno,
    normalizar_run,
    verificar_contrasena
)

class ControladorEmpleados:
    def __init__(self):
        self.dao = EmpleadoDAO()

    def crear_empleado_inicial_si_no_existen(self):
        if self.dao.contar() == 0:
            return {"ok": False, "mensaje": "No existen empleados. Debe crear un gerente inicial."}
        return {"ok": True}

    def crear_empleado(self, run_input, nombre, apellido, cargo, contrasena, contrasena2):

        if not validar_run_chileno(run_input):
            return {"ok": False, "mensaje": "RUN inválido. Use formato 12345678-9."}

        try:
            run = normalizar_run(run_input)
        except Exception as e:
            return {"ok": False, "mensaje": f"RUN inválido: {e}"}

        if self.dao.buscar_por_run(run):
            return {"ok": False, "mensaje": "RUN ya existe."}

        if contrasena != contrasena2:
            return {"ok": False, "mensaje": "Las contraseñas no coinciden."}

        dto = EmpleadoDTO(
            run=run,   
            nombre=nombre,
            apellido=apellido,
            cargo=cargo,
            hash_contrasena=calcular_hash_contrasena(contrasena)
        )

        if self.dao.crear(dto):
            return {"ok": True, "mensaje": "Empleado creado exitosamente."}
        else:
            return {"ok": False, "mensaje": "Error al crear empleado."}
        
    def listar_empleados(self):
        datos = self.dao.listar()
        return [Empleado(d) for d in datos]

    def eliminar_empleado(self, empleado_id):
        if self.dao.eliminar(empleado_id):
            return {"ok": True, "mensaje": "Empleado eliminado."}
        return {"ok": False, "mensaje": "Empleado no encontrado."}

    def editar_empleado(self, emp_id, nombre, apellido, cargo, contrasena, contrasena2):
        actual = self.dao.buscar_por_id(emp_id)
        if not actual:
            return {"ok": False, "mensaje": "Empleado no encontrado."}
        nuevo_hash = None
        if contrasena:
            if contrasena != contrasena2:
                return {"ok": False, "mensaje": "Las contraseñas no coinciden."}
            nuevo_hash = calcular_hash_contrasena(contrasena)
        dto = EmpleadoDTO(
            id=emp_id,
            run=actual.run,
            nombre=nombre or actual.nombre,
            apellido=apellido or actual.apellido,
            cargo=cargo or actual.cargo,
            hash_contrasena=nuevo_hash or actual.hash_contrasena
        )
        ok = self.dao.editar(dto)
        if ok:
            return {"ok": True, "mensaje": "Empleado actualizado correctamente."}
        else:
            return {"ok": False, "mensaje": "Error al actualizar empleado."}

    def login(self, run_input, contrasena):

        if not validar_run_chileno(run_input):
            return {"ok": False, "mensaje": "RUN inválido. Use formato 12345678-9."}
        try:
            run = normalizar_run(run_input)
        except:
            return {"ok": False, "mensaje": "RUN inválido. Use formato 12345678-9."}
        datos = self.dao.buscar_por_run(run)
        if not datos:
            return {"ok": False, "mensaje": "Empleado no encontrado."}
        if not verificar_contrasena(contrasena, datos.hash_contrasena):
            return {"ok": False, "mensaje": "Contraseña incorrecta."}
        empleado = Empleado(datos)
        return {"ok": True, "mensaje": f"Bienvenido {empleado.nombre_completo()}", "empleado": empleado}
