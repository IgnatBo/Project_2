class UserAlreadyExistsError(Exception):
    def __init__(self, user, message="Пользовтель уже существует"):
        self.user = user
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.user}"
    
class UserNotFoundError(Exception):
    def __init__(self, username, message="Пользовтель не найден"):
        self.username = username
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.username}"


class User:
    def __init__(self, username: str, email: str, age: int):
        self.username = username
        self.email = email
        self.age = age
    def __str__(self):
        return (f'Имя {self.username}. Остальное - секрет')
        
class UserManager: 
    def __init__(self):
        self.users={}  
    def add_user(self, user: User):
       if user.username in self.users:
           raise UserAlreadyExistsError(user)
       else:
           self.users[user.username]=user

           
    def remove_user(self, username: str):
        if username not in self.users:
            raise UserNotFoundError(username)
        else:
            del self.users[username]
            

        
    def find_user(self, username: str) -> User:
        if username not in self.users:
            raise UserNotFoundError(username)
        else:
            return self.users[username]
        
   
   
manager=UserManager()

vice=User('Vice', 'ff@ff.ru', 16)
mike=User('Mike', 'ff@ff111.ru', 17)
     
manager.add_user(vice)

try: 
    manager.add_user(vice)
except Exception as e:
    print(e)

try: 
    manager.remove_user('Mike')
except Exception as e:
    print(e)
    



try: 
    manager.find_user('Vice')
    manager.find_user('Mike')
except Exception as e:
    print(e)