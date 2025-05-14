from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3
from config import Config
from utils.decoradores import login_required, admin_required

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')

def conectar():
    return sqlite3.connect(Config.DATABASE)

@dashboard_bp.route('/')
@login_required
@admin_required
def panel_admin():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM empleados")
    total_empleados = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM activos")
    total_activos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    cursor.execute("SELECT numero_activo, descripcion, fecha_compra FROM activos ORDER BY id DESC LIMIT 1")
    ultimo_activo = cursor.fetchone()

    conn.close()

    return render_template('dashboard.html', 
        total_empleados=total_empleados,
        total_activos=total_activos,
        total_usuarios=total_usuarios,
        ultimo_activo=ultimo_activo
    )
