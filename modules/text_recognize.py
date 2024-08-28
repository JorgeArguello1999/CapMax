# Modules
import re 

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

    return set(result_one + result_two + result_tree + result_four)

if __name__ == "__main__":

    # Testing files
    count_bad = 0
    count_good = 0
    count_maybe = 0

    # Count
    good = []
    bad = []
    maybe = []

    for i in range(0, 22):
        with open(f'../test/test_{i}.jpg.txt', 'r') as file:
            file = file.read()
        
        ruc_detect = rucs_detects(file)
        date_detec = date_detect(file)

        # Classify result
        response = "🤔" 
        if ruc_detect != [] and date_detec != set():
            response = "✅"

        if ruc_detect == [] and date_detec == set():
            response = "❌"
        
        
        # Save answers
        if response == "❌": 
            count_bad += 1
            bad.append(f' Test:  {i} {response} | Ruc: {ruc_detect} | Date: {date_detec}')

        if response == "✅": 
            count_good += 1
            good.append(f' Test:  {i} {response} | Ruc: {ruc_detect} | Date: {date_detec}')

        if response == "🤔": 
            count_maybe += 1
            maybe.append(f' Test:  {i} {response} | Ruc: {ruc_detect} | Date: {date_detec}')

    for item in good + bad + maybe:
        print(item)
    
    print(f"✅: {count_good}")
    print(f"🤔: {count_maybe}")
    print(f"❌: {count_bad}")