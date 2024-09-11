import re

# Regular expressions for different fields
REGEX_AMOUNT = re.compile(r'\$\s?(\d+\.\d{2})')
REGEX_RECEIPT_NUMBER = re.compile(r'Comprobante:\s?(\d+)')
REGEX_DESTINATION_ACCOUNT = re.compile(r'Número de cuenta\s+.*?\*\*\*\*(\d+)', re.DOTALL)
REGEX_NAME = re.compile(r'Cuenta destino\s+Nombre\s+(.*?)\s', re.DOTALL)
REGEX_DATE = re.compile(r'Fecha\s+(\d{2}\s\w+\s\d{4})')

def extract_amount(text: str) -> str:
    match = REGEX_AMOUNT.search(text)
    return match.group(1) if match else ""

def extract_receipt_number(text: str) -> str:
    match = REGEX_RECEIPT_NUMBER.search(text)
    return match.group(1) if match else ""

def extract_destination_account(text: str) -> str:
    match = REGEX_DESTINATION_ACCOUNT.search(text)
    return "*****" + match.group(1) if match else ""

def extract_name(text: str) -> str:
    match = REGEX_NAME.search(text)
    return match.group(1).strip() if match else ""

def extract_date(text: str) -> str:
    match = REGEX_DATE.search(text)
    if match:
        # Parse date to YYYY/MM/DD format
        date = match.group(1)
        return format_date(date)
    return ""

def format_date(date_str: str) -> str:
    # Convert date in format "02 sept 2024" to "YYYY/MM/DD"
    months = {
        'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04', 'may': '05', 'jun': '06',
        'jul': '07', 'ago': '08', 'sept': '09', 'oct': '10', 'nov': '11', 'dic': '12'
    }
    day, month, year = date_str.split()
    return f"{year}/{months[month[:4]]}/{day.zfill(2)}"
