import matplotlib.pylab as plt

import numpy as np

import json

from collections import Counter

order_times = np.random.poisson(50, 47)

count, bins, ignored = plt.hist(order_times, 14, normed=False)


drink_types = ['tea', 'latte', 'affogato']

order_types = np.random.choice(drink_types, 47, p = [1/float(3), 1/float(3), 1/float(3)])


#print(Counter(samples).values())
print('len(s): ', len(order_times), 'len(order_types): ', len(order_types))
plt.show()


#iterate s and samples to make into a tuple 
#once have the tuple make it into a dictionary and put it into an array
#use json dump to write the array into a distribution 

order_times.sort()
print('sorted: ', order_times)

count = 0
artificialData = []
for i in range(len(order_times)):
	curr = dict([('order_id', count), ('order_time', order_times[i]), ('type', order_types[i])])
	print(curr)
	artificialData.append(curr)
	count += 1

with open('poisson_mean_50_47_samples_equal_prob_types_of_drinks.json', 'w') as outfile:
	json.dump(artificialData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))