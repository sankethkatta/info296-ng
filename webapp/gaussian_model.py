"""
model_callback for the Gaussian Model
"""

from scipy import stats
import shelve

purchase_ranking = shelve.open("purchase_ranking")
# Reccomendation Model
def model_callback(customer_lnr, state_data=None, purchased_list=None, days_since_last=0):
    """
    This function is called to generate an ordered list of recommendations.
    If purchased_list == None, there are no updates (i.e. being called on pageload)
    Otherwise, the purchased_list will contain the names of the items bought.
    """
    if purchased_list == None:

        # initially sort the purchase_ranking dictionary by key
        sorted_product_key = sorted(purchase_ranking, key = lambda key: purchase_ranking[key]["rank"], reverse=True)

        state_data = {"mean": 0, "stdev": 0, "count": 0}

        return sorted_product_key, state_data


    else:
        # state_data['mean'] += state_data['mean'] / float(state_data['count'])
        # state_data['count'] += 1
        # stats.norm.cdf(x, state_data.get['mean'], state_data.get['stdev'])

        # on update, the value of each product is the frequency/probability, sort the list by value
        for product in purchase_ranking.iterkeys():
            if product in purchased_list:
                purchase_dict = purchase_ranking[product]
                purchase_dict['product_quantity'] = 1
                purchase_dict['time_since_last_step'] += days_since_last
                purchase_dict['rank'] = stats.norm.cdf(float(purchase_dict['time_since_last_step']), (purchase_dict['product_quantity']*purchase_dict['product_mean']), (purchase_dict['product_quantity']*purchase_dict['product_std']))
                purchase_dict['time_since_last_step'] = 0
                purchase_ranking[product] = purchase_dict
            else:
                purchase_dict = purchase_ranking[product]
                purchase_dict['time_since_last_step'] += days_since_last
                purchase_dict['rank'] = stats.norm.cdf(float(purchase_dict['time_since_last_step']), (purchase_dict['product_quantity']*purchase_dict['product_mean']), (purchase_dict['product_quantity']*purchase_dict['product_std']))
                purchase_ranking[product] = purchase_dict
        # store the updated purchase_ranking back to the persistent state
            print product, purchase_ranking[product]['rank']
        purchase_ranking.sync()

        sorted_product_key = sorted(purchase_ranking, key = lambda key: purchase_ranking[key]["rank"], reverse=True)
        state_data = {"mean": 0, "stdev": 0, "count": 0}

        return sorted_product_key, state_data
