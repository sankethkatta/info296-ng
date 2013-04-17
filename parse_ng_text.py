import datetime
import numpy


groups = open('groups.csv','r')
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

transactions = open('hsl_ba003t_uttrekk_mw201303111.txt','r')
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
