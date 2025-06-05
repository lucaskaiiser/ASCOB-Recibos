def show_new_receipt_window():
    from src.windows import NewReceiptWindow
    new_receipt_window = NewReceiptWindow()
    new_receipt_window.grab_set()
    new_receipt_window.transient(new_receipt_window.master)
    new_receipt_window.master.wait_window(new_receipt_window)
    new_receipt_window.mainloop()

def show_edit_receipt_window(receipt_data, master=None):
    from src.windows import EditReceiptWindow
    edit_receipt_window = EditReceiptWindow(receipt_data)
    edit_receipt_window.transient(master or edit_receipt_window.master)
    edit_receipt_window.grab_set()
    master.wait_window(edit_receipt_window)
    

def show_search_receipt_window():
    from src.windows import SearchReceiptWindow
    search_receipt_window = SearchReceiptWindow()
    search_receipt_window.grab_set()
    search_receipt_window.transient(search_receipt_window.master)
    search_receipt_window.master.wait_window(search_receipt_window)
    

def get_receipt(receipt_id):
    from src.models import Receipt
    receipt = Receipt.get_by_id(receipt_id)
    return receipt

def get_all_receipts():
    from src.models import Receipt
    receipts = Receipt.select(
        Receipt.id,
        Receipt.date,
        Receipt.value,
        Receipt.client_name,
        Receipt.debtor
    ).order_by(Receipt.id.desc()).tuples()
    return receipts
def search_receipts(client=None, debtor=None, date=None):
    from src.models import Receipt
    query = Receipt.select()
    filters = []

    if client:
        filters.append(Receipt.client_name.contains(client))
    if debtor:
        filters.append(Receipt.debtor.contains(debtor))
    if date:
        filters.append(Receipt.date == date)

    query = query.where(*filters)
    return query

