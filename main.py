from fastapi import FastAPI
import requests


API_KEY = 'd7eaba510816031d2ab424b5'
url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'


def obtener_conversion():
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
        if response['result'] == 'success':
            return response['conversion_rates']
        else:
            print("Error en los datos de la API")
            return None
    else:
        print(f"Error al obtener datos de la API. Código de error: {response.status_code}")
        return None


def convertir_moneda(cantidad, moneda_origen, moneda_destino):
    tasas_conversion = obtener_conversion()

    if tasas_conversion is None:
        return

    if moneda_origen not in tasas_conversion:
        print(f"Moneda de origen {moneda_origen} no válida.")
        return

    if moneda_destino not in tasas_conversion:
        print(f"Moneda de destino {moneda_destino} no válida.")
        return

    cantidad_en_usd = cantidad / tasas_conversion[moneda_origen]

    cantidad_convertida = cantidad_en_usd * tasas_conversion[moneda_destino]

    print(f"{cantidad} {moneda_origen} es equivalente a {cantidad_convertida:.2f} {moneda_destino}")


if __name__ == "__main__":
    cantidad = float(input("Introduce la cantidad que deseas convertir: "))
    moneda_origen = input("Introduce la moneda de origen (por ejemplo, USD, EUR, PEN): ").upper()
    moneda_destino = input("Introduce la moneda de destino (por ejemplo, USD, EUR, PEN): ").upper()

    # Llamar a la función de conversión
    convertir_moneda(cantidad, moneda_origen, moneda_destino)


