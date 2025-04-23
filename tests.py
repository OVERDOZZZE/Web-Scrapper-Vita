from decouple import config
from bs4 import BeautifulSoup as bs
import requests
import lxml
from pathlib import Path
import threading
import time

MAX_THREADS = 10
semaphore = threading.Semaphore(MAX_THREADS)

start_time = time.time()

headers = {
    'User-Agent': config('USER_AGENT')
}
page_url = config('PAGE_URL')
login_url = config('LOGIN_URL')
base_url = config('BASE_URL')

session = requests.session()

response = session.get(base_url, headers=headers)
soup = bs(response.text, 'lxml')

csrftoken = soup.find('form').find('input').get('value')
print(csrftoken)

payload = {
    'username': config('LOGIN_USERNAME'),
    'password': config('PASSWORD'),
    'csrfmiddlewaretoken': csrftoken
}
headers.update({
    'X-CSRF-Token': csrftoken,
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': login_url
})

login_response = session.post(login_url, data=payload, headers=headers, allow_redirects=True)

soup = bs(login_response.text, 'lxml')
print(soup)
pages = int(soup.find('span', class_='pagination-info').text.split()[-1])

image_dir = Path.home() / 'OneDrive' / 'Рабочий стол' / 'images_'
image_dir.mkdir(parents=True, exist_ok=True)

lock = threading.Lock()


def image_url_holder(url):
    page_response = session.get(url, headers=headers)
    page_soup = bs(page_response.text, 'lxml')

    current_img = page_soup.find('img')
    counter = 0

    while current_img:
        img_src = current_img.get('src')

        if img_src:
            yield img_src

        counter += 1
        current_img = current_img.find_next('img')


def downloader(parameter, url):
    with semaphore:
        print(f"Started downloading from {url}")
        for image_src in parameter(url):
            filename = image_dir / ('photo_' + str(image_src.split('/')[-1]))
            image_response = session.get(image_src, stream=True, timeout=60)
            with lock:
                with open(filename, 'wb') as file:
                    for chunk in image_response.iter_content(1024*1024):
                        file.write(chunk)
            print(f"Downloaded {image_src}")
        print(f"Finished downloading from {url}")


threads = []

for i in range(1, pages+1):
    t = threading.Thread(target=downloader, args=(image_url_holder, page_url + str(i)))
    threads.append(t)
    t.start()


for t in threads:
    t.join()

print('Joins\' were executed')

end_time = time.time()

print(f'Final execution time: {end_time-start_time} seconds')
