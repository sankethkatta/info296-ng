import matplotlib.pyplot as plt
from pandas import Series

f = open('output.txt')
line = f.readline()
new_list = []
while line != "":
	s = line.split()
	line = f.readline()
	new_list.append(s)
print new_list

k_list = list()
size = len(new_list)
k_sum = 0
for i in range(size):
	if i == 0:
		#k_sum = float(new_list[0][1])
		continue
	k_sum = k_sum + (float(new_list[i-1][1])/float(new_list[i][0]))
	k_list.append(float(new_list[i-1][1])/float(new_list[i][0]))
k_avg = k_sum/size
#consu_ser = Series(data=k_list,index=range(len(k_list)))
consu_ser = Series(data=k_list,index=range(len(k_list)))
#print consu_ser.describe()
mean = consu_ser.mean()
std_dev = consu_ser.std()
modified_list = list()
for i in range(len(k_list)):
	if (k_list[i] < mean + std_dev) and (k_list[i] > mean - std_dev):
		modified_list.append(k_list[i])

plt.hist(modified_list)
plt.show()
consu_ser_mod = Series(data=modified_list,index=range(len(modified_list)))
k_avg = consu_ser_mod.sum()/len(modified_list)

thresh_sum = 0
for i in range(size):
	if i == 0:
		continue
	thresh_sum = thresh_sum + float(new_list[i-1][1]) - float(new_list[i][0])*k_avg
thresh_avg = thresh_sum/size

print "k_avg: ", k_avg
print "thresh_avg: ", thresh_avg




