# utils/pdf_generator.py

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

def generar_reporte_pdf(nombre_archivo, empleado, activos, responsable="Sistema"):
    c = canvas.Canvas(nombre_archivo, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Título centrado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, "REPORTE DE ACTIVOS ASIGNADOS")
    y -= 20

    # Fecha y responsable (esquina derecha)
    c.setFont("Helvetica", 9)
    c.drawRightString(width - 50, y, f"Generado el: {fecha_actual}")
    y -= 10
    c.drawRightString(width - 50, y, f"Responsable: {responsable}")
    y -= 30

    # Información del empleado
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Empleado: {empleado[2]} {empleado[3]}")
    y -= 20
    c.drawString(50, y, f"Departamento: {empleado[6]}")
    y -= 20
    c.drawString(50, y, f"Puesto: {empleado[7]}")
    y -= 30

    # Encabezados de tabla
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.lightgrey)
    c.rect(50, y - 5, width - 100, 20, fill=True, stroke=False)
    c.setFillColor(colors.black)

    headers = ["ID", "N° Activo", "Descripción", "Fecha", "Factura", "Monto"]
    col_x = [50, 90, 160, 310, 380, 460]

    for i, header in enumerate(headers):
        c.drawString(col_x[i], y, header)

    y -= 20
    c.setFont("Helvetica", 10)
    total = 0

    # Filas de activos
    for a in activos:
        if y < 50:
            c.showPage()
            y = height - 50

        c.drawString(col_x[0], y, str(a[0]))
        c.drawString(col_x[1], y, a[1])
        c.drawString(col_x[2], y, a[2][:30])
        c.drawString(col_x[3], y, a[3])
        c.drawString(col_x[4], y, a[4])
        c.drawRightString(col_x[5] + 60, y, f"Q {a[5]:,.2f}")
        total += a[5]
        y -= 18

    # Total
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 50, y, f"Total de activos: Q {total:,.2f}")

    c.save()
