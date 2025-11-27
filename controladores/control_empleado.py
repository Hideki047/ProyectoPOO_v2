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

    def crear_empleado(self, codigo, run_input, nombre, apellido, cargo, contrasena, contrasena2):

        # Validar formato
        if not validar_run_chileno(run_input):
            return {"ok": False, "mensaje": "RUN inválido. Use formato 12345678-9."}
        # NORMALIZAR SIEMPRE A FORMATO FINAL
        try:
            run = normalizar_run(run_input)
        except Exception as e:
            return {"ok": False, "mensaje": f"RUN inválido: {e}"}
        # Asegurar que NO exista el RUN ya normalizado
        if self.dao.buscar_por_run(run):
            return {"ok": False, "mensaje": "RUN ya existe."}
        # Validar contraseñas
        if contrasena != contrasena2:
            return {"ok": False, "mensaje": "Las contraseñas no coinciden."}
        # Crear DTO
        dto = EmpleadoDTO(
            codigo=codigo,
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

    def login(self, run_input, contrasena):

        # Validar
        if not validar_run_chileno(run_input):
            return {"ok": False, "mensaje": "RUN inválido. Use formato 12345678-9."}

        # Normalizar
        try:
            run = normalizar_run(run_input)
        except:
            return {"ok": False, "mensaje": "RUN inválido. Use formato 12345678-9."}

        # Buscar empleado
        datos = self.dao.buscar_por_run(run)
        if not datos:
            return {"ok": False, "mensaje": "Empleado no encontrado."}

        # Verificar contraseña
        if not verificar_contrasena(contrasena, datos.hash_contrasena):
            return {"ok": False, "mensaje": "Contraseña incorrecta."}

        empleado = Empleado(datos)
        return {"ok": True, "mensaje": f"Bienvenido {empleado.nombre_completo()}", "empleado": empleado}
