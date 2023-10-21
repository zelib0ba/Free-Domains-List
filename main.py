import xlsxwriter
import wget
import datetime
import zipfile as zip
import os,sys
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import json

os.system('cls||clear')

def get_html(url): # получаем страничку
    ua=UserAgent()
    header = {'User-Agent':str(ua.chrome)}
    r = requests.get(url,headers=header)
    r.encoding = 'utf8'
    return r.text 

soup = BeautifulSoup(get_html('https://www.tcinet.ru/statistics/list-of-domains/'), 'lxml')
head = soup.find("div", class_ = "domain terms ru")

file_name = head.find('a')['href'].split('/')[-1]

url_name = f"https://www.tcinet.ru/{head.find('a')['href']}"


try:
    # скачиваем файл
    wget.download(url_name)
except Exception as err:
    print ('Ошибка скачивания файла')
    print (err)
    sys.exit()
else:
    print (f'\nскачиваем свежий список освобождающихся доменов:')
    
# распаковываем файл
print (f'готово.\nраспаковка и обработка файла:')
zip_file = zip.ZipFile(file_name)
zip_file.extractall()
zip_file.close()

file_name = file_name[0:-4]
with open (f'{file_name}.txt','r') as f:
    a = f.readlines()

# открываем новый файл на запись
workbook = xlsxwriter.Workbook(f'{file_name}.xlsx')
# создаем там "лист"
worksheet = workbook.add_worksheet()
# сохраняем и закрываем
for key,i in enumerate(a): 
    worksheet.write (key,0,f'{i.strip()}')
    worksheet.write(key,1,len(i.strip()[0:-3]))
workbook.close()

os.remove(f'{file_name}.zip')

print (f'ищите общий файл {file_name}.xlsx в папке "{os.getcwd()}"')



# ** список стоп слов 
stop_words_list = ['kazino','sex','gun','drug','strah','penis','pizda','zaim','zhopa','jopa','porno','pron','-', 'cazino', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# ** макс длина домена
domain_name_length = 12
print (f'\nСоздаю файл со списком доменов, в которых нет стоп слов:\n\033[31m{stop_words_list}\033[0m\nи длина доменного имени не больше {domain_name_length} символов\n')

for _ in os.listdir():
    if _.endswith('.txt'):
        file_name = _

with open (f'{os.getcwd()}/{file_name}','r') as f:
    domain_list = f.readlines()


good_domain_list = []
bad_domain_list = []
stop_count = 0

for domain_name in domain_list:
    if len(domain_name.split('.')[0]) <= domain_name_length:
        for stop_word in stop_words_list:
            if stop_word in domain_name:
                stop_count += 1
                break
            else:
                stop_count = 0
        if stop_count > 0:
            bad_domain_list.append (f'{domain_name.strip()}')
        if stop_count == 0:
            good_domain_list.append (f'{domain_name.strip()}')


workbook = xlsxwriter.Workbook(f'{os.getcwd()}/GoodDomains_{file_name[9:17]}.xlsx')
# создаем там "лист"
worksheet = workbook.add_worksheet()
# сохраняем и закрываем
for key,i in enumerate(good_domain_list): 
    worksheet.write (key,0,f'{i.strip()}')
    worksheet.write(key,1,len(i.strip()[0:-3]))
try:
    workbook.close()
except Exception as err:
    print (f'\033[31m\033[1mОшибка записи файла - {err}\033[0m')

os.remove(f'{file_name}')
print (f'ищите обработанный файл GoodDomains_{file_name[9:17]}.xlsx в папке "{os.getcwd()}"')


quit()
# ** функция для проверки домена на занятость. 
def whois (domain):
    url = f'http://api.whois.vu/?q={domain}&clean'
    ua=UserAgent()
    header = {'User-Agent':str(ua.chrome)}
    r = requests.get(url,headers=header)
    r.encoding = 'utf8'
    w = json.loads(r.text)
    if w['available'] != 'yes':
        timestamp = w['expires']
        value = datetime.datetime.fromtimestamp(timestamp)
        res = f"\033[31mДомен HTTP://{w['domain'].upper()} занят \033[0m\nокончение регистрации: {value.strftime('%Y-%m-%d')}\n\n"
    else:
        res = f"\033[32m{w['domain']} свободен\033[0m\n\033[1m•проверить что там было на \033[4mhttps://web.archive.org/web/2/{w['domain']}\n\n\033[0m"
    return res

# ** проверка на занятость доменов из списка good_domain_list
for i in good_domain_list:
    time.sleep(2)
    print (whois(i))


