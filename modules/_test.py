# Recognise module
import text_recognise as tcr

if __name__ == "__main__":

    # Testing files
    count_bad = 0
    count_good = 0
    count_maybe = 0

    # Count
    good = []
    bad = []
    maybe = []

    for i in range(0, 22):
        with open(f'../test/test_{i}.jpg.txt', 'r') as file:
            file = file.read()
        
        ruc_detect = tcr.rucs_detects(file)
        date_detec = tcr.date_detect(file)
        total_v = tcr.total_value_detect(file)

        # Classify result
        response = "🤔" 
        if ruc_detect != [] and date_detec != None and total_v != []:
            response = "✅"

        if ruc_detect == [] and date_detec == None and total_v == []:
            response = "❌"
        
        
        # Save answers
        if response == "❌": 
            count_bad += 1
            bad.append(f' Test:  {i} {response} | Ruc: {ruc_detect} | Date: {date_detec} | Value: {total_v}')

        if response == "✅": 
            count_good += 1
            good.append(f' Test:  {i} {response} | Ruc: {ruc_detect} | Date: {date_detec} | Value: {total_v}')

        if response == "🤔": 
            count_maybe += 1
            maybe.append(f' Test:  {i} {response} | Ruc: {ruc_detect} | Date: {date_detec} | Value: {total_v}')

    for item in good + bad + maybe:
        print(item)
    
    print(f"✅: {count_good}")
    print(f"🤔: {count_maybe}")
    print(f"❌: {count_bad}")