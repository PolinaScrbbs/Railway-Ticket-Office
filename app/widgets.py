import tkinter as tk
from tkinter.ttk import Notebook, Frame, Label

from app.database import get_session
from models.flight.utils import get_all_flights
from models.user.models import Role
from .windows.profile import ProfileWindow

class MainWindow:
    def __init__(self, user):
        self.user = user
        self.flights = get_all_flights(get_session())
    
        self.root = tk.Tk()
        self.root.title("Главное окно")

        tab_control = Notebook(self.root)

        self.main_tab = Frame(tab_control)
        self.profile_tab = Frame(tab_control)

        tab_control.add(self.main_tab, text="Главная")
        tab_control.add(self.profile_tab, text="Профиль")

        for flight in self.flights:
            lb = Label(self.main_tab, text=f"Откуда: {flight.from_location.title}, Куда: {flight.to_location.title}, Номер поезда: {flight.train.number}")
            lb.grid(column=0, row=0)

        self.profile(user)

        tab_control.pack(expand=1, fill="both")

    def profile(self, user):
        full_name = self.user.full_name()
        full_name = Label(self.profile_tab, text=f"ФИО : {full_name}")
        full_name.grid(column=0, row=0)

        role = "Администратор" if user.role == Role.ADMIN else "Пользователь"
        role = Label(self.profile_tab, text=f"Роль: {role}")
        role.grid(column=0, row=1)

    def switch_to_profile(self):
        self.tab1.grid_remove()  # Убираем отображение первой вкладки
        self.profile_window = ProfileWindow(self.tab2, self.user)  # Создаем ProfileWindow на второй вкладке
        self.profile_window.run()

    def switch_to_main(self):
        if hasattr(self, 'profile_window'):  # Проверяем, существует ли атрибут profile_window
            self.profile_window.close()  # Закрываем ProfileWindow, если оно открыто
        self.tab1.grid()  # Отображаем первую вкладку

    def run(self):
        self.root.mainloop()
