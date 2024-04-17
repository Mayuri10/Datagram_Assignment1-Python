import random
import time,psycopg2
import requests,json
from bs4 import BeautifulSoup

class Crawler():
    def __init__(self):
        self.db_name = 'postgres'
        self.user = 'postgres'
        self.password = 'password'
        self.host = 'localhost'
        self.links = []
        self.list_of_dict = []
        self.headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

    def createconnection(self):

        self.conn = psycopg2.connect(dbname=self.db_name,user=self.user,password=self.password,host=self.host)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS CategoryData"
                         " ( sequence_id serial, category_url varchar, product_url varchar PRIMARY KEY);")

        print("Connection Created Successfully")
        self.conn.commit()

    def pushdata(self,datalist):

        self.cur.execute('Insert into CategoryData ( category_url,product_url) Values(%s,%s)',(datalist[0],datalist[1],))

        print("Data Inserted for: ",datalist[1])

        self.conn.commit()

    def removejunck(self,string):
        return str(string).replace("\\n",'').replace('\\t','').replace('\\r','').replace("\n",'').replace('\t','').replace('\r','').strip()
    def parse(self,resp):
        soup = BeautifulSoup(resp.text,'html.parser')

        #------------Name------------------------
        name = ''
        temp = soup.find('h1',class_="uk-title product-title")
        if temp:
            name = temp.text

        #---------OriginalPrice---------------------
        orip = ''
        temp = soup.find('span',class_="old-price")
        if temp:
            temp2 = temp.find('span',class_="price")
            if temp2:
                orip = temp2.text


        #-----------Saleprice---------------
        sprice = ''
        temp = soup.find('span', class_="special-price")
        if temp:
            temp2 = temp.find('span', class_="price")
            if temp2:
                sprice = temp2.text

        if not sprice:
            try:
                sprice = soup.find('div',class_="product-info-price").find('span',class_="price").text
            except:
                pass

        #-----------Round 2 decemal-----------
        orip = orip.replace('€','').replace(",",".")
        if orip:
            orip = round(float(orip),2)
            orip = str(orip).replace(".",',').strip()

        sprice = sprice.replace('€', '').replace(",", ".")
        if sprice:
            sprice = round(float(sprice), 2)
            sprice = str(sprice).replace(".", ',').strip()



        #-----------------Brand------------------
        brand = ''
        temp = soup.find('h2',class_="uk-manufacturer")
        if temp:
            brand  = temp.text

        #-----------ImageURL--------------------------
        imgurl = ''
        temp = soup.find('img',alt="main product photo")
        if temp:
            imgurl = temp['data-amsrc']

        dict = {
            'name' : self.removejunck(name),
            'original_price' : self.removejunck(orip),
            'sale_price' : self.removejunck(sprice),
            'brand':self.removejunck(brand),
            'img_url':self.removejunck(imgurl),
            'product_url':self.removejunck(resp.url)

        }
        print(dict)
        self.list_of_dict.append(dict)


    def downloadurls(self):
        for each in self.links:
            time.sleep(random.randint(1,4))
            print('Hitting URL: ',each)
            resp = requests.get(each,headers=self.headers)
            print(resp)
            if resp.status_code == 200:
                self.parse(resp)

        with open('jsonfile_utf8.json', "w", encoding="utf-8") as json_file:
            json.dump(self.list_of_dict, json_file, indent=4, ensure_ascii=False)

    def category_crawl(self,url):
        self.createconnection()

        resp = requests.get(url,headers=self.headers)
        print(resp)

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text,'html.parser')

            urls = [x['href'] for x  in soup.find_all('a',class_="uk-position-cover uk-cover-link-product")]
            self.links.extend(urls)
            for e  in urls:
                self.pushdata([url,e])


            total_num_prod  = soup.find('span',class_="uk-total-products-amount")
            if total_num_prod:
                total_num_prod = int(total_num_prod.text)
            product_per_page = soup.find('span',class_="uk-current-products-amount")
            if product_per_page:
                product_per_page = int(product_per_page.text)

            numpages = int(total_num_prod/product_per_page) + 1
            print("Number of pages: ",numpages)
            for i in range(2,numpages+1):
                time.sleep(random.randint(1,3))
                print("Paginating page: ",i)
                resp = requests.get(url + "?p={}".format(i),headers=self.headers)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')

                    urls = [x['href'] for x in soup.find_all('a', class_="uk-position-cover uk-cover-link-product")]
                    self.links.extend(urls)
                    for e in urls:
                        self.pushdata([url + "?p={}".format(i), e])
                    print('Total URL found: ',len(urls))
                    print(urls)
                    print("\n--------------------------------------------------\n")
                    
            self.links = list(set(self.links))


            self.downloadurls()

if __name__ == '__main__':
    url = 'https://www.pascalcoste-shopping.com/esthetique/fond-de-teint.html'
    obj = Crawler()
    obj.category_crawl(url)