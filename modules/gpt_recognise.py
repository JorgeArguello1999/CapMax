from dotenv import load_dotenv
from os import getenv
load_dotenv()

import base64
import requests
import json

# OpenAI API Key
api_key = getenv('GPT_KEY')

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Query 
consult = """ 
De este texto extraído de una imagen de factura, me gustaría que extraigas los siguientes datos:
RUC: Cliente y proveedor
Fecha: Emisión de la factura
Valores: Los valores totales, subtotales, iva 
# Factura: El número de factura
Auth Factura: El número de autenticación de la factura.

Hazlo en un json con este estilo:
{
  "title": "test_11.jpg",
  "response": true,
  "process": {
    "rucs": {
      "vendor": "10 a 13",
      "client": "10 a 13"
    },
    "dates": [
      "12/08/2024"
    ],
    "total_value": [
      4.66
    ],
    "factura_auth": [
        "7 a 49 digitos"
    ],
    "factura_n": [
      "000107529"
    ]
  }
}
"""

# Path to your image
image_path = "../uploads/test_13.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

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

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# Print the response in a readable format
response_dict = response.json()
formatted_response = json.dumps(response_dict, indent=4)
print(formatted_response)