# Datagram Python project using request library and beautiful soup
Data-gram Technical round projects:

Web Crawling and Product Extraction
- Target URL: https://www.pascalcoste-shopping.com/esthetique/fond-de-teint.html


Python packages use: 
import random
import time,psycopg2
import requests,json
from bs4 import BeautifulSoup

Database use: PostgreSql:
#---------------- For running code please change you own credential in script for database connection----------------------------
self.db_name = 'postgres'
self.user = 'postgres'
self.password = 'password'
self.host = 'localhost'

Run file in any python IDE or cmd where python is available.

First Script: Assignmen1.py:
- I this script I visited the multiple pages available for the given URL category
- Scrape all the product URLs (~110)
- Created relational database to store category and product url
- Hit all the URL's
- Parse the data in require format
- Save the file in JSON readable format

After running Assignmen1.py. You will get an output of: jsonfile_utf8.json

Second Script:- DB_Operations.py
- Created a relational databse which is mentioned in Assinmen1.py
- Read json file
- store the data in postgressql

Both the script are indivisual to run but sequence is important as we have to pass output JSON file from Asignmen1.py to DB_Operations.py
