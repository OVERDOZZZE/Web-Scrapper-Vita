from decouple import config
from pathlib import Path


class Config:
    base_url = config('BASE_URL')
    login_url = config('LOGIN_URL')
    login_username = config('LOGIN_USERNAME')
    password = config('PASSWORD')
    page_url = config('PAGE_URL')
    user_agent = config("USER_AGENT")
    page = 1
    time_sleep = 3
    PATH = Path.home() / 'OneDrive' / 'Рабочий стол' / 'Scrapping' / 'Vita_Scrapper'

