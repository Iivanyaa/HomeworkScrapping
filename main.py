# div class = "vacancy-serp-item"
# span class = "bloko-header-section-2"
# 

import requests
from bs4 import BeautifulSoup

# получаем страницу с самыми свежими вакансиями
ret = requests.get('https://spb.hh.ru/search/vacancy?L_save_area=true&text=Python+django+flask&search_field=name&search_field=description&excluded_text=&area=1&area=2&salary=&currency_code=USD&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50')
soup = bs4.BeautifulSoup(ret.text, 'lxml')

# извлекаем посты
vacancies = soup.find_all('href', class_='serp-item__title')
for post in vacancies:
   print(post)
   post_id = post.parent.attrs.get('id')
   # если идентификатор не найден, это что-то странное, пропускаем
   if not post_id:
       continue
   post_id = int(post_id.split('_')[-1])
   print('post', post_id)

   # извлекаем хабы поста
   hubs = post.find_all('a', class_='hub-link')
   for hub in hubs:
       hub_lower = hub.text.lower()
       # ищем вхождение хотя бы одного желаемого хаба
       if any([hub_lower in desired for desired in DESIRED_HUBS]):
           # пост нам интересен - делаем с ним все что захотим:
           # можно отправит в телеграм уведомление, можно на почту и т.п.
           title_element = post.find('a', class_='post__title_link')
           print(title_element.text, title_element.attrs.get('href'))

           # так как пост уже нам подошел - дальше нет смысла проверять хабы
           break
