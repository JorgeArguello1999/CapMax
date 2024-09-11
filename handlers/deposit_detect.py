from concurrent.futures import ThreadPoolExecutor

from modules import deposit_recognise as dpr

def get_response(text:str, file_path:str) -> dict:
    regex = regex_response(text)
    # Create a qualifier answer
    return regex

def regex_response(text:str) -> dict:
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
            'date': date.result()
        }