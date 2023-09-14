import json
from abc import ABC, abstractmethod

import requests
import csv

from utils.svn_utils import full_path_name_file

# апи ключ для подключения к superjob.ru
API_SJ_KEY = 'v3.r.133561358.458aaf582a8dbe18b8cad038cb823741f7e0691a.a799f49596fb6a882aade1f69f46fd2fd5d76707'
# апи для подключения к https://apilayer.com/marketplace/exchangerates_data-api
API_KEY = 'oyuiDH1M3lgWqX6TD475VxjZWn7U8d5i'

RATES_EXCHANGE = {  "AED": 0.038179,
                    "AFN": 0.821498,
                    "ALL": 1.035978,
                    "AMD": 4.01265,
                    "ANG": 0.018733,
                    "AOA": 8.611728,
                    "ARS": 3.638273,
                    "AUD": 0.01615,
                    "AWG": 0.01871,
                    "AZN": 0.017687,
                    "BAM": 0.018936,
                    "BBD": 0.020986,
                    "BDT": 1.140706,
                    "BGN": 0.019062,
                    "BHD": 0.003919,
                    "BIF": 29.44225,
                    "BMD": 0.010394,
                    "BND": 0.01414,
                    "BOB": 0.071822,
                    "BRL": 0.050782,
                    "BSD": 0.010393,
                    "BTC": 3.90447e-07,
                    "BTN": 0.862558,
                    "BWP": 0.141412,
                    "BYN": 0.026235,
                    "BYR": 203.73009,
                    "BZD": 0.020951,
                    "CAD": 0.014062,
                    "CDF": 25.622178,
                    "CHF": 0.009308,
                    "CLF": 0.000333,
                    "CLP": 9.188228,
                    "CNY": 0.075645,
                    "COP": 40.9353,
                    "CRC": 5.541029,
                    "CUC": 0.010394,
                    "CUP": 0.275451,
                    "CVE": 1.06756,
                    "CZK": 0.239112,
                    "DJF": 1.85059,
                    "DKK": 0.072708,
                    "DOP": 0.590023,
                    "DZD": 1.420187,
                    "EGP": 0.321813,
                    "ERN": 0.155916,
                    "ETB": 0.574607,
                    "EUR": 0.009749,
                    "FJD": 0.023566,
                    "FKP": 0.008324,
                    "GBP": 0.008374,
                    "GEL": 0.027233,
                    "GGP": 0.008324,
                    "GHS": 0.119371,
                    "GIP": 0.008324,
                    "GMD": 0.628837,
                    "GNF": 89.227155,
                    "GTQ": 0.081804,
                    "GYD": 2.174616,
                    "HKD": 0.081369,
                    "HNL": 0.256083,
                    "HRK": 0.072914,
                    "HTG": 1.40831,
                    "HUF": 3.746295,
                    "IDR": 159.930199,
                    "ILS": 0.039727,
                    "IMP": 0.008324,
                    "INR": 0.86319,
                    "IQD": 13.611595,
                    "IRR": 439.189061,
                    "ISK": 1.416442,
                    "JEP": 0.008324,
                    "JMD": 1.605818,
                    "JOD": 0.007361,
                    "JPY": 1.531671,
                    "KES": 1.525881,
                    "KGS": 0.921706,
                    "KHR": 42.628815,
                    "KMF": 4.770506,
                    "KPW": 9.354973,
                    "KRW": 13.824074,
                    "KWD": 0.003211,
                    "KYD": 0.008661,
                    "KZT": 4.842916,
                    "LAK": 206.788935,
                    "LBP": 156.22281,
                    "LKR": 3.36238,
                    "LRD": 1.938032,
                    "LSL": 0.196556,
                    "LTL": 0.030692,
                    "LVL": 0.006287,
                    "LYD": 0.050423,
                    "MAD": 0.105541,
                    "MDL": 0.186679,
                    "MGA": 47.006287,
                    "MKD": 0.599508,
                    "MMK": 21.826573,
                    "MNT": 36.142929,
                    "MOP": 0.0838,
                    "MRO": 3.710796,
                    "MUR": 0.465657,
                    "MVR": 0.15987,
                    "MWK": 11.328141,
                    "MXN": 0.17818,
                    "MYR": 0.048667,
                    "MZN": 0.657445,
                    "NAD": 0.196562,
                    "NGN": 7.99007,
                    "NIO": 0.3803,
                    "NOK": 0.111678,
                    "NPR": 1.380097,
                    "NZD": 0.017589,
                    "OMR": 0.004002,
                    "PAB": 0.010393,
                    "PEN": 0.038455,
                    "PGK": 0.038185,
                    "PHP": 0.590016,
                    "PKR": 3.094786,
                    "PLN": 0.04523,
                    "PYG": 75.663001,
                    "QAR": 0.037846,
                    "RON": 0.048451,
                    "RSD": 1.143227,
                    "RUB": 1,
                    "RWF": 12.461401,
                    "SAR": 0.038986,
                    "SBD": 0.087509,
                    "SCR": 0.136696,
                    "SDG": 6.247923,
                    "SEK": 0.116239,
                    "SGD": 0.014176,
                    "SHP": 0.012647,
                    "SLE": 0.231192,
                    "SLL": 205.289252,
                    "SOS": 5.919602,
                    "SSP": 6.252361,
                    "SRD": 0.397685,
                    "STD": 215.142935,
                    "SYP": 135.144479,
                    "SZL": 0.196307,
                    "THB": 0.37202,
                    "TJS": 0.114129,
                    "TMT": 0.036484,
                    "TND": 0.032547,
                    "TOP": 0.024872,
                    "TRY": 0.280123,
                    "TTD": 0.070553,
                    "TWD": 0.331844,
                    "TZS": 26.036206,
                    "UAH": 0.383879,
                    "UGX": 38.717382,
                    "USD": 0.010394,
                    "UYU": 0.397727,
                    "UZS": 126.328859,
                    "VEF": 34603.155899,
                    "VES": 0.346086,
                    "VND": 251.856126,
                    "VUV": 1.266483,
                    "WST": 0.028593,
                    "XAF": 6.350822,
                    "XAG": 0.000464,
                    "XAU": 5.458996e-06,
                    "XCD": 0.028091,
                    "XDR": 0.007865,
                    "XOF": 6.350822,
                    "XPF": 1.160041,
                    "YER": 2.601976,
                    "ZAR": 0.197093,
                    "ZMK": 93.561962,
                    "ZMW": 0.213334,
                    "ZWL": 3.34699
                }

def get_exchange_rates():


    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=&base=RUB"

    response = requests.request("GET", url, headers={"apikey": API_KEY}, data={})

    status_code = response.status_code
    result = response.text

    print(status_code)
    print(result)


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
        self.params['keyword'] = new_key


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
                 town: str, area_name: str, responsibility: str, employer: str):
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
        self.area_name = area_name
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

    def add_vacancy(vacancy: Vacancy):
        self.vacancies.extend(vacancy.json_item)

    def get_vacancies_by_salary(salary: str):
        # "100 000-150 000 руб."
        t_sal = salary.replace(' руб.', '-руб.').split('-')
        t_salary_from = int(t_sal[0].replace(' ', ''))
        t_salary_to = int(t_sal[1].replace(' ', ''))
        vacancies_salary = []
        for t_vac in self.vacancies:
            if (t_vac['salary_from'] >= t_salary_from) and \
               (t_vac['salary_to'] <= t_salary_to):
               vacancies_salary.append(t_vac)
        return vacancies_salary


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
            print('---------------')
            print(temp_fv)

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