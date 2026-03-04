from pydantic import BaseModel

class Empleado(BaseModel):
    nombre: str
    cedula: str
    cargo: str
    departamento: str
    salario_base: float
    fecha_ingreso: str
    tipo_contrato: str
    correo: str
