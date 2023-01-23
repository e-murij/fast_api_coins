import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db, Base
from fake_data_db_test.fill_db import fill_db_fake_data
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False,
                              bind=engine)


@pytest.fixture(scope="function")
def app_start():
    """
    Создание новой базы для тестированя и ее удаление после каждого теста
    """
    Base.metadata.create_all(engine)
    yield app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app_start):
    """
    Подключение к тестовой базе и наполнениение ее даными
    """
    connection = engine.connect()
    session = SessionTesting(bind=connection)
    fill_db_fake_data("fake_data_db_test/fake_tests_data.json", session)
    yield session


@pytest.fixture(scope="function")
def client(app_start, db_session):
    """
    Создание TestClient с подключением к тестовой базе
    """

    def get_db_test():
        db = SessionTesting()
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = get_db_test
    with TestClient(app) as client:
        yield client


def get_cookies_superuser(client):
    """Авторизоваться как администратор"""
    request_data_user = {
        "username": "test",
        "is_superuser": True,
        "password": "test"
    }
    client.post("/api/user/register", json=request_data_user)
    response_user = client.post("/api/user/login", json=request_data_user)
    return response_user.cookies


def get_cookies_user(client):
    """Авторизоваться как пользователь"""
    request_data_user = {
        "username": "test",
        "is_superuser": False,
        "password": "test"
    }
    client.post("/api/user/register", json=request_data_user)
    response_user = client.post("/api/user/login", json=request_data_user)
    return response_user.cookies


