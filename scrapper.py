import requests
from bs4 import BeautifulSoup as bs
import lxml
from decouple import config
import time
from pathlib import Path


base_url = config('BASE_URL')
login_url = config('LOGIN_URL')
login_username = config('LOGIN_USERNAME')
password = config('PASSWORD')
page_url = config('PAGE_URL')
user_agent = config("USER_AGENT")
page = 1
PATH = Path.home() / 'OneDrive' / 'Рабочий стол' / 'SCRAPPING' / 'Vita_Scrapper'

headers = {
    'User-Agent' : user_agent,
}


session = requests.session()

response = session.get(login_url)
soup = bs(response.text, 'lxml')
csrftoken = soup.find('form').find('input').get('value')

cookies = response.cookies

headers['X-CSRF-Token'] = csrftoken
headers['X-Requested-With'] = 'XMLHttpRequest'
headers['Referer'] = login_url

payload = {
    'csrfmiddlewaretoken' : csrftoken,
    'username': login_username,
    'password': password,
}

login_response = session.post(login_url, data=payload, headers=headers, allow_redirects=True)
soup = bs(login_response.text, 'lxml')
pages = int(soup.find('span', class_='pagination-info').text.split()[-1])


def file_loader(url):
    img_dir = PATH / 'Images'
    img_dir.mkdir(parents=True, exist_ok=True)
    filename = img_dir / ('photo_' + url.split('/')[-1])

    response = requests.get(url, stream=True, timeout=60)
    
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(1024*1024):
            file.write(chunk)


def product_scrapper(pages):
    for page in range(1, pages+1):
        time.sleep(2)
        url = page_url + str(page)
        
        response = session.get(url, headers=headers)
        soup = bs(response.text, 'lxml')
        product_data = soup.find_all('div', class_='product-card')

        for product in product_data:
            name = product.find('div', class_='product-info').find('h2').text
            code = product.find('p', class_='code').text.split(':')[-1].strip()
            image_url = product.find('img').get('src')
            file_loader(image_url)
            
            yield name, code, image_url
