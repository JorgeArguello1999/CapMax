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
    Return: (list) Items with RUCs in order of appearance.
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

    results.extend([0] * (2 - len(results)))

    try: results = [ int(result) for result in results ]
    except: results = results
    
    return {
        "vendor": results[0],
        "client": results[1]
    }

def date_detect(text: str) -> list:
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

    # Replace newline characters with hyphens to ensure continuity
    text = re.sub(r'\n', '-', text)

    # Regular expression pattern to match "TOTAL" followed by an optional currency symbol and a numeric value
    regex = r"TOTAL\s*\$?\s*([\d,\.]+)"

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

# TESTs
# _test.py