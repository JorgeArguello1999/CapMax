from datetime import datetime

def get_valid_dates(dates):
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