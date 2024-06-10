import tkinter as tk
from tkinter.ttk import Notebook, Frame, Style, Treeview

from app.database import get_session
from .models.utils import get_all_flights
from .models.utils import get_flight_tickets
from .models.models import Role

class MainWindow:
    def on_tree_select(self, event):
        selected_items = event.widget.selection()
        if selected_items:
            selected_item = selected_items[0]
            item_values = event.widget.item(selected_item, "values")
            flight_id = item_values[0]
            self.completion_tickets_tree(flight_id)
            self.flight_tree.pack_forget()
            self.ticket_tree.pack(fill="both", expand=True)
            self.add_back_button()
            event.widget.selection_remove(selected_item)


    def __init__(self, user):
        self.init_variables(user)
        self.root = tk.Tk()
        self.root.title("Главное окно")
        tab_control = Notebook(self.root)
        self.main_tab = Frame(tab_control)
        self.profile_tab = Frame(tab_control)
        tab_control.add(self.main_tab, text="Главная")
        tab_control.add(self.profile_tab, text="Профиль")
        self.back_button = None
        self.style = Style()
        self.style.configure("Treeview", font=("Arial", 10), rowheight=30)
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        self.create_flight_tree(self.main_tab)
        self.completion_flight_tree()
        self.create_tickets_tree(self.main_tab)
        self.flight_tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.profile(user)
        tab_control.pack(expand=1, fill="both")

    def add_back_button(self):
        if self.back_button:
            self.back_button.destroy()

        self.back_button = tk.Button(self.main_tab, text="Назад", command=self.on_back_button_click)
        self.back_button.pack(side="top", pady=10)

    def on_back_button_click(self):
        self.ticket_tree.pack_forget()
        self.flight_tree.pack(fill="both", expand=True)
        self.back_button.destroy()

    def init_variables(self, user):
        self.user = user
        self.session = get_session()
        self.flights = get_all_flights(self.session)

    def profile(self, user):
        full_name = self.user.full_name()
        full_name_label = tk.Label(self.profile_tab, text=f"ФИО: {full_name}")
        full_name_label.grid(column=0, row=0)
        role = "Администратор" if user.role == Role.ADMIN else "Пользователь"
        role_label = tk.Label(self.profile_tab, text=f"Роль: {role}")
        role_label.grid(column=0, row=1)

    def add_style(self, tree):
        tree.configure(style="Treeview")
        for column in tree["columns"]:
            tree.column(column, anchor="center", width=150)
        tree.column("ID", width=0, stretch=tk.NO)

    def create_flight_tree(self, main_tab):
        self.flight_tree = Treeview(main_tab, columns=("ID", "Direction", "Train", "Travel Time"), show="headings")
        self.flight_tree.heading("ID", text="", anchor="center")
        self.flight_tree.heading("Direction", text="Направление")
        self.flight_tree.heading("Train", text="Поезд")
        self.flight_tree.heading("Travel Time", text="Время поездки")
        self.flight_tree.pack(fill="both", expand=True)

        self.add_style(self.flight_tree)

    def completion_flight_tree(self):
        for flight in self.flights:
            self.flight_tree.insert("", "end", values=(
                flight.id,
                flight.direction,
                flight.train.number,
                flight.travel_time
            ))

    def create_tickets_tree(self, main_tab):
        self.ticket_tree = Treeview(main_tab, columns=("ID", "Flight", "Seat", "Price", "Is Round Trip"), show="headings")
        self.ticket_tree.column("ID", width=0, stretch=tk.NO)
        self.ticket_tree.heading("ID", text="", anchor="center")
        self.ticket_tree.heading("Flight", text="Рейс")
        self.ticket_tree.heading("Seat", text="Номер места")
        self.ticket_tree.heading("Price", text="Цена")
        self.ticket_tree.heading("Is Round Trip", text="В оба конца")
        self.ticket_tree.pack(fill="both", expand=True)

        self.add_style(self.ticket_tree)
        self.ticket_tree.pack_forget()

    def completion_tickets_tree(self, flight_id):
        for item in self.ticket_tree.get_children():
            self.ticket_tree.delete(item)

        tickets = get_flight_tickets(self.session, flight_id)

        if tickets:
            for ticket in tickets:
                self.ticket_tree.insert("", "end", values=(
                    ticket.id,
                    ticket.flight.direction,
                    ticket.seat.number,
                    f"{ticket.price}₽",
                    "Да" if ticket.is_round_trip else "Нет"
                ))
        else:
            self.ticket_tree.insert("", "end", values=("Билетов нет", "", "", ""))

    def run(self):
        self.root.mainloop()
        self.session.close()
