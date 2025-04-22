import requests
from bs4 import BeautifulSoup as bs
import lxml
import time
from pathlib import Path


class FileManager:
    def __init__(self, path: Path):
        self.img_dir = path / 'Images'
        self.img_dir.mkdir(parents=True, exist_ok=True)

    def image_loader(self, url):
        filename = self.img_dir / ('photo_' + url.split('/')[-1])
        response = requests.get(url, stream=True, timeout=60)

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(1024*1024):
                file.write(chunk)


class Scrapper:
    def __init__(self, settings, file_manager):
        self.settings = settings
        self.file_manager = file_manager
        self.session = requests.session()
        self.headers = {
            'User-Agent': settings.user_agent
        }
        self._authenticate()

    def _authenticate(self):
        response = self.session.get(self.settings.login_url)
        soup = bs(response.text, 'lxml')
        csrftoken = soup.find('form').find('input').get('value')
        self.headers.update({
            'X-CSRF-Token': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.settings.login_url
        })
        payload = {
            'csrfmiddlewaretoken' : csrftoken,
            'username': self.settings.login_username,
            'password': self.settings.password,
        }
        login_response = self.session.post(
            self.settings.login_url,
            data=payload,
            headers=self.headers
        )
        soup = bs(login_response.text, 'lxml')
        self.pages = int(soup.find('span', class_='pagination-info').text.split()[-1])

    def scrapper(self):
        for page in range(1, self.pages + 1):
            time.sleep(self.settings.time_sleep)
            url = self.settings.page_url + str(page)

            response = self.session.get(url, headers=self.headers)
            soup = bs(response.text, 'lxml')
            product_data = soup.find_all('div', class_='product-card')

            for product in product_data:
                name = product.find('div', class_='product-info').find('h2').text
                code = product.find('p', class_='code').text.split(':')[-1].strip()
                image_url = product.find('img').get('src')

                self.file_manager.image_loader(image_url)

                yield name, code, image_url
