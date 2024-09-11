from vision import gpt_recognise
from vision import google_vision  

# Invoice methods
from handlers import invoice_detect as rd
from handlers import deposit_detect as dt

# Make decision
def make_decision(file_path:str, ia:bool=False, deposit:bool=False) -> dict:
    # Only GPT recognise for Invoice or Deposit
    if ia and deposit == False: return gpt_recognise.process_image(file_path, deposit=False)
    if ia and deposit == True: return gpt_recognise.process_image(file_path, deposit=True)

    # OCR Recognition
    text = google_vision.text_detect(file_path)
    if deposit: return dt.get_response(text=text, file_path=file_path)
    else: return rd.get_response(file_path=file_path, text=text)

