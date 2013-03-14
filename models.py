"""
Main Models file for the ng_db on EC2.
This file defines all the Tables and relationships in the database.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://postgres:info296ng@ec2-50-19-178-30.compute-1.amazonaws.com:5432/ng_db')
session = sessionmaker(bind=engine)()
Base = declarative_base()


class CustomBase(Base):
    __abstract__ = True

    def create(self, commit=True):
        """
        Single-Function add+commit to create new row.
        Pass, commit=False, to defer the commit.
        """
        session.add(self)
        if commit: session.commit()

    def remove(self, commit=True):
        """
        Single-Function delete+commit to delete row.
        Pass, commit=False, to defer the commit.
        """
        session.delete(self)
        if commit: session.commit()

class Customer(CustomBase):
    __tablename__ = 'customer'

    customer_lnr = Column(Integer, primary_key=True)
    household_id = Column(Integer)
    member_id = Column(Integer)
    born_year = Column(Integer)
    gender = Column(String)

class Product(CustomBase):
    __tablename__ = 'product'

    product_lnr = Column(Integer, primary_key=True)
    product_ean_nr = Column(BigInteger)
    product_name = Column(String)
    main_group_nr = Column(Integer)
    main_group_name = Column(String)
    subgroup_nr = Column(Integer)
    subgroup_name = Column(String)
    shopping_list_nr = Column(Integer)

class Store(CustomBase):
    __tablename__ = 'store'

    store_lnr = Column(Integer, primary_key=True)
    brand_chain_nr = Column(Integer)
    brand_chain_name = Column(String)
    corporation_id = Column(Integer)

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == 'create_tables':
            Base.metadata.create_all(engine)
