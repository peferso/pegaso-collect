import os
from bs4 import BeautifulSoup

# Variables
THIS_SCRIPT_PATH = '/home/pietari/PycharmProjects/cars/pegaso-collect'
raw_data_folder = 'raw-data'
html_file = raw_data_folder + '/data_2022-01-08_16-03-51187726_1.html'

# Main

os.chdir(THIS_SCRIPT_PATH)

f = open(html_file, 'r')
html = f.read()
parsed_html = BeautifulSoup(html, features="html.parser")
print(parsed_html.body.find_all('div', attrs={'class':'ma-AdList'}))
f.close()
