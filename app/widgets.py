import tkinter as tk
from tkinter import Button
from tkinter import messagebox
from tkinter.ttk import Notebook, Frame, Style, Treeview
from tkinter.font import Font

from app.database import get_session
from .models.utils import (
    create_reservation, formatted_time, get_all_flights, get_available_tickets, 
    get_reservations, get_user_reservations)
from .models.models import Role

class MainWindow:
    def __init__(self, user):
        self.init_variables(user)
        self.create_flight_tree(self.main_tab)
        self.create_tickets_tree(self.main_tab)
        self.create_reservation_tree(self.reservation_tab)
        self.profile(user)
        
    def add_back_button(self):
        if self.back_button:
            self.back_button.destroy()

        self.back_button = Button(self.main_tab, text="Назад", command=self.on_back_button_click)
        self.back_button.pack(side="top", pady=10)

    def on_back_button_click(self):
        self.ticket_tree.pack_forget()
        self.flight_tree.pack(fill="both", expand=True)
        self.back_button.destroy()

    def init_variables(self, user):
        self.session = get_session()
        self.user = user
        self.flights = get_all_flights(self.session)
        if self.user.role == Role.ADMIN:
            self.reservation = get_reservations(self.session)
        else:
            self.reservation = get_user_reservations(self.session, user.id)

        self.root = tk.Tk()
        self.root.title("Железнодорожная касса")
        self.root.geometry('1100x700')
        self.root.anchor("center")
        self.root.configure(bg="white")

        self.tab_control = Notebook(self.root)
        self.main_tab = Frame(self.tab_control)
        self.reservation_tab = Frame(self.tab_control)
        self.profile_tab = Frame(self.tab_control)

        self.tab_control.add(self.main_tab, text="Рейсы")
        self.tab_control.add(self.reservation_tab, text="Брони")
        self.tab_control.add(self.profile_tab, text="Профиль")
        self.tab_control.pack(expand=1, fill="both")

        self.back_button = None

        self.style = Style()
        self.style.configure("Treeview", font=("Arial", 10), rowheight=30)
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        self.bold_font = Font()
        self.bold_font.configure(weight="bold", size=12)

    def refresh(self):
        self.root.destroy()
        self.__init__(self.user)

    def profile(self, user):
        # Получение полного имени пользователя
        full_name = self.user.full_name
        
        # Создание метки для отображения полного имени пользователя
        full_name_label = tk.Label(self.profile_tab, text=f"ФИО: {full_name}", font=("Arial", 12))
        full_name_label.grid(column=0, row=0, padx=10, pady=5, sticky="w")

        # Определение роли пользователя
        role = "Администратор" if user.role == Role.ADMIN else "Пользователь"
        
        # Создание метки для отображения роли пользователя
        role_label = tk.Label(self.profile_tab, text=f"Роль: {role}", font=("Arial", 12))
        role_label.grid(column=0, row=1, padx=10, pady=5, sticky="w")

    def add_style(self, tree):
        tree.configure(style="Treeview")
        for column in tree["columns"]:
            tree.column(column, anchor="center", width=150)
        tree.column("ID", width=0, stretch=tk.NO)

    def select_flight_tickets(self, event):
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

    def create_flight_tree(self, tab):
        self.flight_tree = Treeview(tab, columns=("ID", "Direction", "Train", "Travel Time"), show="headings")
        self.flight_tree.heading("ID", text="", anchor="center")
        self.flight_tree.heading("Direction", text="Направление")
        self.flight_tree.heading("Train", text="Поезд")
        self.flight_tree.heading("Travel Time", text="Время поездки")
        self.flight_tree.pack(fill="both", expand=True)

        self.add_style(self.flight_tree)
        self.flight_tree.bind('<<TreeviewSelect>>', self.select_flight_tickets)

        self.completion_flight_tree()

    def completion_flight_tree(self):
        for flight in self.flights:
            self.flight_tree.insert("", "end", values=(
                flight.id,
                flight.direction,
                flight.train.number,
                f"{formatted_time(flight.departure_time)} - {formatted_time(flight.arrival_time)}"
            ))

    def select_ticket(self, event):
        selected_items = event.widget.selection()
        if selected_items:
            selected_item = selected_items[0]
            item_values = event.widget.item(selected_item, "values")

            confirmation_message = f"Вы хотите забронировать билет: Вагон {item_values[2]}({item_values[3]}), Место {item_values[4]}, {item_values[1]}?"
            user_response = messagebox.askyesno("Подтверждение бронирования", confirmation_message)

            if user_response:
                create_reservation(self.session, item_values[0], self.user.id)
                self.refresh()
                    
    def create_tickets_tree(self, tab):

        self.ticket_tree = Treeview(tab, columns=("ID", "Flight", "Carriage", "CarriageType", "Seat", "Price", "Is Round Trip"), show="headings")
        self.ticket_tree.heading("ID", text="", anchor="center")
        self.ticket_tree.heading("Flight", text="Рейс")
        self.ticket_tree.heading("Carriage", text="Вагон")
        self.ticket_tree.heading("CarriageType", text="Тип вагона", command=self.sort_by_carriage_type)
        self.ticket_tree.heading("Seat", text="Номер места")
        self.ticket_tree.heading("Price", text="Цена")
        self.ticket_tree.heading("Is Round Trip", text="В оба конца")
        self.ticket_tree.pack(fill="both", expand=True)

        self.add_style(self.ticket_tree)
        self.ticket_tree.bind('<<TreeviewSelect>>', self.select_ticket)

        self.ticket_tree.pack_forget()

    def completion_tickets_tree(self, flight_id):
        for item in self.ticket_tree.get_children():
            self.ticket_tree.delete(item)

        tickets = get_available_tickets(self.session, flight_id)

        for ticket in tickets:
            self.ticket_tree.insert("", "end", values=(
                ticket.id,
                ticket.flight.direction,
                ticket.seat.carriage.number,
                ticket.seat.carriage.get_type(),
                ticket.seat.number,
                f"{ticket.price}₽",
                "Да" if ticket.is_round_trip else "Нет",
            ))

    def sort_by_carriage_type(self):
        data = [(self.ticket_tree.set(child, "CarriageType"), child) for child in self.ticket_tree.get_children("")]
        self.sort_descending = not getattr(self, 'sort_descending', False)
        data.sort(reverse=self.sort_descending)
        for index, (val, child) in enumerate(data):
            self.ticket_tree.move(child, '', index)

    def create_reservation_tree(self, tab):
        if self.reservation == []:
            lb = tk.Label(self.reservation_tab, text=f"Брони отсутствуют", font=self.bold_font)
            lb.grid(column=0, row=0)

        else:
            self.reservation_tree = Treeview(tab, columns=("ID", "Ticket", "User", "Date"), show="headings")
            self.reservation_tree.heading("ID", text="", anchor="center")
            self.reservation_tree.heading("Ticket", text="Номер билета")
            self.reservation_tree.heading("User", text="Пользователь")
            self.reservation_tree.heading("Date", text="Дата брони")
            self.reservation_tree.pack(fill="both", expand=True)

            self.add_style(self.reservation_tree)

            self.completion_reservation_tree()
            
    def completion_reservation_tree(self):
        for reservation in self.reservation:
            self.reservation_tree.insert("", "end", values=(
                reservation.id,
                reservation.ticket.ticket_number,
                reservation.user.full_name,
                formatted_time(reservation.date)
            ))

    def run(self):
        self.root.mainloop()
        self.session.close()
