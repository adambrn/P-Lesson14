#Создайте класс с базовым исключением и дочерние классы-исключения: ошибка уровня, ошибка доступа.

class UserException(Exception):
    pass

class LevelError(UserException):
    def __init__(self, access_level, admin_access_level):
        self.access_level = access_level
        self.admin_access_level = admin_access_level
    
    def __str__(self):
        return f"Уровень доступа пользователя ({self.access_level}) ниже уровня доступа администратора ({self.admin_access_level})."
        

class AccessError(UserException):
    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier
    
    def __str__(self):
        return f"Пользователь '{self.name}' с идентификатором {self.identifier} не имеет доступ к проекту."
       

class IDError(UserException):
    def __init__(self, identifier):
        self.identifier = identifier
    def __str__(self):
        return f"Пользователь с идентификатором {self.identifier} уже существует."
      

