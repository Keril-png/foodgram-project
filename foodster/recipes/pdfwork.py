import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

Font_name = 'FreeSans'
Font_ttf_name = 'FreeSans.ttf'

def make_pdf(all_ingredients):
    buffer = io.BytesIO()
    needed_ingredients = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont(Font_name, Font_ttf_name))
    coordinates = 800
    needed_ingredients.setFont(Font_name, 13)
    for key, value in all_ingredients.items():
        string = f'{key}: {value}'
        needed_ingredients.drawString(100, coordinates, string)
        coordinates-=15
    needed_ingredients.showPage()
    needed_ingredients.save()
    buffer.seek(0)
    return buffer