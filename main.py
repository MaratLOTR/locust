import json
import time
import random
import json
from uuid import uuid4

from locust import HttpUser, task, tag, between


# Статичные данные для тестирования
EMAILS = ["test@test.com",
"tester@test.com",
"test1@test.com",
"test21@test.com",
"test12@test.com",
]
USERS_ID = [5,6,7,17,18,21]

class RESTServerUser(HttpUser):
    """ Класс, эмулирующий пользователя / клиента сервера """
    wait_time = between(1.0, 5.0)       # время ожидания пользователя перед выполнением новой task

    # Адрес, к которому клиенты (предположительно) обращаются в первую очередь (это может быть индексная страница, страница авторизации и т.п.)
    def on_start(self):
        self.client.get("/docs")    # базовый класс HttpUser имеет встроенный HTTP-клиент для выполнения запросов (self.client)

    @tag("get_all_task")
    @task(3)
    def get_all_task(self):
        """ Тест GET-запроса (получение нескольких записей о погоде) """
        email = EMAILS[random.randint(0, 4)]    # получаем случайное значение населенного пункта из списка CITY_NAMES
        with self.client.get(f'/users/auth/',
                             catch_response=True,
                             name='/users/auth',
                             params={"email": email}) as response:
            # Если получаем код HTTP-код 200, то оцениваем запрос как "успешный"
            if response.status_code == 200:
                response.success()
            # Иначе обозначаем как "отказ"
            else:
                response.failure(f'Status code is {response.status_code}')

    # @tag("get_one_task")
    # @task(10)
    # def get_one_task(self):
    #     """ Тест GET-запроса (получение одной записи) """
    #     city_id = random.randint(1, 4)
    #     with self.client.get(f'/api/weatherforecast?city_id={city_id}',
    #                          catch_response=True,
    #                          name='/api/weatherforecast?city_id={ID}') as response:
    #         # Если получаем код HTTP-код 200 или 204, то оцениваем запрос как "успешный"
    #         if response.status_code == 200 or response.status_code == 204:
    #             response.success()
    #         else:
    #             response.failure(f'Status code is {response.status_code}')
    #
    @tag("put_task")
    @task(5)
    def put_task(self):
        rand_id = random.randint(0, 5)
        weight=random.randint(40, 110)
        fat_mass_koef = round(random.uniform(0.4, 0.7), 1)
        test_data = {"user_id": USERS_ID[rand_id],
                     "weight": weight,
                     "fat_mass": int(weight*fat_mass_koef),
                     "muscle_mass": int(weight*(1-fat_mass_koef))}
        post_data = json.dumps(test_data)       # сериализуем тестовые данные в json-строку
        # отправляем POST-запрос с данными (POST_DATA) на адрес <SERVER>/api/weatherforecast
        with self.client.put('/users/weight_fat_muscle_mass',
                              catch_response=True,
                              name='/users/weight_fat_muscle_mass', params=test_data,
                              headers={'content-type': 'application/json'}) as response:
            # проверяем, корректность возвращаемого HTTP-кода
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("post_task")
    @task(5)
    def test_post_query(self):
        test_data = {"sex": True,
        "name": str(uuid4()),
        "height":  random.randint(140, 200),
        "email":  str(uuid4())}
        post_data = json.dumps(test_data)
        with self.client.post('/users/register',
                              name='/users/register',
                              catch_response=True,
                              params=test_data,
                              headers={'content-type': 'application/json'}) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    #
    # @tag("put_task")
    # @task(3)
    # def put_task(self):
    #     """ Тест PUT-запроса (обновление записи о погоде) """
    #     city_id = random.randint(0, 3)  # генерируем случайный id в диапазоне [0, 3]
    #     city_name = CITY_NAMES[city_id]  # получаем случайное значение населенного пункта из списка CITY_NAMES
    #     test_data = {'temperature_c': random.uniform(20.0, 29.9),
    #                  'pressure': random.randint(735, 755),
    #                  'city_id': city_id + 1,
    #                  'weather_type': random.randint(1, 3)}
    #     put_data = json.dumps(test_data)
    #     # отправляем PUT-запрос на адрес <SERVER>/api/weatherforecast/{city_name}
    #     with self.client.put('/api/weatherforecast',
    #                          catch_response=True,
    #                          name='/api/weatherforecast',
    #                          data=put_data,
    #                          headers={'content-type': 'application/json'}) as response:
    #         if response.status_code == 202:
    #             response.success()
    #         else:
    #             response.failure(f'Status code is {response.status_code}')
    #
