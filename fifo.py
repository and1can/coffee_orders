import json
import unittest
from chainmap import ChainMap
import sys

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
	

def profit_metric():
	with open('output_fifo.json') as data_file:
		data = json.load(data_file)

	profit = 0
	for i in range(len(data)):	
		profit += data[i]

#i is input and o is output
#returns the wait time of a particular order
def calcWaitTime(i, o):
	
	return o['start_time'] - i['order_time'] + drink_map[i['type']][0]

def simulateCafeDay(input_filename):

	retdata = []
	metricData = []
	b1_time = 0
	b2_time = 0

	profit = 0
	num_of_order = 0
	wait_time = 0
	barista_avail = 0
	with open(input_filename + '.json') as data_file:
		data = json.load(data_file)

	for i in range(len(data)):
		curr_input = data[i]
		barista = getBarista(b1_time, b2_time)
		if (b1_time == b2_time):
			barista_avail += 1
		if (barista == 1):
			if (b1_time <= 100 and (curr_input['order_time'] <= 100)):
				b1_time, output = baristaProcess(curr_input, barista, b1_time)
				retdata.append(output)
				#create a dictionary that contains input and output information to be written to fifo_metric_output
				curr_input['barista_id'] = output['barista_id']
				curr_input['order_id'] = output['order_id']
				curr_input['start_time'] = output['start_time']
				metricData.append(curr_input)

				#calculating overall metrics of algorithm
				wait_time += calcWaitTime(curr_input, output)
				profit += drink_map[curr_input['type']][1]
				num_of_order += 1
		else:
			if (b2_time <= 100 and (curr_input['order_time'] <= 100)): 
				b2_time, output = baristaProcess(curr_input, barista, b2_time)
				retdata.append(output)

				#create a dictionary that contains input and output information to be written to fifo_metric_output
				curr_input['barista_id'] = output['barista_id']
				curr_input['order_id'] = output['order_id']
				curr_input['start_time'] = output['start_time']
				metricData.append(curr_input)

				#calculating overall metrics of algorithm
				wait_time += calcWaitTime(curr_input, output)
				profit += drink_map[curr_input['type']][1]
				num_of_order += 1
				
			
	with open('output_files/output_fifo' + '.json', 'w') as outfile:
		json.dump(retdata, outfile, indent = 4, sort_keys=True, separators=(',', ':'))

	with open('output_files/fifo_metric_output' + '.json', 'w') as outfile:
		json.dump(metricData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))
	return profit, num_of_order, (num_of_order / float(len(data))), \
	(wait_time / float(num_of_order)), (barista_avail)
	#return 'profit: ' + str(profit), 'num of order: ' +  str(num_of_order), 'percent of order: ' + str(num_of_order / float(len(data))), 'average wait_time: ' + str(wait_time / float(num_of_order)), 'times both baristas available at same time: ' + str(barista_avail)





	
if __name__ == '__main__':
	print(sys.argv)
	if (len(sys.argv) < 2):
		print('need to type a file to run fifo algorithm or type test to run tests')
	else:
	 	if (sys.argv[1] == 'tests'):
			print('running tests')
			unittest.main()
		else: 
			print('running fifo.py on input file ' + str(sys.argv[1]) + '.json')
	#unittest.main()
			
	
