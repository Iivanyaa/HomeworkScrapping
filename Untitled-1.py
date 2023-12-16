# div class = "vacancy-serp-item"
# span class = "bloko-header-section-2"
# 

import requests
import bs4

# получаем страницу с самыми свежими вакансиями
ret = requests.get('https://spb.hh.ru/search/vacancy?L_save_area=true&search_field=name&search_field=description&area=1&area=2&items_on_page=50&currency_code=USD&text=Python+django+flask&enable_snippets=true')
vacancies_list = ret.text

vacancies = bs4.BeautifulSoup(vacancies_list, 'lxml')
vacancies.findall('div', class_'vacancy-serp-item__layout')