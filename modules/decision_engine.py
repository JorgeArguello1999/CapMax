try: 
    from modules import gpt_recognise
except:
    import gpt_recognise

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
            results = gpt_recognise.process_image(path)
    except Exception as e:
        print(e)
    
    return results

if __name__ == '__main__':
    make_decision({
    "rucs": {
      "vendor": "",
      "client": ""
    },
    "dates": [
      "17/07/2024"
    ],
    "total_value": [],
    "factura_auth": [
      "113192617"
    ],
    "factura_n": [
      "000114"
    ]
  })