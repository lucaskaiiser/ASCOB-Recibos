from src.models import Receipt
from datetime import datetime

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
        results.append(item)

    return results

def delete_receipt(receipt_id):
    Receipt.delete_by_id(receipt_id)

def edit_receipt(receipt_id, new_data):
    print(new_data)

    query = Receipt.update(
        **new_data
    ).where(Receipt.id == receipt_id)

    print(query)
    query.execute()
    
