import shelve
import csv

purchase_ranking = shelve.open("purchase_ranking")
INITIAL_TIME = 0
INITIAL_PRODUCT_QUANTITY = 0
INITIAL_RANK = 0

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

for row in csv.reader(open("static/data/frequencies.csv", "r"), delimiter=" "):
    (product_key, product_number, product_mean, product_std) = row[0], row[1], row[2], row[3]
    purchase_ranking[removeNonAscii(product_key)] = {"time_since_last_step": INITIAL_TIME, "product_mean": float(product_mean), "product_std": float(product_std), "product_quantity": INITIAL_PRODUCT_QUANTITY, "rank": float(product_mean)}

purchase_ranking.sync()