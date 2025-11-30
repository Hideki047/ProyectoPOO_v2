from modelos.base_datos import conectar
from controladores.dto.vehiculo_dto import VehiculoDTO


class VehiculoDAO:
    def __init__(self):
        pass

    def crear(self, dto: VehiculoDTO):
        con = conectar()
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO vehiculos (patente, marca, modelo, anio, precio_diario_uf, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                dto.patente,
                dto.marca,
                dto.modelo,
                dto.anio,
                dto.precio_diario_uf,
                dto.estado
            ))
            con.commit()
            return True
        except Exception as e:
            print("ERROR VEHICULO_DAO CREAR:", e)
            return False
        finally:
            cur.close()
            con.close()

    def listar(self, disponibles=None):
        con = conectar()
        cur = con.cursor()
        if disponibles is True:
            cur.execute("SELECT * FROM vehiculos WHERE estado = 'DISPONIBLE'")
        else:
            cur.execute("SELECT * FROM vehiculos")
        rows = cur.fetchall()
        cur.close()
        con.close()
        return [
            VehiculoDTO(
                id=r[0],
                patente=r[1],
                marca=r[2],
                modelo=r[3],
                anio=r[4],
                precio_diario_uf=r[5],
                estado=r[6]
            ) for r in rows
        ]

    def buscar_por_id(self, id_vehiculo):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM vehiculos WHERE id = %s", (id_vehiculo,))
        r = cur.fetchone()
        cur.close()
        con.close()
        if not r:
            return None
        return VehiculoDTO(
            id=r[0],
            patente=r[1],
            marca=r[2],
            modelo=r[3],
            anio=r[4],
            precio_diario_uf=r[5],
            estado=r[6]
        )

    def buscar_por_patente(self, patente):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM vehiculos WHERE patente = %s", (patente,))
        r = cur.fetchone()
        cur.close()
        con.close()
        if not r:
            return None
        return VehiculoDTO(
            id=r[0],
            patente=r[1],
            marca=r[2],
            modelo=r[3],
            anio=r[4],
            precio_diario_uf=r[5],
            estado=r[6]
        )

    def actualizar_estado(self, id_vehiculo, nuevo_estado):
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE vehiculos SET estado = %s WHERE id = %s """, (nuevo_estado, id_vehiculo))
        con.commit()
        cur.close()
        con.close()
        return True

    def editar(self, vehiculo_id, marca, modelo, anio, precio):
        con = conectar()
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE vehiculos
                SET marca=%s, modelo=%s, anio=%s, precio_diario_uf=%s
                WHERE id=%s
            """, (marca, modelo, anio, precio, vehiculo_id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            print("ERROR DAO EDITAR VEHÍCULO:", e)
            return False
        finally:
            cur.close()
            con.close()

    def buscar_por_id(self, vehiculo_id):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM vehiculos WHERE id = %s", (vehiculo_id,))
        row = cur.fetchone()
        cur.close()
        con.close()
        if not row:
            return None
        return VehiculoDTO(
            id=row[0],
            patente=row[1],
            marca=row[2],
            modelo=row[3],
            anio=row[4],
            precio_diario_uf=row[5],
            estado=row[6]
        )

