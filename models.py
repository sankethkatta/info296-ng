"""
Main Models file for the ng_db on EC2. 
This file defines all the Tables and relationships in the database.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://postgres:info296ng@ec2-50-19-178-30.compute-1.amazonaws.com:5432/ng_db')
session = sessionmaker(bind=engine)()
Base = declarative_base()


class CustomBase(Base):
    __abstract__ = True

    def create(self):
        """
        Single-Function add+commit to create new row.
        """
        session.add(self)
        session.commit()

    def remove(self):
        """
        Single-Function delete+commit to delete row. 
        """
        session.delete(self)
        session.commit()

### DEFINE TABLES HERE ###

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 0:
        if sys.argv[1] == 'create_tables':
            Base.metadata.create_all(engine)
