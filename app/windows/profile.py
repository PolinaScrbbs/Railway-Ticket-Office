import tkinter as tk

from models.user.models import Role

class ProfileWindow:
    def __init__(self, master, user):
        self.master = master
        self.master.title("User Profile")
        self.user = user
        
        # Display full name
        full_name = f'ФИО {user.full_name()}'
        self.full_name_label = tk.Label(master, text=full_name)
        self.full_name_label.pack()

        # Display role
        role = "Администратор" if user.role == Role.ADMIN else "Пользователь"
        role = f"Роль: {role}"
        self.role_label = tk.Label(master, text=role)
        self.role_label.pack()

    def run(self):
        self.master.mainloop()


