import json
from abc import ABC, abstractmethod

import requests
import csv

from utils.svn_utils import full_path_name_file

# апи ключ для подключения к superjob.ru
API_SJ_KEY = 'v3.r.133561358.458aaf582a8dbe18b8cad038cb823741f7e0691a.a799f49596fb6a882aade1f69f46fd2fd5d76707'


# def get_exchange_rates():
#
#     url = "https://api.apilayer.com/exchangerates_data/latest?symbols=&base=RUB"
#
#     response = requests.request("GET", url, headers={"apikey": API_KEY}, data={})
#
#     response_data = json.loads(response.text)
#
#     if response.status_code == 200:
#
#         with open(full_path_name_file('data\\ex_rub.json'), 'w',
#                   encoding='UTF-8') as file:
#             json.dump(response_data, file, indent=4, ensure_ascii=False)
#
#     else:
#
#         with open(full_path_name_file('data\\ex_rub.json'), 'r',
#                   encoding='UTF-8') as file:
#             response_data = json.load(file)
#
#     return response_data['rates']


class Vacancys(ABC):
    """
    Класс с абстрактными методами get_request и get_formatted_vacancies
    """
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        pass

class Work_Vacancy():

    """
    Общий класс для заполения вакансиями
    """

    def __init__(self, keyword: str, file_name=None):
        """
        Магический метод инициализации класса
        """
        self.__keyword__ = keyword
        self.vacancies = []
        if file_name != None:
            t_name = file_name
        else:
            t_name = keyword
        self.file_json = f'data\\{t_name}.json'
        self.file_csv = f'data\\{t_name}.csv'
        self.file_txt = f'data\\{t_name}.txt'
        self.params = None
        self.url_api = ''

    @property
    def keyword(self):
        return self.__keyword__

    @keyword.setter
    def keyword(self, new_key):
        self.__keyword__ = new_key
        if self.params != None:
            if 'text' in self.params.keys():
                self.params['text'] = new_key
            if 'keyword' in self.params.keys():
                self.params['keyword'] = new_key
        else:
            self.file_json = f'data\\{new_key}.json'
            self.file_csv = f'data\\{new_key}.csv'
            self.file_txt = f'data\\{new_key}.txt'


    @staticmethod
    def remove_spec_char(text) -> str:
        """
        Удаление \\u символов в тексте
        :param text:
        :return:
        """

        if text == None:
            return ''
        else:
            # if text.count('\u2070') != 0:
            #     st_1 = 1
            #     pass

            for i in ['\u200e', '\u2070']:
                text = text.replace(i, '')
            return text

    def save_json_file(self):
        """
        метод класса для записи в файл json, прописанный в переменной класса file_json
        :return:
        """
        with open(full_path_name_file(self.file_json), 'w',
                  encoding='UTF-8') as file:
            json.dump(self.vacancies, file, indent=4, ensure_ascii=False)
        # pass

    def get_request(self):
        pass

    def get_vacancies(self, pages_count=1):
        """
        Получение вакнсий с определенных API
        :param pages_count:
        :return:
        """
        self.vacancies = []

        for page in range(pages_count):
            page_vac = []
            self.params['page'] = page
            # print(f'\t -> Обрабатываем данные страницы № {page} с {self.url_api}: ', end='')
            try:
                page_vac = self.get_request()
            except Exception as t_err:
                print(t_err)
            else:
                self.vacancies.extend(page_vac)
                # print(f'Загружено {len(page_vac)} вакансий')
            if len(page_vac) == 0:
                break

    def save_csv_file(self, file_name, is_csv=True):
        """
        Запись ф файл csv и txt
        :param file_name: имя файла
        :param is_csv: если True - то пишем в csv, если False - то пишем в txt
        :return:
        """

        csv_col = []
        t_csv_vac = {}

        def get_col_key(key, value:dict):
            for k, v in value.items():
                if not isinstance(v, dict):
                    csv_col.append(key + '|' + k)
                else:
                    get_col_key(key + '|' + k, v)

        def set_key_vac(key, value:dict):
            for k, v in value.items():
                if not isinstance(v, dict):
                    t_csv_vac[key + '|' + k] = v
                else:
                    set_key_vac(key + '|' + k, v)


        if self.vacancies == None:
            return

        if is_csv:

            # собираем список колонок для записей в csv

            csv_col = []

            for key, value in self.vacancies[0].items():
                if not isinstance(value, dict):
                    csv_col.append(key)
                else:
                    get_col_key(key, value)



        # собираем список вакансий
        csv_vacancies = []

        for t_vac in self.vacancies:
            t_csv_vac = {}
            for key, value in t_vac.items():
                if not isinstance(value, dict):
                    t_csv_vac[key] = value
                else:
                    set_key_vac(key, value)
            csv_vacancies.append(t_csv_vac)

        # пишем в csv файл

        if is_csv:


            # пишем в файл

            with open(full_path_name_file(file_name), 'w',
                      encoding='UTF-8') as file:
                wr = csv.DictWriter(file, delimiter=";", fieldnames=csv_col)
                wr.writeheader()
                wr.writerows(csv_vacancies)

        else:

            # пишем в файл

            with open(full_path_name_file(file_name), 'w',
                      encoding='UTF-8') as file:
                for t_csv_vac in csv_vacancies:
                    file.write('----------\n')  # разделитель записей
                    for k_csv, v_csv in t_csv_vac.items():
                        file.write(f'{k_csv}: {v_csv}\n')



