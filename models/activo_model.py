# models/activo_model.py

import sqlite3
from config import Config

def conectar():
    return sqlite3.connect(Config.DATABASE)

def obtener_activos_por_empleado(id_empleado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activos WHERE id_empleado = ? ORDER BY id DESC", (id_empleado,))
    activos = cursor.fetchall()
    conn.close()
    return activos

def insertar_activo(datos):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO activos (numero_activo, descripcion, fecha_compra, numero_factura, monto, id_empleado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datos['numero_activo'],
            datos['descripcion'],
            datos['fecha_compra'],
            datos['numero_factura'],
            datos['monto'],
            datos['id_empleado']
        ))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print("❌ Error al insertar activo:", e)
    finally:
        conn.close()

def obtener_activo_por_id(id_activo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activos WHERE id = ?", (id_activo,))
    activo = cursor.fetchone()
    conn.close()
    return activo

def actualizar_activo(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE activos
        SET numero_activo = ?, descripcion = ?, fecha_compra = ?, numero_factura = ?, monto = ?
        WHERE id = ?
    """, (
        datos['numero_activo'],
        datos['descripcion'],
        datos['fecha_compra'],
        datos['numero_factura'],
        datos['monto'],
        datos['id']
    ))
    conn.commit()
    conn.close()

def eliminar_activo(id_activo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM activos WHERE id = ?", (id_activo,))
    conn.commit()
    conn.close()
