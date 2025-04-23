import threading
from config import Config
from scrapper import Scrapper, FileManager
from utils import ExcelWriter, Spinner
import time

start_time = time.time()


class App:
    def __init__(self):
        self.settings = Config()
        self.file_manager = FileManager(self.settings.PATH)
        self.scrapper = Scrapper(self.settings, self.file_manager)
        self.writer = ExcelWriter(self.settings.PATH)

    def run(self):
        # stop_event = threading.Event()
        # spinner = Spinner(stop_event)
        # spinner_thread = threading.Thread(target=spinner.start)
        # spinner_thread.start()

        self.writer.write(self.scrapper.scrapper())
        #
        # stop_event.set()
        # spinner_thread.join()


if __name__ == '__main__':
    App().run()


end_time = time.time()

print(f'Final execution time: {end_time-start_time} seconds')
