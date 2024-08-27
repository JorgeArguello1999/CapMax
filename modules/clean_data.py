import re

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
    """ 
    # Num
    text = classify(file_path='../test/prueba_2.txt')
    text = search(words_list=text, text=False, search_range=5, keyword="TOTAL", block_hint=3)
    print(text)

    text = classify(file_path='../test/prueba_1.txt')
    text = search(words_list=text, text=False, search_range=5, keyword="TOTAL", block_hint=3)
    print(text)

    text = classify(file_path='../test/prueba_0.txt')
    text = search(words_list=text, text=False, search_range=5, keyword="TOTAL", block_hint=3)
    print(text)

    """
    # Text
    text = classify(file_path='../test/prueba_0.txt')
    text = search(words_list=text, text=True, search_range=5, keyword="SR.", block_hint=1)
    print(text)

    text = classify(file_path='../test/prueba_0.txt')
    text = search(words_list=text, text=True, search_range=9, keyword="FECHA", block_hint=1)
    print(text)



