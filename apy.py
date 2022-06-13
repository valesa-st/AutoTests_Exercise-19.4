import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
from log import logrequests


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'
# --------------------------------------------------------------------------------------------

    @logrequests
    def get_api_key(self, email, password):
        """Получаем Api key"""

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
# ---------------------------------------------------------------------------------------------

    @logrequests
    def get_list_of_pets(self, auth_key, filter):
        """Получение списока питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
# ---------------------------------------------------------------------------------------------

    @logrequests
    def add_new_pet_not_photo(self, auth_key: json, name: str, animal_type: str, age: str):
        """Добавление питомца без фото"""

        headers = {'auth_key': auth_key['key']}
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
            }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
# ----------------------------------------------------------------------------------------------

    @logrequests
    def update_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Добавляем фото питомца"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
# ----------------------------------------------------------------------------------------------

    @logrequests
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int):
        """Обновление данных о питомце"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type,
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
# ----------------------------------------------------------------------------------------------

    @logrequests
    def delete_pet(self, auth_key: json, pet_id: str):
        """Удаление питомца"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
# ------------------------------------------------------------------------------------------------

    @logrequests
    def add_new_pet_and_photo(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str):
        """Добавление питомца с фото"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
