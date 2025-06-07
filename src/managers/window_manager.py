import sys
sys.path.append('')
from src.windows import (
    MainWindow,
    SearchReceiptWindow,
    EditReceiptWindow, 
    NewReceiptWindow
)

from src.controllers import (
    main_controller
)

class WindowManager:
    def __init__(self, root=None):
        self.root = root
        self.controller = main_controller

    def _show_toplevel_window(self, window, master=None):
        if master:
            window.transient(master)

        def grab_and_wait():
            window.grab_set()
            window.focus_set()
            (master or window.master).wait_window(window)

        window.after(100, grab_and_wait)
        window.resizable(False, False)

    def show_new_receipt_window(self, master=None):
        window = NewReceiptWindow(wm=self, master=master)
        self._show_toplevel_window(window, master)

    def show_edit_receipt_window(self, receipt_data, master=None):
        window = EditReceiptWindow(receipt_data, wm=self, master=master)
        self._show_toplevel_window(window, master)

    def show_search_receipt_window(self, master=None):
        window = SearchReceiptWindow(wm=self, master=master)
        self._show_toplevel_window(window, master)


if __name__ == '__main__':
    wm = WindowManager()
    main_window  = MainWindow(wm)
    wm.root = main_window
    main_window.mainloop()



    

            