import tkinter as tk
from tkinter import messagebox

from app.forms.utils import RegistrationValidator
from app.widgets import MainWindow

from ..database import get_session
from ..models.utils import register_user, authenticate_user

class RegistrationWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Регистрация")
        self.root.geometry('500x300')
        self.root.anchor('center')
        self.root.configure(bg="lightblue")

        self.login_label = tk.Label(self.root, text="Логин:", font=("Arial", 10), bg="lightblue")
        self.login_label.grid(row=0, column=0, sticky="e", pady=3, padx=1)
        self.login_entry = tk.Entry(self.root, font=("Arial", 10))
        self.login_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.root, text="Пароль:", font=("Arial", 10), bg="lightblue")
        self.password_label.grid(row=1, column=0, sticky="e", pady=3, padx=1)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 10))
        self.password_entry.grid(row=1, column=1)

        self.surname_label = tk.Label(self.root, text="Фамилия:", font=("Arial", 10), bg="lightblue")
        self.surname_label.grid(row=2, column=0, sticky="e", pady=3, padx=1)
        self.surname_entry = tk.Entry(self.root, font=("Arial", 10))
        self.surname_entry.grid(row=2, column=1)

        self.name_label = tk.Label(self.root, text="Имя:", font=("Arial", 10), bg="lightblue")
        self.name_label.grid(row=3, column=0, sticky="e", pady=3, padx=1)
        self.name_entry = tk.Entry(self.root, font=("Arial", 10))
        self.name_entry.grid(row=3, column=1)

        self.patronymic_label = tk.Label(self.root, text="Отчество:", font=("Arial", 10), bg="lightblue")
        self.patronymic_label.grid(row=4, column=0, sticky="e", pady=3, padx=1)
        self.patronymic_entry = tk.Entry(self.root, font=("Arial", 10))
        self.patronymic_entry.grid(row=4, column=1)

        self.register_button = tk.Button(self.root, text="Зарегистрироваться", command=self.register, font=("Arial", 10), bg="white")
        self.register_button.grid(row=5, pady=9, columnspan=2)

        self.have_account_label = tk.Label(self.root, text="Уже есть аккаунт", font=("Arial", 10), fg="blue", cursor="hand2", bg="lightblue", foreground="black")
        self.have_account_label.grid(row=6, columnspan=2, pady=2)
        self.have_account_label.bind("<Button-1>", self.open_login_window)

    def register(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get().capitalize()
        surname = self.surname_entry.get().capitalize()
        patronymic = self.patronymic_entry.get().capitalize()

        validator = RegistrationValidator(login, password, name, surname, patronymic)
        is_valid, errors = validator.validate()

        if is_valid:
            register_user(get_session(), login, password, name, surname, patronymic)
            messagebox.showinfo("Успешная регистрация", "Пользователь зарегистрирован!")
        else:
            messagebox.showerror("Ошибка регистрации", errors[0])

    def open_login_window(self, event):
        self.root.destroy()
        login_window = LoginWindow()
        login_window.run()

    def run(self):
        self.root.mainloop()

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Авторизация")
        self.root.geometry('500x300')
        self.root.anchor('center')
        self.root.configure(bg="lightblue")
        

        self.login_label = tk.Label(self.root, text="Логин:", font=("Arial", 10), bg="lightblue")
        self.login_label.grid(row=0, column=0, sticky="e", pady=3, padx=1)
        
        self.login_entry = tk.Entry(self.root, width=15, font=("Arial", 10))
        self.login_entry.grid(row=0, column=1, pady=3, padx=1)

        self.password_label = tk.Label(self.root, text="Пароль:", font=("Arial", 10), bg="lightblue")
        self.password_label.grid(row=1, column=0, sticky="e", pady=9, padx=1)
        
        self.password_entry = tk.Entry(self.root, show="*", width=15, font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, pady=1, padx=1)

        self.login_button = tk.Button(self.root, text="Войти", command=self.login, width=10, height=1, font=("Arial", 10), bg="white")
        self.login_button.grid(row=2, columnspan=2, pady=5)

        self.have_account_label = tk.Label(self.root, text="У вас ещё нет аккаунта?", font=("Arial", 10), fg="blue", cursor="hand2", bg="lightblue", foreground="black")
        self.have_account_label.grid(row=3, columnspan=2, pady=5)
        self.have_account_label.bind("<Button-1>", self.open_registration_window)

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        session = get_session()
        user = authenticate_user(session, login, password)

        if user:
            messagebox.showinfo("Успешная авторизация", f"Добро пожаловать, {user.full_name}!")
            self.root.destroy()
            main_window = MainWindow(user)
            main_window.run()
        else:
            messagebox.showerror("Ошибка авторизации", "Неверный логин или пароль")

    def open_registration_window(self, event):
        self.root.destroy()
        login_window = RegistrationWindow()
        login_window.run()

    def run(self):
        self.root.mainloop()
