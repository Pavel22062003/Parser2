import requests
import psycopg2
from employer_id import employers
class Employers:
    'Данный класс получает информацию о работодателях от api hh, и формирует данные для дальнейшей их записи в базу данных'

    all = [] #Список всех эземпляров работодателей
    id_employer ={} #Словарь где хранятся название компании и их id, это сделано для того, чтобы потом присвоить вакансии правильный id работодателя
    def __init__(self,employer_id,hh_employer_id,trusted,company_name,type,area):
        '''При инициализации класс получает несколько атрибутов , далее они записываются в список all,'''
        self.employer_id = employer_id
        self.hh_employer_id = hh_employer_id #id работодателя на hh.ru
        self.trusted = trusted #Проверена ли компания
        self.company_name = company_name # Название компании
        self.type = type # Тип компании
        self.area = area # В каком городе компания
        self.all.append(self) # Добавление экземпялра в список all
    @classmethod
    def get_request(cls):
        """Метод делает запрос к api hh.ru, формирует из этих данных атрибуты экземпляра, потом вызывает инициализацию экземпляра"""
        counter = 1 # счётчик айдишников работодателей
        for i in employers:
            sourse = requests.get(f'https://api.hh.ru/employers/{employers[i]}')
            data = sourse.json()

            employer_id = counter
            hh_employer_id = data['id']
            trusted = data['trusted']
            company_name = data['name']
            type = data['type']
            area = data['area']['name']
            cls.id_employer[company_name] = counter # запись названия компании и её айдишника в словарь id_employer
            counter += 1

            cls(employer_id,hh_employer_id,trusted,company_name,type,area) #создание экземпляра класса



class Vacancies:
    """Данный класс получает информацию о вакансиях от работодателей с которыми работал класс Employers от api hh, и формирует данные для дальнейшей их записи в базу данных"""

    all = []
    def __init__(self,vacancy_id,name,city,salary_from,experience,employer_id,url):
        """Принцип работы здесь такой же , что и в классе Employers"""
        self.vacancy_id = vacancy_id
        self.name = name #Название вакансии
        self.city = city
        self.salary_from = salary_from #Минимальная зарплата по вакансии
        self.experience = experience #Требуемый опыт работв
        self.employer_id = employer_id #id работодателя
        self.url = url #ссылка на вакансию
        self.all.append(self) # добавление экземпялра в список all

    @classmethod
    def get_request(cls):
        """Принцип работы такой же что и get_request класса Employers"""
        counter = 1
        for i in employers:
            sourse = requests.get(f'https://api.hh.ru/vacancies?employer_id={employers[i]}')
            data = sourse.json()

            for i in range(len(data['items'])):
                vacancy_id = counter
                name = data['items'][i]['name']
                if data['items'][i]['address'] == None:
                    city = None
                else:
                    city = data['items'][i]['address']['city']
                if data['items'][i]['salary'] == None:
                    salary_from = None
                else:
                    salary_from = data['items'][i]['salary']['from']

                if data['items'][i]['experience'] == None:
                    experience = None
                else:
                    experience = data['items'][i]['experience']['name']
                employer_id = Employers.id_employer[data['items'][i]['employer']['name']] #Получение правильного айдишника компании их словаря id_employer класса Employers
                url = data['items'][i]['apply_alternate_url']
                counter += 1

                cls(vacancy_id,name,city,salary_from,experience,employer_id,url)


class DATABASE:
    """Данный класс создаёт базу данных и заполняет её"""
    data_base_name = 'hh_ru'#название базы данных

    def create_data_base(self)-> bool:
        #Метод для создания базы данных
        try:
            conn = psycopg2.connect(host='localhost',database='postgres',user='postgres',password='Persik012')
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE {self.data_base_name}')
            cursor.close()
            conn.close()
            return True
        except: #True означает,что база данных создана создана
            return True

    def create_employer_table(self)->bool:
       """Метод создаёт таблице employers"""
       try:
           with psycopg2.connect(host='localhost',database=self.data_base_name,user='postgres',password='Persik012') as conn:
               with conn.cursor() as cur:
                  cur.execute('CREATE TABLE employers '
                              '(employer_id serial PRIMARY KEY, '
                              'company_name varchar, '
                              'trusted bool, '
                              'type varchar(150), ' 
                              'area varchar(50),'
                              'hh_employer_id int)')

           conn.close()
           return True
       except:#True означает,что таблица создана
           return True

    def create_vacancies_table(self)->bool:
        """Метод для создания таблицы vacancies"""
        try:
           with psycopg2.connect(host='localhost', database=self.data_base_name, user='postgres', password='Persik012') as conn:

               with conn.cursor() as cur:
                  cur.execute('CREATE TABLE vacancies '
                            '(vacancy_id serial PRIMARY KEY, '
                            'vacancy_name varchar, '
                            'area varchar(50), '
                            'salary_from int, '
                            'experience varchar(50),'
                            'employer_id int, '
                            'vacancy_url varchar,'
                            'CONSTRAINT fk_vacancies_employer_id FOREIGN KEY(employer_id) REFERENCES employers(employer_id))')
           conn.close()
           return True
        except:
            return True











      #  except:#True означает,что таблица создана
       #     return True

    def insert_into_employers(self):
        """Метод записывает данные в таблицу employers"""
        Employers.get_request() #вызов метода класса employers для получения данных
        with psycopg2.connect(host='localhost',database=self.data_base_name,user='postgres',password='Persik012') as conn:
            with conn.cursor() as cur:
                for i in Employers.all: #считывание данных из списка all класса Employers
                   cur.execute('INSERT INTO employers VALUES(%s,%s,%s,%s,%s,%s)',(i.employer_id,i.company_name,i.trusted,i.type,i.area,i.hh_employer_id))
        conn.close()

    def insert_into_vacancies(self):
        """Метод записывает данные в таблицу vacancies"""
        Vacancies.get_request() ##вызов метода класса Vacancies для получения данных
        with psycopg2.connect(host='localhost', database=self.data_base_name, user='postgres',
                              password='Persik012') as conn:
            with conn.cursor() as cur:

                for i in Vacancies.all: #считывание данных из списка all класса Vacancies
                    cur.execute('INSERT INTO vacancies VALUES(%s,%s,%s,%s,%s,%s,%s)',(i.vacancy_id, i.name, i.city, i.salary_from, i.experience, i.employer_id,i.url))













