from employer_id import employers
from utils import *
from Creator import *
print('Здравствуйте!')
print('Программа имеет вакансии 10 компаний')
for i in employers:
    print(i)

print('Хотите посмотреть?')
answer = input('Да/Нет')
if answer.lower() == 'да':

    data_base = DATABASE() #Создание экземпляра класса DATABSE
    data_base.create_data_base()#Создание базы данных

    data_base.create_employer_table()#Создание таблицы employers
    data_base.create_vacancies_table()#Создание таблицы vacancies
    data_base.insert_into_employers()#Заполние таблицы employers
    data_base.insert_into_vacancies()#заполнение таблицы vacancies



    while True:

     print('Вы можете посмтреть:')
     print('Список всех компаний и количество вакансий у каждой компании. Для этого нажмите 1')
     print('Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию. Для этого нажмите 2')
     print('Среднюю зарплату по вакансиям. Для этого нажмите 3' )
     print('Список всех вакансий, у которых зарплата выше средней по всем вакансиям. Для этого нажмите 4')
     print('Список всех вакансий, по ключевому слову. Для этого нажмите 5')

     print('Введите цифру')
     guest = int(input())
     if guest == 1:
         get_companies_and_vacancies_count() #Вызов функции из файла utils

     elif guest == 2:
         get_all_vacancies()

     elif guest == 3:
         get_avg_salary()

     elif guest == 4:
         get_vacancies_with_higher_salary()

     elif guest == 5:
         word = input('Введите ключевое слово, например - Python')
         get_vacancies_with_keyword(word)

     print('Хотите продолжить?')
     finish = input('Да/Нет')

     if finish.lower() == 'да':
         pass
     else:
         print('До свидания!')
         break

else:
    print('До свидания!')


