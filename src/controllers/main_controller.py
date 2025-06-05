from src.models import Receipt

def get_receipt(receipt_id):
    return Receipt.get_by_id(receipt_id)


def get_all_receipts():
    return Receipt.select(
        Receipt.id,
        Receipt.date,
        Receipt.value,
        Receipt.client_name,
        Receipt.debtor
    ).order_by(Receipt.id.desc()).tuples()


def search_receipts(client=None, debtor=None, date=None):
    query = Receipt.select(
        Receipt.id,
        Receipt.date,
        Receipt.value,
        Receipt.client_name,
        Receipt.debtor).order_by(Receipt.id.desc())
    filters = []

    if date:
        filters.append(Receipt.date == date)
    if client:
        filters.append(Receipt.client_name.contains(client))
    if debtor:
        filters.append(Receipt.debtor.contains(debtor))

    if filters:
        query = query.where(*filters)

    
    return query