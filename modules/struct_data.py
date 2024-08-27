from modules import clean_data as clr

# Struct with data
class Data:
    """Data Struct for facturas\n

    Keyword arguments:\n
    text: (str) All text\n 
    Return: (dict) with all data
    """
    
    def __init__(self, text:str) -> None:
        self.text = text

    def to_dict(self):
        words_list = clr.classify(text=self.text)

        # Fields 
        proveedor_ruc = clr.search(words_list, text=False, search_range=5, keyword="RUC", block_hint=1)
        proveedor_nam = clr.search(words_list, text=True, search_range=5, keyword="PROVEEDOR", block_hint=1)
        comprobante_nu = clr.search(words_list, text=False, search_range=5, keyword="COMPROBANTE", block_hint=1)
        fecha_comprob = clr.search(words_list, text=False, search_range=5, keyword="FECHA", block_hint=1)
        valor_total = clr.search(words_list, text=False, search_range=5, keyword="TOTAL", block_hint=3)
        cliente_name = clr.search(words_list, text=True, search_range=5, keyword="CLIENTE", block_hint=2)

        # Data on Structure
        return {
            "Proveedor_Name": proveedor_nam,
            "Proveedor_RUC": proveedor_ruc,
            "Cliente_Name": cliente_name,
            "Comprobante": comprobante_nu,
            "Date": fecha_comprob,
            "Total_value": valor_total
        }

if __name__ == '__main__':
    with open('../test/prueba_0.txt', 'r') as file:
        file = file.read()

    data = Data(file)
    print(data.to_dict())