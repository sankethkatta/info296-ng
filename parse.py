"""
This file parses the raw data and inserts into the ng_db using the models
defined in models.py
"""

import models, csv, os, sys
from datetime import datetime

def insert_customer():
    customer_reader = csv.reader(open(os.path.join('data', 'BA007_Kunde.txt'), 'rb'), delimiter='\t')
    customer_reader.next() # Skip the header row
    count = 0
    for row in customer_reader:
        count += 1
        sys.stdout.write('Customer: %s\r' % count)
        sys.stdout.flush()

        models.Customer(customer_lnr = int(row[0]),
                        household_id = int(row[1]),
                        member_id = int(row[2]),
                        born_year = int(row[3]) if row[3] else None,
                        gender = row[4]).create(commit=False)

        # Only commit every n objects to speed up insertion
        if count % 200 == 0: models.session.commit()

    # Extra commit for ones that got missed in the mod
    models.session.commit()

def insert_product():
    product_reader = csv.reader(open(os.path.join('data', 'BA008_Vare.txt'), 'rb'), delimiter='\t')
    product_reader.next() # Skip the header row
    count = 0
    for row in product_reader:
        count += 1
        sys.stdout.write('Product: %s\r' % count)
        sys.stdout.flush()

        # cp865 is the Norwegian language encoding
        models.Product(product_lnr = int(row[0]),
                       product_ean_nr = float(row[1]),
                       product_name = row[2].decode('cp865'),
                       main_group_nr = int(row[3]),
                       main_group_name = row[4].decode('cp865'),
                       subgroup_nr = int(row[5]),
                       subgroup_name = row[6].decode('cp865'),
                       shopping_list_nr = int(row[7])).create(commit=False)

        # Only commit every n objects to speed up insertion
        if count % 200 == 0: models.session.commit()

    # Extra commit for ones that got missed in the mod
    models.session.commit()

def insert_store():
    store_reader = csv.reader(open(os.path.join('data', 'WF002_Butikk.txt'), 'rb'), delimiter='\t')
    store_reader.next() # Skip the header row
    count = 0
    for row in store_reader:
        count += 1
        sys.stdout.write('Store: %s\r' % count)
        sys.stdout.flush()

        models.Store(store_lnr = int(row[0]),
                     brand_chain_nr = int(row[1]),
                     brand_chain_name = row[2],
                     corporation_id = int(row[3])).create(commit=False)

        # Only commit every n objects to speed up insertion
        if count % 200 == 0: models.session.commit()

    # Extra commit for ones that got missed in the mod
    models.session.commit()

def insert_transaction():
    transaction_reader = csv.reader(open(os.path.join('data', 'hsl_ba003t_uttrekk_mw201303111.txt'), 'rb'), delimiter='\t')
    transaction_reader.next() # Skip the header row
    count = 0
    for row in transaction_reader:
        count += 1
        sys.stdout.write('Transaction: %s\r' % count)
        sys.stdout.flush()

        models.Transaction(recipt_lnr = int(row[0]),
                           product_lnr = int(row[1]),
                           time_lnr = int(row[2]),
                           sales_datetime = datetime.strptime(row[3], '%m/%d/%Y %H:%M:%S'),
                           store_lnr = int(row[4]),
                           customer_lnr = int(row[5]),
                           product_quantity_weight = float(row[6]),
                           gross_sales = float(row[7])).create(commit=False)

        # Only commit every n objects to speed up insertion
        if count % 200 == 0: models.session.commit()

    # Extra commit for ones that got missed in the mod
    models.session.commit()

if __name__ == '__main__':
    # insert_customer()
    # insert_product()
    # insert_store()
    insert_transaction()
