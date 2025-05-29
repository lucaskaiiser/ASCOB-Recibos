from src.models import Receipt

def show_new_receipt_window():
    from src.windows import NewReceiptWindow
    new_receipt_window = NewReceiptWindow()
    new_receipt_window.mainloop()

def show_edit_receipt_window():
    from src.windows import EditReceiptWindow
    edit_receipt_window = EditReceiptWindow()
    edit_receipt_window.mainloop()

def show_search_receipt_window():
    from src.windows import SearchReceiptWindow
    search_receipt_window = SearchReceiptWindow()
    search_receipt_window.mainloop()

