#! /usr/bin/env python3

from typing import ContextManager
import requests
import pymysql.cursors


from bs4 import BeautifulSoup


URL_LIST = []

# Text extraction from html
def req2text(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    return text


def dbconnect():
    cnx = pymysql.connect(
    host="192.168.33.10",
    user="testuser",
    password="test123",
    database="TESTDB",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
) 

    return cnx

 

# write to db
def writedb(cursor, cnx, sql_statment, val1, val2):
    try:
        cursor.execute(sql_statment, (val1, val2))
        cnx.commit()
    except:
        cnx.rollback()
    


# fetch whole table from db
def readtable(cnx, table):
    cursor = cnx.cursor()
    sql_statement = "SELECT * FROM id=%s"
    cursor.execute(sql_statement, table)
    rows = cursor.fetchall()
    return rows



def main():
    cnx = dbconnect()
  
    #
    #  where the magic happens
    # 
    #     

    #writedb(cnx.cursor, cnx, s,url, text)
    mycursor = cnx.cursor()
    mycursor.execute("SELECT * FROM `sites`")
    wholetable =  mycursor.fetchall()
    for x in wholetable:
        print(x['id'], x['url'],x['category'])
        

    cnx.close()

if __name__ == "__main__":
    main()