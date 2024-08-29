# Modules
import re 

from typing import List

""" Recognize differents items, depends that you need
"""

def rucs_detects(text:str="") -> list:
    """RUC Detect
    Ruc is a item wit 10 numbers or maybe 13
    This function is only for Ecuador Country
    
    Keyword arguments:
    text: (str) All text for recognize
    Return: (list) Items with answer
    """
    # Clean data from letters, spaces or symbols 
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub('\n', '', text)

    # Ruc from proveedor or costumer is on first part
    large = len(text)//3
    text = text[:large*2]

    # REGEX item with 10-13 items large
    items_10_13 = re.findall(r'\d{10,13}', text) 

    # REGEX item with 13 items large and 001 code for ruc
    ruc_numbers = re.findall(r'\b\d{10}001\b', text)

    # Mix result
    results = set(ruc_numbers + items_10_13)

    prefix = [ f'0{i}' for i in range(1, 10) ] + [ f'{i}' for i in range(11, 25) ] + [ '88', '90' ]
    suffix = '001'

    # Classify Items with 10 or 13 
    results = [ x for x in results if (
        (len(x) == 10 or len(x) == 13) and 
        (x.startswith(tuple(prefix)) and x.endswith(suffix))
    ) ]

    return results

def date_detect(text:str) -> list:
    """Date detect
    This function get date field from text
    
    Keyword arguments:
    text: (str) All text from photo
    Return: (list) Items with date
    """
    # Clean spaces from data
    text = re.sub('\n', ' ', text)

    # Search with digits
    texto = re.sub('\.', '', text)
    regex = r'\b\d{1,2}/[a-zA-Z]{3}/\d{2,4}\b'
    result_one = re.findall(regex, texto)

    # Search only nums
    texto = re.sub(r"[^\d/]", "-", text)
    regex = r"\b\d{1,2}/(?:\d{1,2}|[a-zA-Z]{3})/\d{2,4}\b"
    result_two = re.findall(regex, texto)

    # Search with '-'
    regex = r'\b\d{1,2}-\d{1,2}-\d{2,4}\b'
    result_tree = re.findall(regex, text)

    # Search with '.'
    regex = r'\b\d{2}\.\d{2}\.\d{4}\b'
    result_four = re.findall(regex, text)

    results = list(
        set(result_one + result_two + result_tree + result_four)
    )

    results = normalize_dates(results)
    return find_middle_date(results)

# Normalize date
def normalize_dates(dates):
    def normalize_date(date):
        # Define regex patterns for different date formats
        patterns = [
            (r'^(\d{1,2})/(\d{1,2})/(\d{2,4})$', lambda d, m, y: f"{d.zfill(2)}/{m.zfill(2)}/{y.zfill(4) if len(y) == 4 else '20' + y.zfill(2)}"),
            (r'^(\d{1,2})-(\d{1,2})-(\d{2,4})$', lambda d, m, y: f"{d.zfill(2)}/{m.zfill(2)}/{y.zfill(4) if len(y) == 4 else '20' + y.zfill(2)}"),
            (r'^(\d{2})\.(\d{2})\.(\d{4})$', lambda d, m, y: f"{d.zfill(2)}/{m.zfill(2)}/{y}"),
            (r'^(\d{2})/([a-zA-Z]{3})/(\d{2,4})$', lambda d, m, y: f"{d.zfill(2)}/{month_map.get(m.lower(), m)}/{y.zfill(4) if len(y) == 2 else y}")
        ]
        
        month_map = {
            'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'ago': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dic': '12'
        }

        for pattern, formatter in patterns:
            match = re.match(pattern, date)
            if match:
                return formatter(*match.groups())
        
        return date  # Return the original date if no pattern matched

    return [normalize_date(date) for date in dates]

def find_middle_date(dates: List[str]) -> str:
    if not dates:
        return None  # Return None if the list is empty

    # Convert all dates to a common format for comparison
    dates = sorted(dates, key=lambda date: (
        int(date.split('/')[2]),  # Year
        int(date.split('/')[1]),  # Month
        int(date.split('/')[0])   # Day
    ))
    
    # Select the middle date
    mid_index = len(dates) // 2
    if len(dates) % 2 == 0:
        # If the list length is even, return the average of the two central elements
        return dates[mid_index - 1]
    else:
        # If the list length is odd, return the middle element
        return dates[mid_index]


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