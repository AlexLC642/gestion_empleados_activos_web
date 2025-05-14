# controllers/activos.py

from flask import Blueprint, render_template, request, redirect, url_for
from models.activo_model import (
    obtener_activos_por_empleado,
    insertar_activo,
    obtener_activo_por_id,
    actualizar_activo,
    eliminar_activo
)
from models.empleado_model import obtener_empleado_por_id
from utils.decoradores import login_required, admin_required

activos_bp = Blueprint('activos_bp', __name__, url_prefix='/activos')

# 👁 Vista pública para empleados o admin
@activos_bp.route('/<int:id_empleado>')
@login_required
def ver_activos(id_empleado):
    activos = obtener_activos_por_empleado(id_empleado)
    empleado = obtener_empleado_por_id(id_empleado)
    return render_template('activos.html', activos=activos, empleado=empleado)

# 🔒 Solo admin puede agregar activos
@activos_bp.route('/agregar/<int:id_empleado>', methods=['POST'])
@login_required
@admin_required
def agregar_activo(id_empleado):
    datos = {
        'numero_activo': request.form['numero_activo'],
        'descripcion': request.form['descripcion'],
        'fecha_compra': request.form['fecha_compra'],
        'numero_factura': request.form['numero_factura'],
        'monto': request.form['monto'],
        'id_empleado': id_empleado
    }
    insertar_activo(datos)
    return redirect(url_for('activos_bp.ver_activos', id_empleado=id_empleado))

# 🔒 Solo admin puede editar activos
@activos_bp.route('/editar/<int:id_activo>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_activo(id_activo):
    if request.method == 'GET':
        activo = obtener_activo_por_id(id_activo)
        return render_template('editar_activo.html', activo=activo)
    else:
        datos = {
            'id': id_activo,
            'numero_activo': request.form['numero_activo'],
            'descripcion': request.form['descripcion'],
            'fecha_compra': request.form['fecha_compra'],
            'numero_factura': request.form['numero_factura'],
            'monto': float(request.form['monto']),
            'id_empleado': int(request.form['id_empleado'])
        }
        actualizar_activo(datos)
        return redirect(url_for('activos_bp.ver_activos', id_empleado=datos['id_empleado']))

# 🔒 Solo admin puede eliminar activos
@activos_bp.route('/eliminar/<int:id_activo>/<int:id_empleado>')
@login_required
@admin_required
def eliminar_activo_route(id_activo, id_empleado):
    eliminar_activo(id_activo)
    return redirect(url_for('activos_bp.ver_activos', id_empleado=id_empleado))
