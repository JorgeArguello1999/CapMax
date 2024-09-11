from concurrent.futures import ThreadPoolExecutor

from vision import gpt_recognise
from modules import deposit_recognise as dpr

def get_response(text: str, file_path: str) -> dict:
    regex = regex_response(text)

    score = calculate_score(
        amount=regex['amount'], 
        receipt_number=regex['receipt_number'], 
        destination_account=regex['destination_account'], 
        name=regex['name'], 
        date=regex['date']
    )

    result = regex
    if score < 3:
        print(f">>> Using GPT results... Score [{score}]")
        result = gpt_recognise.process_image(file_path)
    else:
        print(f">>> Using REGEX results... Score [{score}]")

    return result

# Función para calificar las respuestas obtenidas por REGEX
def calculate_score(amount, receipt_number, destination_account, name, date):
    score = 5  

    if not amount: score -= 1
    if not receipt_number: score -= 1
    if not destination_account: score -= 1
    if not name: score -= 1
    if not date: score -= 1

    return score

# Obtener los datos usando REGEX con el uso de múltiples hilos
def regex_response(text: str) -> dict:
    with ThreadPoolExecutor() as executor:
        amount = executor.submit(dpr.extract_amount, text=text)
        receipt_number = executor.submit(dpr.extract_receipt_number, text=text)
        destination = executor.submit(dpr.extract_destination_account, text=text)
        name = executor.submit(dpr.extract_name, text=text)
        date = executor.submit(dpr.extract_date, text=text)

        return {
            'amount': amount.result(),
            'receipt_number': receipt_number.result(),
            'destination_account': destination.result(),
            'name': name.result(),
            'date': date.result(),
            'ai': False  
        }