import requests
import json

# parametro
names = ["Pedro", "Jose", "Juan","Miguel","John","Paul","Sabrina","Katherina"]

paises = {}

# invoca el servicio web 
# se recibe en un diccionario
for name in names:
    url = "https://api.nationalize.io/?name=" + name
    result = requests.get(url).json()
    pais = result["country"][0]["country_id"]
    # print(pais)
    if pais in paises:
        paises[pais] += 1
    else:
        paises[pais] = 1

# muestra el resultado
print(json.dumps(paises, indent=4))
#print(json.dumps(result, indent = 4))