class Vacancy():

    """
    класс одной вакансии
    """

    def __init__(self, name: str, url: str, salary: str, requirements: str,
                 town: str, responsibility: str, employer: str):
        """
        :param name: имя вакансии
        :param url: ссылка на выкансию
        :param salary: зарплата
        :param requirements: требования к вакансии
        """
        self.name = name
        self.url = url
        self.requirements = requirements
        self.town = town
        self.responsibility = responsibility
        self.employer = employer
        # 100 000-150 000 руб.
        t_sal = salary.replace(' руб.', '-руб.').split('-')
        self.salary_from = int(t_sal[0].replace(' ', ''))
        self.salary_to = int(t_sal[1].replace(' ', ''))
        self.salary_currency = 'RUR'
        self.json_item = {'name': self.name,
                          'area_name': self.town,
                          'url': self.url,
                          'salary_from': self.salary_from,
                          'salary_to': self.salary_to,
                          'salary_cur': self.salary_currency,
                          'requirement': self.requirements,
                          'responsibility': self.responsibility,
                          'employer': self.employer,
                          'api': 'manual_add',
                         }



class Formatted_Vacancies(Work_Vacancy):

    """
    Класс для отформатированых вакансий
    """

    def __init__(self, keyword: str):
        super().__init__(self, keyword)
        self.vacancies = []

    def add_vacancy(self, vacancy: Vacancy):
        """
        Добавить новую вакансию
        :return:
        """
        self.vacancies.append(vacancy.json_item)

    def get_vacancies_by_salary(self, salary: str):
        """
        Выдать список ваканcий с зарплатой в пределах записи в переменную salary
        :return:
        """
        # "100 000-150 000 руб."
        t_sal = salary.replace(' руб.', '-руб.').split('-')
        t_salary_from = int(t_sal[0].replace(' ', ''))
        t_salary_to = int(t_sal[1].replace(' ', ''))
        vacancies_salary = []
        for t_vac in self.vacancies:
            t_from = t_vac['salary_from']
            t_to = t_vac['salary_to']
            if t_to < t_from:
                t_to = t_from
            if (t_from >= t_salary_from) and (t_to <= t_salary_to):
               vacancies_salary.append(t_vac)

        print(f'\nСписок вакансий с зарплатной вилкой: \033[33m{salary}\033[39m')
        if vacancies_salary == []:
            print('\tНе найдено вакансий')
        else:
            print(f'\tНайдено {len(vacancies_salary)} вакансий:')
            for t_vac in vacancies_salary:
                print(f'-> от {t_vac["salary_from"]} до {t_vac["salary_to"]} руб.: '
                      f'{t_vac["name"]} ({t_vac["api"]})')


    def find_vacancies(self, find_name: str):
        """
        Поиск вакансий по слову
        :param find_name:
        :return:
        """
        find_vac = []
        find_name = find_name.lower().strip()
        for t_vac in self.vacancies:
            if find_name in t_vac['name'].lower():
                find_vac.append(t_vac)

        print(f'\nРезультат поиска вакансий по слову \033[33m{find_name}\033[39m')
        if find_vac == []:
            print('\tНе найдено вакансий')
        else:
            print(f'\tНайдено {len(find_vac)} вакансий:')
            for t_vac in find_vac:
                print(f'-> {t_vac["name"]} ({t_vac["area_name"]}, {t_vac["api"]})')


    def print_vacancies(self):
        """
        Вывод на экран отформатированных вакансий
        :return:
        """
        for t_vac in self.vacancies:
            print(f'\033[33mНаименование вакансии\033[39m: {t_vac["name"]}')
            print(f'\033[33mГород вакансии\033[39m: {t_vac["area_name"]}')
            print(f'\033[33mЗаказчик\033[39m: {t_vac["employer"]}')
            print(f'\033[33mСсылка на вакансию\033[39m: {t_vac["url"]}')

            str_salary = ''
            if t_vac["salary_from"] != 0:
                str_salary = f'от {t_vac["salary_from"]} '
            if t_vac["salary_to"] != 0:
                str_salary += f'до {t_vac["salary_to"]} '
            if str_salary != '':
                str_salary += 'руб.'
            print(
                f'\033[33mЗарплата\033[39m: {"не указана" if str_salary == "" else str_salary}')

            print(f'\033[33mТребования\033[39m: {t_vac["requirement"]}')
            print(f'\033[33mОтветсвенность\033[39m: {t_vac["responsibility"]}')

            if t_vac["api"] == 'HH':
                print('Вакансия загружена с \033[33mhh.ru\033[39m')
            elif t_vac['api'] == 'SuperJob':
                print('Вакансия загружена с \033[33msuperjob.ru\033[39m')
            elif t_vac['api'] == 'manual_add':
                print('Вакансия введена в ручную')

            print(' ---------------- ')

    def sort_vacancies(self):
        """
        Отсортировать вакансии по зарплате от минимальной к максимальной
        """
        print('\n\033[33mСписок вакансий до сортировки:\033[39m')
        for temp_vac in self.vacancies:
            print(f'-> от {temp_vac["salary_from"]} до {temp_vac["salary_to"]} руб.: '
                  f'{temp_vac["name"]} ({temp_vac["api"]})')

        self.vacancies = sorted(self.vacancies, key=lambda x:x['salary_from'])

        print('\n\033[33mСписок вакансий после сортировки:\033[39m')
        for temp_vac in self.vacancies:
            print(f'-> от {temp_vac["salary_from"]} до {temp_vac["salary_to"]} руб.: '
                  f'{temp_vac["name"]} ({temp_vac["api"]})')

    def get_top_vacancies(self, count_top=10):
        """
        Вывести топ по зарплатам
        count_top - количество вакансий в топ листе
        """
        self.vacancies = sorted(self.vacancies, key=lambda x:x['salary_from'], reverse=True)

        print(f'\n\033[33mТоп-{count_top} вакансий по зарплате:\033[39m')
        for temp_vac in self.vacancies:
            count_top -= 1
            print(f'-> от {temp_vac["salary_from"]} до {temp_vac["salary_to"]} руб.: '
                  f'{temp_vac["name"]} ({temp_vac["api"]})')
            if count_top == 0:
                break

