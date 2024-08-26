import re

def buscar_campo(texto, campo):
    # Crear una expresión regular para buscar el valor del campo
    patron = rf"{campo}:\s*(\d+\.\d{{2}})"
    
    # Buscar el valor en el texto usando la expresión regular
    valor_match = re.search(patron, texto)
    
    # Si el valor no está en la misma línea, buscar en las siguientes líneas
    if not valor_match:
        valor_match = re.search(rf"{campo}:[\s\S]*?(\d+\.\d{{2}})", texto)
    
    # Obtener el valor encontrado o indicar que no se encontró
    return valor_match.group(1) if valor_match else "No encontrado"

# Supongamos que este es el texto extraído por OCR
extracted_text = """
O LIEME TOCO
AL
RED DE SERVICIOS
Facilito
Prostjo, company
(1286) CENTRO AUTORIZADO DE
RECAUDACION
20131 RUC-0992663235001
COMPROBANTE DE RECAUDACION CNT
COMPROBANTE - 20240813845585
FIJA.-TELEVISION-
MARIN-032894821
ARLOS MANUEL
RECAUDACION: UT 200OT INTERNET
TIPO
REFERENCIA:
032894822
VILLAFUERTE GAVILANES CARLOS
NOMBRE.
MANUEL
cha:
PUYO
Angelita Ortiz
AGENCIA:
COD. USUARIO:
SEC ADQ/SW:
128636 PUYO
10609
845585/789653
UUID: F1416D77-9EA2-4C83-A454-AA1D081796B4
FECHA HORA:
12/08/2024 16:34:47
CIUDAD:
PASTAZA
ARMA RUC: 160080
ELIA NATABEL NOTA DE VEN
001-001-
0002427
N°1131483094
VALOR TRANSACCION:
7.15
COMISION:
0.00
TOTAL:
7.15
MENSAJE:
TRANSACCION OK
OPERADO POR: RED DE SERVICIOS FACILITO
ESCANEA Y PARTICIPA EN EL BORTED DE UN
PAGO DE PLANILLA
TAMBIÉN PUEDES ACCEDER DESDE
NEGALI
ADA TU PLANLA
*APLICAN TEAMUNDE Y CONDICIONES
EN ESTA VENTANILLA COBRA TUS GIROS
CIS @ W Western Union
expre 55
"""

# Usar la función para buscar "VALOR TRANSACCION" y "TOTAL"
valor_transaccion = buscar_campo(extracted_text, "REFERENCIA")
total = buscar_campo(extracted_text, "TOTAL")

# Imprimir los resultados
print(f"ciudad: {valor_transaccion}")
print(f"Total: {total}")
