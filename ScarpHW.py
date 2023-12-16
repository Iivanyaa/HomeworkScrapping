import requests
import bs4
import fake_headers
import json

headers_gen = fake_headers.Headers(os='win', browser='chrome')
number_scarped_vacancies = 1
selected_vacancies = {}
selected_vacancies_number = 0

params = {
    'L_save_area': 'true',
    'text': 'python',
    'search_field': 'name',
    'excluded_text': '',
    'area': ['1', '2'],
    'salary': '',
    'currency_code': 'RUB',
    'order_by': 'relevance',
    'search_period': 0,
    'only_with_salary': 'true',
    'expirience': 'doesNotMatter',
    'page': 0,
    'items_on_page': '20'
}
HOST = 'https://spb.hh.ru/search/vacancy'
response = requests.get(HOST, headers=headers_gen.generate(), params=params)

while response.status_code == 200:
    response = requests.get(HOST, headers=headers_gen.generate(), params=params)
    page_number = params['page']
    print(F'Открыта страница HH №{page_number + 1}')
    page_html_data = response.text
    page_soup = bs4.BeautifulSoup(page_html_data, 'lxml')
    vacancies = page_soup.find_all('div', class_='vacancy-serp-item-body')
    print(F'найдено {len(vacancies)} вакансий на странице')
    if len(vacancies) > 0:
        for vacancy in vacancies:
            company_name_tag = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary')
            if company_name_tag is None:
                company_name = 'Название компании отсутствует'
            else:
                company_name = company_name_tag.text.strip()
                company_name = company_name.replace('\xa0', ' ')
                vacancy_name = (vacancy.find('span')).text.strip()
                salary = (vacancy.find('span', class_='bloko-header-section-2')).text.strip()
                salary = salary.replace('\u202f', ' ')
                city_tag = vacancy.find('div', class_='vacancy-serp-item-company')
                city = (city_tag.find_all('div', class_='bloko-text'))[1].text.strip()
                link = (vacancy.find('a', class_='serp-item__title'))['href']
                if '$' not in salary:
                    print(F'{number_scarped_vacancies}) Вакансия {vacancy_name} проанализирована (зарплата не в долларах)')
                    number_scarped_vacancies += 1
                else:
                    vacancy_response = requests.get(link, headers=headers_gen.generate())
                    vacancy_html_data = vacancy_response.text
                    vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, 'lxml')
                    vacancy_description_tag = vacancy_soup.find('div', class_='vacancy-description')
                    if vacancy_description_tag is None:
                        print(F'{number_scarped_vacancies}) Вакансия {vacancy_name} проанализирована (описание вакансии отсутствует)')
                        number_scarped_vacancies += 1
                    else:
                        vacancy_description_text = vacancy_description_tag.text.strip()
                        if ('Django' in vacancy_description_text and 'Flask' in vacancy_description_text):
                            selected_vacancies[selected_vacancies_number] = {
                                'Город': city,
                                'Название компании': company_name,
                                'Название вакансии': vacancy_name,
                                'Вилка ЗП': salary,
                                'Ссылка': link
                                }
                            print(F'{number_scarped_vacancies}) Вакансия {vacancy_name} проанализирована (параметры совпадают, добавлена в словарь)')
                            number_scarped_vacancies += 1
                            selected_vacancies_number += 1
                        else:
                            print(F'{number_scarped_vacancies}) Вакансия {vacancy_name} проанализирована (параметры не совпадают, в словарь не добавлена)')
                            number_scarped_vacancies += 1 
        params['page'] += 1
    else:
        print('Вакансии закончились')
        break
 
with open('selected_vacancies.json', 'w') as file:
    json.dump(selected_vacancies, file)


