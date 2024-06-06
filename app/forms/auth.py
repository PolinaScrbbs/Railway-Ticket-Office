import tkinter as tk
from tkinter import messagebox

from app.widgets import MainWindow

from ..database import get_session
from models.user.utils import register_user, authenticate_user

class RegistrationWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Регистрация")

        # Логин
        self.login_label = tk.Label(self.root, text="Логин:")
        self.login_label.grid(row=0, column=0, sticky="w")
        self.login_entry = tk.Entry(self.root)
        self.login_entry.grid(row=0, column=1)

        # Пароль
        self.password_label = tk.Label(self.root, text="Пароль:")
        self.password_label.grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)

        # Имя
        self.name_label = tk.Label(self.root, text="Имя:")
        self.name_label.grid(row=2, column=0, sticky="w")
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=2, column=1)

        # Фамилия
        self.surname_label = tk.Label(self.root, text="Фамилия:")
        self.surname_label.grid(row=3, column=0, sticky="w")
        self.surname_entry = tk.Entry(self.root)
        self.surname_entry.grid(row=3, column=1)

        # Отчество
        self.patronymic_label = tk.Label(self.root, text="Отчество:")
        self.patronymic_label.grid(row=4, column=0, sticky="w")
        self.patronymic_entry = tk.Entry(self.root)
        self.patronymic_entry.grid(row=4, column=1)

        # Кнопка "Зарегистрироваться"
        self.register_button = tk.Button(self.root, text="Зарегистрироваться", command=self.register)
        self.register_button.grid(row=5, columnspan=2)

        # Кнопка "Уже есть аккаунт"
        self.have_account_button = tk.Button(self.root, text="Уже есть аккаунт", command=self.open_login_window)
        self.have_account_button.grid(row=6, columnspan=2)

    def register(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        patronymic = self.patronymic_entry.get()

        register_user(get_session(), login, password, name, surname, patronymic)

        messagebox.showinfo("Успешная регистрация", "Пользователь зарегистрирован!")

    def open_login_window(self):
        # Закрываем окно регистрации
        self.root.destroy()
        # Открываем окно авторизации
        login_window = LoginWindow()
        login_window.run()

    def run(self):
        self.root.mainloop()

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Авторизация")

        # Логин
        self.login_label = tk.Label(self.root, text="Логин:")
        self.login_label.grid(row=0, column=0, sticky="w")
        self.login_entry = tk.Entry(self.root)
        self.login_entry.grid(row=0, column=1)

        # Пароль
        self.password_label = tk.Label(self.root, text="Пароль:")
        self.password_label.grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)

        # Кнопка "Войти"
        self.login_button = tk.Button(self.root, text="Войти", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        # Кнопка "Уже есть аккаунт"
        self.have_account_button = tk.Button(self.root, text="У вас ещё нет аккаунта?", command=self.open_registration_window)
        self.have_account_button.grid(row=6, columnspan=2)

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        session = get_session()
        user = authenticate_user(session, login, password)

        if user:
            messagebox.showinfo("Успешная авторизация", f"Добро пожаловать, {user.full_name()}!")
            # Закрываем окно авторизации
            self.root.destroy()
            main_window = MainWindow(user)
            main_window.run()
        else:
            messagebox.showerror("Ошибка авторизации", "Неверный логин или пароль")

    def open_registration_window(self):
        # Закрываем окно регистрации
        self.root.destroy()
        # Открываем окно авторизации
        login_window = RegistrationWindow()
        login_window.run()

    def run(self):
        self.root.mainloop()
