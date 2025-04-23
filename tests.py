from decouple import config
from bs4 import BeautifulSoup as bs
import requests
import lxml
from pathlib import Path
import threading
import time
from typing import Generator


class ConfigLoader:
    def __init__(self):
        self.user_agent = config('USER_AGENT')
        self.page_url = config('PAGE_URL')
        self.login_url = config('LOGIN_URL')
        self.base_url = config('BASE_URL')
        self.username = config('LOGIN_USERNAME')
        self.password = config('PASSWORD')


class SessionManager:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.session = requests.Session()
        self.headers = {
            'User-Agent': self.config.user_agent
        }

    def authenticate(self):
        response = self.session.get(self.config.base_url, headers=self.headers)
        soup = bs(response.text, 'lxml')
        csrftoken = soup.find('form').find('input').get('value')

        payload = {
            'username': self.config.username,
            'password': self.config.password,
            'csrfmiddlewaretoken': csrftoken
        }
        self.headers.update({
            'X-CSRF-Token': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.config.login_url
        })

        login_response = self.session.post(self.config.login_url, data=payload, headers=self.headers, allow_redirects=True)
        soup = bs(login_response.text, 'lxml')
        return int(soup.find('span', class_='pagination-info').text.split()[-1])


class ImageExtractor:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    def extract_urls(self, url: str) -> Generator[str, None, None]:
        page_response = self.session_manager.session.get(url, headers=self.session_manager.headers)
        page_soup = bs(page_response.text, 'lxml')
        current_img = page_soup.find('img')

        while current_img:
            img_src = current_img.get('src')
            if img_src:
                yield img_src
            current_img = current_img.find_next('img')


class ImageDownloader:
    def __init__(self, session_manager: SessionManager, image_dir: Path, lock: threading.Lock):
        self.session_manager = session_manager
        self.image_dir = image_dir
        self.lock = lock

    def download(self, img_url):
        filename = self.image_dir / ('photo_' + str(img_url.split('/')[-1]))
        image_response = self.session_manager.session.get(img_url, stream=True, timeout=60)
        with self.lock:
            with open(filename, 'wb') as file:
                for chunk in image_response.iter_content(1024 * 1024):
                    file.write(chunk)


class ScraperController:
    def __init__(self):
        self.config = ConfigLoader()
        self.session_manager = SessionManager(self.config)
        self.extractor = ImageExtractor(self.session_manager)
        self.lock = threading.Lock()
        self.image_dir = Path.home() / 'OneDrive' / 'Рабочий стол' / 'images_'
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.downloader = ImageDownloader(self.session_manager, self.image_dir, self.lock)
        self.max_threads = 10
        self.semaphore = threading.Semaphore(self.max_threads)

    def handle_download(self, url):
        with self.semaphore:
            for img_url in self.extractor.extract_urls(url):
                self.downloader.download(img_url)

    def run(self):
        start_time = time.time()
        pages = self.session_manager.authenticate()
        threads = []

        for i in range(1, pages + 1):
            full_url = self.config.page_url + str(i)
            t = threading.Thread(target=self.handle_download, args=(full_url,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print("Joins' were executed")
        end_time = time.time()
        print(f'Final execution time: {end_time - start_time} seconds')


if __name__ == '__main__':
    ScraperController().run()
