
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

    for_vac = Formatted_Vacancies(keyword_find)

    for t_vac in (hh, sj):
        t_vac.get_vacancies(COUNT_LOAD_PAGE)
        for_vac.vacancies.extend(t_vac.get_formatted_vacancies())

    while True:
        print('\n -----= Меню =----- ')
        print(f'Количество загруженных вакансий: {len(for_vac.vacancies)}\n')
        print(f'\t\033[32m[1]\033[39m - указать новое слово для поиска вакансий '
              f'(текущее слово для поиска: {keyword_find})')
        print('\t\033[32m[2]\033[39m - записать вакансии c HH и SJ в файл JSON и TXT')
        print('\t\033[32m[3]\033[39m - вывести список вакансий')
        print('\t\033[32m[4]\033[39m - отсортировать по минимальной зарплате')

        print('\t\033[34m[0]\033[39m - выход из программы')

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
                    for_vac.keyword = temp_word
                    for_vac.vacancies = []
                    for t_vac in (hh, sj):
                        t_vac.keyword = temp_word
                        t_vac.get_vacancies(t_vac.get_request(), COUNT_LOAD_PAGE)
                        for_vac.vacancies.extend(t_vac.get_formatted_vacancies())

                keyword_find = temp_word

        elif user_input == '2':
            for t_vac in (hh, sj, for_vac):
                print(f'{t_vac.__class__.__name__}: Запись в файл {full_path_name_file(t_vac.file_json)}')
                t_vac.save_json_file()
                print(f'{t_vac.__class__.__name__}: Запись в файл {full_path_name_file(t_vac.file_txt)}')
                t_vac.save_csv_file(t_vac.file_txt, False)

            print(f'{for_vac.__class__.__name__}: Запись в файл {full_path_name_file(for_vac.file_csv)}')
            for_vac.save_csv_file(for_vac.file_csv)

        elif user_input == '3':
            print('\nСписок вакансий: ')
            for t_vac in for_vac.vacancies:
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
                print(f'\033[33mЗарплата\033[39m: {"не указана" if str_salary == "" else str_salary}')

                print(f'\033[33mТребования\033[39m: {t_vac["requirement"]}')
                print(f'\033[33mОтветсвенность\033[39m: {t_vac["responsibility"]}')

                if t_vac["api"] == 'HH':
                    print('Вакансия загружена с hh.ru\033[39m')
                else:
                    print('Вакансия загружена с superjob.ru\033[39m')

                print(' ---------------- ')


            pass
        elif user_input == '4':
            # print(user_input)
            pass


if __name__ == '__main__':
    main()