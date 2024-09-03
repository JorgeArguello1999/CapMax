import text_recognise as tcr
from tabulate import tabulate
from colorama import Fore, Style, init

# Inicializa colorama para la compatibilidad en todas las plataformas
init(autoreset=True)

def colorize_response(response):
    if response == "✅":
        return Fore.GREEN + response
    elif response == "❌":
        return Fore.RED + response
    else:
        return Fore.YELLOW + response

if __name__ == "__main__":

    count_bad = 0
    count_good = 0
    count_maybe = 0

    total_rucs_detected = 0
    total_dates_detected = 0
    total_values_detected = 0
    total_facture_detected = 0
    total_auth_facture_detected = 0

    results = []

    items = 26
    for i in range(0, items):
        try:
            with open(f'../test/test_{i}.jpg.txt', 'r') as file:
                file_content = file.read()

            ruc_detect = tcr.rucs_detects(file_content)
            date_detect = tcr.date_detect(file_content)
            total_v = tcr.total_value_detect(file_content)
            factura_n = tcr.invoice_number(file_content)
            auth_factura_n = tcr.auth_invoice_number(file_content)

            total_rucs_detected += len(ruc_detect) - list(ruc_detect.values()).count('')
            total_dates_detected += len(date_detect) if date_detect else 0
            total_values_detected += len(total_v)
            total_facture_detected += len(factura_n)
            total_auth_facture_detected += len(auth_factura_n)

            response = "🤔" 
            if all([ruc_detect["vendor"], date_detect, total_v, factura_n, auth_factura_n]):
                response = "✅"
            elif not any([ruc_detect["vendor"], date_detect, total_v, factura_n, auth_factura_n]):
                response = "❌"

            results.append([
                i,
                colorize_response(response),
                ruc_detect,
                date_detect or 'N/A',
                total_v or 'N/A',
                factura_n or 'N/A',
                auth_factura_n or 'N/A'
            ])

            if response == "❌": 
                count_bad += 1
            elif response == "✅": 
                count_good += 1
            else: 
                count_maybe += 1

        except Exception as e:
            print(f"Error procesando test_{i}: {str(e)}")
            continue

    # Imprimir los resultados en forma de tabla
    headers = ["Test", "Resultado", "RUC", "Fechas", "Valores", "# Factura", "Auth Factura"]
    print(tabulate(results, headers=headers, tablefmt="fancy_grid"))

    # Resumen general con colores
    print("\nResumen General:")
    print(Fore.GREEN + f"✅: {count_good} | Casos completamente detectados")
    print(Fore.YELLOW + f"🤔: {count_maybe} | Casos parcialmente detectados")
    print(Fore.RED + f"❌: {count_bad} | Casos no detectados")
    
    # Estadísticas adicionales
    print("\nEstadísticas Detalladas:")
    print(f"Total de RUCs detectados: {total_rucs_detected}")
    print(f"Total de fechas detectadas: {total_dates_detected}")
    print(f"Total de valores detectados: {total_values_detected}")
    print(f"Total de # facturas detectadas: {total_facture_detected}")
    print(f"Total de # Auth facturas detectadas: {total_auth_facture_detected}")
    print()
    print(f"Promedio de RUCS detectados por archivo: {(total_rucs_detected / (items * 2)) * 100:.2f}%")
    print(f"Promedio de fechas detectadas por archivo: {(total_dates_detected / items) * 100:.2f}%")
    print(f"Promedio de valores detectados por archivo: {(total_values_detected / items) * 100:.2f}%")
    print(f"Promedio de # facturas detectadas por archivo: {(total_facture_detected / items) * 100:.2f}%")
    print(f"Promedio de # Auth facturas detectadas por archivo: {(total_auth_facture_detected / items) * 100:.2f}%")