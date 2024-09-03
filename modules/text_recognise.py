import re

try:
    import validate_date as vd
except: 
    from modules import validate_date as vd

# Precompile regex patterns
REGEX_RUC = re.compile(r'\d{10,13}')
REGEX_DATE = re.compile(r'\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|\d{1,2}[-/.][a-zA-Z]{3}[-/.]\d{2,4})\b')
REGEX_TOTAL = re.compile(r"\bTOTAL\b\s*\$?\s*([\d,\.]+)")
REGEX_INVOICE = re.compile(r'\b\d{3}-\d{3}-\d{9}\b')
REGEX_AUTH_INVOICE = re.compile(r"AUT\. SRI\s*\.?\s*N?°?\s*\d{10}|AUTORIZACIÓN\s+SRI\s*[#N°]?\s*\d{10}|N°\s*\d{10}|AUTORIZACIÓN\s*\d{49}|\d{49}")
REGEX_INVOICE_6_7_DIGITS = re.compile(r'\b0{3,4}[1-9]\d{2,5}\b')
REGEX_INVOICE_9_DIGITS = re.compile(r'\b0{3,6}[1-9]\d{2,5}\b')

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
    return vd.get_most_recent_date(valid_dates)

def total_value_detect(text: str) -> list:
    text = re.sub('\n', ' ', text).upper()
    text = re.sub(r'[^a-zA-Z0-9.,]', ' ', text)

    results = [
        float(val.replace(',', '.')) for val in REGEX_TOTAL.findall(text) if val.replace('.', '', 1).isdigit()
    ]
    return [max(results)] if results else []

def invoice_number(text: str) -> list:
    text_cleaned = re.sub(r'\n', ' ', text)
    results = REGEX_INVOICE.findall(text_cleaned)
    results = list(set(results))

    if results == []: 
        text_cleaned = re.sub(r'\D', '-', re.sub(r'\n', ' ', text))[:len(text) * 2 // 3]
        results = REGEX_INVOICE_6_7_DIGITS.findall(text_cleaned) or REGEX_INVOICE_9_DIGITS.findall(text_cleaned)
        results = list(set(results))[:1]

    return results

def auth_invoice_number(text: str) -> list:
    result = REGEX_AUTH_INVOICE.findall(re.sub('\n', ' ', text).upper())
    return list(set([
        re.sub(r'\D', '', res) for res in result
    ]))