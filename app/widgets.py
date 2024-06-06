import tkinter as tk

class MainWindow:
    def __init__(self, user):
        self.user = user

        self.root = tk.Tk()
        self.root.title("Главное окно")

        # Создаем навигационную панель
        self.create_navigation_bar()

        # Отображаем информацию об авторизованном пользователе
        self.display_user_info()

    def create_navigation_bar(self):
        self.navbar_frame = tk.Frame(self.root)
        self.navbar_frame.pack(side="top", fill="x")

        self.home_button = tk.Button(self.navbar_frame, text="Главная", command=self.show_home_page)
        self.home_button.pack(side="left")

        self.profile_button = tk.Button(self.navbar_frame, text="Профиль", command=self.show_profile_page)
        self.profile_button.pack(side="left")

        self.logout_button = tk.Button(self.navbar_frame, text="Выйти", command=self.logout)
        self.logout_button.pack(side="right")

    def display_user_info(self):
        user_info_label = tk.Label(self.root, text=f"Вы вошли как: {self.user.full_name()}")
        user_info_label.pack(side="top", anchor="ne")

    def show_home_page(self):
        # Здесь можно добавить код для отображения главной страницы
        pass

    def show_profile_page(self):
        # Здесь можно добавить код для отображения страницы профиля пользователя
        pass

    def logout(self):
        # Здесь можно добавить код для выхода из учетной записи
        pass

    def run(self):
        self.root.mainloop()