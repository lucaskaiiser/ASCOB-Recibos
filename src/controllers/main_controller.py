def show_new_receipt_window():
    from src.windows import NewReceiptWindow
    new_receipt_window = NewReceiptWindow()
    new_receipt_window.grab_set()
    new_receipt_window.transient(new_receipt_window.master)
    new_receipt_window.master.wait_window(new_receipt_window)
    new_receipt_window.mainloop()

def show_edit_receipt_window():
    from src.windows import EditReceiptWindow
    edit_receipt_window = EditReceiptWindow()
    edit_receipt_window.transient(edit_receipt_window.master)
    edit_receipt_window.master.wait_window(edit_receipt_window)
    edit_receipt_window.mainloop()

def show_search_receipt_window():
    from src.windows import SearchReceiptWindow
    search_receipt_window = SearchReceiptWindow()
    search_receipt_window.grab_set()
    search_receipt_window.transient(search_receipt_window.master)
    search_receipt_window.master.wait_window(search_receipt_window)
    search_receipt_window.mainloop()

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