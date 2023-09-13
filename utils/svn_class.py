import json
from abc import ABC, abstractmethod

import requests
import csv

from utils.svn_utils import full_path_name_file

API_SJ_KEY = 'v3.r.133561358.458aaf582a8dbe18b8cad038cb823741f7e0691a.a799f49596fb6a882aade1f69f46fd2fd5d76707'

class Vacancys(ABC):

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        pass

class Work_Vacancy():

    def __init__(self, keyword:str):
        self.__keyword__ = keyword
        self.vacancies = []
        self.file_json = ''
        self.file_csv = ''
        self.file_txt = ''
        self.params = None
        self.url_api = ''

    @property
    def keyword(self):
        return self.__keyword__

    @keyword.setter
    def keyword(self, new_key):
        self.__keyword__ = new_key
        self.params['keyword'] = new_key


    def save_json_file(self):
        with open(full_path_name_file(self.file_json), 'w',
                  encoding='UTF-8') as file:
            json.dump(self.vacancies, file, indent=4, ensure_ascii=False)
        # pass

    def get_request(self):
        pass

    def get_vacancies(self, pages_count=1):
        self.vacancies = []

        for page in range(pages_count):
            page_vac = []
            self.params['page'] = page
            print(f'\t -> Обрабатываем данные страницы № {page} с {self.url_api}: ', end='')
            try:
                page_vac = self.get_request()
            except Exception as t_err:
                print(t_err)
            else:
                self.vacancies.extend(page_vac)
                print(f'Загружено {len(page_vac)} вакансий')
            if len(page_vac) == 0:
                break

    def save_csv_file(self):

        csv_col = []

        def get_col_key(key, value:dict):
            for k, v in value.items():
                if not isinstance(v, dict):
                    csv_col.append(key + '|' + k)
                else:
                    get_col_key(key + '|' + k, v)


        if self.vacancies == None:
            return

        csv_vacancies = []


        for key, value in self.vacancies[0].items():
            if not isinstance(value, dict):
                csv_col.append(key)
            else:
                get_col_key(key, value)

        print(csv_col)

        # for t_vac in self.vacancies:
        #
        #     for key, value in self.vacancies[0].items():
        #         if not isinstance(value, dict):
        #         new_data[key] = value
        #     else:
        #         for k, v in value.items():
        #             new_data[key + "_" + k] = v
        #
        # # for t_key in self.vacancies.keys():
        # #     cols.append(t_key)
        #
        # with open(full_path_name_file(self.file_csv), 'w',
        #           encoding='UTF-8') as file:
        #     wr = csv.DictWriter(file, fieldnames=new_data)
        #     wr.writeheader()
        #     wr.writerows(self.vacancies)

        # cols = ['Name', 'Age', 'Gender']
        # data = [{'Name': 'John', 'Age': '20', 'Gender': 'Male'},
        #         {'Name': 'James', 'Age': '28', 'Gender': 'Male'},
        #         {'Name': 'Cardi', 'Age': '25', 'Gender': 'Female'}]
        # # path = "C:/Users/HP/OneDrive/Desktop/DEMO.csv"
        # with open(path, 'w') as f:

class Formatted_Vacancies(Work_Vacancy):

    def __init__(self, keyword:str):
        self.file_json = f'data\\{keyword}.json'
        self.file_csv = f'data\\{keyword}.csv'
        self.file_txt = f'data\\{keyword}.txt'


class Vacancy():

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


class HeadHunterAPI(Vacancys, Work_Vacancy):

    url = 'https://api.hh.ru/vacancies'
    file_json = 'data\\vac_hh.json'

    def __init__(self, keyword, count_vac_per_page=100):
        super().__init__(keyword)
        self.params = {'text': self.__keyword__,
                       'page': None,
                       'per_page': count_vac_per_page,
                       'archived': False
                       }
        # self.headers = {'User-Agent': 'MyApp/1.0 (svn_wolf@mail.ru)'}
        self.headers = {}
        self.url_api = 'HH.ru'
        # self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise Exception(f'Ошибка получения вакансий! Статус ошибки: {response.status_code}')
        # data = response.content.decode()
        # response.close()
        return response.json()['items']

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
            # print(temp_fv)
            formatted_vacancies.append(temp_fv)
        return formatted_vacancies


class SuperJobAPI(Vacancys, Work_Vacancy):

    url = 'https://api.superjob.ru/2.0/vacancies/'
    file_json = 'data\\vac_sj.json'

    def __init__(self, keyword, count_vac_per_page=100):
        super().__init__(keyword)
        self.params = {'count': count_vac_per_page,
                       'keyword': self.__keyword__,
                       'page': None,
                       'archived': False
                       }
        self.headers = {'X-Api-App-id': API_SJ_KEY}
        self.url_api = 'SuperJob.ru'

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise Exception(f'Ошибка получения вакансий! Статус ошибки: {response.status_code}')
        # data = response.content.decode()
        # response.close()
        return response.json()['objects']

    def get_formatted_vacancies(self):
        formatted_vacancies = []

        for temp_vac in self.vacancies:
            temp_fv = {'name': temp_vac['profession'],
                       'area_name': temp_vac['town']['title'],
                       'url': temp_vac['link'],
                       'salary_from': temp_vac['payment_from'] if temp_vac['payment_from'] != None else 0,
                       'salary_to': temp_vac['payment_to'] if temp_vac['payment_to'] != None else 0,
                       'salary_cur': 'RUR' if temp_vac['currency'].lower() == 'rub' else None,
                       'requirement': temp_vac['candidat'],
                       'responsibility': temp_vac['candidat'],
                       'employer': temp_vac['client']['title'],
                       'api': 'SuperJob',
                       }
            # print(temp_fv)
            formatted_vacancies.append(temp_fv)
        return formatted_vacancies