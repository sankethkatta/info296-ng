f = open('hsl_ba003t_uttrekk_mw201303111.txt','r')
line = f.readline()
count = 1
counts = {}
data = []
dates1 = set()
dates2 = []

while line != "":  	
	line = f.readline()
	comps = line.split()
	#print line
	try:
		#if comps[6] == '5955861' and comps[1] != '57230':
		#	print line
			
		if comps[6] == '5955861' and comps[1] == '15706': #LETTMELK 1L Q, 57394 OST MATLAGINGSOST, yogurt,grapes,detergent,pepsi
			print line
			dates2.append((long(comps[2]),float(comps[7])))
		
		if comps[6] == '5955861':
			dates1.add(long(comps[2]))
			#data.append((long(comps[2]),line))

		if count % 1000000 == 0:
			print count, len(dates1), len(dates2)
		
	except IndexError:
		break
	
	count = count + 1

import scipy.io
dates1 = list(dates1)
dates3 = [0.0]*len(dates1)
for i in dates2:
	dates3[dates1.index(i[0])] = i[1]

scipy.io.savemat('out2.mat', mdict={'visits2':dates3})
	
"""
	if counts.has_key(comps[6]):
		counts[comps[6]] = counts[comps[6]] + 1
	else:
		counts[comps[6]] = 1
	
	if count % 1000000 == 0:
		print count
	count = count + 1

counts_list = []
for i in counts:
	counts_list.append((counts[i],i))

counts_list.sort(reverse=True)

hist = [ c[0] for c in counts_list]
names = [ c[1] for c in counts_list]

import scipy.io
print counts_list[:10]
print counts_list[len(counts_list)/4]

scipy.io.savemat('out.mat', mdict={'products':hist,'names':names})
"""
