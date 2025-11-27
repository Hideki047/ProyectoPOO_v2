from modelos.base_datos import conectar
from controladores.dto.arriendo_dto import ArriendoDTO


class ArriendoDAO:

    def crear(self, dto: ArriendoDTO):
        con = conectar()
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO arriendos (
                    vehiculo_id, cliente_id, empleado_id,
                    fecha_inicio, fecha_fin,
                    valor_uf, total_uf, total_clp, estado
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                dto.vehiculo_id,
                dto.cliente_id,
                dto.empleado_id,
                dto.fecha_inicio,
                dto.fecha_fin,
                dto.valor_uf,
                dto.total_uf,
                dto.total_clp,
                dto.estado,
            ))
            con.commit()
            return True
        except Exception as e:
            print("ERROR ARRIENDO_DAO CREAR:", e)
            return False
        finally:
            cur.close()
            con.close()

    def listar(self):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM arriendos")
        filas = cur.fetchall()
        cur.close()
        con.close()

        lista = []
        for f in filas:
            lista.append(ArriendoDTO(
                id=f[0],
                vehiculo_id=f[1],
                cliente_id=f[2],
                empleado_id=f[3],
                fecha_inicio=f[4],
                fecha_fin=f[5],
                valor_uf=f[6],
                total_uf=f[7],
                total_clp=f[8],
                estado=f[9],
            ))
        return lista

    def buscar_por_id(self, arriendo_id):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM arriendos WHERE id = %s", (arriendo_id,))
        f = cur.fetchone()
        cur.close()
        con.close()
        if not f:
            return None
        return ArriendoDTO(
            id=f[0],
            vehiculo_id=f[1],
            cliente_id=f[2],
            empleado_id=f[3],
            fecha_inicio=f[4],
            fecha_fin=f[5],
            valor_uf=f[6],
            total_uf=f[7],
            total_clp=f[8],
            estado=f[9],
        )

    def actualizar_estado(self, arriendo_id, nuevo_estado):
        con = conectar()
        cur = con.cursor()
        cur.execute("UPDATE arriendos SET estado = %s WHERE id = %s", (nuevo_estado, arriendo_id))
        con.commit()
        cur.close()
        con.close()
        return True
