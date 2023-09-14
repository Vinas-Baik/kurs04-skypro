
from utils.svn_utils import *
from utils.svn_class import *

COUNT_LOAD_PAGE = 1
COUNT_VAC_PER_PAGE = 20


def user_menu(keyword_find, count_vac) -> str:
    print('\n -----= Меню =----- ')
    print(f'Количество загруженных вакансий: {count_vac}\n')
    print(f'\t\033[32m[1]\033[39m - указать новое слово для поиска вакансий '
          f'(текущее слово для поиска: {keyword_find})')
    print('\t\033[32m[2]\033[39m - записать вакансии c HH и SJ в '
          'файлы JSON и TXT')
    print('\t\033[32m[3]\033[39m - записать отформатированные '
          'вакансии в файлы JSON, TXT и CSV')
    print()
    print('\t\033[34m[4]\033[39m - вывести список вакансий')
    print('\t\033[34m[5]\033[39m - отсортировать по минимальной зарплате')
    print('\t\033[34m[6]\033[39m - вывести ТОП вакансий по зарплате')
    print('\t\033[34m[7]\033[39m - отобрать вакансии по зарплате')
    print('\t\033[34m[8]\033[39m - отобрать вакансии по зарплате')
    print()
    print('\t\033[35m[9]\033[39m - добавить новую вакансию')
    print()
    print('\t\033[31m[0]\033[39m - выход из программы')

    menu_item = '0123456789'.strip()

    user_input = check_line_entry(
        f'Выберите пункт меню ({", ".join(menu_item)})',
        ''.join(menu_item),
        f'разрешен ввод только {", ".join(menu_item)}')
    return user_input

def main():

    keyword_find = 'python'

    print(f'\n-> Установлено слово для поиска вакансий: '
          f'\033[32m{keyword_find}\033[39m')

    hh = HeadHunterAPI(keyword_find, COUNT_VAC_PER_PAGE)
    sj = SuperJobAPI(keyword_find, COUNT_VAC_PER_PAGE)
    for_vac = Formatted_Vacancies(keyword_find)

    for t_vac in (hh, sj):
        t_vac.get_vacancies(COUNT_LOAD_PAGE)
        for_vac.vacancies.extend(t_vac.get_formatted_vacancies())

    while True:
        user_input = user_menu(keyword_find, len(for_vac.vacancies))

        if user_input == '0':
            print('Пока !')
            break
        elif user_input == '1':
            print(f'\n -> Установлено слово для поиска вакансий: '
                  f'\033[32m{keyword_find}\033[39m ')
            temp_word = input('Введите новое слово для поиска (пустой ввод - '
                              'слово для поиска остается старым): ').strip().lower()
            if temp_word != '':
                if temp_word != keyword_find:
                    print(f'-> Установлено новое слово для поиска вакансий: '
                          f'\033[32m{temp_word}\033[39m ')
                    for_vac.keyword = temp_word
                    for_vac.vacancies = []
                    for t_vac in (hh, sj):
                        t_vac.keyword = temp_word
                        t_vac.get_vacancies(COUNT_LOAD_PAGE)
                        for_vac.vacancies.extend(t_vac.get_formatted_vacancies())

                keyword_find = temp_word

        elif user_input == '2':
            print('\n\t\t \033[35m---= Запись вакансий c HH и SJ в файлы =---\033[39m\n')
            for t_vac in (hh, sj, for_vac):
                print(f'Запись в файл {full_path_name_file(t_vac.file_json)}')
                t_vac.save_json_file()
                print(f'Запись в файл {full_path_name_file(t_vac.file_txt)}')
                t_vac.save_csv_file(t_vac.file_txt, False)

        elif user_input == '3':
            print('\n\t\t \033[35m---= Запись отформатированных вакансий в файлы =---\033[39m\n')
            print(f'Запись в файл {full_path_name_file(for_vac.file_json)}')
            for_vac.save_json_file()
            print(f'Запись в файл {full_path_name_file(for_vac.file_txt)}')
            for_vac.save_csv_file(for_vac.file_txt, False)
            print(f'Запись в файл {full_path_name_file(for_vac.file_csv)}')
            for_vac.save_csv_file(for_vac.file_csv)


        elif user_input == '4':
            print('\nСписок вакансий: ')
            for_vac.print_vacancies()

        elif user_input == '5':
            for_vac.sort_vacancies()

        elif user_input == '6':
            count_top = check_line_entry('Введите количество вакансий в ТОП',
                                         '0123456789', 'разрешен ввод только цифр')
            for_vac.get_top_vacancies(int(count_top))

        elif user_input == '7':
            sal_from_vac = check_line_entry('Начальная зарплата',
                                         '0123456789', 'разрешен ввод только цифр')
            sal_to_vac = check_line_entry('Начальная зарплата',
                                         '0123456789', 'разрешен ввод только цифр')
            for_vac.get_vacancies_by_salary(f'{sal_from_vac}-{sal_to_vac} руб.')

        elif user_input == '8':
            find_word = check_line_entry('Введите слово для поиска ')
            for_vac.find_vacancies(find_word)


        elif user_input == '9':
            print('Добавление новой вакансии:')
            name_vac = check_line_entry('Имя вакансии (\033[35mexit\033[39m - выход)')
            if name_vac.lower() != 'exit':
                area_vac = check_line_entry('Город')
                url_vac = check_line_entry('Ссылка на вакансию')
                sal_from_vac = check_line_entry('Начальная зарплата',
                                                '0123456789', 'разрешен ввод только цифр')
                sal_to_vac = check_line_entry('Конечная зарплата',
                                              '0123456789', 'разрешен ввод только цифр')
                req_vac = check_line_entry('Требования')
                res_vac = check_line_entry('Обязанности')
                emp_vac = check_line_entry('Название организации')

                for_vac.add_vacancy(Vacancy(name=name_vac, url=url_vac,
                                            salary=f'{sal_from_vac}-{sal_to_vac} руб.',
                                            requirements=req_vac, town=area_vac,
                                            responsibility=res_vac, employer=emp_vac))



if __name__ == '__main__':
    main()