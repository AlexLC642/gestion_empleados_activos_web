# controllers/reportes.py

from flask import Blueprint, send_file
from models.empleado_model import obtener_empleado_por_id
from models.activo_model import obtener_activos_por_empleado
from utils.pdf_generator import generar_reporte_pdf
import os

reportes_bp = Blueprint('reportes_bp', __name__, url_prefix='/reporte')

@reportes_bp.route('/<int:id_empleado>')
def generar_reporte(id_empleado):
    empleado = obtener_empleado_por_id(id_empleado)
    activos = obtener_activos_por_empleado(id_empleado)

    filename = f"reporte_empleado_{id_empleado}.pdf"
    path = os.path.join("database", filename)

    responsable = "Alex Estuardo Lem Cac"  # en el futuro: session['usuario']
    generar_reporte_pdf(path, empleado, activos, responsable)

    return send_file(path, as_attachment=True)
