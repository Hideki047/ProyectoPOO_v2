from modelos.base_datos import conectar
from controladores.dto.cliente_dto import ClienteDTO


class ClienteDAO:
    def __init__(self):
        pass

    def crear(self, dto: ClienteDTO):
        con = conectar()
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO clientes (run, nombre, apellido, direccion, telefono)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                dto.run,
                dto.nombre,
                dto.apellido,
                dto.direccion,
                dto.telefono
            ))
            con.commit()
            return True
        except Exception as e:
            print("ERROR CLIENTE_DAO CREAR:", e)
            return False
        finally:
            cur.close()
            con.close()

    def listar(self):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM clientes")
        rows = cur.fetchall()
        cur.close()
        con.close()

        return [
            ClienteDTO(
                id=r[0],
                run=r[1],
                nombre=r[2],
                apellido=r[3],
                direccion=r[4],
                telefono=r[5]
            ) for r in rows
        ]

    def buscar_por_run(self, run):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM clientes WHERE run = %s", (run,))
        r = cur.fetchone()
        cur.close()
        con.close()

        if not r:
            return None

        return ClienteDTO(
            id=r[0],
            run=r[1],
            nombre=r[2],
            apellido=r[3],
            direccion=r[4],
            telefono=r[5]
        )

    def buscar_por_id(self, cliente_id):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
        r = cur.fetchone()
        cur.close()
        con.close()

        if not r:
            return None

        return ClienteDTO(
            id=r[0],
            run=r[1],
            nombre=r[2],
            apellido=r[3],
            direccion=r[4],
            telefono=r[5]
        )

    def actualizar(self, dto: ClienteDTO):
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE clientes
            SET nombre = %s, apellido = %s, direccion = %s, telefono = %s
            WHERE id = %s
        """, (
            dto.nombre,
            dto.apellido,
            dto.direccion,
            dto.telefono,
            dto.id
        ))
        con.commit()
        cur.close()
        con.close()
        return True

    def eliminar(self, cliente_id):
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
        filas_afectadas = cur.rowcount
        con.commit()
        cur.close()
        con.close()
        return filas_afectadas > 0
