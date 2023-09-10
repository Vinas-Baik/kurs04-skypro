import json
import os
import requests

URL_HH = 'https://api.hh.ru/vacancies'

params = {
    'text': 'python',
    # Текст фильтра. В имени должно быть слово "Аналитик"
    'page': 0,  # Индекс страницы поиска на HH
    'per_page': 5 # Кол-во вакансий на 1 странице
}

req = requests.get(URL_HH, params)  # Посылаем запрос к API
data = req.content.decode()         # Декодируем его ответ, чтобы Кириллица отображалась корректно
req.close()

# print(data)
for t_data in data:
    print(t_data)


# data = json.loads(response.text)

# print(data)