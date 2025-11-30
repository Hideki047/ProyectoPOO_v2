from modelos.base_datos import conectar
from controladores.dto.empleado_dto import EmpleadoDTO

class EmpleadoDAO:
    def __init__(self):
        pass

    def crear(self, dto: EmpleadoDTO):
        con = conectar()
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO empleados (run, nombre, apellido, cargo, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                dto.run,
                dto.nombre,
                dto.apellido,
                dto.cargo,
                dto.hash_contrasena))
            con.commit()
            return True
        except Exception as e:
            print("ERROR EMPLEADO_DAO CREAR:", e)
            return False
        finally:
            cur.close()
            con.close()

    def listar(self):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM empleados")
        rows = cur.fetchall()
        cur.close()
        con.close()
        return [
            EmpleadoDTO(
                id=f[0],
                run=f[1],
                nombre=f[2],
                apellido=f[3],
                cargo=f[4],
                hash_contrasena=f[5],
                creado_en=f[6]           
            )
            for f in rows
        ]

    def contar(self):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM empleados")
        cantidad = cur.fetchone()[0]
        cur.close()
        con.close()
        return cantidad

    def buscar_por_run(self, run):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM empleados WHERE run = %s", (run,))
        row = cur.fetchone()
        cur.close()
        con.close()
        if not row:
            return None
        return EmpleadoDTO(
            id=row[0],
            run=row[1],
            nombre=row[2],
            apellido=row[3],
            cargo=row[4],
            hash_contrasena=row[5],
            creado_en=row[6]            
        )

    def eliminar(self, empleado_id):
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM empleados WHERE id = %s", (empleado_id,))
        filas_afectadas = cur.rowcount
        con.commit()
        cur.close()
        con.close()
        return filas_afectadas > 0

    def editar(self, dto: EmpleadoDTO):
        con = conectar()
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE empleados
                SET nombre=%s, apellido=%s, cargo=%s, password_hash=%s
                WHERE id=%s
            """, (dto.nombre, dto.apellido, dto.cargo, dto.hash_contrasena, dto.id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            print("ERROR DAO EDITAR:", e)
            return False
        finally:
            cur.close()
            con.close()

    def buscar_por_id(self, emp_id):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM empleados WHERE id = %s", (emp_id,))
        row = cur.fetchone()
        cur.close()
        con.close()
        if not row:
            return None
        return EmpleadoDTO(
            id=row[0],
            run=row[1],
            nombre=row[2],
            apellido=row[3],
            cargo=row[4],
            hash_contrasena=row[5],
            creado_en=row[6]
        )
            


