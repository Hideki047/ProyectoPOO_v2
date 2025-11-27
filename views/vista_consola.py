import os
import pwinput
from datetime import datetime
# Controladores
from controladores.control_empleado import ControladorEmpleados
from controladores.control_cliente import ControladorClientes
from controladores.control_vehiculo import ControladorVehiculos
from controladores.control_arriendo import ControladorArriendos

class VistaConsola:
    def __init__(self):
        self.ctrl_empleados = ControladorEmpleados()
        self.ctrl_clientes = ControladorClientes()
        self.ctrl_vehiculos = ControladorVehiculos()
        self.ctrl_arriendos = ControladorArriendos()

    def limpiar(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pausar(self):
        input("\nPresione Enter para continuar...")

    def crear_gerente_inicial(self):
        self.limpiar()
        print("=============================")
        print("=== Crear Gerente Inicial ===")
        print("=============================")
        codigo = input("Código: ").strip()
        run = input("RUN: ").strip()
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        contrasena = pwinput.pwinput("Contraseña: ", mask="*")
        contrasena2 = pwinput.pwinput("Repetir Contraseña: ", mask="*")

        res = self.ctrl_empleados.crear_empleado(
            codigo=codigo,
            run_input=run,
            nombre=nombre,
            apellido=apellido,
            cargo="Gerente",
            contrasena=contrasena,
            contrasena2=contrasena2
        )

        print(res["mensaje"])
        self.pausar()

    def login(self):
        self.limpiar()
        print("=============")
        print("=== LOGIN ===")
        print("=============")

        for _ in range(3):
            run = input("RUN: ").strip()
            contrasena = pwinput.pwinput("Contraseña: ", mask="*")

            res = self.ctrl_empleados.login(run, contrasena)

            if res["ok"]:
                print(res["mensaje"])
                self.pausar()
                return res["empleado"]

            print("❌", res["mensaje"])

        print("❌ Máximo de intentos alcanzado.")
        return None

    def flujo_empleado(self):
        self.limpiar()

        while True:
            res = self.ctrl_empleados.crear_empleado_inicial_si_no_existen()
            if res["ok"]:
                break
            self.crear_gerente_inicial()

        empleado = self.login()
        if not empleado:
            return

        while True:
            self.limpiar()
            print("======================")
            print("=== MENÚ PRINCIPAL ===")
            print("======================")

            if empleado.puede_gestionar_empleados():
                print("1) Empleados")
                print("2) Clientes")
                print("3) Vehículos")
                print("4) Arriendos")
                print("0) Salir")
                op = input("Opción: ").strip()

                if op == "1": self.menu_empleados()
                elif op == "2": self.menu_clientes()
                elif op == "3": self.menu_vehiculos()
                elif op == "4": self.menu_arriendos(empleado)
                elif op == "0": break
                else: print("Opción inválida.")

            else:
                print("1) Clientes")
                print("2) Arriendos")
                print("0) Salir")
                op = input("Opción: ").strip()

                if op == "1": self.menu_clientes()
                elif op == "2": self.menu_arriendos(empleado)
                elif op == "0": break
                else: print("Opción inválida.")

    def flujo_cliente(self):
        while True:
            self.limpiar()
            print("====================")
            print("=== MENÚ CLIENTE ===")
            print("====================")
            print("1) Ver vehículos disponibles")
            print("0) Volver")
            op = input("Opción: ").strip()

            if op == "1":
                self.limpiar()
                self.listar_disponibles()
                self.pausar()
            elif op == "0":
                break
            else:
                print("Opción inválida.")
                self.pausar()

    def menu_principal(self):
        while True:
            self.limpiar()
            print("============================")
            print("=== BIENVENIDO A RENTACAR ===")
            print("============================")
            print("1) Soy Cliente")
            print("2) Soy Empleado")
            print("0) Salir")
            op = input("Opción: ").strip()

            if op == "1":
                self.flujo_cliente()
            elif op == "2":
                self.flujo_empleado()
            elif op == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
                self.pausar()
    # ==========================
    # EMPLEADOS
    # ==========================

    def menu_empleados(self):
        while True:
            self.limpiar()
            print("============================")
            print("=== Gestión de Empleados ===")
            print("============================")
            print("1) Crear empleado")
            print("2) Listar empleados")
            print("3) Eliminar empleado")
            print("0) Volver")
            op = input("Opción: ")

            if op == "1": self.crear_empleado()
            elif op == "2": self.listar_empleados()
            elif op == "3": self.eliminar_empleado()
            elif op == "0": break
            else: print("❌ Opción inválida.")

    def crear_empleado(self):
        self.limpiar()
        print("======================")
        print("=== Crear Empleado ===")
        print("======================")
        codigo = input("Código: ")
        run = input("RUN: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        cargo = input("Cargo (Gerente/Ejecutivo): ").title()

        c1 = pwinput.pwinput("Contraseña: ", mask="*")
        c2 = pwinput.pwinput("Repetir contraseña: ", mask="*")

        res = self.ctrl_empleados.crear_empleado(
            codigo=codigo, run_input=run, nombre=nombre,
            apellido=apellido, cargo=cargo,
            contrasena=c1, contrasena2=c2
        )
        print(res["mensaje"])

    def listar_empleados(self):
        empleados = self.ctrl_empleados.listar_empleados()
        if not empleados:
            print("No hay empleados.")
        else:
            for e in empleados:
                d = e.obtener_datos()
                print(f"[{d.id}] {d.codigo} | {d.nombre} {d.apellido} | {d.run} | Cargo: {d.cargo}")
        self.pausar()

    def eliminar_empleado(self):
        self.limpiar()
        print("=== Eliminar Empleado ===")
        empleados = self.ctrl_empleados.listar_empleados()
        if not empleados:
            print("No hay empleados.")
            self.pausar()
            return

        for e in empleados:
            d = e.obtener_datos()
            print(f"[{d.id}] {d.codigo} | {d.nombre} {d.apellido}")
        
        print("0) Volver")

        try:
            emp_id = int(input("ID empleado: "))
            if emp_id == 0:
                return
        except:
            print("ID inválido.")
            return

        res = self.ctrl_empleados.eliminar_empleado(emp_id)
        print(res["mensaje"])

    # ==========================
    # CLIENTES
    # ==========================

    def menu_clientes(self):
        while True:
            self.limpiar()
            print("===========================")
            print("=== Gestión de Clientes ===")
            print("===========================")
            print("1) Crear cliente")
            print("2) Listar clientes")
            print("3) Editar cliente")
            print("4) Eliminar cliente")
            print("0) Volver")
            op = input("Opción: ")

            if op == "1": self.crear_cliente()
            elif op == "2": self.listar_clientes()
            elif op == "3": self.editar_cliente()
            elif op == "4": self.eliminar_cliente()
            elif op == "0": break
            else: print("❌ Opción inválida.")

    def crear_cliente(self):
        self.limpiar()
        print("=====================")
        print("=== Crear Cliente ===")
        print("=====================")
        run = input("RUN: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        direccion = input("Dirección: ")
        telefono = input("Teléfono: ")

        res = self.ctrl_clientes.crear_cliente(run, nombre, apellido, direccion, telefono)
        print(res["mensaje"])

    def listar_clientes(self):
        clientes = self.ctrl_clientes.listar_clientes()
        if not clientes:
            print("No hay clientes.")
        else:
            for c in clientes:
                d = c.obtener_datos()
                print(f"[{d.id}] {d.run} - {d.nombre} {d.apellido} | Tel: {d.telefono}")
        self.pausar()

    def editar_cliente(self):
        self.limpiar()
        try:
            cid = int(input("ID cliente: "))
        except:
            print("ID inválido.")
            return

        nombre = input("Nuevo nombre: ") or None
        apellido = input("Nuevo apellido: ") or None
        direccion = input("Nueva dirección: ") or None
        telefono = input("Nuevo teléfono: ") or None

        res = self.ctrl_clientes.editar_cliente(cid, nombre, apellido, direccion, telefono)
        print(res["mensaje"])

    def eliminar_cliente(self):
        self.limpiar()
        print("=== Eliminar Cliente ===")
        clientes = self.ctrl_clientes.listar_clientes()
        if not clientes:
            print("No hay clientes.")
            self.pausar()
            return

        for c in clientes:
            d = c.obtener_datos()
            print(f"[{d.id}] {d.run} - {d.nombre} {d.apellido}")

        print("0) Volver")

        try:
            cid = int(input("ID cliente: "))
            if cid == 0:
                return
        except:
            print("ID inválido.")
            return
        res = self.ctrl_clientes.eliminar_cliente(cid)
        print(res["mensaje"])
        self.pausar()

    # ==========================
    # VEHÍCULOS
    # ==========================

    def menu_vehiculos(self):
        while True:
            self.limpiar()
            print("============================")
            print("=== Gestión de Vehículos ===")
            print("============================")
            print("1) Crear vehículo")
            print("2) Listar vehículos")
            print("3) Listar disponibles")
            print("0) Volver")
            op = input("Opción: ")

            if op == "1": self.crear_vehiculo()
            elif op == "2": self.listar_vehiculos()
            elif op == "3": self.listar_disponibles()
            elif op == "0": break
            else: print("❌ Opción inválida.")

    def crear_vehiculo(self):
        self.limpiar()
        print("======================")
        print("=== Crear Vehículo ===")
        print("======================")

        patente = input("Patente: ").upper()
        marca = input("Marca: ")
        modelo = input("Modelo: ")

        try:
            anio = int(input("Año: "))
        except:
            print("Año inválido.")
            return

        try:
            precio = float(input("Precio UF/día: "))
        except:
            print("Precio inválido.")
            return

        res = self.ctrl_vehiculos.crear_vehiculo(patente, marca, modelo, anio, precio)
        print(res["mensaje"])

    def listar_vehiculos(self):
        vehiculos = self.ctrl_vehiculos.listar_vehiculos()
        if not vehiculos:
            print("No hay vehículos.")
        else:
            for v in vehiculos:
                d = v.obtener_datos()
                print(f"[{d.id}] {d.patente} | {d.marca} {d.modelo} | Año {d.anio}")
        self.pausar()

    def listar_disponibles(self):
        vehiculos = self.ctrl_vehiculos.listar_vehiculos(disponibles=True)
        if not vehiculos:
            print("No hay disponibles.")
        else:
            for v in vehiculos:
                d = v.obtener_datos()
                print(f"[{d.id}] {d.patente} | {d.marca} {d.modelo}")
        self.pausar()

    # ==========================
    # ARRIENDOS
    # ==========================

    def menu_arriendos(self, empleado):
        while True:
            self.limpiar()
            print("============================")
            print("=== Gestión de Arriendos ===")
            print("============================")
            print("1) Crear arriendo")
            print("2) Listar arriendos")
            print("3) Cancelar arriendo")
            print("0) Volver")
            op = input("Opción: ")

            if op == "1": self.crear_arriendo(empleado)
            elif op == "2": self.listar_arriendos()
            elif op == "3": self.cancelar_arriendo()
            elif op == "0": break
            else: print("❌ Opción inválida.")

    def crear_arriendo(self, empleado):
        self.limpiar()
        print("=== Crear Arriendo ===")
        
        # 1. Seleccionar Cliente
        print("\n--- Seleccionar Cliente ---")
        clientes = self.ctrl_clientes.listar_clientes()
        if not clientes:
            print("No hay clientes registrados. Debe crear uno primero.")
            self.pausar()
            return

        for c in clientes:
            d = c.obtener_datos()
            print(f"[{d.id}] {d.run} - {d.nombre} {d.apellido}")
        
        print("0) Volver")
        
        try:
            cliente_id = int(input("ID Cliente: "))
            if cliente_id == 0: return
        except:
            print("ID inválido.")
            self.pausar()
            return

        # 2. Seleccionar Vehículo
        self.limpiar()
        print("=== Crear Arriendo ===")
        print("\n--- Seleccionar Vehículo Disponible ---")
        vehiculos = self.ctrl_vehiculos.listar_vehiculos(disponibles=True)
        if not vehiculos:
            print("No hay vehículos disponibles.")
            self.pausar()
            return

        for v in vehiculos:
            d = v.obtener_datos()
            print(f"[{d.id}] {d.patente} | {d.marca} {d.modelo}")
            
        print("0) Volver")

        try:
            vehiculo_id = int(input("ID Vehículo: "))
            if vehiculo_id == 0: return
        except:
            print("ID inválido.")
            self.pausar()
            return

        # 3. Fechas
        self.limpiar()
        print("=== Crear Arriendo ===")
        print("\n--- Ingreso de Fechas (AAAA-MM-DD) ---")
        
        f_inicio_str = input("Fecha Inicio: ")
        f_fin_str = input("Fecha Fin: ")

        try:
            fecha_inicio = datetime.strptime(f_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(f_fin_str, "%Y-%m-%d")
        except ValueError:
            print("Formato de fecha inválido. Use AAAA-MM-DD.")
            self.pausar()
            return

        # 4. Crear
        res = self.ctrl_arriendos.crear_arriendo(
            empleado, vehiculo_id, cliente_id, fecha_inicio, fecha_fin
        )
        
        print(res["mensaje"])
        if res["ok"]:
            data = res["data"]
            print(f"Total Días: {data['dias']}")
            print(f"Total UF: {data['total_uf']:.2f}")
            print(f"Total CLP: ${data['total_clp']:,.0f}")
        
        self.pausar()

    def listar_arriendos(self):
        arr = self.ctrl_arriendos.listar_arriendos()
        if not arr:
            print("No hay arriendos.")
        else:
            for a in arr:
                d = a.obtener_datos()
                print(f"ID: {d.id} | Vehículo: {d.vehiculo_id} | Cliente: {d.cliente_id} | Estado: {d.estado}")
        self.pausar()

    def cancelar_arriendo(self):
        self.limpiar()
        print("=== Cancelar Arriendo ===")
        arr = self.ctrl_arriendos.listar_arriendos()
        if not arr:
            print("No hay arriendos.")
            self.pausar()
            return

        for a in arr:
            d = a.obtener_datos()
            print(f"ID: {d.id} | Vehículo: {d.vehiculo_id} | Cliente: {d.cliente_id} | Estado: {d.estado}")

        print("0) Volver")

        try:
            aid = int(input("ID arriendo: "))
            if aid == 0:
                return
        except:
            print("ID inválido.")
            return
        res = self.ctrl_arriendos.cancelar_arriendo(aid)
        print(res["mensaje"])
        self.pausar()
