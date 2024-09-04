from vision import gpt_recognise
from vision import google_vision  

# Invoice methods
from handlers import rucs_detect as rd

# Make decision
def make_decision(file_path:str, ia:bool=False, deposit:bool=False) -> dict:
    # Only GPT recognise for Invoice 
    if ia and deposit == False: return gpt_recognise.process_image(file_path)
    if ia and deposit == True: return gpt_recognise.process_image(file_path)
    
    if deposit: return 0

    # OCR Recognition
    text = google_vision.text_detect(file_path)
    return rd.get_response(file_path=file_path, text=text)

