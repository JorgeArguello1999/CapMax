from datetime import datetime

def get_valid_dates(dates: list) -> list:
    """
    Extract, format, and sort unique valid dates from a list of date strings.

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
        for date_format in formats:
            try:
                # Attempt to parse the date string using the current format
                parsed_date = datetime.strptime(date, date_format)

                # Format the parsed date to "dd/mm/yyyy" and add it to the valid dates list
                valid_dates.append(parsed_date.strftime("%d/%m/%Y"))
                parsed = True
                break

            except ValueError:
                # Continue to the next format if the current format does not match
                continue

        if not parsed:
            print(f"Invalid date: {date}")

    # Remove duplicates
    valid_dates = list(set(valid_dates))

    # Convert date strings to datetime objects for sorting
    try:
        date_objects = [datetime.strptime(date, "%d/%m/%Y") for date in valid_dates]
        # Sort the dates
        sorted_dates = sorted(date_objects)
        # Convert the dates back to strings
        sorted_dates_str = [date.strftime("%d/%m/%Y") for date in sorted_dates]
    except Exception as e:
        sorted_dates_str = []
        print(e)

    return sorted_dates_str