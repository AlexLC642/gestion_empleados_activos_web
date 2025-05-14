from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from config import Config
from models.empleado_model import obtener_empleados

usuarios_bp = Blueprint('usuarios_bp', __name__, url_prefix='/usuarios')

def conectar():
    return sqlite3.connect(Config.DATABASE)

@usuarios_bp.route('/')
def listar_usuarios():
    if 'usuario' not in session or session.get('rol') != 'admin':
        return redirect(url_for('auth_bp.login_admin'))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT u.id, u.username, u.nombre, u.rol, e.nombres || ' ' || e.apellidos FROM usuarios u LEFT JOIN empleados e ON u.id_empleado = e.id")
    usuarios = cursor.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios)

@usuarios_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    if 'usuario' not in session or session.get('rol') != 'admin':
        return redirect(url_for('auth_bp.login_admin'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['nombre']
        rol = request.form['rol']
        id_empleado = request.form['id_empleado'] or None


        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (username, password, nombre, rol, id_empleado) VALUES (?, ?, ?, ?, ?)", 
                           (username, password, nombre, rol, id_empleado))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Nombre de usuario ya existe", "error")
        conn.close()
        return redirect(url_for('usuarios_bp.listar_usuarios'))

    empleados = obtener_empleados()
    return render_template('agregar_usuario.html', empleados=empleados)

@usuarios_bp.route('/eliminar/<int:id>')
def eliminar_usuario(id):
    if 'usuario' not in session or session.get('rol') != 'admin':
        return redirect(url_for('auth_bp.login_admin'))

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('usuarios_bp.listar_usuarios'))

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'usuario' not in session or session.get('rol') != 'admin':
        return redirect(url_for('auth_bp.login_admin'))

    conn = conectar()
    cursor = conn.cursor()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['nombre']
        rol = request.form['rol']
        id_empleado = request.form['id_empleado'] or None

        cursor.execute("""
            UPDATE usuarios 
            SET username = ?, password = ?, nombre = ?, rol = ?, id_empleado = ?
            WHERE id = ?
        """, (username, password, nombre, rol, id_empleado, id))
        conn.commit()
        conn.close()
        return redirect(url_for('usuarios_bp.listar_usuarios'))

    # GET
    cursor.execute("SELECT id, username, password, nombre, rol, id_empleado FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    empleados = obtener_empleados()
    conn.close()
    return render_template('editar_usuario.html', usuario=usuario, empleados=empleados)
