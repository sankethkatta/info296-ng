from flask import Flask, render_template, request
import json
import datetime
from scipy import stats
import shelve
import pprint

app = Flask(__name__)

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
        sorted_product_key = sorted(purchase_ranking, key = lambda key: purchase_ranking[key]["rank"])

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
                purchase_dict['product_quantity'] = 0
                purchase_dict['time_since_last_step'] = 0
                purchase_dict['rank'] = stats.norm.cdf(float(purchase_dict['time_since_last_step']), (purchase_dict['product_quantity']*purchase_dict['product_mean']), (purchase_dict['product_quantity']*purchase_dict['product_std']))
                purchase_ranking[product] = purchase_dict
            else:
                purchase_dict = purchase_ranking[product]
                purchase_dict['time_since_last_step'] += days_since_last
                purchase_ranking[product] = purchase_dict
        # store the updated purchase_ranking back to the persistent state
        purchase_ranking.sync()

        sorted_product_key = sorted(purchase_ranking, key = lambda key: purchase_ranking[key]["rank"])
        state_data = {"mean": 0, "stdev": 0, "count": 0}

        return sorted_product_key, state_data


# HTTP Routes
@app.route('/<int:customer_lnr>')
def index(customer_lnr):
    """
    Serves the index page and displays initial recommendations.
    """
    recs, state_data = model_callback(customer_lnr)

    return render_template('index.html', rec_list=recs,
                                         state_data=json.dumps(state_data),
                                         customer_lnr=customer_lnr)

@app.route('/update', methods=['POST'])
def update():
    """
    Called via AJAX with a purchased_list, returns an updated reccomendation list.
    """

    state_data = request.json.get('state_data')
    customer_lnr = request.json.get('customer_lnr')
    purchased_list = request.json.get('purchased_list')
    days_since_last = int(request.json.get('time_step_since_last_purchase'))

    new_list, state_data = model_callback(customer_lnr, state_data, purchased_list, days_since_last=days_since_last)

    return render_template('rec_list.html', rec_list=new_list,
                                            state_data=json.dumps(state_data),
                                            customer_lnr=customer_lnr,
                                            hidden=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)