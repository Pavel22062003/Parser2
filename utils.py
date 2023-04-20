from DBManager import DBManager
"""Функции для приведение информации из DBManager в читабельный вид"""
manger = DBManager()
def get_companies_and_vacancies_count():
    result = manger.get_companies_and_vacancies_count()
    for i in result:
        print(f'Компания - {i[0]} ')
        print(f'Количество вакансий - {i[1]}')
        print()



def get_all_vacancies():
    result = manger.get_all_vacancies()
    for i in result:
        print(f'Вакансия - {i[0]}')
        print(f'Минимальная зарплата - {i[1]}')
        print(f'Ссылка на ваканисю - {i[2]}')
        print(f'Название компании - {i[3]}')
        print()

def get_avg_salary():
    print(f'{manger.get_avg_salary()} руб')

def get_vacancies_with_higher_salary():
    result = manger.get_vacancies_with_higher_salary()
    for i in result:
        print(f'Вакансия - {i[0]}')
        print()


def get_vacancies_with_keyword(word):
    result = manger.get_vacancies_with_keyword(word.title())
    for i in result:
        print(f'Вакансия - {i[1]}')
        print(f'Ссылка на вакансию - {i[6]}')
        print()
