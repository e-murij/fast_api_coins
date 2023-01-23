import json
import models


def fill_db_fake_data(filename, db):
    """ Наполнение пустой базы данными из файла fake_tests_data.json"""
    with open(filename, 'r', encoding='UTF-8') as file:
        data = json.load(file)

    for item in data['type']:
        new_item = models.Type(**item)
        db.add(new_item)

    for item in data['currency']:
        new_item = models.Currency(**item)
        db.add(new_item)

    for item in data['md']:
        new_item = models.Md(**item)
        db.add(new_item)

    for item in data['state']:
        new_item = models.State(**item)
        db.add(new_item)

    for item in data['user']:
        new_item = models.User(**item)
        db.add(new_item)

    for item in data['coins']:
        new_item = models.Coins(**item)
        db.add(new_item)

    db.commit()
