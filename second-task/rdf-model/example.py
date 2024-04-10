import json

archivo_json = 'first-task/metadata.json'

# Abrimos el archivo JSON para leer los datos
with open(archivo_json, 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# Llamamos a la función auxiliar con los datos JSON
#imprimir_claves_valores(datos)
def contar_valores_nulos(datos, contador_nulos):
    if isinstance(datos, dict):
        for llave, valor in datos.items():
            if valor in [None, "", 0]:
                if llave in contador_nulos:
                    contador_nulos[llave] += 1
                else:
                    contador_nulos[llave] = 1
            elif isinstance(valor, (dict, list)):
                contar_valores_nulos(valor, contador_nulos)
    elif isinstance(datos, list):
        for item in datos:
            contar_valores_nulos(item, contador_nulos)

# Este código asume que ya has cargado tus datos JSON en la variable `datos`.
# Puedes hacerlo usando json.load() como lo has mencionado en tu pregunta.
contador_nulos = {}
# Supongamos que `datos` es tu variable que contiene los datos JSON ya cargados.
contar_valores_nulos(datos, contador_nulos)

print(contador_nulos)
