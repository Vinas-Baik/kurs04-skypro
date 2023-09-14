## Курсовой проект по ООП “Парсер вакансий”

Сделан Садыковым Виктором Наильевичем 

студентом курса Скайпро Питон разработчик 

Класс Formatted_Vacancies(Work_Vacancy) - содержит следущие данные с вакансий, загруженных с сайтов HH и SuperJob:
1. имя вакансии
2. город вакансии
3. ссылка на вакансию
4. зарплата минимальная
5. зарплата максимальная
6. требования
7. обязанности
8. фирма заказчик
9. ключ api - откуда загружена вакансия

класс Work_Vacancy():  - содержит переменные и функции для использования в дочерних классах:
1. Formatted_Vacancies
2. HeadHunterAPI
3. SuperJobAPI


Меню 


-> Установлено слово для поиска вакансий: python

 -----= Меню =----- 
Количество загруженных вакансий: 37

	[1] - указать новое слово для поиска вакансий (текущее слово для поиска: python)
	[2] - записать вакансии c HH и SJ в файлы JSON и TXT
	[3] - записать отформатированные вакансии в файлы JSON, TXT и CSV

	[4] - вывести список вакансий
	[5] - отсортировать по минимальной зарплате
	[6] - вывести ТОП вакансий по зарплате
	[7] - отобрать вакансии по зарплате
	[8] - отобрать вакансии по слову

	[9] - добавить новую вакансию

	[0] - выход из программы
Выберите пункт меню (0, 1, 2, 3, 4, 5, 6, 7, 8, 9): 

1 пункт - указать слово и произвести поиск вакансий на ХХ и СуперДжоб по введенному слову
2 пункт - записывает данные загруженные с ХХ и СуперДжоб в файлы JSON и TXT в папку data 
3 пункт - записывает отформатированные вакансии в файлы JSON, TXT, CSV в папку data, имя файла задается словом для поиска 
4 пункт - выводит список отформатированных вакансий на экран 
5 пункт - сортирует вакансии от минимальной зарплаты до максимальной 
6 пункт - выводит топ вакансий по зарплате (количество задает пользователь)
7 пункт - отбирает вакансии по зарплатной вилке (вилку задает пользователь)
8 пункт - ищет вакансии по наличию слова, заданного пользователем для поиска,
9 пункт - добавляем вакансию, которую затем можно записать в файлы, отсортировать и найти по слову 

0 - выход 
