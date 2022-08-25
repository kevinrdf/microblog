import requests
import json

# parametro
name = "Pedro"

# url del API REST
url = "https://api.nationalize.io/?name=" + name

# invoca el servicio web 
# se recibe en un diccionario
result = requests.get(url).json()

# muestra el resultado
print(json.dumps(result, indent = 4))