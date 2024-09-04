from concurrent.futures import ThreadPoolExecutor

from vision import gpt_recognise
from modules import invoice_recognise as trc

def get_response(text:str, file_path:str) -> dict:
    regex = regex_response(text)

    score = calculate_score(
        ruc_detect=regex['rucs'], 
        date_detect=regex['date'], 
        total_v=regex['total_value'], 
        factura_n=regex['factura_n'], 
        auth_factura_n=regex['factura_auth']
    )

    result = regex
    if score < 3:
        print(f">>> Using GPT results... Score [{score}]")
        result = gpt_recognise.process_image(file_path)
    else:
        print(f">>> Using REGEX results... Score [{score}]")

    return result   

# Quality the answers
def calculate_score(ruc_detect, date_detect, total_v, factura_n, auth_factura_n):
    score = 5
    if not ruc_detect.get("vendor"): score -= 1
    if not ruc_detect.get("client"): score -= 1
    if not date_detect: score -= 1
    if not total_v: score -= 1
    if not factura_n: score -= 1
    if not auth_factura_n: score -= 1
    return score

# Get REGEX response if invoice
def regex_response(text:str) -> dict:
    with ThreadPoolExecutor() as executor:
        rucs = executor.submit(trc.rucs_detects, text=text)
        date = executor.submit(trc.date_detect, text=text)
        total = executor.submit(trc.total_value_detect, text=text)
        factura_auth = executor.submit(trc.auth_invoice_number, text=text)
        factura_numb = executor.submit(trc.invoice_number, text=text)

        return {
            'rucs': rucs.result(),
            'date': date.result(),
            'total_value': total.result(),
            'factura_auth': factura_auth.result(),
            'factura_n': factura_numb.result(),
            'ai': False  # Indicador de que es una respuesta generada por regex
        }