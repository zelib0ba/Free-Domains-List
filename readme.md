## Free Domains List  
### Скрипт создает список удаляемых доменов в зоне RU  
каждый раз при запуске скрипта, берется свежий список удалемых доменов в зоне RU с сайта [_ТЦИ_](https://www.tcinet.ru/statistics/list-of-domains/)  
на выходе получаем 2 xlsx файла:  
**RUDelListYYYMMDD.xlsx** - список всех доменов (первый столбец список доменов , второй длина домена).  
**GoodDomains_YYYYMMDD.xlsx** - список доменов без стоп слов, переменная [`stop_words_list`](https://github.com/zelib0ba/Free-Domains-List/blob/main/main.py#L66) и максимальной длиной доменного имени, переменная [`domain_name_lengt`](https://github.com/zelib0ba/Free-Domains-List/blob/main/main.py#L69)  

p.s. так же есть функция [`whois`](https://github.com/zelib0ba/Free-Domains-List/blob/main/main.py#L116) проверки списка доменов на занятость.  
