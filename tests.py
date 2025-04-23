from decouple import config
from bs4 import BeautifulSoup as bs
import requests
import lxml
from pathlib import Path
import threading
import time
from typing import Generator
import logging
import uuid


class CustomLogger:
    def __init__(self, log_file: Path):
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.DEBUG)
        self.log_file = log_file
        self._setup_handlers()

    def _setup_handlers(self):
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger
    

class ConfigLoader:
    def __init__(self):
        self.user_agent = config('USER_AGENT')
        self.page_url = config('PAGE_URL')
        self.login_url = config('LOGIN_URL')
        self.base_url = config('BASE_URL')
        self.username = config('LOGIN_USERNAME')
        self.password = config('PASSWORD')
        self.main_path = Path.home() / 'OneDrive' / 'Рабочий стол' 
        self.log_file = self.main_path / 'logs.txt'


class SessionManager:
    def __init__(self, config: ConfigLoader, logger: logging.Logger):
        self.config = config
        self.session = requests.Session()
        self.headers = {
            'User-Agent': self.config.user_agent
        }
        self.logger = logger

    def authenticate(self):
        try:
            response = self.session.get(self.config.base_url, headers=self.headers)
            soup = bs(response.text, 'lxml')
            csrftoken = soup.find('form').find('input').get('value')
            self.logger.info("CSRF token retrieved")

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
            pages = int(soup.find('span', class_='pagination-info').text.split()[-1])

            if not pages:
                soup.select_one('span', class_='pagination-info')

            self.logger.info(f"Authentication successful, found {pages} pages")
            
            return pages
        except Exception as e:
            self.logger.error(f'Error {e} when trying to authenticate')


class ImageExtractor:
    def __init__(self, session_manager: SessionManager, logger: logging.Logger):
        self.session_manager = session_manager
        self.logger = logger

    def extract_urls(self, url: str) -> Generator[str, None, None]:
        try:
            page_response = self.session_manager.session.get(url, headers=self.session_manager.headers)
            page_soup = bs(page_response.text, 'lxml')

            for img_tag in page_soup.find_all('img'):
                img_src = img_tag.get('src')
                if img_src:
                    yield img_src
                                
        except Exception as e:
            self.logger.error(f'Error {e} when trying to extract urls')


class ImageDownloader:
    def __init__(self, session_manager: SessionManager, image_dir: Path, lock: threading.Lock, logger: logging.Logger):
        self.session_manager = session_manager
        self.image_dir = image_dir
        self.lock = lock
        self.logger = logger

    def download(self, img_url):
        try:
            filename = self.image_dir / f'{uuid.uuid4()}.jpg'
            image_response = self.session_manager.session.get(img_url, stream=True, timeout=60)
            with self.lock:
                with open(filename, 'wb') as file:
                    for chunk in image_response.iter_content(1024 * 1024):
                        file.write(chunk)
            self.logger.info(f"Downloaded {img_url}")
        except Exception as e:
            self.logger.error(f'Error {e} when trying to download image')


class ScraperController:
    def __init__(self):
        self.config = ConfigLoader()
        self.logger = CustomLogger(self.config.log_file).get_logger()
        self.session_manager = SessionManager(self.config, self.logger)
        self.extractor = ImageExtractor(self.session_manager, self.logger)
        self.lock = threading.Lock()
        self.image_dir = self.config.main_path / '_images'
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.downloader = ImageDownloader(self.session_manager, self.image_dir, self.lock, self.logger)
        self.max_threads = 10
        self.semaphore = threading.Semaphore(self.max_threads)

    def handle_download(self, url):
        with self.semaphore:
            self.logger.info(f"Started downloading from {url}")
            for img_url in self.extractor.extract_urls(url):
                self.downloader.download(img_url)
            self.logger.info(f"Finished downloading from {url}")

    def run(self):
        self.logger.info('Start of the program execution')
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

        self.logger.info("Joins' were executed")
        end_time = time.time()
        self.logger.info(f'Final execution time: {end_time - start_time} seconds')


if __name__ == '__main__':
    ScraperController().run()
    