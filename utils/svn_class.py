import json
from abc import ABC, abstractmethod

import requests

from utils.svn_utils import full_path_name_file

API_SJ_KEY = 'v3.r.133561358.458aaf582a8dbe18b8cad038cb823741f7e0691a.a799f49596fb6a882aade1f69f46fd2fd5d76707'

class Vacancys(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_request(self):
        pass

    def save_json_file(self):
        pass

    def get_formatted_vacancies(self):
        pass


class Vacancy:

    def __init__(self, name, url, salary, requirements):
        """

        :param name: имя вакансии
        :param url: ссылка на выкансию
        :param salary: зарплата
        :param requirements: требования к вакансии
        """
        self.name = name
        self.url = url
        self.salary = salary
        self.requirements = requirements


class HeadHunterAPI(Vacancys):

    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword_find, count_vac_per_page=100):
        self.__keyword__ = keyword_find
        self.params = {'text': self.__keyword__,
                       'page': None,
                       'per_page': count_vac_per_page,
                       'archived': False
                       }
        # self.headers = {'User-Agent': 'MyApp/1.0 (svn_wolf@mail.ru)'}
        self.headers = {}
        self.vacancies = []
        self.file_json = 'data\\vac_hh.json'

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise Exception(f'Ошибка получения вакансий! Статус ошибки: {response.status_code}')
        # data = response.content.decode()
        # response.close()
        return response.json()['items']

    @property
    def keyword(self):
        return self.__keyword__

    @keyword.setter
    def keyword(self, new_key):
        self.__keyword__ = new_key
        self.params['text'] = new_key

    def get_vacancies(self, pages_count=1):
        self.vacancies = []

        for page in range(pages_count):
            page_vac = []
            self.params['page'] = page
            print(f'\t -> Обрабатываем данные страницы № {page} с HH.ru: ', end='')
            try:
                page_vac = self.get_request()
            except Exception as t_err:
                print(t_err)
            else:
                self.vacancies.extend(page_vac)
                print(f'Загружено {len(page_vac)} вакансий')
            if len(page_vac) == 0:
                break

    def save_json_file(self):
        with open(full_path_name_file(self.file_json), 'w', encoding = 'UTF-8') as file:
            json.dump(self.vacancies, file)

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for temp_vac in self.vacancies:
            temp_fv = {'name': temp_vac['name'],
                       'area_name': temp_vac['area']['name'],
                       'url': temp_vac['alternate_url'],
                       'salary_from': temp_vac['salary']['from'] if temp_vac['salary'] != None else 0,
                       'salary_to': temp_vac['salary']['to'] if temp_vac['salary'] != None else 0,
                       'salary_cur': temp_vac['salary']['currency'] if temp_vac['salary'] != None else 'RUR',
                       'requirement': temp_vac['snippet']['requirement'],
                       'responsibility': temp_vac['snippet']['responsibility'],
                       'employer': temp_vac['employer']['name'],
                       'api': 'HH',
                       }
            formatted_vacancies.append(temp_fv)
        return formatted_vacancies


class SuperJobAPI(Vacancys):

    url = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, keyword_find, count_vac_per_page=100):
        self.__keyword__ = keyword_find
        self.params = {'count': count_vac_per_page,
                       'keyword': self.__keyword__,
                       'page': None,
                       'archived': False
                       }
        self.headers = {'X-Api-App-id': API_SJ_KEY}
        self.vacancies = []
        self.file_json = 'data\\vac_sj.json'

    @property
    def keyword(self):
        return self.__keyword__

    @keyword.setter
    def keyword(self, new_key):
        self.__keyword__ = new_key
        self.params['keyword'] = new_key


    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise Exception(f'Ошибка получения вакансий! Статус ошибки: {response.status_code}')
        # data = response.content.decode()
        # response.close()
        return response.json()['objects']

    def get_vacancies(self, pages_count=1):
        self.vacancies = []

        for page in range(pages_count):
            page_vac = []
            self.params['page'] = page
            print(f'\t -> Обрабатываем данные страницы № {page} с SuperJob.ru: ', end='')
            try:
                page_vac = self.get_request()
            except Exception as t_err:
                print(t_err)
            else:
                self.vacancies.extend(page_vac)
                print(f'Загружено {len(page_vac)} вакансий')
            if len(page_vac) == 0:
                break

    def save_json_file(self):
        with open(full_path_name_file(self.file_json), 'w') as file:
            json.dump(self.vacancies, file)

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for temp_vac in self.vacancies:
            temp_fv = {'name': temp_vac['profession'],
                       'area_name': temp_vac['client']['town']['title'],
                       'url': temp_vac['link'],
                       'salary_from': temp_vac['payment_from'] if temp_vac['payment_from'] != None else 0,
                       'salary_to': temp_vac['payment_to'] if temp_vac['payment_to'] != None else 0,
                       'salary_cur': temp_vac['currency'],
                       'requirement': temp_vac['snippet']['requirement'],
                       'responsibility': temp_vac['snippet']['responsibility'],
                       'employer': temp_vac['client']['title'],
                       'api': 'SuperJob',
                       }
            formatted_vacancies.append(temp_fv)
        return formatted_vacancies