import csv
import shelve

g_csv = csv.reader(open("groups.csv", 'rb'), delimiter=';', quotechar='"')
g_shelve = shelve.open("groups.shelve")

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

g_csv.next()
for row in g_csv:
    product_lnr, subgroup_nr, subgroup_name = row
    g_shelve[subgroup_nr] = removeNonAscii(subgroup_name.rstrip())

g_shelve.sync()
g_shelve.close()
