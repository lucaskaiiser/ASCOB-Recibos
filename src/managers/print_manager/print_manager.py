from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
import locale
from num2words import num2words
from babel.dates import format_date
from datetime import date

hoje = date.today()

valor = 15000.50
reais = int(valor)
centavos = round((valor - reais) * 100)

extenso = f"{num2words(reais, lang='pt_BR')} reais"
if centavos:
    extenso += f" e {num2words(centavos, lang='pt_BR')} centavos"

try:    
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    print('impossivel usar locale brasileiro')

base_dir = os.path.dirname(__file__)
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir =  os.path.join(os.path.dirname(__file__), "static")
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template("receipt.html")

dados = {
    "receipt_id": "1395271".zfill(7),
    "debtor": "Fulano de Tal",
    "value": f'{valor:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."),
    "extenso": extenso.capitalize(),
    "address": "rua egito",
    "description": "Esta é uma descrição",
    "cobrador": "Evandro".upper(),
    "logo_dir": 'static/logo.png',
    "today":f'Manaus, {format_date(hoje, format='long', locale='pt_BR')}' 
    
}

html_renderizado = template.render(**dados)

#with open("recibo_renderizado.html", "w", encoding="utf-8") as f:
#    f.write(html_renderizado)

HTML(string=html_renderizado, base_url=base_dir).write_pdf("recibo.pdf")