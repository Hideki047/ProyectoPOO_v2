import hashlib
import re
import requests
from datetime import datetime


def calcular_hash_contrasena(contrasena: str) -> str:
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def verificar_contrasena(contrasena_plana: str, hash_contrasena: str) -> bool:
    return calcular_hash_contrasena(contrasena_plana) == hash_contrasena


def validar_run_chileno(run: str) -> bool:
    try:
        run_normalizado = normalizar_run(run)
    except ValueError:
        return False

    numero, dv = run_normalizado.split("-", maxsplit=1)
    dv_calculado = _calcular_dv(numero)
    return dv_calculado == dv


def _calcular_dv(numero: str) -> str:
    factores = [2, 3, 4, 5, 6, 7]
    suma = 0
    for i, digito in enumerate(reversed(numero)):
        suma += int(digito) * factores[i % len(factores)]
    resto = 11 - (suma % 11)
    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)


def validar_telefono(telefono: str) -> bool:
    return re.fullmatch(r"\+?\d{8,15}", telefono) is not None


def obtener_valor_uf(fecha: datetime) -> float:
    fecha_str = fecha.strftime("%d-%m-%Y")
    url = f"https://mindicador.cl/api/uf/{fecha_str}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        serie = data.get("serie", [])
        if not serie:
            raise ValueError("No hay datos de UF para la fecha indicada.")
        return float(serie[0]["valor"])
    except Exception as e:
        print(f"[ERROR API UF] {e}")
        while True:
            try:
                valor_manual = float(input("Ingrese valor UF manualmente: "))
                return valor_manual
            except ValueError:
                print("Valor invalido, intente nuevamente.")

def normalizar_run(run: str) -> str:
    if not run:
        raise ValueError("RUN vacío")
    run_limpio = run.replace(".", "").replace(" ", "").upper()
    if "-" in run_limpio:
        partes = run_limpio.split("-", maxsplit=1)
        if len(partes) != 2:
            raise ValueError("RUN con formato inválido.")
        numero, dv = partes
    else:
        if len(run_limpio) < 2:
            raise ValueError("RUN demasiado corto.")
        numero, dv = run_limpio[:-1], run_limpio[-1]
    if not numero.isdigit():
        raise ValueError("RUN inválido, el cuerpo debe ser numérico.")
    numero = str(int(numero))

    return f"{numero}-{dv}"

