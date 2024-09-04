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
def make_decision(data:dict) -> dict:
    score = calculate_score(
        ruc_detect=data['rucs'], 
        date_detect=data['dates'], 
        total_v=data['total_value'], 
        factura_n=data['factura_n'], 
        auth_factura_n=data['factura_auth']
    )

    results = data
    try: 
        if score <= 5: 
            print(f">>> Using GPT for recognise...  Score [{score}]")
    except Exception as e:
        print(e)
    
    return results
  

def get_response(file_path:str) -> dict:
    text = google_vision.text_detect(file_path=file_path)

    # First thread
    regex = regex_response(text)

    # Second thread 
    gpt = gpt_response(file_path)

    return regex, gpt

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
            'ai': False

        }