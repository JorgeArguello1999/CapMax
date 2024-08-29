# Modules
import validate_date as vd
import re 

""" Recognize differents items, depends that you need
"""

def rucs_detects(text: str = "") -> list:
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

    return results

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
    
    results = list(set(results))
    if len(results) >= 2:
        results = vd.get_valid_dates(results)

    return results

def total_value_detect(text:str) -> list:
    """Search Total Value\n
    
    Keyword arguments:\n
    text: (str) All texto to search
    Return: (list) with possible total value
    """

    text = text.upper()
    regex = r"TOTAL\s*\$?\s*([\d,\.]+)"
    results = re.findall(regex, text)

    return results

# TESTs
# _test.py