class HeadHunterAPI(Vacancys, Work_Vacancy):

    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword, count_vac_per_page=100):
        super().__init__(keyword, 'vac_hh')
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
            if temp_vac['salary'] != None:
                if temp_vac['salary']['currency'] != 'RUR':
                    continue

            t_salary_from = 0
            t_salary_to = 0
            if temp_vac['salary'] != None:
                if temp_vac['salary']['from'] != None:
                    t_salary_from = temp_vac['salary']['from']
                if temp_vac['salary']['to'] != None:
                    t_salary_to = temp_vac['salary']['to']

            temp_fv = {'name': self.remove_spec_char(temp_vac['name']),
                       'area_name': self.remove_spec_char(temp_vac['area']['name']) if temp_vac['area'] !=None else '',
                       'url': temp_vac['alternate_url'],
                       'salary_from': t_salary_from,
                       'salary_to': t_salary_to,
                       'salary_cur': 'RUR',
                       'requirement': self.remove_spec_char(temp_vac['snippet']['requirement']) if temp_vac['snippet'] !=None else '',
                       'responsibility': self.remove_spec_char(temp_vac['snippet']['responsibility']) if temp_vac['snippet'] !=None else '',
                       'employer': self.remove_spec_char(temp_vac['employer']['name']) if temp_vac['employer'] !=None else '',
                       'api': 'HH',
                       }

            formatted_vacancies.append(temp_fv)
        return formatted_vacancies


class SuperJobAPI(Vacancys, Work_Vacancy):

    url = 'https://api.superjob.ru/2.0/vacancies/'

    def __init__(self, keyword, count_vac_per_page=100):
        super().__init__(keyword, 'vac_sj')
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
            # print('\033[32m-------------------------------------------------------\033[39m')
            # print(temp_vac)
            if temp_vac['currency'].lower() != 'rub':
                continue

            temp_fv = {'name': self.remove_spec_char(temp_vac['profession']),
                       'area_name': self.remove_spec_char(temp_vac['town']['title']) if temp_vac['town'] !=None else '',
                       'url': temp_vac['link'],
                       'salary_from': temp_vac['payment_from'] if temp_vac['payment_from'] != None else 0,
                       'salary_to': temp_vac['payment_to'] if temp_vac['payment_to'] != None else 0,
                       'salary_cur': 'RUR',
                       'requirement': self.remove_spec_char(temp_vac['candidat']),
                       'responsibility': self.remove_spec_char(temp_vac['candidat']),
                       'employer': self.remove_spec_char(temp_vac['firm_name']),
                       'api': 'SuperJob',
                       }
            # print(temp_fv)
            # print('---------------')
            # print(temp_fv)

            formatted_vacancies.append(temp_fv)
        return formatted_vacancies