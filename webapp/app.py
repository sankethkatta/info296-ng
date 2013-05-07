from flask import Flask, render_template, request
import json, datetime
from emperical_model import get_rankings, update_rankings, init_rankings, tommy
import pdb

app = Flask(__name__)

# There will be a pre-index page that feeds CUSTOMER_LNR
# into the now index() view
CUSTOMER_LNR = 5955861

# Empirical Model
def model_callback(customer_lnr, purchased_items=None, days_since_last=0):
    """
    This function is called to generate an ordered list of recommendations.
    If purchased_items == None, there are no updates (i.e. being called on pageload)
    Otherwise, the purchased_items will contain the names of the items bought.
    """
    INITAL_DAYS = 5 # Intially there needs to be day timestep

    if purchased_items == None:
        return init_rankings(INITAL_DAYS)
    
    else:
        for group in tommy.iterkeys():
            if group in purchased_items:
                """ if product purchased we update rankings"""
                update_rankings(group, days_since_last, purchased_items[group], purchased=True)

            else:
                """else we mark purchased as False, so that only days are incremented"""
                update_rankings(group, days_since_last, 0, purchased=False)

        return get_rankings(days_since_last) 

# HTTP Routes
@app.route('/')
def index():
    """
    Serves the index page and displays initial recommendations.
    """
    recs = model_callback(CUSTOMER_LNR)

    return render_template('index.html', rec_list=recs,
                                         customer_lnr=CUSTOMER_LNR)

@app.route('/update', methods=['POST'])
def update():
    """
    Called via AJAX with a purchased_items, returns an updated reccomendation list.
    """


    purchased_items = request.json.get('purchased_items')
    days_since_last = int(request.json.get('time_step_since_last_purchase'))
    new_list = model_callback(CUSTOMER_LNR, purchased_items, days_since_last=days_since_last)


    return render_template('rec_list.html', rec_list=new_list,
                                            customer_lnr=CUSTOMER_LNR)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
