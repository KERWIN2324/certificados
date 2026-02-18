# src/utils.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from datetime import date

def generar_certificado(user, curso):
    carpeta = os.path.join('src', 'static', 'certificados')
    os.makedirs(carpeta, exist_ok=True)

    nombre_pdf = f"{user.username}_{curso.nombre_curso}.pdf".replace(" ", "_")
    ruta_pdf = os.path.join(carpeta, nombre_pdf)

    c = canvas.Canvas(ruta_pdf, pagesize=A4)
    ancho, alto = A4

    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(ancho/2, alto-200, "CERTIFICADO DE APROBACIÓN")

    c.setFont("Helvetica", 18)
    c.drawCentredString(ancho/2, alto-300, f"Se otorga a: {user.username}")
    c.drawCentredString(ancho/2, alto-350, f"Por aprobar el curso: {curso.nombre_curso}")
    c.drawCentredString(ancho/2, alto-400, f"Fecha: {date.today().strftime('%d/%m/%Y')}")

    c.showPage()
    c.save()

    return f"certificados/{nombre_pdf}"
