from dotenv import load_dotenv
from os import getenv

import requests
import base64
import json
import re

# Load environment variables from a .env file
load_dotenv()

# OpenAI API Key
api_key = getenv('GPT_KEY')

# Query for the model
consult = """ 
From this text extracted from an invoice image, I would like you to extract the following data:
RUC: Client and provider
Date: Invoice issuance date
Values: Total values, subtotals, VAT 
# Invoice: The invoice number
Auth Invoice: The authentication number of the invoice.

Do it in a JSON format like this:
{"title": "test_11.jpg", "response": true, "process": {"rucs": {"vendor": "ID or RUC of the invoice owner", "client": "ID or RUC of the invoice client"}, "dates": ["12/08/2024"],"total_value": [$$.$$], "factura_auth": ["7 to 49 digits"], "factura_n": ["invoice number"], "ai": True (Ever True)}} 
"""

# Function to encode the image in base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image(image_path):
    """
    Processes an image to extract information using the OpenAI API.

    :param image_path: Path to the image file to process.
    :return: JSON response from the API with the extracted data.
    """
    # Get the base64 string of the image
    base64_image = encode_image(image_path)

    # Configure headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Configure the payload for the request
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": consult
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # Send the POST request to the OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Get the response and return it in JSON format
    response_dict = response.json()
    output = response_dict['choices'][0]['message']['content']

    # JSON convert
    results = re.sub(r'\n| |```|json', '', output)
    results = json.loads(results)

    try:
      return results['process']
    except:
      return []

# Example usage
if __name__ == "__main__":
    image_path = "../uploads/test_13.jpg"  # Path to your image
    result = process_image(image_path)
    print(result['process'])