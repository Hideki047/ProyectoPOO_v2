import os
import pwinput
from datetime import date
from datetime import datetime
from controladores.control_empleado import ControladorEmpleados
from controladores.control_cliente import ControladorClientes
from controladores.control_vehiculo import ControladorVehiculos
from controladores.control_arriendo import ControladorArriendos
from servicios.utilidades import validar_run_chileno, validar_telefono,normalizar_run


class VistaConsola:
    def __init__(self):
        self.ctrl_empleados = ControladorEmpleados()
        self.ctrl_clientes = ControladorClientes()
        self.ctrl_vehiculos = ControladorVehiculos()
        self.ctrl_arriendos = ControladorArriendos()

    # ============================================================
    # FORMATO PARA TITULO 
    # ============================================================
    def titulo(self, texto):
        self.limpiar()
        print("========================================")
        print(f"=== {texto.center(30)} ===")
        print("========================================\n")

    def limpiar(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pausar(self):
        input("\nPresione Enter para continuar...")

    # ============================================================
    # CREAR GERENTE INICIAL
    # ============================================================
    def crear_gerente_inicial(self):
        self.titulo("Crear Gerente Inicial")
        while True:
            while True:
                run = input("RUN: ").strip()
                try:
                    run_normalizado = normalizar_run(run)
                except:
                    print("RUN inválido. Use formato 12345678-9.")
                if validar_run_chileno(run_normalizado):
                    run= run_normalizado
                    break
                else:
                    print("RUN invalido, ingresar un RUN valido...")
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            contrasena = pwinput.pwinput("Contraseña: ", mask="*")
            contrasena2 = pwinput.pwinput("Repetir Contraseña: ", mask="*")
            res = self.ctrl_empleados.crear_empleado(
                run_input=run,
                nombre=nombre,
                apellido=apellido,
                cargo="Gerente",
                contrasena=contrasena,
                contrasena2=contrasena2
            )
            print(res["mensaje"])
            if res["ok"]:
                op = input("¿Desea agregar otro USUARIO? (Y/N): ").strip().lower()
                if op == "y":
                    self.titulo("Crear Gerente Inicial")
                    continue
                else:
                    break
            else:
                print("Intentemos nuevamente...")
        self.pausar()

    # ============================================================
    # LOGIN
    # ============================================================
    def login(self):
        self.titulo("LOGIN")
        for _ in range(3):
            while True:
                run = input("RUN: ").strip()
                try:
                    run_normalizado = normalizar_run(run)
                except:
                    print("RUN inválido. Use formato 12345678-9.")
                    continue
                if validar_run_chileno(run_normalizado):
                    run = run_normalizado
                    break
                else:
                    print("RUN inválido. Use formato 12345678-9.")
            contrasena = pwinput.pwinput("Contraseña: ", mask="*")
            res = self.ctrl_empleados.login(run, contrasena)
            if res["ok"]:
                print(res["mensaje"])
                self.pausar()
                return res["empleado"]
            print("❌", res["mensaje"])
        print("❌ Máximo de intentos alcanzado.")
        return None

    # ============================================================
    # MENU EMPLEADO
    # ============================================================
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
            self.titulo("MENÚ PRINCIPAL")
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

    # ============================================================
    # MENU CLIENTE
    # ============================================================
    def flujo_cliente(self):
        while True:
            self.titulo("Menú Cliente")
            print("1) Ver vehículos disponibles")
            print("0) Volver")
            op = input("Opción: ").strip()
            if op == "1":
                self.listar_disponibles()
                self.pausar()
            elif op == "0":
                break
            else:
                print("Opción inválida.")
                self.pausar()

    # ============================================================
    # MENU PRINCIPAL INICIO
    # ============================================================
    def menu_principal(self):
        while True:
            self.titulo("Bienvenido a Rentacar")
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

    # ============================================================
    # EMPLEADOS
    # ============================================================
    def menu_empleados(self):
        while True:
            self.titulo("Gestión de Empleados")
            print("1) Crear empleado")
            print("2) Listar empleados")
            print("3) Eliminar empleado")
            print("4) Editar empleado")
            print("0) Volver")
            op = input("Opción: ")

            if op == "1": self.crear_empleado()
            elif op == "2": self.listar_empleados()
            elif op == "3": self.eliminar_empleado()
            elif op == "4": self.editar_empleado()
            elif op == "0": break
            else:
                print("❌ Opción inválida.")

    def crear_empleado(self):
        self.titulo("Crear Empleado")
        while True:
            print("[0] Volver")
            run = input("RUN: ").strip()
            if run == "0":
                input("Enter para continuar...")
                return
            try:
                run_n = normalizar_run(run)
            except:
                print("RUN inválido. Use formato 12345678-9.")
                continue
            if validar_run_chileno(run_n):
                run = run_n
                break
            else:
                print("RUN inválido. Use formato 12345678-9.")
                continue

        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        cargo = input("Cargo (Gerente/Ejecutivo): ").title().strip()
        c1 = pwinput.pwinput("Contraseña: ", mask="*")
        c2 = pwinput.pwinput("Repetir contraseña: ", mask="*")
        res = self.ctrl_empleados.crear_empleado(
            run_input=run,
            nombre=nombre,
            apellido=apellido,
            cargo=cargo,
            contrasena=c1,
            contrasena2=c2
        )

        print(res["mensaje"])
        self.pausar()

    def listar_empleados(self):
        self.titulo("Listado de Empleados")
        empleados = self.ctrl_empleados.listar_empleados()
        if not empleados:
            print("No hay empleados.")
        else:
            for e in empleados:
                d = e.obtener_datos()
                print(f"[{d.id}] | {d.nombre} {d.apellido} | {d.run} | Cargo: {d.cargo}")
        self.pausar()

    def eliminar_empleado(self):
        self.titulo("Eliminar Empleado")
        empleados = self.ctrl_empleados.listar_empleados()
        if not empleados:
            print("No hay empleados registrados.")
            self.pausar()
            return
        for e in empleados:
            d = e.obtener_datos()
            print(f"[{d.id}] | {d.nombre} {d.apellido}")
        print("[0] Volver")
        while True:
            emp_id = input("ID empleado: ").strip()
            if emp_id == "0":
                return
            if not emp_id.isdigit():
                print("Error: Debe ingresar un número válido.")
                continue
            emp_id = int(emp_id)
            existe = any(e.obtener_datos().id == emp_id for e in empleados)
            if not existe:
                print("❌ ID no encontrado. Seleccione uno de la lista.")
                continue
            print(f"\n¿Seguro que desea eliminar a:")
            print(f"   {d.nombre} {d.apellido} (RUN {d.run}) ?")
            confirmar = input("Ingrese Y para confirmar, N para cancelar: ").strip().lower()
            if confirmar != "y":
                print("❌ Eliminación cancelada.")
                self.pausar()
                return
            res = self.ctrl_empleados.eliminar_empleado(emp_id)
            print(res["mensaje"])
            self.pausar()
            return

    def editar_empleado(self):
        self.titulo("Editar Empleado")
        empleados = self.ctrl_empleados.listar_empleados()
        if not empleados:
            print("No hay empleados.")
            self.pausar()
            return
        for e in empleados:
            d = e.obtener_datos()
            print(f"[{d.id}] {d.nombre} {d.apellido} | {d.run} | Cargo: {d.cargo}")
        print("[0] Volver\n")
        try:
            emp_id = int(input("ID empleado: ").strip())
            if emp_id == 0:
                return
        except:
            print("ID inválido.")
            self.pausar()
            return
        empleado = None
        for e in empleados:
            if e.obtener_datos().id == emp_id:
                empleado = e
                break
        if empleado is None:
            print("ID no encontrado.")
            self.pausar()
            return
        datos = empleado.obtener_datos()
        print("\n*** Dejar vacío para mantener el valor actual ***\n")
        nuevo_nombre = input(f"Nuevo nombre ({datos.nombre}): ").strip() or datos.nombre
        nuevo_apellido = input(f"Nuevo apellido ({datos.apellido}): ").strip() or datos.apellido
        nuevo_cargo = input(f"Nuevo cargo ({datos.cargo}) [Gerente/Ejecutivo]: ").strip().title()
        if nuevo_cargo == "":
            nuevo_cargo = datos.cargo
        cambio_pass = input("¿Cambiar contraseña? (Y/N): ").strip().lower()
        if cambio_pass == "y":
            c1 = pwinput.pwinput("Nueva contraseña: ", mask="*")
            c2 = pwinput.pwinput("Repetir contraseña: ", mask="*")
        else:
            c1 = None
            c2 = None
        print("\n¿Confirmar cambios? (Y/N): ")
        confirmar = input().strip().lower()
        if confirmar != "y":
            print("Edición cancelada.")
            self.pausar()
            return
        res = self.ctrl_empleados.editar_empleado(
            emp_id,
            nuevo_nombre,
            nuevo_apellido,
            nuevo_cargo,
            c1,
            c2
        )
        print(res["mensaje"])
        self.pausar()

    # ============================================================
    # CLIENTES
    # ============================================================
    def menu_clientes(self):
        while True:
            self.titulo("Gestión de Clientes")
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
            else:
                print("❌ Opción inválida.")

    def crear_cliente(self):
        self.titulo("Crear Cliente")
        while True:
            run = input("RUN: ").strip()
            try:
                run_normalizado = normalizar_run(run)
            except:
                print("RUN inválido. Use formato 12345678-9.")
                continue
            if validar_run_chileno(run_normalizado):
                run = run_normalizado
                break
            else:
                print("RUN inválido. Use formato 12345678-9.")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        direccion = input("Dirección: ")
        while True:
            telefono = input("Teléfono: ")
            if validar_telefono(telefono):
                break
            print("Teléfono inválido. Use solo números y prefijo + (opcional).")
        res = self.ctrl_clientes.crear_cliente(run, nombre, apellido, direccion, telefono)
        print(res["mensaje"])
        self.pausar()

    def listar_clientes(self):
        self.titulo("Listado de Clientes")
        clientes = self.ctrl_clientes.listar_clientes()
        if not clientes:
            print("No hay clientes.")
        else:
            for c in clientes:
                d = c.obtener_datos()
                print(f"[{d.id}] {d.run} - {d.nombre} {d.apellido} | Tel: {d.telefono}")
        self.pausar()

    def editar_cliente(self):
        self.titulo("Editar Cliente")
        clientes = self.ctrl_clientes.listar_clientes()
        if not clientes:
            print("No hay clientes registrados...")
            self.pausar
            return
        self.titulo("Editar Cliente")
        for c in clientes: 
            d= c.obtener_datos()
            print(f"[{d.id}] {d.run} - {d.nombre} {d.apellido}")
        print("[0] Volver")
        try:
            cid = int(input("ID Cliente: "))
            if cid == 0:
                return
        except:
            print("ID Invalido")
            self.pausar()
            return
        self.limpiar
        print("Deja en blanco el dato que NO desea modificar...")
        nombre = input("Nuevo nombre: ") or None
        apellido = input("Nuevo apellido: ") or None
        direccion = input("Nueva dirección: ") or None
        telefono = input("Nuevo teléfono: ") or None
        res = self.ctrl_clientes.editar_cliente(cid, nombre, apellido, direccion, telefono)
        print(res["mensaje"])
        self.pausar()

    def eliminar_cliente(self):
        self.titulo("Eliminar Cliente")
        clientes = self.ctrl_clientes.listar_clientes()
        if not clientes:
            print("No hay clientes.")
            self.pausar()
            return
        for c in clientes:
            d = c.obtener_datos()
            print(f"[{d.id}] {d.run} - {d.nombre} {d.apellido}")
        print("[0] Volver")
        try:
            cid = int(input("ID cliente: "))
            if cid == 0:
                return
        except:
            print("ID inválido.")
            return
        confirmar = input("¿Seguro que desea eliminar este cliente? (Y/N): ").strip().lower()
        if confirmar != "y":
            print("Operación cancelada.")
            self.pausar()
            return
        res = self.ctrl_clientes.eliminar_cliente(cid)
        print(res["mensaje"])
        self.pausar()

    # ============================================================
    # VEHÍCULOS
    # ============================================================
    def menu_vehiculos(self):
        while True:
            self.titulo("Gestión de Vehículos")
            print("1) Crear vehículo")
            print("2) Listar vehículos")
            print("3) Listar disponibles")
            print("4) Editar vehiculos")
            print("0) Volver")
            op = input("Opción: ")

            if op == "1": self.crear_vehiculo()
            elif op == "2": self.listar_vehiculos()
            elif op == "3": self.listar_disponibles()
            elif op == "4": self.editar_vehiculo()
            elif op == "0": break
            else: print("❌ Opción inválida.")

    def crear_vehiculo(self):
    
        self.titulo("Crear Vehículo")
        while True: 
            print("[0] Volver")
            patente = input("Patente: ").upper()
            if patente == "0":
                return
            if len(patente) < 0:
                print("Patente invalida, intente nuevamente...")
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
            self.pausar()
            return
        
    def listar_vehiculos(self):
        self.titulo("Listado de Vehículos")
        vehiculos = self.ctrl_vehiculos.listar_vehiculos()
        if not vehiculos:
            print("No hay vehículos.")
        else:
            for v in vehiculos:
                d = v.obtener_datos()
                print(f"[{d.id}] {d.patente} | {d.marca} {d.modelo} | Año {d.anio} | UF/dia {d.precio_diario_uf}")
        self.pausar()

    def listar_disponibles(self):
        self.titulo("Vehículos Disponibles")
        vehiculos = self.ctrl_vehiculos.listar_vehiculos(disponibles=True)
        if not vehiculos:
            print("No hay disponibles.")
        else:
            for v in vehiculos:
                d = v.obtener_datos()
                print(f"[{d.id}] {d.patente} | {d.marca} {d.modelo}")
        self.pausar()

    def editar_vehiculo(self):
        self.titulo("Editar Vehículo")
        vehiculos = self.ctrl_vehiculos.listar_vehiculos()
        if not vehiculos:
            print("No hay vehículos registrados.")
            self.pausar()
            return
        for v in vehiculos:
            d = v.obtener_datos()
            print(f"[{d.id}] {d.patente} | {d.marca} {d.modelo} | Año {d.anio}")
        print("\n[0] Volver")
        while True:
            vid_input = input("ID del vehículo a editar: ").strip()
            if vid_input == "0":
                return  
            if not vid_input.isdigit():
                print("❌ ID inválido. Debe ser un número entero.")
                continue
            vid = int(vid_input)
            vehiculo = self.ctrl_vehiculos.buscar_por_id(vid)
            if vehiculo is None:
                print("❌ No existe un vehículo con ese ID.")
                continue
            break
        d = vehiculo.obtener_datos()
        print("\n--- Nuevos datos (ENTER para mantener el valor actual) ---")
        marca = input(f"Marca ({d.marca}): ").strip() or d.marca
        modelo = input(f"Modelo ({d.modelo}): ").strip() or d.modelo
        while True:
            anio_input = input(f"Año ({d.anio}): ").strip()
            if anio_input == "":
                anio = d.anio
                break
            if anio_input.isdigit():
                anio = int(anio_input)
                break
            print("❌ El año debe ser un número válido.")
        while True:
            precio_input = input(f"Precio UF/día ({d.precio_diario_uf}): ").strip()
            if precio_input == "":
                precio = d.precio_diario_uf
                break
            try:
                precio = float(precio_input)
                break
            except:
                print("❌ El precio debe ser un número.")
        confirmar = input("¿Confirmar cambios? (Y/N): ").strip().lower()
        if confirmar != "y":
            print("Edición cancelada.")
            self.pausar()
            return
        res = self.ctrl_vehiculos.editar_vehiculo(
            vid, marca, modelo, anio, precio
        )
        print(res["mensaje"])
        self.pausar()

    # ============================================================
    # ARRIENDOS
    # ============================================================
    def menu_arriendos(self, empleado):
        while True:
            self.titulo("Gestión de Arriendos")
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
        while True:
            self.titulo("Crear Arriendo")
            clientes = self.ctrl_clientes.listar_clientes()
            if not clientes:
                print("No hay clientes registrados. Debe crear uno primero.")
                return self.pausar()
            print("\n--- Seleccionar Cliente ---")
            for c in clientes:
                d = c.obtener_datos()
                print(f"[{d.id}] {d.run} - {d.nombre} {d.apellido}")
            print("[0] Volver")
            while True:
                cid = input("ID Cliente: ").strip()
                if cid == "0":
                    return
                if not cid.isdigit():
                    print("❌ ID inválido. Debe ser un número.")
                    continue
                cid = int(cid)
                cliente = self.ctrl_clientes.buscar_por_id(cid)
                if not cliente:
                    print("❌ No existe un cliente con ese ID.")
                    continue
                break

            self.titulo("Crear Arriendo")
            print("\n--- Seleccionar Vehículo Disponible ---")
            vehiculos = self.ctrl_vehiculos.listar_vehiculos(disponibles=True)
            if not vehiculos:
                print("No hay vehículos disponibles.")
                return self.pausar()
            for v in vehiculos:
                d = v.obtener_datos()
                print(f"[{d.id}] {d.patente} | {d.marca} {d.modelo}")
            print("[0] Volver")
            while True:
                vid = input("ID Vehículo: ").strip()
                if vid == "0":
                    return
                if not vid.isdigit():
                    print("❌ ID inválido. Debe ser un número.")
                    continue
                vid = int(vid)
                vehiculo = self.ctrl_vehiculos.buscar_por_id(vid)
                if not vehiculo:
                    print("❌ No existe un vehículo con ese ID.")
                    continue
                break

            self.titulo("Crear Arriendo")
            print("\n--- Ingreso de Fechas (AAAA-MM-DD) ---")
            while True:
                f1 = input("Fecha Inicio: ").strip()
                f2 = input("Fecha Fin: ").strip()
                try:
                    fecha_inicio = datetime.strptime(f1, "%Y-%m-%d")
                    fecha_fin = datetime.strptime(f2, "%Y-%m-%d")
                    if fecha_fin < fecha_inicio:
                        print("❌ La fecha fin no puede ser antes que la fecha inicio.")
                        continue
                    break
                except ValueError:
                    print("❌ Formato inválido. Use AAAA-MM-DD.")
                    continue
            res = self.ctrl_arriendos.crear_arriendo(
                empleado, vid, cid, fecha_inicio, fecha_fin
            )
            print("\n" + res["mensaje"])
            if res["ok"]:
                d = res["data"]
                print(f"Días Totales: {d['dias']}")
                print(f"UF Total: {d['total_uf']:.2f}")
                print(f"CLP Total: ${d['total_clp']:,.0f}")
            self.pausar()
            return

    def listar_arriendos(self):
        self.titulo("Listado de Arriendos")
        arriendos = self.ctrl_arriendos.listar_arriendos()
        if not arriendos:
            print("No hay arriendos registrados.")
            self.pausar()
            return
        hoy = date.today()
        print("ID | Cliente | Vehículo | Fechas | Estado | Total")
        print("-" * 95)
        for a in arriendos:
            cliente = f"{a.cliente_nombre} {a.cliente_apellido}"
            vehiculo = f"{a.vehiculo_marca} {a.vehiculo_modelo}"
            fechas = f"{a.fecha_inicio.date()} → {a.fecha_fin.date()}"
            estado = "EXPIRADO" if a.fecha_fin.date() < hoy else "VIGENTE"
            total = f"{a.total_uf:.2f} UF | ${a.total_clp:,}"
            print(f"{a.id} | {cliente} | {vehiculo} | {fechas} | {estado} | {total}")
        self.pausar()

    def cancelar_arriendo(self):
        self.limpiar()
        self.titulo("Cancelar Arriendo")
        arriendos = self.ctrl_arriendos.listar_arriendos()
        if not arriendos:
            print("No hay arriendos registrados.")
            self.pausar()
            return
        print("ID | Cliente | Vehículo | Estado")
        print("-" * 70)
        for a in arriendos:
            d = a.obtener_datos()
            print(f"{d['id']} | {d['cliente']} | {d['vehiculo']} | {d['estado']}")
        print("\n0) Volver")

        while True:
            op = input("ID Arriendo a cancelar: ").strip()
            if op == "0":
                return
            if not op.isdigit():
                print("❌ Debe ingresar un número.")
                continue
            aid = int(op)
            arriendo = self.ctrl_arriendos.buscar_por_id(aid)
            if not arriendo:
                print("❌ No existe un arriendo con ese ID.")
                continue
            break
        confirmar = input("¿Confirmar cancelación? (Y/N): ").strip().lower()
        if confirmar != "y":
            print("Cancelado.")
            self.pausar()
            return
        res = self.ctrl_arriendos.cancelar_arriendo(aid)
        print(res["mensaje"])
        self.pausar()

