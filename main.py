import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import mysql.connector as msql
from mysql.connector import Error
# try:
#     conn=msql.connect(host="localhost", user="root",password="")
#     if conn.is_connected():
#         cursor=conn.cursor()
#         cursor.execute("CREATE DATABASE aws")
#         print("Database is created!")
# except Error as e:
#     print("error while connecting to mysql",e)

theverge_r1 = requests.get("https://www.theverge.com/")
cover_theverge= theverge_r1.content
soap_theverge= BeautifulSoup(cover_theverge,'html5lib')
all_cover_articles=soap_theverge.find_all('li',{'class':'duet--content-cards--content-card'})

number_of_artcles= 5

id_theverge=[]
url_theverge=[]
headline_theverge=[]
author_theverge=[]
date_theverge=[]

for n in np.arange(0,number_of_artcles):
    #getting id
    id=(1+n)
    #print(id)
    id_theverge.append(id)

    #getting urls
    url=all_cover_articles[n].find("a")['href']
    #print(url)
    url_theverge.append(url)

    #getting headline
    headline=all_cover_articles[n].find("a",{"class":'group-hover:shadow-underline-franklin'}).get_text()
    #print(headline)
    headline_theverge.append(headline)

    #getting author name
    author=all_cover_articles[n].find("a",{'class':"text-gray-31"}).get_text()
    #print(author)
    author_theverge.append(author)

    #getting time-date
    date=all_cover_articles[n].find("span",{'class':"text-gray-63"}).get_text()
    #print(date)
    date_theverge.append(date)

dictionary={"Id":id_theverge ,"Url":url_theverge,"Headline":headline_theverge,"Author":author_theverge,"Date":date_theverge}
df=pd.DataFrame(dictionary,columns=["Id", "Url", "Headline", "Author", "Date"])
df.to_csv("C:\\Users\\MOHD ZAID\\Desktop\\website scrapping\\data.csv")
df=pd.read_csv("C:\\Users\\MOHD ZAID\\Desktop\\website scrapping\\data.csv")
print(df)
print(df.dtypes)
try:
    conn=msql.connect(host="localhost",database="aws", user="root",password="")
    if conn.is_connected():
        cursor=conn.cursor()
        cursor.execute("select database();")
        record=cursor.fetchone()
        print("You're connected to database:", record)
        cursor.execute("DROP TABLE IF EXISTS news_data_1;")
        print("creating table....")
        cursor.execute("CREATE TABLE news_data_1(Id varchar(100), Url varchar(500), Headline varchar(350), Author varchar(255), Date varchar(100))")
        print("Table is created!")
        for i,row in df.iterrows():
            sql="INSERT INTO aws.news_data_1 VALUES(%s,%s,%s,%s,%s)"
            data_news=(id , url,headline,author, date)
            cursor.execute(sql,data_news,tuple(row))
            print("Record inserted!")
            conn.commit()
except Error as e:
    print("Error while  connecting to mysql",e)
          