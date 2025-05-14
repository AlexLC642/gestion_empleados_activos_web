# controllers/empleados.py

from flask import Blueprint, render_template, request, redirect, url_for
from models.empleado_model import (
    obtener_empleados,
    insertar_empleado,
    obtener_empleado_por_id,
    actualizar_empleado,
    eliminar_empleado
)
from utils.decoradores import login_required

empleados_bp = Blueprint('empleados_bp', __name__, url_prefix='/empleados')

@empleados_bp.route('/')
@login_required
def listar_empleados():
    empleados = obtener_empleados()
    return render_template('empleados.html', empleados=empleados)

@empleados_bp.route('/agregar', methods=['POST'])
@login_required
def agregar_empleado():
    datos = {
        'codigo': request.form['codigo'],
        'nombres': request.form['nombres'],
        'apellidos': request.form['apellidos'],
        'direccion': request.form['direccion'],
        'telefono': request.form['telefono'],
        'departamento': request.form['departamento'],
        'puesto': request.form['puesto']
    }
    insertar_empleado(datos)
    return redirect(url_for('empleados_bp.listar_empleados'))

@empleados_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_empleado(id):
    if request.method == 'GET':
        empleado = obtener_empleado_por_id(id)
        return render_template('editar_empleado.html', empleado=empleado)
    else:
        datos = {
            'id': id,
            'codigo': request.form['codigo'],
            'nombres': request.form['nombres'],
            'apellidos': request.form['apellidos'],
            'direccion': request.form['direccion'],
            'telefono': request.form['telefono'],
            'departamento': request.form['departamento'],
            'puesto': request.form['puesto']
        }
        actualizar_empleado(datos)
        return redirect(url_for('empleados_bp.listar_empleados'))

@empleados_bp.route('/eliminar/<int:id>')
@login_required
def eliminar_empleado_route(id):
    eliminar_empleado(id)
    return redirect(url_for('empleados_bp.listar_empleados'))
