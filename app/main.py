from fastapi import FastAPI
from app.prediccion import router as prediccion_router

app = FastAPI(
    title="ERP - Módulo Recursos Humanos",
    description="API del ERP con integración de IA predictiva",
    version="1.0.0"
)

app.include_router(prediccion_router)

@app.get("/")
def root():
    return {"mensaje": "ERP RRHH activo ✅"}
