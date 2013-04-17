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
      
      groups = open('static/data/groups.csv','r')
      inverted_index = {}
      name_lookup = {}
      
      USER = '5955861'
      CONFIDENCE_THRESH = 5

      gline = groups.readline()
      gline = groups.readline()

      while gline != "":
        comps = gline.split(';')
      	inverted_index[comps[0]] = comps[1]
      	name_lookup[comps[1]] = comps[2].strip().strip('"')
      	gline = groups.readline()

      transactions = open('static/data/hsl_ba003t_uttrekk_mw201303111.txt','r')
      tline = transactions.readline()
      tline = transactions.readline()

      transaction_table = {}
      count = 1
      while tline != "":
      	comps = tline.split() 
      	if comps[6] == USER and inverted_index.has_key(comps[1]):
      		transaction_tuple = (datetime.datetime.strptime(comps[3],"%m/%d/%Y"),float(comps[7]),name_lookup[inverted_index[comps[1]]])
      		group = inverted_index[comps[1]]
      		if not transaction_table.has_key(group):
      			transaction_table[group] = []
      		transaction_table[group].append(transaction_tuple)

      	if count % 1000000 == 0:
      		print str((count/92000000.0)*100)+"% Complete"

      	count = count + 1
      	tline = transactions.readline()

      transition_models = []
      for group in transaction_table:
      	transaction_table[group].sort()
      	normalized_date_quantities = []
      	tally = 0
      	for i in range(1,len(transaction_table[group])):
      		if (transaction_table[group][i][0]-transaction_table[group][i-1][0]).days == 0:
      			tally = tally + transaction_table[group][i-1][1]
      		else:
      			tally = transaction_table[group][i-1][1]
      			normalized_date_quantities.append((transaction_table[group][i][0]-transaction_table[group][i-1][0]).days/tally)
      	if len(normalized_date_quantities) > CONFIDENCE_THRESH:
      		mean = numpy.mean(normalized_date_quantities)
      		std = numpy.std(normalized_date_quantities)
      		outliers = []
      		for i in range(0,len(normalized_date_quantities)):
      			if abs(normalized_date_quantities[i] - mean) > 2*std:
      				outliers.append(i)
      		normalized_date_quantities = [i for j, i in enumerate(normalized_date_quantities) if j not in outliers]
      		transition_models.append((numpy.std(normalized_date_quantities),numpy.mean(normalized_date_quantities),group,transaction_table[group][0][2]))
      transition_models.sort()
      
      for t in transition_models:
      	print t[3],t[2],t[1],t[0]
      
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
    
    new_list = model_callback(customer_lnr, prev_rec_list, purchased_list)
    
    return render_template('rec_list.html', rec_list=new_list,
                                            customer_lnr=customer_lnr,
                                            hidden=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)