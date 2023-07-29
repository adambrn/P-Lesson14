""" На семинаре 13 был создан проект по работе с пользователями (имя, id, уровень).
Напишите 3-7 тестов pytest для данного проекта.
Используйте фикстуры. """

import pytest
import os
import json
from projects import Project
from exceptions import AccessError, LevelError
from users import User


@pytest.fixture
def empty_project():
    # Создаем пустой экземпляр проекта для тестирования
    project = Project()
    return project


@pytest.fixture
def loaded_project(tmp_path):
    # Создаем временный файл JSON с примерами данных пользователей
    data = {
        "1": {"123": "John Doe", "2":"user"},
        "2": {"456": "Jane Smith"},
        "7": {"1":"admin"}
    }
    filename = tmp_path / "test_users.json"
    with open(filename, "w") as file:
        json.dump(data, file)

    project = Project.load_users_from_json(filename)
    return project


def test_empty_project_login(empty_project):
    # вход в пустой проект должно вызывать AccessError
    with pytest.raises(AccessError):
        empty_project.login("John Doe", 123)


def test_loaded_project_login(loaded_project):
    loaded_project.login("John Doe", 123)
    assert loaded_project.admin is not None
    assert loaded_project.admin.name == "John Doe"
    assert loaded_project.admin.identifier == 123


def test_add_user_level(loaded_project):
    # уровень доступа
    with pytest.raises(LevelError):
        loaded_project.login("admin", 1)
        loaded_project.add_user("Jain Doe", 3, access_level=1)  

def test_remove_user(loaded_project):
    loaded_project.remove_user("John Doe", 123)
    assert len(loaded_project.users) == 3

    # удаление несуществующего пользователя не должно вызывать ошибок
    loaded_project.remove_user("Несуществующий Пользователь", 999)


def test_exit_save(tmp_path):
    # cохранения пользователей в JSON файл при выходе из контекста
    filename = tmp_path / "test_exit_users.json"
    with Project.load_users_from_json(filename) as project:
        project.add_user("John Doe", 123, access_level=1)
        project.add_user("Jane Smith", 456, access_level=2)
        assert len(project.users) == 2
    # перезагрузка 
    with Project.load_users_from_json(filename) as project:
        assert len(project.users) == 2


def test_user_equality():
    # cравнение User
    user1 = User("John Doe", 123)
    user2 = User("John Doe", 123)
    user3 = User("Jane Smith", 456)

    assert user1 == user2
    assert user1 != user3

if __name__ == '__main__':
    pytest.main(['-v'])