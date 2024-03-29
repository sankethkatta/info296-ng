import pickle
import pprint
# from pandas import Series
# import matplotlib.pyplot as plt
import numpy
from collections import defaultdict, Counter
import shelve

groups_lookup = shelve.open("groups.shelve")

def lookup(id): 
    """
    Returns the appropriate group name for a group_id
    To create the shelve file used run:
    
    python groups_shelve.py
    """
    return groups_lookup[str(id)]

tommy = defaultdict(list) #group ==> array of t/q

def give_probability(group, day):
    """
    Returns the probability for a given product group and day
    """
    #print "length of t/q for cigarrettes: ", len(normalized_date_quantities)
    mean = numpy.mean(tommy[group])
    std = numpy.std(tommy[group])
    #print "mean: ", mean, " std: ", std
    mod_norm = []
    #chopping off the edges
    #Counter: histogram
    for i in xrange(len(tommy[group])):
        if (tommy[group][i] < mean + std) and (tommy[group][i] > mean - std):
            mod_norm.append(tommy[group][i])
    #rounding the consumption rate values to the nearest integer (day counts)       
    mod_norm = map(lambda x:round(x),mod_norm)
    rounded = Counter(mod_norm)
    rounded = dict(rounded)
    #rounded = sorted(rounded, key = lambda key:rounded[key])
    sorted(rounded)
    #print rounded
    
    #normalization
    for key,val in rounded.iteritems():
        rounded[key] = float(val)/len(mod_norm)
    distsum = 0 
    
    #summing the probabilities
    for key,val in rounded.iteritems():
        if key>day:
            break   
        distsum = distsum + val
    #print rounded, "distsum: ", distsum
    return distsum
        
    #prob_dist = map(lambda x:float(x)/len(mod_norm), rounded.values())
    
    #print prob_dist


pkl_file = open('data.pkl', 'rb')
transaction_table =  pickle.load(pkl_file) #group, and an array of the quantity and the day intervals
transition_models = pickle.load(pkl_file) #mean and variance for each group
pkl_file.close()

def update_rankings(group, consumption):
    """
    Update a product group with a new consumption rate datapoint
    """
    tommy[group].append(consumption)

def get_rankings():
    """
    Returns a ranked list of products
    """
    rankings = []
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
        tommy[group] = normalized_date_quantities
        prob = give_probability(group, 5)
        rankings.append((prob, lookup(group)))

    rankings.sort(reverse=True)
    return rankings

    # var = Series(data = mod_norm, index = xrange(len(mod_norm)))
    # var_orig = Series(data = normalized_date_quantities, index = xrange(len(normalized_date_quantities)))
    # print "length of the mod norm", len(mod_norm)

    # #print var_orig
    # plt.hist(var)
    # #plt.hist(var_orig)
    # plt.show()


#pp = pprint.PrettyPrinter()
#pp.pprint(transaction_table)
#print 
