import json
import matplotlib.pyplot as plt
import sys

if (len(sys.argv) < 2):
	print('type: python validate_distribution.py file_name')
	print('where file_name is the name of the input file to visualize the distribution')
else:
	with open(sys.argv[1] + '.json') as data_file:
		data = json.load(data_file)
	orders_map = {}
	for i in range(len(data)):
		curr = data[i]
		if (curr['order_time'] not in orders_map):
			orders_map[curr['order_time']] = 1
		else:
			orders_map[curr['order_time']] += 1
	
	

	plt.bar(orders_map.keys(), orders_map.values())
	plt.show()