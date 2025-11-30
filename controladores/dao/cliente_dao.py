from modelos.base_datos import conectar
from controladores.dto.cliente_dto import ClienteDTO

class ClienteDAO:
    def __init__(self):
        self.conn = conectar()

    def crear(self, dto: ClienteDTO):
        try:
            cur = self.conn.cursor()
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
            self.conn.commit()
            return True
        except Exception as e:
            print("ERROR CLIENTE_DAO CREAR:", e)
            return False
        finally:
            cur.close()

    def listar(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM clientes")
        rows = cur.fetchall()
        cur.close()
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
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM clientes WHERE run = %s", (run,))
        r = cur.fetchone()
        cur.close()
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
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
            r = cur.fetchone()
            cur.close()
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
        except Exception as e:
            print("ERROR CLIENTE_DAO buscar_por_id:", e)
            return None

    def actualizar(self, dto: ClienteDTO):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE clientes
            SET nombre=%s, apellido=%s, direccion=%s, telefono=%s
            WHERE id=%s
        """, (
            dto.nombre,
            dto.apellido,
            dto.direccion,
            dto.telefono,
            dto.id
        ))
        self.conn.commit()
        cur.close()
        return True

    def eliminar(self, cliente_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
        afectado = cur.rowcount
        self.conn.commit()
        cur.close()
        return afectado > 0
