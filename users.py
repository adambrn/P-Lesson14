""" Вспомните задачу из семинара 8 про сериализацию данных, где в бесконечном цикле запрашивали имя, личный идентификатор и уровень доступа (от 1 до 7).
Напишите класс пользователя, который хранит эти данные в свойствах экземпляра.
Реализуйте магический метод проверки на равенство пользователей """

class User:
    def __init__(self, name, identifier, access_level = None):
        self.name = name
        self.identifier = identifier
        if access_level:
            self.access_level = access_level
     

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.identifier == other.identifier
    
    def __str__(self):
        return f'user:{self.name} id:{self.identifier}' 
    
    def __repr__(self):
        return f"User('{self.name}','{self.identifier}','{self.access_level}')"


if __name__ == "__main__":
    print(User('Админ','1'))