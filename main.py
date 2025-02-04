from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

API_KEY = 'd7eaba510816031d2ab424b5'
url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'


class ConversionRequest(BaseModel):
    cantidad: float
    moneda_origen: str
    moneda_destino: str


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
        return None

    if moneda_origen not in tasas_conversion:
        raise HTTPException(status_code=400, detail=f"Moneda de origen {moneda_origen} no válida.")
    
    if moneda_destino not in tasas_conversion:
        raise HTTPException(status_code=400, detail=f"Moneda de destino {moneda_destino} no válida.")

    cantidad_en_usd = cantidad / tasas_conversion[moneda_origen]
    cantidad_convertida = cantidad_en_usd * tasas_conversion[moneda_destino]

    return {"cantidad_convertida": round(cantidad_convertida, 2)}


@app.post("/convertir/")
async def convertir(data: ConversionRequest):
    resultado = convertir_moneda(data.cantidad, data.moneda_origen.upper(), data.moneda_destino.upper())
    
    if resultado is None:
        raise HTTPException(status_code=500, detail="Error al obtener la conversión.")
    
    return {"cantidad": data.cantidad, "moneda_origen": data.moneda_origen, 
            "moneda_destino": data.moneda_destino, "cantidad_convertida": resultado["cantidad_convertida"]}
