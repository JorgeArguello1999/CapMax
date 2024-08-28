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
    

if __name__ == "__main__":

    with open('../test/prueba_0.txt', 'r') as file:
        file = file.read()
    
    print(rucs_detects(file))