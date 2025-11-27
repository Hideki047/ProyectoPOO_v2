from datetime import timedelta

class Arriendo:
    def __init__(self, dto):
        self._dto = dto

    def puede_cancelarse(self, fecha_actual):
        delta = self._dto.fecha_inicio - fecha_actual
        return delta >= timedelta(hours=4)

    def obtener_id(self):
        return self._dto.id

    def obtener_datos(self):
        return self._dto
