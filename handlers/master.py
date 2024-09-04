from vision import gpt_recognise as gv
from modules import text_recognise as trc
from vision import google_vision  

# Get score from response
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
def make_decision(data:dict, path:str) -> dict:
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
            results = gv.process_image(path)
    except Exception as e:
        print(e)
    
    return results
  
# Get a response
def get_response(file_path:str) -> dict:
    # Detect text
    text_detect = google_vision.text_detect(file_path=file_path)

    # Classify and search by REGEX
    text_detect = {
        'rucs': trc.rucs_detects(text=text_detect),
        'dates': trc.date_detect(text=text_detect),
        'total_value': trc.total_value_detect(text=text_detect),
        'factura_auth': trc.auth_invoice_number(text=text_detect), 
        'factura_n': trc.invoice_number(text=text_detect),
        'ai': False,
    }

    return make_decision(text_detect, file_path)

