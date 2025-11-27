class EmpleadoDTO:
    def __init__(self, id=None, codigo=None, run=None, nombre=None, apellido=None, cargo=None, creado_en=None, hash_contrasena=None):
        self.id = id
        self.codigo = codigo
        self.run = run
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.creado_en = creado_en
        self.hash_contrasena = hash_contrasena
