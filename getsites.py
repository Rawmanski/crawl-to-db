#! /usr/bin/env python3
"""
Script for simple data writing and reading to/from MySQL.

"""
import pymysql
from pymysql import cursors

import extract_topic

from bs4 import BeautifulSoup
from urllib.request import urlopen

INPUT_FILE = ''
URL_LIST = []

def req2text(url):
    """ Returns parsed text from a given url

    Parameters
    ----------
    url : str
        url to parse
        
    Return
    ------
    text : str    
    """
    res = urlopen(url).read()
    soup = BeautifulSoup(res, 'html.parser')
    for script in soup(["script", "style"]):
        script.decompose()
    liste = list(soup.stripped_strings)
    space = ' '
    text = space.join(liste)
    return text


def dbconnect():
    """ Returns db connection
    Configure for your needs with db credentials
            
    Return
    ------
    cnx : Connection object    
    """
    cnx = pymysql.connect(
    host="",
    user="",
    password="",
    database="",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
) 
    return cnx

 
def writedb(cursor, cnx, sql_statment, val1, val2, val3):
    """ Write to DB 

    Parameters
    ----------
    cursor : Cursor Object 
        (pymysql.cursors.Cursor())
    cnx    : Connection Object 
        database connection (pymysql.connection.Connction())
    sql_statement: str
        SQL Expression to execute
    url    : str
        Given url which is parsed
    text    : str
        parsed text
    category    : str
        processed category 
   
    """
    try:
        cursor.execute(sql_statment, (val1, val2, val3))
        cnx.commit()
    except:
        cnx.rollback()
    



def readtable(cnx, table):
    """ Returns fetched rows from DB

    Parameters
    ----------
    cnx    : Connection Object 
        database connection (pymysql.connection.Connction())
    table: str
        which table to    
        
    Return
    ------
    rows : list 
        all rows from selected table    
    """
    cursor = cnx.cursor()
    sql_statement = "SELECT * FROM id=%s"
    cursor.execute(sql_statement, table)
    rows = cursor.fetchall()
    return rows



def main(url):
    
    text = req2text(url)
    category = extract_topic.main(text)
    # db open
    cnx = dbconnect()
    cursor = cnx.cursor()
    sql="INSERT INTO `sites` (`url`, `text`, `category`) VALUES (%s, %s, %s)"
    writedb(cursor, cnx, sql, url, text, category)

    cnx.close()

if __name__ == "__main__":
    main(URL)