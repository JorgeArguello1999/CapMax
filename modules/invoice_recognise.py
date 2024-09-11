import re

from modules import validate_date as vd

# Precompile regex patterns
REGEX_RUC = re.compile(r'\d{10,13}')
REGEX_DATE = re.compile(r'\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|\d{1,2}[-/.][a-zA-Z]{3}[-/.]\d{2,4})\b')
REGEX_TOTAL = re.compile(r'\bTOTAL(?:[\s:]*[A-Z\s]*[\$]?[\s]*)?([\d.,]+)\b', re.IGNORECASE)
REGEX_INVOICE = re.compile(r'\b\d{3}-\d{3}-\d{9}\b')
REGEX_AUTH_INVOICE = re.compile(r"AUT\. SRI\s*\.?\s*N?°?\s*\d{10}|AUTORIZACIÓN\s+SRI\s*[#N°]?\s*\d{10}|N°\s*\d{10}|AUTORIZACIÓN\s*\d{49}|\d{49}")
REGEX_INVOICE_6_7_DIGITS = re.compile(r'\b0{3,4}[1-9]\d{2,5}\b')
REGEX_INVOICE_9_DIGITS = re.compile(r'\b0{3,6}[1-9]\d{2,5}\b')
REGEX_ADDRESS = re.compile(r'\b(?:Av|Avenida|Calle)\s+[A-Za-z\s]+(?:y\s+[A-Za-z\s]+)?\b', re.IGNORECASE)
REGEX_SERIAL_NUMBER = re.compile(r'\b\d{3}-\d{3}\b')

# Prefix and Suffix for RUC detection
PREFIXES = {f'0{i}' for i in range(1, 10)}.union({f'{i}' for i in range(11, 25)}, {'88', '90'})
SUFFIX = '001'

def rucs_detects(text: str = "") -> dict:
    text = re.sub('/', '1', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)[:len(text) * 2 // 3]
    results = [
        ruc for ruc in REGEX_RUC.findall(text) if (
            len(ruc) in {10, 13} and ruc[:2] in PREFIXES and ruc.endswith(SUFFIX)
        )
    ]

    seen = set()
    unique_results = [
        ruc for ruc in results if not (
            ruc in seen or seen.add(ruc)
        )
    ]
    return {
        "vendor": unique_results[0] if unique_results else '', 
        "client": unique_results[1] if len(unique_results) > 1 else ''
    }

def date_detect(text: str) -> str:
    text = re.sub('\n', ' ', text)[:len(text) * 2 // 3]
    results = [
        re.sub(r'[-.]', '/', date) for date in REGEX_DATE.findall(text)
    ]
    valid_dates = vd.get_valid_dates(list(set(results)))
    try:
        return vd.get_most_recent_date(valid_dates)[0]
    except Exception as e:
        print(f'>>> Error: {str(e)}')
        return ""

def total_value_detect(text: str) -> list:
    text = re.sub('\n', ' ', text).upper()
    text = re.sub(r'[^a-zA-Z0-9.,]', ' ', text)

    results = REGEX_TOTAL.findall(text)
    results = [float(val.replace(',', '.')) for val in results if val.replace('.', '', 1).isdigit()]
    results = [result for result in results if len(str(result)) < 7]

    results = [max(results)] if results else []
    try:
        return str(results[0])
    except Exception as e:
        print(f">>> Error: {str(e)}")
        return ""

def invoice_number(text: str) -> list:
    text_cleaned = re.sub(r'\n', ' ', text)
    results = REGEX_INVOICE.findall(text_cleaned)
    results = list(set(results))

    if results == []: 
        text_cleaned = re.sub(r'\D', '-', re.sub(r'\n', ' ', text))[:len(text) * 2 // 3]
        results = REGEX_INVOICE_6_7_DIGITS.findall(text_cleaned) or REGEX_INVOICE_9_DIGITS.findall(text_cleaned)
        results = list(set(results))[:1]

    try:
        return results[0]
    except Exception as e:
        print(f">>> Error: {str(e)}")
        return ""

def auth_invoice_number(text: str) -> list:
    result = REGEX_AUTH_INVOICE.findall(re.sub('\n', ' ', text).upper())
    result = list(set([
        re.sub(r'\D', '', res) for res in result
    ]))

    try:
        return result[0]
    except Exception as e:
        print(f">>> Error: {str(e)}")

def extract_address(text: str) -> str:
    # Clean text to remove unnecessary characters
    text_cleaned = re.sub(r'[^A-Za-z\s]', ' ', text)
    text_cleaned = re.sub('\n', ' ', text_cleaned)
    # Find all address patterns
    addresses = REGEX_ADDRESS.findall(text_cleaned)
    
    # Return the first found address, if any, or an empty string
    result = addresses[0] if addresses else ""
    try:
        return result[:40]
    except Exception as e:
        print(f">>> Error: {str(e)}")
        return ""

def extract_serial_number(text: str) -> str:
    # Find all serial numbers that match the pattern
    serial_numbers = REGEX_SERIAL_NUMBER.findall(text)
    
    # Return the first found serial number, if any, or an empty string
    return serial_numbers[0] if serial_numbers else ""