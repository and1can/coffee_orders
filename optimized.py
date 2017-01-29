import json
import unittest
from chainmap import ChainMap

#key is the type of drink
#value is tuple
#0th tuple value is brew time
#1st tuple value is profit
drink_map = dict([("tea", [3, 2]), ("latte", [4, 3]), ("affogato", [7, 5])])

#function returns 1 for barista 1 and 2 for barista 2
#the barista returned is the first to be available
#t1 is the next available time or barista 1
#t2 is the next available time for barista 2
def getBarista(t1, t2):
	if (t1 <= t2):
		return 1
	else: 
		return 2

#def process(d1, d2, alternate_bool):
	#print('processing: ', d1, d2)
#	d1_wait = drink_map[d1['type']][0]
#	d2_wait = drink_map[d2['type']][0]
#	if (d1_wait <= d2_wait):
#		if (alternate_bool):
#			return (d2, d1)
#		else:
#			return (d1, d2)
#	else:
#		if (alternate_bool):
#			return (d1, d2)
#		else:
#			return (d2, d1)

def process(d1, d2):
	#print('processing: ', d1, d2)
	d1_wait = drink_map[d1['type']][0]
	d2_wait = drink_map[d2['type']][0]
	if (d1_wait <= d2_wait):
		return (d1, d2)
	else:
		return (d2, d1)

#returns the startTime
#b is the start time of the barista
#o is the order time
def getStartTime(b, o):
	if (b > o): 
		return b
	else: 
		return o

#returns the new time for particular barista after completing current order
#bTime is the current time of availability for barista
#drink is the type of drink for the current order
def incrementTime(bTime, drink):
	#print('bTime: ', bTime, 'drink', drink)
	return bTime + drink_map[drink][0]

#curr is the array that contains order_time, type, and order_id
#barista is the id of the barista that will process order
#b_time is time that barista processing order is available 
#returns an array returnData with new start_time, the new availble time for barista that is processing order
#and the output for the order respectively. 
def baristaProcess(curr, barista, b_time):
	returnData = []
	start_time = getStartTime(b_time, curr['order_time'])
	b_time = incrementTime(start_time, curr['type'])
	order = dict([("barista_id", barista), ("start_time", start_time), ("order_id", curr['order_id'])])
	return b_time, order

#i is input and o is output
#returns the wait time of a particular order
def calcWaitTime(i, o):
	
	return o['start_time'] - i['order_time'] + drink_map[i['type']][0]

def optimize(input_filename):
	offset = 0 

	retData = []
	metricData = []
	b1_time = 0
	b2_time = 0

	profit = 0
	num_of_order = 0
	wait_time = 0
	barista_avail = 0

	alternate_bool = True
	
	with open(input_filename + '.json') as data_file:
		data = json.load(data_file)
	for i in range(len(data) / 2):
		d1 = data[i + offset]
		d2 = data[i + offset + 1]
		#print('alternate_bool', alternate_bool)
		offset += 1
		#barista1_order, barista2_order = process(d1, d2, alternate_bool)
		barista1_order, barista2_order = process(d1, d2)
		alternate_bool = not alternate_bool
		b1_order_time = drink_map[barista1_order['type']][0]
		b2_order_time = drink_map[barista2_order['type']][0]

		if (b1_time + b1_order_time <= 100):
			b1_time, output = baristaProcess(barista1_order, 1, b1_time)
			retData.append(output)
			wait_time += calcWaitTime(barista1_order, output)
			profit += drink_map[barista1_order['type']][1]
			num_of_order += 1

			#create a dictionary that contains input and output information to be written to fifo_metric_output
		
			barista1_order['barista_id'] = output['barista_id']
			barista1_order['order_id'] = output['order_id']
			barista1_order['start_time'] = output['start_time']
			metricData.append(barista1_order)

		if (b2_time + b2_order_time <= 100):
			b2_time, output = baristaProcess(barista2_order, 2, b2_time)
			retData.append(output)
			wait_time += calcWaitTime(barista2_order, output)
			profit += drink_map[barista2_order['type']][1]
			num_of_order += 1

			#create a dictionary that contains input and output information to be written to fifo_metric_output
			
			barista2_order['barista_id'] = output['barista_id']
			barista2_order['order_id'] = output['order_id']
			barista2_order['start_time'] = output['start_time']
			metricData.append(barista2_order)

	if (len(data) % 2 == 1):
		print('we have odd case', 'last data point: ', data[len(data) - 1])
		lastData = data[len(data) - 1]
		barista = getBarista(b1_time, b2_time)
		lastOrderTime = drink_map[lastData['type']][0]
		print('barista: ', barista, 'b1_time: ', b1_time, 'b2_time: ', b2_time, 'lastOrderTime: ', lastOrderTime)
		if (barista == 1 and b1_time + lastOrderTime <= 100):
			b1_time, output = baristaProcess(lastData, barista, b1_time)
			retData.append(output)

			#create a dictionary that contains input and output information to be written to fifo_metric_output
			lastData['barista_id'] = output['barista_id']
			lastData['order_id'] = output['order_id']
			lastData['start_time'] = output['start_time']
			metricData.append(lastData)

			#calculating overall metrics of algorithm
			wait_time += calcWaitTime(lastData, output)
			profit += drink_map[lastData['type']][1]
			num_of_order += 1
		elif (barista == 2 and b2_time + lastOrderTime <= 100):
			b1_time, output = baristaProcess(lastData, barista, b2_time)
			retData.append(output)

			#create a dictionary that contains input and output information to be written to fifo_metric_output
			lastData['barista_id'] = output['barista_id']
			lastData['order_id'] = output['order_id']
			lastData['start_time'] = output['start_time']
			metricData.append(lastData)

			#calculating overall metrics of algorithm
			wait_time += calcWaitTime(lastData, output)
			profit += drink_map[lastData['type']][1]
			num_of_order += 1

	
	with open('optimized_metric_output' + '.json', 'w') as outfile:
		json.dump(metricData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))
	

	with open('output_optimized' + '.json', 'w') as outfile:
		json.dump(retData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))
	#return 'profit: ' + str(profit), 'num of order: ' +  str(num_of_order), 'percent of order: ' + str(num_of_order / float(len(data))), 'average wait_time: ' + str(wait_time / float(num_of_order)), 'times both baristas available at same time: ' + str(barista_avail)
	return str(profit), str(num_of_order), str(num_of_order / float(len(data))), str(wait_time / float(num_of_order)), str(barista_avail)



	