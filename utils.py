import xlsxwriter
import sys
import time
from scraper import PATH


def loading_spinner(stop_event):
    spinner = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write('\rLoading... ' + spinner[idx % len(spinner)])
        sys.stdout.flush()
        idx += 1
        time.sleep(0.3)
    sys.stdout.write('\rDone!      \n')


def writer(parameter, pages):
    filename = PATH / 'data.xlsx'

    book = xlsxwriter.Workbook(filename=filename)
    page = book.add_worksheet('Products')

    row = 1
    column = 0

    page.set_column('A:A', 20)
    page.set_column('B:B', 20)
    page.set_column('C:C', 50)
    page.set_column('D:D', 50)

    page.write(0, column, 'Product Name')
    page.write(0, column+1, 'Product Code')
    page.write(0, column+2, 'Product Image URL')


    for product in parameter(pages):
        page.write(row, column, product[0])
        page.write(row, column+1, product[1])
        page.write(row, column+2, product[2])
        row += 1
        
    book.close()


