from flask import Flask, render_template, request
import json
app = Flask(__name__)

def model_callback(customer_lnr, purchased_list=None):
    """
    This function is called to generate an ordered list of recommendations.
    If purchased_list == None, there are no updates (i.e. being called on pageload)
    Otherwise, the purchased_list will contain the names of the items bought.
    """
    return ["hello", "bye", "hi"]


# HTTP ROUTES
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
    customer_lnr = request.json.get('customer_lnr')
    purchased_list = request.json.get('purchased_list')
    new_list = model_callback(customer_lnr, purchased_list)
    return render_template('rec_list.html', rec_list=new_list,
                                            customer_lnr=customer_lnr,
                                            hidden=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)