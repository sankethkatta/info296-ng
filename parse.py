"""
This file parses the raw data and inserts into the ng_db using the models
defined in models.py
"""

import models, csv, os, sys

customer_reader = csv.reader(open(os.path.join('data', 'BA007_Kunde.txt'), 'rb'), delimiter='\t')
product_reader = csv.reader(open(os.path.join('data', 'BA008_Vare.txt'), 'rb'), delimiter='\t')
store_reader = csv.reader(open(os.path.join('data', 'WF002_Butikk.txt'), 'rb'), delimiter='\t')

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

product_reader.next() # Skip the header row
count = 0
for row in product_reader:
    count += 1
    sys.stdout.write('Product: %s\r' % count)
    sys.stdout.flush()

    models.Product(product_lnr = int(row[0]),
                   product_ean_nr = float(row[1]),
                   product_name = row[2],
                   main_group_nr = int(row[3]),
                   main_group_name = row[4],
                   subgroup_nr = int(row[5]),
                   subgroup_name = row[6],
                   shopping_list_nr = int(row[7])).create(commit=False)

    # Only commit every n objects to speed up insertion
    if count % 200 == 0: models.session.commit()

# Extra commit for ones that got missed in the mod
models.session.commit()

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