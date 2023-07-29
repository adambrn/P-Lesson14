""" Доработаем задачи 3 и 4. Создайте класс Project, содержащий атрибуты – список пользователей проекта и админ проекта. Класс имеет следующие методы:
Классовый метод загрузки данных из JSON файла (из второй задачи 8 семинара)
Метод входа в систему – требует указать имя и id пользователя. Далее метод создает пользователя и проверяет есть ли он в списке пользователей проекта. Если в списке его нет, то вызывается исключение доступа. Если пользователь присутствует в списке пользователей проекта, то пользователь, который входит получает его уровень доступа и становится администратором.
Метод добавление пользователя в список пользователей. Если уровень пользователя меньше, чем уровень админа, вызывайте исключение уровня доступа.
* метод удаления пользователя из списка пользователей проекта
* метод сохранения списка пользователей в JSON файл при выходе из контекстного менеджера """

import json
import os
from exceptions import AccessError, LevelError, IDError
from users import User

class Project:
    def __init__(self):
        self.users = []
        self.admin = None

    @classmethod
    def load_users_from_json(cls, filename):
        if not os.path.exists(filename):
            # Если файл не существует, создаем пустой файл с пустым словарем
            with open(filename, 'w') as file:
                json.dump({}, file)
        with open(filename, 'r') as file:
            data = json.load(file)
            project = cls()
            project.json_file = filename #сохраняем в классе имя файла
            for access_level, users_data in data.items():
                for identifier, name in users_data.items():
                    user = User(name, int(identifier), int(access_level))
                    project.users.append(user)
            return project

    def login(self, name, identifier):
        login_user = User(name, identifier)
        if login_user in self.users:
            self.admin = self.users[self.users.index(login_user)]
        else:
            raise AccessError(name, identifier)

    def add_user(self, name, identifier, access_level):
        new_user = User(name, identifier, access_level)

        if new_user in self.users:
            raise IDError(identifier)

        if self.admin and access_level < self.admin.access_level:
            raise LevelError(access_level, self.admin.access_level)
        self.users.append(new_user)

    def remove_user(self, name, identifier):
        user_to_remove = User(name, identifier)
        if user_to_remove in self.users:
            self.users.remove(user_to_remove)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save_users_to_json()

    def save_users_to_json(self):
        data = {}
        for user in self.users:
            access_level = user.access_level
            identifier = user.identifier
            name = user.name
            if access_level not in data:
                data[access_level] = {}
            data[access_level][identifier] = name

        with open(self.json_file, 'w') as file:
            json.dump(data, file, indent=2)

if __name__ == "__main__":
   
    with Project.load_users_from_json("users.json") as project:

        #project.login("John Doe", 123)
        #print(f"Logged in as admin: {project.admin}")

        project.add_user("Jane Smith", 456, access_level=5)
        project.login("Jane Smith", 456)
        print(f"Logged in as admin: {project.admin}")

        #project.add_user("John Doe", 123, access_level=4)
        #project.remove_user("John Doe", 123)

        project.remove_user("Jane Smith", 555)
        print(*project.users)



