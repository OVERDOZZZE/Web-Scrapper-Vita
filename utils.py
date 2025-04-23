import xlsxwriter
import sys
import time


class ExcelWriter:
    def __init__(self, path):
        self.filepath = path / 'config' / 'data.xlsx'

    def write(self, data_generator):
        # book = xlsxwriter.Workbook(filename=self.filepath)
        # page = book.add_worksheet('Products')
        # headers = ['Name', 'Code', 'Image URL']
        #
        # for i, header in enumerate(headers):
        #     page.write(0, i, header)
        #
        # page.set_column('A:A', 20)
        # page.set_column('B:B', 20)
        # page.set_column('C:C', 50)
        #
        # row = 1
        for product in data_generator:
            pass
            # for i in range(len(product)):
            #     page.write(row, i, product[i])
            # row += 1
        #
        # book.close()
    

class Spinner:
    def __init__(self, stop_event):
        self.stop_event = stop_event

    def start(self):
        spinner = ['|', '/', '-', '\\']
        idx = 0
        while not self.stop_event.is_set():
            sys.stdout.write('\rLoading... ' + spinner[idx % len(spinner)])
            sys.stdout.flush()
            idx += 1
            time.sleep(0.3)
        sys.stdout.write('\rDone!       \n')
