from src.models import Receipt
from datetime import datetime
from src.managers import print_manager

def get_receipt(receipt_id):
    return Receipt.get_by_id(receipt_id)


def get_all_receipts():
    receipts = Receipt.select(
        Receipt.id,
        Receipt.date,
        Receipt.value,
        Receipt.client_name,
        Receipt.debtor
    ).order_by(Receipt.id.desc()).tuples()

    results = []
    for item in receipts:
        item = list(item)
        item[1] = item[1].strftime('%d/%m/%Y')
        item[2] = 'R$ ' + print_manager._convert_float_to_br_finance(item[2])
        results.append(item)
    return results



def search_receipts(client=None, debtor=None, date=None):
    query = Receipt.select(
        Receipt.id,
        Receipt.date,
        Receipt.value,
        Receipt.client_name,
        Receipt.debtor).order_by(Receipt.id.desc())
    filters = []

    if date:
        date_obj = datetime.strptime(date, "%d/%m/%Y").date()
        filters.append(Receipt.date == date_obj)
    if client:
        filters.append(Receipt.client_name.contains(client))
    if debtor:
        filters.append(Receipt.debtor.contains(debtor))

    if filters:
        query = query.where(*filters)

    results = []

    for item in query.tuples():
        item = list(item)
        item[1] = item[1].strftime('%d/%m/%Y')
        item[2] = 'R$ ' + print_manager._convert_float_to_br_finance(item[2])
        results.append(item)

    return results

def delete_receipt(receipt_id):
    Receipt.delete_by_id(receipt_id)

def edit_receipt(receipt_id, new_data):
    for item, value in new_data.items():
        try:
            new_data[item] = value.strip()
        except:
            pass

    query = Receipt.update(
        **new_data
    ).where(Receipt.id == receipt_id)

    print(query)
    query.execute()

def render_pdf(receipt_data):
    print_manager.render_pdf(receipt_data)

def print_pdf(receipt_data):
    print_manager.print_pdf_async(receipt_data)