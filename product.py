from click import echo
from requests import Session, session
from sqlalchemy import create_engine,Column,Integer,String,Date, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db',echo=False)
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True)
    product_name = Column('Product Name',String)
    product_price = Column('Product Price',Integer)
    product_quantity = Column('Product Quantity',Integer)
    date_updated = Column('Date updated',Date)