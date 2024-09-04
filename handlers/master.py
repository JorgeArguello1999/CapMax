from concurrent.futures import ThreadPoolExecutor

from modules import text_recognise as trc
from vision import gpt_recognise
from vision import google_vision  

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

# Make decision
def make_decision(regex_results:dict, gpt_results:dict) -> dict:
    score = calculate_score(
        ruc_detect=regex_results['rucs'], 
        date_detect=regex_results['date'], 
        total_v=regex_results['total_value'], 
        factura_n=regex_results['factura_n'], 
        auth_factura_n=regex_results['factura_auth']
    )

    if score < 3:
        print(f">>> Using GPT results... Score [{score}]")
        return gpt_results
    else:
        print(f">>> Using regex results... Score [{score}]")
        return regex_results

def get_response(file_path:str) -> dict:
    text = google_vision.text_detect(file_path=file_path)

    # First thread: regex response
    regex = regex_response(text)

    # Second thread: GPT response
    gpt = gpt_response(file_path)

    # Make decision based on regex score
    results = make_decision(regex_results=regex, gpt_results=gpt)

    return results

def gpt_response(file_path:str) -> dict:
    return gpt_recognise.process_image(file_path)

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