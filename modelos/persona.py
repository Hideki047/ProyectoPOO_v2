
class Persona:
    def __init__(self, run, nombre, apellido):
        self._run = run
        self._nombre = nombre
        self._apellido = apellido

    def obtener_run(self):
        return self._run

    def obtener_nombre(self):
        return self._nombre

    def obtener_apellido(self):
        return self._apellido

    def asignar_run(self, run):
        self._run = run

    def asignar_nombre(self, nombre):
        self._nombre = nombre

    def asignar_apellido(self, apellido):
        self._apellido = apellido

    def nombre_completo(self):
        return f"{self._nombre} {self._apellido}"







