from datetime import date

class Arriendo:
    def __init__(self, dto):
        self.id = dto.id
        self.vehiculo_id = dto.vehiculo_id
        self.cliente_id = dto.cliente_id
        self.empleado_id = dto.empleado_id
        self.fecha_inicio = dto.fecha_inicio
        self.fecha_fin = dto.fecha_fin
        self.total_uf = dto.total_uf
        self.total_clp = dto.total_clp
        self.estado = dto.estado

        # Datos adicionales por JOIN
        self.cliente_nombre = dto.cliente_nombre
        self.cliente_apellido = dto.cliente_apellido
        self.vehiculo_marca = dto.vehiculo_marca
        self.vehiculo_modelo = dto.vehiculo_modelo

    # -----------------------------
    #   Lógica de fechas
    # -----------------------------

    def expiro(self):
        """Devuelve True si la fecha_fin ya pasó."""
        # Convertimos fecha_fin a date si es datetime
        fin = self.fecha_fin.date() if hasattr(self.fecha_fin, "date") else self.fecha_fin
        hoy = date.today()
        return fin < hoy

    def obtener_estado(self):
        return "EXPIRADO" if self.expiro() else self.estado

    def puede_cancelarse(self, ahora):
        """
        Un arriendo es cancelable solo si:
        - Está vigente (no expirado)
        - Su estado actual no es 'CANCELADO'
        """
        # Si ya está cancelado → NO se puede cancelar
        if self.estado == "CANCELADO":
            return False

        # Si ya expiró → NO se puede cancelar
        if self.expiro():
            return False

        # Si la fecha de inicio ya pasó → NO se puede cancelar
        if self.fecha_inicio.date() <= ahora.date():
            return False

        return True


    def obtener_datos(self):
        return {
            "id": self.id,
            "cliente": f"{self.cliente_nombre} {self.cliente_apellido}",
            "vehiculo": f"{self.vehiculo_marca} {self.vehiculo_modelo}",

            "fecha_inicio": (
                self.fecha_inicio.date()
                if hasattr(self.fecha_inicio, "date")
                else self.fecha_inicio
            ),

            "fecha_fin": (
                self.fecha_fin.date()
                if hasattr(self.fecha_fin, "date")
                else self.fecha_fin
            ),

            "estado": self.obtener_estado(),
            "total_uf": self.total_uf,
            "total_clp": self.total_clp
        }
