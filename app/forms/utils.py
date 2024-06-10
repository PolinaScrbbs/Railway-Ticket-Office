import re

class RegistrationValidator:
    def __init__(self, login: str, password: str, name: str, surname: str, patronymic: str):
        self.login = login
        self.password = password
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.errors = []

    def validate_login(self):
        if not self.login:
            self.errors.append("Логин не может быть пустым.")
        elif len(self.login) < 3:
            self.errors.append("Логин должен содержать не менее 3 символов.")
        elif len(self.login) > 20:
            self.errors.append("Логин должен содержать не более 20 символов.")
        elif not re.match("^[a-zA-Z0-9]+$", self.login):
            self.errors.append("Логин может содержать только латинские буквы и цифры.")
        elif not re.search("[a-z]", self.login):
            self.errors.append("Логин должен содержать хотя бы одну строчную букву.")
        elif not re.search("[A-Z]", self.login):
            self.errors.append("Логин должен содержать хотя бы одну заглавную букву.")
        return not bool(self.errors)

    def validate_password(self):
        if not self.password:
            self.errors.append("Пароль не может быть пустым.")
        elif len(self.password) < 8:
            self.errors.append("Пароль должен содержать не менее 8 символов.")
        elif not re.search("[a-z]", self.password):
            self.errors.append("Пароль должен содержать хотя бы одну строчную букву.")
        elif not re.search("[A-Z]", self.password):
            self.errors.append("Пароль должен содержать хотя бы одну заглавную букву.")
        elif not re.search("[0-9]", self.password):
            self.errors.append("Пароль должен содержать хотя бы одну цифру.")
        elif not re.search("[!@#$%^&*()_+-=]", self.password):
            self.errors.append("Пароль должен содержать хотя бы один специальный символ.")
        return not bool(self.errors)

    def validate_name(self):
        if not self.name:
            self.errors.append("Имя не может быть пустым.")
        elif not re.match("^[А-Яа-яЁё]+$", self.name):
            self.errors.append("Имя может содержать только русские буквы.")
        return not bool(self.errors)

    def validate_surname(self):
        if not self.surname:
            self.errors.append("Фамилия не может быть пустой.")
        elif not re.match("^[А-Яа-яЁё]+$", self.surname):
            self.errors.append("Фамилия может содержать только русские буквы.")
        return not bool(self.errors)

    def validate_patronymic(self):
        if not self.patronymic:
            self.errors.append("Отчество не может быть пустым.")
        elif not re.match("^[А-Яа-яЁё]+$", self.patronymic):
            self.errors.append("Отчество может содержать только русские буквы.")
        return not bool(self.errors)

    def validate(self):
        self.errors = []
        self.validate_login()
        self.validate_password()
        self.validate_name()
        self.validate_surname()
        self.validate_patronymic()
        return not bool(self.errors), self.errors

