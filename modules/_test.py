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

    results = []

    for i in range(0, 22):
        with open(f'../test/test_{i}.jpg.txt', 'r') as file:
            file = file.read()
        
        ruc_detect = tcr.rucs_detects(file)
        date_detec = tcr.date_detect(file)
        total_v = tcr.total_value_detect(file)
        factura_n = tcr.invoice_number(file)

        total_rucs_detected += len(ruc_detect)
        total_dates_detected += len(date_detec)
        total_values_detected += len(total_v)

        response = "🤔" 
        if ruc_detect and date_detec and total_v:
            response = "✅"
        elif not ruc_detect and not date_detec and not total_v:
            response = "❌"

        # Guardar el resultado para la tabla
        results.append([
            i,
            colorize_response(response),
            ruc_detect,
            date_detec,
            total_v,
            factura_n,
        ])

        if response == "❌": 
            count_bad += 1
        elif response == "✅": 
            count_good += 1
        else: 
            count_maybe += 1

    # Imprimir los resultados en forma de tabla
    headers = ["Test", "Resultado", "RUC", "Fechas", "Valores", "# Factura"]
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
    print(f"Promedio de RUCs detectados por archivo: {total_rucs_detected / 22:.2f}")
    print(f"Promedio de fechas detectadas por archivo: {total_dates_detected / 22:.2f}")
    print(f"Promedio de valores detectados por archivo: {total_values_detected / 22:.2f}")
