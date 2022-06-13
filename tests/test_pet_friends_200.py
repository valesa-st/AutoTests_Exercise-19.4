from api import PetFriends
from settings import *
import os


pf = PetFriends()


def test_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест на получение Api key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
# --------------------------------------------------------------------------------------------------------


def test_get_all_pets_with_valid_key(filter='my_pets'):
    """Тест на получение списка питомцев"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    if len(result['pets']) == 0:
        assert len(result['pets']) == 0
    else:
        assert 'pets' in result
# --------------------------------------------------------------------------------------------------------


def test_add_new_pet_with_valid_data_not_photo(name=add_name, animal_type=add_animal_type, age=add_age):
    """Тест добавления питомца с корректными данными без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Запрашиваем ключ api и сохраняем в переменную auth_key

    status, result = pf.add_new_pet_not_photo(auth_key, name, animal_type, age)  # Добавляем питомца
    assert status == 200
    assert result['name'] == add_name
# -------------------------------------------------------------------------------------------------------


def test_add_new_pet_only_photo(pet_photo=add_pet_photo):
    """Тест на добавление фото питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем, что Status Code = 200 и имя питомца соответствует заданному
        assert status == 200
        # assert result['pet_photo'] == add_pet_photo
    else:
        # если список питомцев пустой, то получаем исключение с текстом об отсутствии моих питомцев
        raise Exception("There is no my pets")
# ----------------------------------------------------------------------------------------------------


def test_successful_update_self_pet_info(name=update_name, animal_type=update_animal_type, age=update_age):
    """Тест на обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что Status code = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == update_name
    else:
        # если список питомцев пустой, то получаем исключение с текстом об отсутствии моих питомцев
        raise Exception("There is no my pets")
# --------------------------------------------------------------------------------------------------


def test_delete_pet_valid_user():
    """Тест на удаление питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пуст, то добавляем нового питомца и повторно запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_not_photo(auth_key, add_name, add_age, add_animal_type)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Повторно запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что Status code = 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
# ---------------------------------------------------------------------------------------------------------


def test_add_new_pet_with_valid_data_and_photo(name=add_name, animal_type=add_animal_type, age=add_age,
                                               pet_photo=add_pet_photo):
    """Тест добавления питомца с корректными данными и фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Запрашиваем ключ api и сохраняем в переменную auth_key

    status, result = pf.add_new_pet_and_photo(auth_key, name, animal_type, age, pet_photo)  # Добавляем питомца
    assert status == 200
    assert result['name'] == name
