import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

Font_name = 'FreeSans'
Font_ttf_name = 'FreeSans.ttf'
Font_size = 13
start_coordinates = 800
delta_coordinates = 15


def make_pdf(all_ingredients):
    buffer = io.BytesIO()
    needed_ingredients = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont(Font_name, Font_ttf_name))
    coordinates = start_coordinates
    needed_ingredients.setFont(Font_name, Font_size)
    for key, value in all_ingredients.items():
        string = f'{key}: {value}'
        needed_ingredients.drawString(100, coordinates, string)
        coordinates -= delta_coordinates

    needed_ingredients.showPage()
    needed_ingredients.save()
    buffer.seek(0)
    return buffer
