import json
import sys
import metric

#key is the type of drink
#value is tuple
#0th tuple value is brew time
#1st tuple value is profit
drink_map = dict([("tea", [3, 2]), ("latte", [4, 3]), ("affogato", [7, 5])])

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

#sort the orders based on how long it takes to brew in increasing order and return as tuple
def sort_orders(o1, o2, o3):
	orders = sorted([o1, o2, o3], key = lambda order: (drink_map[order['type']][0]))
	return orders

def processOrder(b_time, barista, order, wait_time, profit, num_of_orders):
	if (b_time + drink_map[order['type']][0] <= 100):
		b_time, output = baristaProcess(order, barista, b_time)
		wait_time += calcWaitTime(order, output)
		profit += drink_map[order['type']][1]
		num_of_orders += 1

		#create a dictionary that contains input and output information to be written to fifo_metric_output
		
		order['barista_id'] = output['barista_id']
		order['order_id'] = output['order_id']
		order['start_time'] = output['start_time']
		return (True, output, wait_time, profit, num_of_orders, b_time, order)
	return (False, None, wait_time, profit, num_of_orders, b_time, None)

def view_three(input_filename):

	retData = []
	metricData = []
	b1_time = 0
	b2_time = 0
	profit = 0
	num_of_order = 0
	wait_time = 0

	with open(input_filename + '.json') as data_file:
		data = json.load(data_file)

	for i in range(len(data) / 3):
		o1 = data[0]
		o2 = data[1]
		o3 = data[2]
		fast, med, slow = sort_orders(o1, o2, o3)
		barista, b_time = getBarista(b1_time, b2_time)
		
		#make these two chunks into a helper function called processOrder
		valid, output, wait_time, profit, num_of_orders, b_time, order = processOrder(b_time, barista, fast)
		if (valid):
			retData.append(ouput)
			metricData.append(order)
			if (barista == 1):
				b1_time = b_time
			else:
				b2_time = b_time

		valid, output, wait_time, profit, num_of_orders, b_time, order = processOrder(b_time, barista, med)
		if (valid):
			retData.append(ouput)
			metricData.append(order)
			if (barista == 1):
				b1_time = b_time
			else:
				b2_time = b_time

		valid, output, wait_time, profit, num_of_orders, b_time, order = processOrder(b_time, barista, slow)
		if (valid):
			retData.append(ouput)
			metricData.append(order)
			if (barista == 1):
				b1_time = b_time
			else:
				b2_time = b_time
		
		
		data = data[3::]

	#greedily process remainder 
	for i in range(len(data)):
		curr = data[i]
		b_time = 0
		barista = 0
		if (b1_time < b2_time):
			b_time = b1_time
			barista = 1
		else: 
			b_time = b2_time
			barista = 2
		valid, output, wait_time, profit, num_of_orders, b_time, order = processOrder(b_time, barista, curr)
		if (valid):
			retData.append(ouput)
			metricData.append(order)
			if (barista == 1):
				b1_time = b_time
			else:
				b2_time = b_time

	with open('output_files/optimized_metric_output' + '.json', 'w') as outfile:
		json.dump(metricData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))
	

	with open('output_files/output_optimized' + '.json', 'w') as outfile:
		json.dump(retData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))
	return str(profit), str(num_of_order), str(num_of_order / float(len(data))), str(wait_time / float(num_of_order)), str(barista_avail)
	#print('remaining data: ', data)

	#handle case with remainder of data

if __name__ == '__main__':
	print(sys.argv)
	if (len(sys.argv) < 2):
		print('need to type a file to run optimized algorithm')
	else: 
		print('running optimzed.py on input file ' + str(sys.argv[1]) + '.json')
		profit, num_of_orders, percent_of_orders, average_wait_time, _ = view_three(sys.argv[1])
		print('profit: ' + str(profit), 'num of order: ' +  str(num_of_orders), 'percent of order: ' + \
		 str(percent_of_orders), 'average wait_time: ' + str(average_wait_time))
		metric.metricCalc('output_files/optimized_metric_output', sys.argv[1], False)