def test_health_check(client):
    """
    Тест клиента
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "User"}


# Тестиование функций для подключения пользователей
def test_user_create_ok(client):
    """
    Создаем польователя с правильным набором данных
    """
    request_data = {
        "username": "test",
        "is_superuser": False,
        "password": "test"
    }
    response = client.post("/api/user/register", json=request_data)
    assert response.status_code == 201
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "user created"


def test_user_create_uncorrect_data(client):
    """
        Создаем пользователя с неполным набором данных
    """
    request_data = {
        "is_superuser": False,
        "password": "test"
    }
    response = client.post("/api/user/register", json=request_data)
    assert response.status_code == 422


def test_user_create_user_already_exists(client):
    """
        Создаем пользователя с username содержащимся в базе
    """
    request_data = {
        "username": "admin",
        "is_superuser": True,
        "password": "admin"
    }
    response = client.post("/api/user/register", json=request_data)
    assert response.status_code == 409


def test_user_login(client):
    """
        Логин пользователя
    """
    request_data = {
        "username": "test",
        "is_superuser": True,
        "password": "test"
    }
    client.post("/api/user/register", json=request_data)
    response = client.post("/api/user/login", json=request_data)
    assert response.status_code == 200
    assert response.cookies.get('logged_in') == 'True'


def test_user_logout(client):
    """
            Логаут пользователя
    """
    request_data = {
        "username": "test",
        "is_superuser": True,
        "password": "test"
    }
    client.post("/api/user/register", json=request_data)
    response = client.post("/api/user/login", json=request_data)
    response = client.get("/api/user/logout", cookies=response.cookies)
    assert response.status_code == 200


# Тестирование CRUD операций со словарями
def test_dict_post(client):
    """
       Создание новой записи в словарях
    """
    request_data = {
        "name": "test",
    }
    response = client.post("/api/dictionary/type", json=request_data)
    assert response.status_code == 201
    assert response.json().get('name') == 'test'

    response = client.post("/api/dictionary/currency", json=request_data)
    assert response.status_code == 201
    assert response.json().get('name') == 'test'

    response = client.post("/api/dictionary/md", json=request_data)
    assert response.status_code == 201
    assert response.json().get('name') == 'test'

    response = client.post("/api/dictionary/state", json=request_data)
    assert response.status_code == 201
    assert response.json().get('name') == 'test'


def test_dict_get(client):
    """
           Получение всех записей из словаря
    """
    response = client.get("/api/dictionary/type")
    assert response.status_code == 200
    assert len(response.json().get('type')) == 3

    response = client.get("/api/dictionary/currency")
    assert response.status_code == 200
    assert len(response.json().get('currency')) == 3

    response = client.get("/api/dictionary/md")
    assert response.status_code == 200
    assert len(response.json().get('md')) == 3

    response = client.get("/api/dictionary/state")
    assert response.status_code == 200
    assert len(response.json().get('state')) == 3


def test_dict_put(client):
    """
           Изменение записи в словарях
    """
    request_data = {
        "name": "test",
    }
    response = client.put("/api/dictionary/type/1", json=request_data)
    assert response.status_code == 200
    assert response.json().get('name') == 'test'
    assert response.json().get('id') == 1

    response = client.put("/api/dictionary/currency/1", json=request_data)
    assert response.status_code == 200
    assert response.json().get('name') == 'test'
    assert response.json().get('id') == 1

    response = client.put("/api/dictionary/md/1", json=request_data)
    assert response.status_code == 200
    assert response.json().get('name') == 'test'
    assert response.json().get('id') == 1

    response = client.put("/api/dictionary/state/1", json=request_data)
    assert response.status_code == 200
    assert response.json().get('name') == 'test'
    assert response.json().get('id') == 1


def test_dict_delete(client):
    """
               Удаление записи в словарях
    """
    response = client.delete("/api/dictionary/type/1")
    assert response.status_code == 204
    response = client.get("/api/dictionary/type")
    assert len(response.json().get('type')) == 2

    response = client.delete("/api/dictionary/currency/1")
    assert response.status_code == 204
    response = client.get("/api/dictionary/type")
    assert len(response.json().get('type')) == 2

    response = client.delete("/api/dictionary/md/1")
    assert response.status_code == 204
    response = client.get("/api/dictionary/type")
    assert len(response.json().get('type')) == 2

    response = client.delete("/api/dictionary/state/1")
    assert response.status_code == 204
    response = client.get("/api/dictionary/type")
    assert len(response.json().get('type')) == 2


# Тестирование CRUD операций с монетками
def test_coins_post_unauthorized(client):
    """
        Создание монетки неавторизованным пользователем
    """
    request_data = {
        "description": "test",
        "type_id": 2,
        "currency_id": 2,
        "nominal_value": "4000",
        "md_id": 2,
        "state_id": 2,
        "year": "1900",
        "serial_number": "1122",
        "user_id": 3
    }
    response = client.post("/api/coins", json=request_data)
    assert response.status_code == 401


def test_coins_post_ok(client):
    """
            Создание монетки авторизованным пользователем
    """
    request_data = {
        "description": "test",
        "type_id": 2,
        "currency_id": 2,
        "nominal_value": "4000",
        "md_id": 2,
        "state_id": 2,
        "year": "1900",
        "serial_number": "1122",
        "user_id": 3
    }
    response = client.post("/api/coins", json=request_data,
                           cookies=get_cookies_superuser(client))
    assert response.status_code == 201
    assert response.json().get('description') == 'test'


def test_coins_get_superuser(client):
    """Получение всех записей о монетках как администратор"""
    response = client.get("/api/coins", cookies=get_cookies_superuser(client))
    assert response.status_code == 200
    assert response.json().get('results') == 3


def test_coins_delete_superuser(client):
    """Удаление любой монетки как администратор"""
    response = client.delete("/api/coins/1",
                             cookies=get_cookies_superuser(client))
    assert response.status_code == 204
    response = client.get("/api/coins", cookies=get_cookies_superuser(client))
    assert response.json().get('results') == 2


def test_coins_put_superuser(client):
    """Изменение любой монетки как администратор"""
    request_data = {
        "description": "test",
        "type_id": 2,
        "currency_id": 2,
        "nominal_value": "4000",
        "md_id": 2,
        "state_id": 2,
        "year": "1900",
        "serial_number": "1122",
        "user_id": 4
    }
    response = client.put("/api/coins/1",
                          cookies=get_cookies_superuser(client),
                          json=request_data)
    assert response.status_code == 200
    assert response.json().get('description') == "test"


def test_coins_get_user(client):
    """Получение только своих монеток как пользователь"""
    cookies = get_cookies_user(client)
    response = client.get("/api/coins", cookies=cookies)
    assert response.status_code == 200
    assert response.json().get('results') == 0
    request_data = {
        "description": "test",
        "type_id": 2,
        "currency_id": 2,
        "nominal_value": "4000",
        "md_id": 2,
        "state_id": 2,
        "year": "1900",
        "serial_number": "1122",
        "user_id": 4
    }
    client.post("/api/coins", json=request_data, cookies=cookies)
    response = client.get("/api/coins", cookies=cookies)
    assert response.status_code == 200
    assert response.json().get('results') == 1


def test_coins_put_user_ok(client):
    """Изменение своих монеток как пользователь"""
    cookies = get_cookies_user(client)
    request_data = {
        "description": "money",
        "type_id": 2,
        "currency_id": 2,
        "nominal_value": "4000",
        "md_id": 2,
        "state_id": 2,
        "year": "1900",
        "serial_number": "1122",
    }
    client.post("/api/coins", json=request_data, cookies=cookies)
    request_data = {
        "description": "test",
        "type_id": 2,
        "currency_id": 2,
        "nominal_value": "4000",
        "md_id": 2,
        "state_id": 2,
        "year": "1900",
        "serial_number": "1122",
    }
    response = client.put("/api/coins/4", json=request_data, cookies=cookies)
    assert response.status_code == 200
    assert response.json().get('description') == "test"


def test_coins_put_user_fobbiden(client):
    """Изменение чужих монеток как пользователь"""
    cookies = get_cookies_user(client)
    request_data = {
        "description": "test",
        "type_id": 2,
        "currency_id": 2,
        "nominal_value": "4000",
        "md_id": 2,
        "state_id": 2,
        "year": "1900",
        "serial_number": "1122",
    }
    response = client.put("/api/coins/1", json=request_data, cookies=cookies)
    assert response.status_code == 403


def test_coins_delete_user_ok(client):
    """Удаление своих монеток как пользователь"""
    cookies = get_cookies_user(client)
    request_data = {
        "description": "test",
        "type_id": 2,
        "currency_id": 2,
        "nominal_value": "4000",
        "md_id": 2,
        "state_id": 2,
        "year": "1900",
        "serial_number": "1122",
    }
    client.post("/api/coins", json=request_data, cookies=cookies)
    response = client.delete("/api/coins/4", cookies=cookies)
    assert response.status_code == 204


def test_coins_delete_user_forbbiden(client):
    """Удаление чужих монеток как пользователь"""
    cookies = get_cookies_user(client)
    response = client.delete("/api/coins/1", cookies=cookies)
    assert response.status_code == 403
