import json
import unittest
from fifo import simulateCafeDay
from optimized import optimize


#set test To False if want to display the metrics
#else the metrics will not display: line 94 onwards are the metrics
def metricCalc(metric_file_name, input_file_name, test=True):
	tea_count = 0
	latte_count = 0
	affogato_count = 0
	tea_wait_time = 0
	latte_wait_time = 0
	affogato_wait_time = 0

	tea_avg_wait = 0
	latte_avg_wait = 0
	affogato_avg_wait = 0

	with open(metric_file_name + '.json') as data_file:
		data = json.load(data_file)

	for i in range(len(data)):
		curr = data[i]
		if (curr['type'] == 'tea'):
			tea_count += 1
			tea_wait_time += (curr['start_time'] - curr['order_time'] + 3)
		elif (curr['type'] == 'latte'):
			latte_count += 1
			latte_wait_time += (curr['start_time'] - curr['order_time'] + 4)
		else:
			affogato_count += 1
			affogato_wait_time += (curr['start_time'] - curr['order_time'] + 7)

	#make sure no divide by zero in average wait time. also calculate the average wait 
	#times for each type of drink 

	if (tea_wait_time != 0):
		tea_avg_wait = float(tea_wait_time) / tea_count
	else:
		tea_avg_wait = 0
	if (latte_wait_time != 0):
		latte_avg_wait = float(latte_wait_time) / latte_count
	else:
		latte_avg_wait = 0
	if (affogato_wait_time != 0): 
		affogato_avg_wait = float(affogato_wait_time) / affogato_count
	else:
		affogato_avg_wait = 0

	with open(input_file_name + '.json') as data_file:
		data = json.load(data_file)
	
	tea_total = 0
	latte_total = 0
	affogato_total = 0
	orders_map = {}
	for i in range(len(data)):
		if (data[i]['type'] == 'tea'):
			tea_total += 1
		elif(data[i]['type'] == 'latte'):
			latte_total += 1
		else:
			affogato_total += 1

		curr = data[i]
		if (curr['order_time'] not in orders_map):
			orders_map[curr['order_time']] = 1
		else:
			orders_map[curr['order_time']] += 1
	
	

	#plt.bar(orders_map.keys(), orders_map.values())
	#plt.show()

	tea_percent_comp = 0
	latte_percent_comp = 0
	affogato_percent_comp = 0
	
	
	#calculate the average percentage of orders completed fore ach
	#type of drink. also make sure not to divide by zero 
	if (tea_total != 0):
		tea_percent_comp = tea_count / float(tea_total)
	
	if (latte_total != 0):
		latte_percent_comp = latte_count / float(latte_total)

	if (affogato_total != 0):
		affogato_percent_comp = affogato_count / float(affogato_total)

	if (not test):
		print('tea_comp: ', tea_count, 'latte_comp:', latte_count, 'affogato_count: ', affogato_count)
		print('tea_total: ', tea_total, 'latte_total: ', latte_total, 'affogato_total', affogato_total)
		print('tea_avg_wait', tea_avg_wait, 'latte_avg_wait', latte_avg_wait, 'affogato_avg_wait', affogato_avg_wait)
		print('tea_percent_comp', tea_percent_comp, 'latte_percent_comp', latte_percent_comp, 'affogato_percent_comp', affogato_percent_comp)
	return (tea_avg_wait, latte_avg_wait, affogato_avg_wait, tea_percent_comp, \
		latte_percent_comp, affogato_percent_comp)





