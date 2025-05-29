from src.models import start_database_connection
from src.windows import MainWindow

start_database_connection()

main_window = MainWindow()
main_window.mainloop()