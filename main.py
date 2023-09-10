# Параметры доступа
# ID	2942
# Secret key v3.r.133561358.458aaf582a8dbe18b8cad038cb823741f7e0691a.a799f49596fb6a882aade1f69f46fd2fd5d76707

import requests

from utils.svn_utils import *
from utils.svn_class import *

COUNT_LOAD_PAGE = 1
COUNT_VAC_PER_PAGE = 5

def main():
    keyword_find = 'python'

    print(f'-> Установлено слово для поиска вакансий: '
          f'{keyword_find}')

    hh = HeadHunterAPI(keyword_find, COUNT_VAC_PER_PAGE)
    sj = SuperJobAPI(keyword_find, COUNT_VAC_PER_PAGE)

    vacancies_json = []
    for t_vac in (hh, sj):
        t_vac.get_vacancies(COUNT_LOAD_PAGE)
        # t_vac.save_json_file()
        vacancies_json.extend(t_vac.vacancies)

    while True:
        print('\n -----= Меню =----- ')
        print(f'Количество загруженных вакансий: {len(vacancies_json)}\n')
        print(f'\t-> [1] - указать новое слово для поиска вакансий '
              f'(текущее слово для поиска: {keyword_find})')
        print('\t-> [2] - записать вакансии в файл')
        print('\t-> [3] - вывести список вакансий')
        print('\t-> [4] - отсортировать по минимальной зарплате')

        print('\t-> [0] - выход из программы')

        menu_item = '01234'.strip()

        user_input = check_line_entry(f'Выберите пункт меню ({", ".join(menu_item)})',
                                      ''.join(menu_item),
                                      f'разрешен ввод только {", ".join(menu_item)}')
        if user_input == '0':
            print('Пока !')
            break
        elif user_input == '1':
            print(f'\n -> Установлено слово для поиска вакансий: {keyword_find} ')
            temp_word = input('Введите новое слово для поиска (пустой ввод - '
                              'слово для поиска остается старым):').strip().lower()
            if temp_word != '':
                if temp_word != keyword_find:
                    print(f'-> Установлено новое слово для поиска вакансий: '
                          f'{keyword_find}')
                    vacancies_json = []
                    for t_vac in (hh, sj):
                        t_vac.keyword = temp_word
                        t_vac.get_vacancies(COUNT_LOAD_PAGE)
                        vacancies_json.extend(t_vac.vacancies)
                keyword_find = temp_word

        elif user_input == '2':
            for t_vac in (hh, sj):
                print(f'{t_vac.__class__.__name__}: Запись в файл {full_path_name_file(t_vac.file_json)}')
                t_vac.save_json_file()

        elif user_input == '3':
            for t_vac in (hh, sj):
                print(f'--------------- {t_vac.__class__.__name__} -------------------------- ')
                print(t_vac.vacancies)
            pass
        elif user_input == '4':
            # print(user_input)
            pass






if __name__ == '__main__':
    main()