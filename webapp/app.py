from flask import Flask, render_template, request
import json
import datetime
import numpy


app = Flask(__name__)

# Reccomendation Model
def model_callback(customer_lnr, prev_rec_list=None, purchased_list=None):
    """
    This function is called to generate an ordered list of recommendations.
    If purchased_list == None, there are no updates (i.e. being called on pageload)
    Otherwise, the purchased_list will contain the names of the items bought.
    """
    if purchased_list == None:
        # After loading with the default frequency, construct the list based on sorting each item's frequency.
        return [("Milk", 0), ("Cheese", 0), ("Bread", 0), ("Eggs", 0)]
    else:
        # TODO: if purchase_list is not None, then we take the prev_rec_list and update the previous frequency
        return [("Milk", 0), ("Cheese", 0), ("Bread", 0), ("Eggs", 0)]



# HTTP Routes
@app.route('/<int:customer_lnr>')
def index(customer_lnr):
    """
    Serves the index page and displays initial recommendations.
    """
    recs = model_callback(customer_lnr)
    
    return render_template('index.html', rec_list=recs,
                                         customer_lnr=customer_lnr)

@app.route('/update', methods=['POST'])
def update():
    """
    Called via AJAX with a purchased_list, returns an updated reccomendation list.
    """
    
    prev_rec_list = request.json.get('prev_rec_list')
    customer_lnr = request.json.get('customer_lnr')
    purchased_list = request.json.get('purchased_list')
    time_step = request.json.get('time_step_since_last_purchase')
    
    new_list = model_callback(customer_lnr, prev_rec_list, purchased_list)
    
    return render_template('rec_list.html', rec_list=new_list,
                                            customer_lnr=customer_lnr,
                                            hidden=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)