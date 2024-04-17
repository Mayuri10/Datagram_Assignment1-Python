import psycopg2
import json

class DB():
    def __init__(self):
        self.db_name = 'postgres'
        self.user = 'postgres'
        self.password = 'password'
        self.host = 'localhost'

    def createconnection(self):

        self.conn = psycopg2.connect(dbname=self.db_name,user=self.user,password=self.password,host=self.host)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS ProductData"
                         " ( sequence_id serial, product_name varchar, original_price varchar,sale_price varchar, brand varchar, img_url varchar, product_url varchar"
                         ", FOREIGN KEY (product_url) REFERENCES CategoryData(product_url))")

        print("Connection Created Successfully")
        self.conn.commit()

    def insertdata(self):
        self.createconnection()
        with open('jsonfile_utf8.json', 'r',encoding="utf-8") as json_file:
            products_data = json.load(json_file)

        for product in products_data:
            self.cur.execute(
                'Insert into ProductData ( product_name , original_price ,sale_price , brand , img_url , product_url ) Values(%s,%s,%s,%s,%s,%s)', (
               product['name'],product['original_price'],product['sale_price'],product['brand'],product['img_url'],product['product_url']))

            print("Data Inserted for: ", product['product_url'])

            self.conn.commit()

if __name__ == '__main__':
    obj = DB()
    obj.insertdata()