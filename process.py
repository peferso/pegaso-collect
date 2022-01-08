from bs4 import BeautifulSoup
raw_data_folder = 'pegaso-collect/raw-data'
html = raw_data_folder + '/data_2022-01-08_15-17-12376385_1.html'
parsed_html = BeautifulSoup(html, features="html.parser")
print(parsed_html.body.find('div', attrs={'class':'ma-AdList'}).text)
