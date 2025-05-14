from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from config import Config
from models.activo_model import obtener_activos_por_empleado
from models.empleado_model import obtener_empleado_por_id
from utils.decoradores import login_required

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

def conectar():
    return sqlite3.connect(Config.DATABASE)

@auth_bp.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        usuario = request.form['username']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM usuarios WHERE username=? AND password=? AND rol='admin'", (usuario, password))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            session['usuario'] = resultado[0]
            session['rol'] = 'admin'
            return redirect(url_for('empleados_bp.listar_empleados'))
        else:
            flash("Credenciales inválidas o rol incorrecto", "error")
            return redirect(url_for('auth_bp.login_admin'))

    return render_template('login_admin.html')

@auth_bp.route('/login-empleado', methods=['GET', 'POST'])
def login_empleado():
    if request.method == 'POST':
        usuario = request.form['username']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, id_empleado FROM usuarios WHERE username=? AND password=? AND rol='empleado'", (usuario, password))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            session['usuario'] = resultado[0]
            session['rol'] = 'empleado'
            session['id_empleado'] = resultado[1]
            return redirect(url_for('auth_bp.panel_empleado'))
        else:
            flash("Credenciales inválidas o rol incorrecto", "error")
            return redirect(url_for('auth_bp.login_empleado'))

    return render_template('login_empleado.html')

@auth_bp.route('/panel-empleado')
@login_required
def panel_empleado():
    if session.get('rol') != 'empleado' or 'id_empleado' not in session:
        flash("Acceso restringido a empleados.", "error")
        return redirect(url_for('inicio'))

    id_empleado = session['id_empleado']
    activos = obtener_activos_por_empleado(id_empleado)
    empleado = obtener_empleado_por_id(id_empleado)

    return render_template('activos.html', activos=activos, empleado=empleado)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))
