import matplotlib.pylab as plt

import numpy as np

import json

from collections import Counter

import sys

order_times = np.random.poisson(35, 47)

count, bins, ignored = plt.hist(order_times, 14, normed=False)


drink_types = ['tea', 'latte', 'affogato']

order_types = np.random.choice(drink_types, 47, p = [2/float(6), 3/float(6), 1/float(6)])



plt.show()


#iterate s and samples to make into a tuple 
#once have the tuple make it into a dictionary and put it into an array
#use json dump to write the array into a distribution 

order_times.sort()

count = 0
artificialData = []
for i in range(len(order_times)):
	curr = dict([('order_id', count), ('order_time', order_times[i]), ('type', order_types[i])])
	artificialData.append(curr)
	count += 1

if (len(sys.argv) < 2):
	print('specify what input file will be called once generated')
else:
	with open('input_files/' + str(sys.argv[1] + '.json'), 'w') as outfile:
		json.dump(artificialData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))