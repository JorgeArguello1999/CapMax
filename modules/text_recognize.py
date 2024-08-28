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
    text = re.sub('\n', '', text)

    # Search date field "DD/MM/YYYY"
    pattern = r'\d{2}/\d{2}/\d{4}\b'
    result = re.findall(pattern, text)

    if result == []: 
        # Search date field "DD/MM/YY" 
        pattern = r'\d{1,3}/\d{1,3}/\d{2,4}\b'
        result = re.findall(pattern, text)

    return result


if __name__ == "__main__":

    # Testing files
    count_bad = 0
    count_good = 0
    for i in range(0, 22):
        with open(f'../test/test_{i}.jpg.txt', 'r') as file:
            file = file.read()
        
        ruc_detect = rucs_detects(file)
        date_detec = date_detect(file)

        response = "❌"
        if ruc_detect != [] and date_detec != []:
            response = "✅"
        
        if response == "❌": count_bad += 1
        if response == "✅": count_good += 1

        print(f''' Test:  {i} {response} | Ruc: {ruc_detect} | Date: {date_detec} ''')
    
    print(f"❌: {count_bad}")
    print(f"✅: {count_good}")