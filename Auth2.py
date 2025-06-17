import hashlib
import uuid

class User:
    """
    Базовый класс, представляющий пользователя.
    """
    users = []  # Список для хранения всех пользователей

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        User.users.append(self)  # Добавляем пользователя в список

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check_password(stored_password, provided_password):
        """
        Проверка пароля.
        """
        return stored_password == provided_password

    def get_details(self):
        return self.__doc__

class Customer(User):
    """
    Класс, представляющий клиента, наследующий класс User.
    """
    def __init__(self, username, email, password, address):
        super().__init__(username, email, password)  # Вызов конструктора родителя
        self.address = address  # Установка атрибута address

    def get_details(self):
        return self.__doc__

class Admin(User):
    """
    Класс, представляющий администратора, наследующий класс User.
    """
    def __init__(self, username, email, password, admin_level):
        super().__init__(username, email, password)  # Вызов конструктора родителя
        self.admin_level = admin_level  # Установка атрибута admin_level

    def get_details(self):
        return self.__doc__

    @classmethod
    def list_users(cls):
        """
        Выводит список всех пользователей.
        """
        for user in User.users:
            print('Имя:', user.username, '\nEmail:', user.email, '\nТип:', user.__class__.__name__, '\n')

    @classmethod
    def delete_user(cls, username):
        """
        Удаляет пользователя по имени пользователя.
        """
        for i, user in enumerate(User.users):
            if user.username == username:
                del User.users[i]
                print(f"Пользователь {username} удалён")
                return
        print(f"Пользователь {username} не найден")

class AuthenticationService:
    """
    Сервис для управления регистрацией и аутентификацией пользователей.
    """
    def __init__(self):
        self.session_user = None  # Текущий пользователь
        self.session_hash = None  # Хеш сессии

    def register(self, user_class, username, email, password, *args):
        """
        Регистрация нового пользователя.
        """
        # Проверка уникальности username
        if any(user.username == username for user in User.users):
            print(f"Ошибка: Имя пользователя '{username}' занято")
            return False
        
        # Создание пользователя
        new_user = user_class(username, email, self.hash_password(password), *args)
        print(f"Пользователь {username} зарегистрирован")
        return True

    def login(self, username, password):
        """
        Аутентификация пользователя.
        """
        for user in User.users:
            if user.username == username:
                if user.password == self.hash_password(password):
                    self.session_user = user
                    self.session_hash = uuid.uuid4()
                    print(f"Вход выполнен: {username} ({user.__class__.__name__})")
                    return True
                else:
                    print("Ошибка: Неверный пароль")
                    return False
        print("Ошибка: Пользователь не найден")
        return False

    def logout(self):
        """
        Выход пользователя из системы.
        """
        if self.session_user:
            print(f"Выход: {self.session_user.username}")
            self.session_user = None
            self.session_hash = None
        else:
            print("Ошибка: Нет активной сессии")

    def get_current_user(self):
        """
        Возвращает текущего вошедшего пользователя.
        """
        if self.session_user:
            print(f"Текущий пользователь: {self.session_user.username} ({self.session_user.__class__.__name__})")
        else:
            print("Ошибка: Нет активной сессии")

    @staticmethod
    def hash_password(password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()



# Пример
auth_service = AuthenticationService()

# Регистрируем клиента
auth_service.register(Customer, "alice", "alice@example.com", "pass123", "ул. Центральная, 1")
print("---")

# Регистрируем администратора
auth_service.register(Admin, "admin", "admin@example.com", "adminPass", "super")
print("---")

# Неудачная регистрация (дубликат)
auth_service.register(Customer, "alice", "alice2@example.com", "pass456", "ул. Новая, 2")
print("---")

# Вход клиента
auth_service.login("alice", "pass123")
auth_service.get_current_user()
print("---")

# Выход
auth_service.logout()
auth_service.get_current_user()
print("---")

# Вход администратора
auth_service.login("admin", "adminPass")
auth_service.get_current_user()
print("---")

# Администратор смотрит список пользователей
print("Список пользователей:")
Admin.list_users()
print("---")

# Администратор удаляет клиента
Admin.delete_user("alice")
print("---")

# Обновленный список
print("Обновленный список:")
Admin.list_users()
print("---")

# Попытка входа удаленного пользователя
auth_service.logout()
auth_service.login("alice", "pass123")