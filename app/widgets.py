import tkinter as tk
from tkinter.ttk import Notebook, Frame, Label, Style, Treeview

from app.database import get_session
from models.flight.models import Flight
from models.flight.utils import get_all_flights
from models.reservation.models import Ticket
from models.user.models import Role
from .windows.profile import ProfileWindow

class MainWindow:
    def __init__(self, user):
        self.user = user
        self.session = get_session()
        self.flights = get_all_flights(self.session)

        self.root = tk.Tk()
        self.root.title("Главное окно")

        tab_control = Notebook(self.root)

        self.main_tab = Frame(tab_control)
        self.profile_tab = Frame(tab_control)

        tab_control.add(self.main_tab, text="Главная")
        tab_control.add(self.profile_tab, text="Профиль")

        # Создаем таблицу для отображения рейсов
        tree = Treeview(self.main_tab, columns=("From", "To", "Train Number", "Departure Time", "Arrival Time"), show="headings")
        tree.heading("From", text="Откуда")
        tree.heading("To", text="Куда")
        tree.heading("Train Number", text="Номер поезда")
        tree.heading("Departure Time", text="Начало рейса")
        tree.heading("Arrival Time", text="Прибытие в пункт назначения")
        tree.pack(fill="both", expand=True)

        style = Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Применяем стиль к конкретным столбцам таблицы
        for column in tree["columns"]:
            tree.column(column, anchor="center", width=150)  # Горизонтальное выравнивание по центру и установка ширины

        for flight in self.flights:
            tree.insert("", "end", values=(
                flight.from_location.title,
                flight.to_location.title,
                flight.train.number,
                flight.departure_time,
                flight.arrival_time
            ))

        # tree.bind("<<TreeviewSelect>>", self.tikets())

        self.profile(user)

        tab_control.pack(expand=1, fill="both")

    def profile(self, user):
        full_name = self.user.full_name()
        full_name_label = Label(self.profile_tab, text=f"ФИО: {full_name}")
        full_name_label.grid(column=0, row=0)

        role = "Администратор" if user.role == Role.ADMIN else "Пользователь"
        role_label = Label(self.profile_tab, text=f"Роль: {role}")
        role_label.grid(column=0, row=1)

    # def tikets(self):
    #     tree = Treeview(self.main_tab, columns=("Flight", "Seat", "Price", "Is Round Trip"), name="headings", show="headings")

    def run(self):
        self.root.mainloop()
        self.session.close()  # Закрываем сессию после завершения работы GUI
