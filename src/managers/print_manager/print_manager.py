from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
from num2words import num2words
from babel.dates import format_date
from datetime import date
import win32api
import tempfile
import threading
#import win32api

base_dir = os.path.dirname(__file__)
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir =  os.path.join(os.path.dirname(__file__), "static")
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template("receipt_cm.html")

def _format_today():
    today = date.today()
    return f'Manaus, {
        format_date(today, format='long', locale='pt_BR')
    }'

def _convert_value_to_words(value:float):
    reais = int(value)
    centavos = round((value - reais) * 100)

    extenso = f"{num2words(reais, lang='pt_BR')} reais"
    if centavos:
        extenso += f" e {num2words(centavos, lang='pt_BR')} centavos"
    
    return extenso.capitalize()

def _convert_float_to_br_finance(value:float):
    return f'{value:,.2f}'.replace(
        ",", "X"
    ).replace(
        ".", ","
    ).replace(
        "X", "."
    )

def _create_receipt_data_dict(receipt_data):
    dados = {
        "receipt_id": str(receipt_data['id']).zfill(7),
        "debtor": receipt_data['debtor'],
        "value": _convert_float_to_br_finance(receipt_data['value']),
        "extenso": _convert_value_to_words(receipt_data['value']),
        "address": receipt_data['address'],
        "description": receipt_data['description'],
        "cobrador": receipt_data['cobrador'].upper(),
        "logo_dir": 'static/logo.png',
        "today": _format_today()
    }

    return dados

def render_pdf(receipt_data):
    data_dict = _create_receipt_data_dict(receipt_data)
    html_renderizado = template.render(**data_dict)
    HTML(string=html_renderizado, base_url=base_dir).write_pdf("recibo.pdf")

def print_pdf_(receipt_data):
    data_dict = _create_receipt_data_dict(receipt_data)
    html_str = template.render(**data_dict)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        HTML(string=html_str).write_pdf(temp_pdf.name)

        
        win32api.ShellExecute(
            0,
            "print",
            temp_pdf.name,
            None,
            ".",
            0
        )

def print_pdf(receipt_data):
    import subprocess
    data_dict = _create_receipt_data_dict(receipt_data)
    html_str = template.render(**data_dict)
    sumatra_path = os.path.join(base_dir, 'bin', 'sumatra.exe')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        pdf_path = f'{temp_pdf.name}-{id(temp_pdf)}'
        HTML(string=html_str, base_url=base_dir).write_pdf(pdf_path)

    subprocess.run([
        sumatra_path,
        "-print-to-default",
        pdf_path
    ], check=True)

    os.remove(pdf_path)

def print_pdf_async(receipt_data):
    def task():
        try:
            print_pdf(receipt_data)
        except Exception as e:
            print(f"Erro na impressão: {e}")
    
    thread = threading.Thread(target=task, daemon=True)
    thread.start()