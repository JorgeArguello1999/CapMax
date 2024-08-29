from datetime import datetime

def get_valid_dates(dates:list) -> list:
    """
    Extract and format valid dates from a list of date strings.

    Parameters:
    dates (list of str): A list of date strings in various formats.

    Returns:
    list of str: A sorted list of unique valid dates formatted as "dd/mm/yyyy".
    """
    # List of possible date formats to try
    formats = ["%d/%m/%y", "%d/%m/%Y", "%d/%m/%y", "%d/%m/%Y", "%d/%m/%y"]
    valid_dates = []

    for date in dates:
        parsed = False
        for format in formats:
            try:
                # Attempt to parse the date string using the current format
                parsed_date = datetime.strptime(date, format)

                # Format the parsed date to "dd/mm/yyyy" and add it to the valid dates list
                valid_dates.append(parsed_date.strftime("%d/%m/%Y"))
                parsed = True

                break

            except ValueError:
                # Continue to the next format if the current format does not match
                continue

        if not parsed:
            print(f"Invalid date: {date}")

    # Remove duplicates, sort the list, and return the result
    return sorted(set(valid_dates))

def ordenar_fechas(fechas:list) -> list:
    try:
        # Convertir las fechas a objetos datetime
        fechas_datetime = [datetime.strptime(fecha, "%d-%m-%Y") for fecha in fechas]

        # Ordenar las fechas
        fechas_ordenadas = sorted(fechas_datetime)

        # Convertir las fechas de vuelta a strings
        fechas_ordenadas_str = [fecha.strftime("%d-%m-%Y") for fecha in fechas_ordenadas]
    
    except Exception as e:
        fechas_ordenadas_str = []
        print(e)

    return fechas_ordenadas_str
