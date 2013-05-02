from flask import Flask, render_template, request
import json, datetime
from scipy import stats
from emperical_model import get_rankings, update_rankings, init_rankings, tommy

app = Flask(__name__)
CUSTOMER_LNR = 5955861

# Empirical Model
def model_callback(customer_lnr, purchased_list=None, days_since_last=0):
    """
    This function is called to generate an ordered list of recommendations.
    If purchased_list == None, there are no updates (i.e. being called on pageload)
    Otherwise, the purchased_list will contain the names of the items bought.
    """
    INITAL_DAYS = 5 # Intially there needs to be day timestep

    if purchased_list == None:
        return init_rankings(INITAL_DAYS)
    
    else:
        for group in tommmy:
            if group in purchased_list:
                """ if product purchased we update rankings"""
                update_rankings(group['group_id'], days_since_last, group['quantity'], purchased=True)

            else:
                """else we mark purchased as False, so that only days are incremented"""
                update_rankings(group['group_id'], days_since_last, 0, purchased=False)

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
    Called via AJAX with a purchased_list, returns an updated reccomendation list.
    """

    customer_lnr = request.json.get('customer_lnr')
    purchased_list = request.json.get('purchased_list')
    days_since_last = int(request.json.get('time_step_since_last_purchase'))

    new_list = model_callback(customer_lnr, purchased_list, days_since_last=days_since_last)

    return render_template('rec_list.html', rec_list=new_list,
                                            customer_lnr=customer_lnr,
                                            hidden=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
