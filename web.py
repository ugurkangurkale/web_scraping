from bs4 import BeautifulSoup
import requests
import time
import mysql.connector

def filmekleme(title,year
               ):
    connection = mysql.connector.connect(host="localhost",
                                         user="root",
                                         password="",
                                         database="filmler")
    cursor = connection.cursor()
    sql = ("INSERT INTO filmler(film_name,film_year) Values(%s,%s)")
    val = (title,year)
    cursor.execute(sql,val)
    try:
        connection.commit()
    except mysql.connector.Error as err:
        print("Hata Oluştu",err)
    finally:
        connection.close()
    print("Database Bağlantısı Kesildi...")

headers ={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}


url = ("https://www.imdb.com/chart/top/")

html = requests.get(url, headers = headers).content
soup = BeautifulSoup(html,"html.parser")

list = soup.find("tbody",{"class":"lister-list"}).find_all("tr")
id = 0
for tr in list:
    title = tr.find("td",{"class":"titleColumn"}).find("a").text
    year = tr.find("td",{"class":"titleColumn"}).find("span").text.strip("()")
    link = "https://www.imdb.com/" +tr.find("td",{"class":"titleColumn"}).find("a")["href"]
    time.sleep(1)
    html2 = requests.get(link, headers = headers).content
    soup2 = BeautifulSoup(html2,"html.parser")
    link2 = "https://www.imdb.com/" + soup2.find("div",{"class":"ipc-title__wrapper"}).find("a")["href"]
    id+=1

    html3 = requests.get(link2, headers = headers).content
    soup3 = BeautifulSoup(html3,"html.parser")
    aktör = "https://www.imdb.com/" + soup3.find("ul",{"class":"quicklinks"}).find("li",{"class":"subnav_item_main"}).find("a")["href"]
    
    html4 =requests.get(aktör, headers = headers).content
    soup4 =BeautifulSoup(html4,"html.parser")
    oyuncu = soup4.find("div",{"id":"media_index_name_filters"}).find("ul",{"class":"media_index_filter_section"}).find_all("li")
    print(f"{id}-Film adı: {title}, {year} \n OYUNCULARI:")
    """for x in oyuncu:
        oyuncular=soup4.find("li",{"class":""}).find("a")
        y = x.text.replace("(","")  
        z = y[:20].strip()
        print(z)"""
    filmekleme(title,year)