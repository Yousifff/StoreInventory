import sqlalchemy
from product import engine,session,Base,Product
import csv
import time
import datetime


def menu():
    print('''
          \n***** Store Inventory *****
          \ra) Add an inventory 
          \rv) List inventory
          \rb) Database backup
          \re) Exit
          ''')
    
    choise = input("What would you like ? ")
    if choise not in ['a', 'b', 'v','e']:
        input("Please Enter a valid option : ")
    else:
        return choise


def clean_date(date_str):
    date = date_str.split("/")
    if len(date) < 3:
        raise ValueError("Date Format must by Month/Day/Year")
    else:
        month = int(date_str.split('/')[0])
        day = int(date_str.split('/')[1])
        year = int(date_str.split('/')[2])
        return datetime.date(year,month,day)
    

def clean_price(price_str):
    price = None
   
    try:
        if "$" in price_str:
            price = float(price_str.split("$")[1])
        else:
            price = float(price_str)
       
        #print(price)
    except ValueError:
        input('''
              \n*****Price ERROR *****
              \rThe price should be a number without a currency number
              \rEx: 10.99
              \rPress enter to try again.
              \r************************
              ''')
        return
    else:
        return int(price * 100) 

def load_csv():
    
    with open('inventory.csv','r') as csvfile:
        data = csv.DictReader(csvfile)
        for line in data:
            item = session.query(Product).filter(Product.product_name == line['product_name']).one_or_none()
            if item == None:
                productName = line['product_name']
                productPrice = clean_price(line['product_price'])
                productQuantity = int(line['product_quantity'])
                try:
                    productDateUpdated = clean_date(line['date_updated'])
                except ValueError as err:
                    print(err)
                product = Product(product_name=productName,product_price=productPrice,product_quantity=productQuantity,date_updated=productDateUpdated)
                session.add(product)
        session.commit()




def database_backup():
    with open('backup.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name', 'Product Price', 'Product Quantity','Date updated'])
        for inventory in session.query(Product):
            writer.writerow([inventory.id,inventory.product_name,inventory.product_price,inventory.product_quantity,inventory.date_updated])

def add_product():
    Product_Name = input("Enter a product name : ")
    quantity_error = True
    
    while quantity_error:
        try:
            Product_Quantity = int(input("Enter a product quantity : "))
            quantity_error = False
        except ValueError:
            print("Product Quantity must be an integer number!!!\n")
    
    price_error = True
    while price_error:
        Product_Price = input("Enter a product price : ")
        Product_Price = clean_price(Product_Price)
        if type(Product_Price) == int:
            price_error = False
       
        
    date_error = True
    while date_error:
        Product_Date = input("Enter a date, Month/Day/Year : ")
        try:
            Product_Date = clean_date(Product_Date)
        except ValueError as err:
            print(err)
        if type(Product_Date) == datetime.date:
            date_error = False
    
    new_product = Product(product_name=Product_Name,product_price=Product_Price,product_quantity=Product_Quantity,date_updated=Product_Date)
    session.add(new_product)
    
    session.commit()
            
def product_view():
    product_id_list = []
    prod_id = ''
    product_info = None
    found = False
    for product_id in session.query(Product):
        product_id_list.append(product_id.id)
  
    try:
        prod_id = int(input("Enter a product ID : "))
    except ValueError:
        print("ID entered must be a number ")
    else:
        if prod_id in product_id_list:
            product_info = session.query(Product).filter(Product.id==prod_id).one_or_none()
            print(f'''
            \nProduct Name: {product_info.product_name}
            \rPrice: ${product_info.product_price / 100}
            \rQuantity: {product_info.product_quantity}
            \rDate: {product_info.date_updated}
            ''')
        else:
            print("The entered ID is not in database!")    
   
        
   
    
        

def run_app():
    load_csv()
    while True:
        
        choise = menu()
        
        if choise == 'a':
            add_product()
        elif choise == 'v':
            product_view()
        elif choise == 'b':
            database_backup()
        elif choise == 'e':
            break

if __name__ == '__main__':
    Base.metadata.create_all(engine) 
    #load_csv()
    run_app()