import sys
import os

# Agregar la ruta del directorio principal
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)
os.environ['GOOGLE_CLOUD_CREDENTIALS'] = '../.venv/credentials_vision_api.json'

from handlers import master as master

if __name__ == '__main__':
    file = '../app/uploads/test_0.jpg'
    results = master.get_response(file)
    print(results)