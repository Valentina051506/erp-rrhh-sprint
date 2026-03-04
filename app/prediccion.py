from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import json

router = APIRouter(prefix="/api", tags=["Analítica RRHH"])

class DatosEmpleado(BaseModel):
    edad: int
    salario: float
    nivel_satisfaccion: int
    horas_extras: int

AZURE_ML_ENDPOINT = "https://<TU_ENDPOINT>.azureml.ms/score"
AZURE_ML_TOKEN = "<TU_TOKEN>"

@router.post("/empleados/riesgo-renuncia")
async def predecir_fuga_talento(empleado: DatosEmpleado):
    datos = {
        "Inputs": {
            "data": [[
                empleado.edad,
                empleado.salario,
                empleado.nivel_satisfaccion,
                empleado.horas_extras
            ]]
        },
        "GlobalParameters": 1.0
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {AZURE_ML_TOKEN}'
    }
    try:
        respuesta = requests.post(
            AZURE_ML_ENDPOINT,
            data=json.dumps(datos),
            headers=headers
        )
        respuesta.raise_for_status()
        resultado = respuesta.json()
        prediccion = resultado.get("Results", [0])[0]
        riesgo = "⚠️ Alto Riesgo de Renuncia" if prediccion == 1 else "✅ Empleado Estable"
        return {"status": "success", "diagnostico_ia": riesgo}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error con servicio IA: {str(e)}")
