import threading
from utils import loading_spinner, writer
from scraper import product_scrapper, pages


if __name__ == '__main__':
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=loading_spinner, args=(stop_event,))
    spinner_thread.start()

    writer(parameter=product_scrapper, pages=pages)
    
    stop_event.set()
    spinner_thread.join()
