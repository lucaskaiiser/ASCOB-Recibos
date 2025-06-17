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

        window.withdraw()  

        def center_window_and_show():
            window.update_idletasks()  
            width = window.winfo_width()
            height = window.winfo_height()
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            window.geometry(f'{width}x{height}+{x}+{y}')

            window.deiconify()
            window.grab_set()
            window.focus_set()
            (master or window.master).wait_window(window)

        window.after(100, center_window_and_show)
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



    

            