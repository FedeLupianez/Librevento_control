import requests
import json

url = 'http://127.0.0.1:8000/login?email_usuario=prueba_0@gmail&clave=hola_mundo'

data = {
    "email": "prueba_0@gmail",
    "clave": "hola_mundo"
}

response = requests.get(url)

if (response.status_code == 200):
    print("Usuario logueado : ", response.json())
else:
    print("error logueando ")