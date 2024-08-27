import json
import re

# Struct with data
class Data:
    def __init__(
            self, p_ruc, p_nam, c_num, f_com, v_total, c_name 
            ) -> None:
        self.proveedor_ruc = p_ruc
        self.proveedor_nam = p_nam
        self.comprobate_nu = c_num
        self.fecha_comprob = f_com
        self.valor_total = v_total
        self.cliente_name = c_name

    def to_dict(self):
        return {
            "Proveedor_Name": self.proveedor_nam,
            "Proveedor_RUC": self.proveedor_ruc,
            "Cliente_Name": self.cliente_name,
            "Comprobante": self.comprobate_nu,
            "Date": self.fecha_comprob,
            "Total_value": self.valor_total
        }

def create_data_from_text(text: str) -> Data:
    # Classify Text
    words_list = classify(text=text)

    # Search specific data
    p_ruc = search(words_list, text=False, search_range=5, keyword="RUC", block_hint=1)
    p_nam = search(words_list, text=True, search_range=5, keyword="PROVEEDOR", block_hint=1)
    c_num = search(words_list, text=False, search_range=5, keyword="COMPROBANTE", block_hint=1)
    f_com = search(words_list, text=True, search_range=5, keyword="FECHA", block_hint=1)
    v_total = search(words_list, text=False, search_range=5, keyword="TOTAL", block_hint=3)
    c_name = search(words_list, text=True, search_range=5, keyword="CLIENTE", block_hint=2)

    # Return Struct with data
    data = Data(p_ruc, p_nam, c_num, f_com, v_total, c_name)
    return json.dumps(data.to_dict(), indent=4)


# Extract text and create a list 
def classify(file_path:str=None, text:str=None) -> list:
    """Classify the text to list items
    
    Keyword arguments:\n
    file_path: If you have your text on file\n
    text: You can send text directly\n
    Return: List with items (words or lines)
    """

    text = text
    if file_path != None:
        try: 
            with open(file_path, 'r') as file:
                file = file.read()
            text = file

        except Exception as e:
            print(str(e))
            text = str(e)
    text = text.upper()
    
    # Convert words into list
    return text.splitlines()

# Search a items
def search(words_list:list, text:bool=False, search_range:int=5, keyword:str="", block_hint:int=4) -> list:
    """Search items on text
   
    Keyword arguments:
    words_list: (list) Text on list \n
    text: (bool) False if you want search a NUM item or True if you want search TEXT\n
    search_range: (int) How many items you should go through to find the data\n
    keyword: (str) Keyword to search in your text \n
    block_hint: (int) 1: Initial | 2: Middle | 3: Finally

    Return: List of possible answers
    """

    # Select the block to work
    words_list_size = len(words_list)
    block_size = words_list_size//3
    
    if block_hint == 1: block_range = range(0, block_size)
    if block_hint == 2: block_range = range(block_size, 2*block_size)
    if block_hint == 3: block_range = range(2*block_size, words_list_size)
    else: block_range = range(words_list_size)

    # 1-> Position | 2-> Item
    results = [[i, words_list[i]] for i in block_range if keyword in words_list[i]]

    # Text detect
    if text == True: 
        result = []
        for item in results:
            for i in range(search_range):
                result.append(words_list[item[0]+i])
        return result

    # Num detect
    if text == False:
        for item in results: 
            num_bool = ','.join(re.findall(r'\d+', item[1]))

            # Result found
            if num_bool != '': return num_bool  

            # Empty
            other_words = [words_list[item[0] + i] for i in range(search_range)]
            other_words = ''.join(other_words)
            other_words = ','.join(re.findall(r'\d+', other_words))
            return other_words
            

if __name__ == '__main__':
    data_instance = create_data_from_text('../test/prueba_0.txt')
    print(data_instance)