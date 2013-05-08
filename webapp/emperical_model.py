import pickle, numpy, shelve
from collections import defaultdict, Counter, namedtuple

# Load necessary data files:
groups_lookup = shelve.open("groups.shelve") # lookup table for group_id to group name
pkl_file = open('data.pkl', 'rb') 
transaction_table =  pickle.load(pkl_file) #group, and an array of the quantity and the day intervals
transition_models = pickle.load(pkl_file) #mean and variance for each group
pkl_file.close()

def lookup(id): 
    """
    returns the appropriate group name for a group_id
    to create the shelve file used run:
    
    python groups_shelve.py
    """
    return groups_lookup[str(id)]

tommy = defaultdict(list) # dictionary group ==> list of t/q values
def give_probability(group, day, quantity):
    """
    returns the probability for a given product group_id and day 
    """
    mean = numpy.mean(tommy[group])
    std = numpy.std(tommy[group])
    mod_norm = []
    #chopping off the edges
    #counter: histogram
    for i in xrange(len(tommy[group])):
        if (tommy[group][i] < (mean + std)) and (tommy[group][i] > (mean - std)):
            mod_norm.append(tommy[group][i])
    #rounding the consumption rate values to the nearest integer (day counts)       
    mod_norm = map(lambda x:round(x),mod_norm)
    rounded = Counter(mod_norm)
    rounded = dict(rounded)
    sorted(rounded)
    
    #normalization
    for key,val in rounded.iteritems():
        rounded[key] = float(val)/len(mod_norm)
    distsum = 0 
    
    #summing the probabilities
    for key,val in rounded.iteritems():
        if key>(day/float(quantity + 1)):
            #print "break at: day=%s t/q=%s" % (day, (day/float(1 + quantity)))
            #print "distsum=%s" % distsum
            break   
        distsum = distsum + val
    #print "numerator: %s, denominator: %s" % (distsum, float(quantity + 1))
    return distsum

def update_rankings(group, time, quantity, purchased=False):
    """
    update a product group_id with a new consumption rate datapoint, 
    using time / quantity.
    """
    if purchased:
        """increment time, append t/q, reset time to 0 """
        groups_timestep[group] += time
        tommy[group].append(groups_timestep[group] / float(quantity))
        groups_timestep[group] = 0

    else:
        """increment time only, consumption rate does not change"""
        groups_timestep[group] += time

# namedtuple for easier access to rankings
ProductGroup = namedtuple('ProductGroup', ('prob', 'group_id', 'group_name'))
groups_timestep = defaultdict(lambda: 0) # for storing timesteps (default value 0 if key does not exist)
def init_rankings(day_timestep):
    """
    This builds the Inital list of rankings from the dataset
    returns a descending ranked list of products (namedtuple instances in the following format)
    [product(prob, group_id, group_name), ....]
    """
    global tommy
    tommy = defaultdict(list)
    rankings = []
    last_day_store = max([transaction_table[group][-1][0] for group in transaction_table])
    for group in transaction_table: 
        transaction_table[group].sort()
        normalized_date_quantities = []
        quantity = 0


        # Runs over transaction_table to create inital t/q values
        for i in range(1,len(transaction_table[group])):
            days = (transaction_table[group][i][0]-transaction_table[group][i-1][0]).days

            if days == 0:
                quantity += transaction_table[group][i-1][1]
            else:
                quantity = transaction_table[group][i-1][1]
                normalized_date_quantities.append(days/float(quantity))

        THRESHOLD = 20
        days_since_last_purchase = (last_day_store - transaction_table[group][-1][0]).days 
        if days_since_last_purchase > THRESHOLD:
            groups_timestep[group] = 0
        else:
            groups_timestep[group] = days_since_last_purchase
        tommy[group] = normalized_date_quantities
        prob = give_probability(group, groups_timestep[group], transaction_table[group][-1][1])
        rankings.append(ProductGroup(prob, group, lookup(group)))

    rankings.sort(reverse=True, key=lambda x: x.prob)
    return rankings

def get_rankings(day_timestep, quantities):
    """
    Once the inital_rankings has been built, get_rankings can be called to give new rankings
    returns a descending ranked list of products (namedtuple instances in the following format)
    [product(prob, group_id, group_name), ....]
    """
    rankings = [ProductGroup(give_probability(group, groups_timestep[group], quantities.get(group, 0)), group, lookup(group)) for group in tommy]
    rankings.sort(reverse=True)
    return rankings
