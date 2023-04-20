import psycopg2
class DBManager:

    def get_companies_and_vacancies_count(self):
        companies_and_vacancies = []
        with psycopg2.connect(host='localhost', database='hh_ru', user='postgres', password='Persik012') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, COUNT(vacancy_id) '
                            'FROM vacancies '
                            'INNER JOIN employers USING(employer_id) '
                            'GROUP BY company_name')

                rows = cur.fetchall()
                for row in rows:
                    companies_and_vacancies.append(list(row))

        conn.close()
        return companies_and_vacancies

    def get_all_vacancies(self):
        all_vacancies = []
        with psycopg2.connect(host='localhost', database='hh_ru', user='postgres', password='Persik012') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name,salary_from,vacancy_url,company_name '
                            'FROM vacancies '
                            'INNER JOIN employers USING(employer_id)')

                rows = cur.fetchall()
                for row in rows:
                    all_vacancies.append(list(row))

        conn.close()
        return all_vacancies

    def get_avg_salary(self):
        avg_salary = ''
        with psycopg2.connect(host='localhost',database='hh_ru',user='postgres',password='Persik012') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT ROUND(AVG(salary_from),2) '
                            'FROM vacancies')
                rows = cur.fetchall()
                for row in rows:
                    avg_salary = list(row)[0]

        return avg_salary

    def get_vacancies_with_higher_salary(self):
        vacancies_with_higher_salary = []

        with psycopg2.connect(host='localhost',database='hh_ru',user='postgres',password='Persik012') as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT vacancy_name FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)')

                rows = cur.fetchall()
                for row in rows:
                    vacancies_with_higher_salary.append(list(row))

        return vacancies_with_higher_salary

    def get_vacancies_with_keyword(self,word=None):

        vacancies_with_keyword =[]

        with psycopg2.connect(host='localhost', database='hh_ru', user='postgres', password='Persik012') as conn:
            with conn.cursor() as cur:
                execute = f"""SELECT * FROM vacancies WHERE vacancy_name LIKE '%{word}%'"""
                cur.execute(execute)
                rows =cur.fetchall()
                for row in rows:
                    vacancies_with_keyword.append(list(row))

        return vacancies_with_keyword










