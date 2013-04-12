from flask import Flask, render_template, request
import json
app = Flask(__name__)

@app.route('/')
def index():
    customer_lnr = 1234
    recs = model_callback(customer_lnr)
    return render_template('index.html', rec_list=recs,
                                         customer_lnr=customer_lnr)

@app.route('/update', methods=['POST'])
def update():
    print request.json
    customer_lnr = request.json.get('customer_lnr')
    purchased_list = request.json.get('purchased_list')
    new_list = model_callback(customer_lnr, purchased_list)
    return render_template('rec_list.html', rec_list=new_list,
                                            customer_lnr=customer_lnr,
                                            hidden=True)

def model_callback(customer_lnr, purchased_list=None):
    return ["hello", "bye", "hi"]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)