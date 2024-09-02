# Modules
import re 

# Own modules
try:
    import validate_date as vd
except: 
    from modules import validate_date as vd


""" 
Recognize differents items, depends that you need
"""

def rucs_detects(text: str = "") -> dict:
    """RUC Detect
    RUC is an item with 10 or 13 numbers.
    This function is only for Ecuador Country.
    
    Keyword arguments:
    text: (str) All text for recognition.
    Return: (dict) {
        'vendor': int,
        'client': int
    }.
    """
    # Clean data from letters, spaces or symbols 
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub('\n', '', text)

    # RUC from provider or customer is usually on the first part
    large = len(text) // 3
    text = text[:large * 2]

    # REGEX items with 10-13 characters length
    items_10_13 = re.findall(r'\d{10,13}', text) 

    prefix = [f'0{i}' for i in range(1, 10)] + [f'{i}' for i in range(11, 25)] + ['88', '90']
    suffix = '001'

    # Classify Items with 10 or 13 
    results = [ x for x in items_10_13 if (
        (len(x) == 10 or len(x) == 13) and 
        (x.startswith(tuple(prefix)) and x.endswith(suffix))
    )]

    # Eliminate duplicates while maintaining order
    seen = set()
    results = [item for item in results if (
        item not in seen and not seen.add(item)
    )]

    results.extend([''] * (2 - len(results)))

    return {
        "vendor": results[0],
        "client": results[1]
    }

def date_detect(text: str) -> str:
    """Date detect
    This function extracts date fields from text.

    Keyword arguments:
    text: (str) All text from the photo
    Return: (list) Items with date
    """
    # Clean spaces from data
    text = re.sub('\n', ' ', text)

    # Unified regex pattern for various date formats
    regex = r'\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|\d{1,2}[-/.][a-zA-Z]{3}[-/.]\d{2,4})\b'
    
    # Find all matching date patterns
    results = re.findall(regex, text)
    
    # Replace dashes and dots with slashes for standardization
    results = [re.sub(r'[-.]', '/', result) for result in results]
    
    # ReFormat dates
    results = vd.get_valid_dates(list(set(results)))

    # Most Recent dates filter
    results = vd.get_most_recent_date(list(set(results)))

    return results

def total_value_detect(text: str) -> list:
    """
    Search for the total value in a given text.

    Parameters:
    text (str): The text in which to search for the total value.

    Returns:
    list: A list containing the highest detected total value, 
    or an empty list if no valid total value is found.
    """

    # Normalize the text by converting it to uppercase
    text = text.upper()

    # Regular expression pattern to match "TOTAL" followed by an optional currency symbol and a numeric value
    regex = r"\bTOTAL\b\s*\$?\s*([\d,\.]+)"

    # Find all matches of the pattern in the text
    results = re.findall(regex, text)

    # Replace commas with dots to standardize decimal points
    results = [result.replace(',', '.') for result in results]

    # Convert all detected values to float, or 0.0 if conversion fails
    results = [
        float(result) if result.replace('.', '', 1).isdigit() else 0.0
        for result in results
    ]

    # Sort the results in descending order
    results = sorted(results, reverse=True)

    # Return the highest value or an empty list if no values are found
    return results[:1] if results else []

def invoice_number(text: str) -> list:
    """Extracts potential invoice numbers from the text
    
    Args:
        text (str): All text from photo
    
    Returns:
        list: A list of unique Invoice numbers found.
    """
    # Clean the text
    text_cleaned = re.sub(r'\n', ' ', text)
    text_cleaned = re.sub(' ', '-', text_cleaned)
    text_cleaned = re.sub(r'\D', '-', text_cleaned)

    # Work with the first two-thirds of the text
    large = len(text) // 3
    sub_text = text[:large * 2]

    # Find 6-7 digits with 3-4 leading zeros
    regex_6_7_digits = r'\b0{3,4}[1-9]\d{2,5}\b'
    results_one = re.findall(regex_6_7_digits, sub_text)

    # If no results found, search for 9 digits with 3-6 leading zeros
    if not results_one:
        regex_9_digits = r'\b0{3,6}[1-9]\d{2,5}\b'
        results_two = re.findall(regex_9_digits, sub_text)
    else:
        results_two = []

    # Combine results and remove duplicates
    results = list(set(results_one + results_two))

    # Return the results
    return [results[0]] if results else []

def auth_invoice_number(text: str) -> list: 
    """Extracts potential invoice auth numbers from the provided text.

    Args:
        text (str): All text from the photo.
    
    Returns:
        list: A list of unique Auth invoice numbers found in the text.
    """
    # Normalize text by replacing newlines and converting to uppercase
    result = re.sub('\n', ' ', text).upper()

    # Regular expressions to match various formats of invoice numbers
    regex_patterns = [
        r"AUT\. SRI\s*\.?\s*N?°?\s*\d{10}",            # Matches various formats of "AUT. SRI" with optional spaces, periods, and "N°"
        r"AUTORIZACIÓN\s+SRI\s*[#N°]?\s*\d{10}",       # Matches "AUTORIZACIÓN SRI" with optional # or N° followed by 10 digits
        r"N°\s*\d{10}",                                # Matches "N°" followed by 10 digits
        r"AUTORIZACIÓN\s*\d{49}",                      # Matches "AUTORIZACIÓN" followed by 49 digits
        r'\d{49}'                                      # Matches 49 digits
    ]

    # Combine all patterns into a single regular expression
    combined_regex = '|'.join(regex_patterns)

    # Find all matches based on the combined regex pattern
    results = re.findall(combined_regex, result)

    # Clean the results by removing non-digit characters
    results = [re.sub(r'\D', '', res) for res in results]

    # Return a list of unique invoice numbers
    return list(set(results))


# TESTs
# _test.py