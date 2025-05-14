# models/empleado_model.py

import sqlite3
from config import Config

def conectar():
    return sqlite3.connect(Config.DATABASE)

def obtener_empleados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados ORDER BY id DESC")
    empleados = cursor.fetchall()
    conn.close()
    return empleados

def insertar_empleado(datos):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO empleados (codigo, nombres, apellidos, direccion, telefono, departamento, puesto)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datos['codigo'],
            datos['nombres'],
            datos['apellidos'],
            datos['direccion'],
            datos['telefono'],
            datos['departamento'],
            datos['puesto']
        ))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("❌ Error al insertar:", e)
    finally:
        conn.close()

def obtener_empleado_por_id(id_empleado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id = ?", (id_empleado,))
    empleado = cursor.fetchone()
    conn.close()
    return empleado

def actualizar_empleado(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE empleados
        SET codigo = ?, nombres = ?, apellidos = ?, direccion = ?, telefono = ?, departamento = ?, puesto = ?
        WHERE id = ?
    """, (
        datos['codigo'],
        datos['nombres'],
        datos['apellidos'],
        datos['direccion'],
        datos['telefono'],
        datos['departamento'],
        datos['puesto'],
        datos['id']
    ))
    conn.commit()
    conn.close()

def eliminar_empleado(id_empleado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id = ?", (id_empleado,))
    conn.commit()
    conn.close()
