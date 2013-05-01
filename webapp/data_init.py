import shelve
import csv
from scipy import stats

purchase_ranking = shelve.open("purchase_ranking")
INITIAL_TIME = 0
INITIAL_PRODUCT_QUANTITY = 1

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

total_mean = 0
for row in csv.reader(open("static/data/frequencies.csv", "r"), delimiter=" "):
    (product_key, product_number, product_mean, product_std) = row[0], row[1], row[2], row[3]
    if product_key == "SIGARETTER":
        product_mean = 3
    total_mean += float(product_mean)
    purchase_ranking[removeNonAscii(product_key)] = {"time_since_last_step": INITIAL_TIME, "product_mean": float(product_mean), "product_std": float(product_std), "product_quantity": INITIAL_PRODUCT_QUANTITY, "rank": 0.0}

print total_mean
for key in purchase_ranking.iterkeys():
    cur_dict = purchase_ranking[key]
    cur_dict['rank'] = stats.norm.cdf(float(1), (cur_dict['product_quantity']*cur_dict['product_mean']), (cur_dict['product_quantity']*cur_dict['product_std']))
    purchase_ranking[key] = cur_dict

purchase_ranking.sync()
