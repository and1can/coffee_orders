import json
import unittest
from chainmap import ChainMap

#key is the type of drink
#value is tuple
#0th tuple value is brew time
#1st tuple value is profit
drink_map = dict([("tea", [3, 2]), ("latte", [4, 3]), ("affogato", [7, 5])])

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
	
	with open(input_filename + '.json') as data_file:
		data = json.load(data_file)
	for i in range(len(data) / 2):
		d1 = data[i + offset]
		d2 = data[i + offset + 1]
		offset += 1
		barista1_order, barista2_order = process(d1, d2)
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
	
	with open('optimized_metric_output' + '.json', 'w') as outfile:
		json.dump(metricData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))
	

	with open('output_optimized' + '.json', 'w') as outfile:
		json.dump(retData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))
	#return 'profit: ' + str(profit), 'num of order: ' +  str(num_of_order), 'percent of order: ' + str(num_of_order / float(len(data))), 'average wait_time: ' + str(wait_time / float(num_of_order)), 'times both baristas available at same time: ' + str(barista_avail)
	return str(profit), str(num_of_order), str(num_of_order / float(len(data))), str(wait_time / float(num_of_order)), str(barista_avail)


class TestProcess(unittest.TestCase):

	def test_process_baristaOrderMaintained_When_Two_Orders_are_of_same_type(self):
		barista1, barista2 = process({"order_id":1, "order_time":1, "type":"affogato"},{"order_id":2, "order_time":2, "type":"affogato"} )
		#print('barista1: ', barista1)
		self.assertEquals(barista1['order_id'], 1)
		self.assertEquals(barista2['order_id'], 2)

	def test_first_order_slower_than_second(self):
		barista1, barista2 = process({"order_id":1, "order_time":1, "type":"affogato"},{"order_id":2, "order_time":2, "type":"latte"} )
		self.assertEquals(barista1['order_id'], 2)
		self.assertEquals(barista2['order_id'], 1)

	def test_first_order_faster_than_second(self):
		barista1, barista2 = process({"order_id":1, "order_time":1, "type":"tea"},{"order_id":2, "order_time":2, "type":"latte"} )
		self.assertEquals(barista1['order_id'], 1)
		self.assertEquals(barista2['order_id'], 2)

class TestDrinkMap(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(drink_map['tea'], [3, 2])
	
	def test_latte(self):
		self.assertEqual(drink_map['latte'], [4, 3])

	def test_affogato(self):
		self.assertEqual(drink_map['affogato'], [7, 5])

class TestGetStartTime(unittest.TestCase):
	
	def test_order_time_greater_than_barista_available_time(self):
		self.assertEqual(getStartTime(0, 1), 1)

	def test_order_time_less_than_barista_available_time(self):
		self.assertEqual(getStartTime(1, 0), 1)

class TestIncrementTime(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(incrementTime(0, 'tea'), 3)

	def test_latte(self):
		self.assertEqual(incrementTime(0, 'latte'), 4)

	def test_affogato(self):
		self.assertEqual(incrementTime(0, 'affogato'), 7)

class TestBaristaProcess(unittest.TestCase):

	def test_barista1_order_time_greater_than_barista_availability(self):
		btime, order = baristaProcess({"order_id":1, "order_time":1, "type":"affogato"}, 1, 0)
		self.assertEqual(btime, 8)
		self.assertEquals(order['barista_id'], 1)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_greater_than_barista_availability(self):
		btime, order = baristaProcess({"order_id":1, "order_time":1, "type":"tea"}, 2, 0)
		self.assertEqual(btime, 4)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_less_than_barista_availability(self):
		btime, order = baristaProcess({"order_id":1, "order_time":0, "type":"latte"}, 2, 2)		
		self.assertEqual(btime, 6)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 2)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_same_as_barista_availability(self):
		btime, order = baristaProcess({"order_id":1, "order_time":2, "type":"latte"}, 2, 2)
		self.assertEqual(btime, 6)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 2)
		self.assertEquals(order['order_id'], 1)

class TestCalcWaitTime(unittest.TestCase):

	def test_tea_immediate(self):
		difference = calcWaitTime({"order_id":1, "order_time":1, "type":"tea"}, {"barista_id":1, "start_time":1, "type":"tea"})
		self.assertEquals(difference, 3)

	def test_tea_delay(self):
		difference = calcWaitTime({"order_id":1, "order_time":1, "type":"tea"}, {"barista_id":1, "start_time":2, "type":"tea"})
		self.assertEquals(difference, 4)

	def test_latte_immediate(self):
		difference = calcWaitTime({"order_id":1, "order_time":2, "type":"latte"}, {"barista_id":1, "start_time":2, "type":"latte"})
		self.assertEquals(difference, 4)

	def test_latte_delay(self):
		difference = calcWaitTime({"order_id":1, "order_time":2, "type":"latte"}, {"barista_id":1, "start_time":3, "type":"latte"})
		self.assertEquals(difference, 5)

	def test_affogato_immediate(self):
		difference = calcWaitTime({"order_id":1, "order_time":3, "type":"affogato"}, {"barista_id":1, "start_time":3, "type":"affogato"})
		self.assertEquals(difference, 7)

	def test_affogato_delay(self):
		difference = calcWaitTime({"order_id":1, "order_time":3, "type":"affogato"}, {"barista_id":1, "start_time":4, "type":"affogato"})
		self.assertEquals(difference, 8)

class TestOptimize(unittest.TestCase):

	#test is in optimize_test1
	def test_same_order_time_first_order_is_faster_than_second(self):
		optimize('optimize_test1')
		with open('output_optimized.json') as data_file:
			data = json.load(data_file)
		
		order1 = data[0]
		self.assertEquals(order1['order_id'], 1)
		self.assertEquals(order1['start_time'], 0)
		self.assertEquals(order1['barista_id'], 1)
		
		order2 = data[1]
		self.assertEquals(order2['order_id'], 2)
		self.assertEquals(order2['start_time'], 0)
		self.assertEquals(order2['barista_id'], 2)

	#test is in optimize_test2
	def test_same_order_time_first_order_is_slower_than_second(self):
		optimize('optimize_test2')
		with open('output_optimized.json') as data_file:
			data = json.load(data_file)
		
		order1 = data[0]
		self.assertEquals(order1['order_id'], 2)
		self.assertEquals(order1['start_time'], 0)
		self.assertEquals(order1['barista_id'], 1)
		
		order2 = data[1]
		self.assertEquals(order2['order_id'], 1)
		self.assertEquals(order2['start_time'], 0)
		self.assertEquals(order2['barista_id'], 2)

	#test is in optimize_test3
	def test_first_order_time_is_first_and_order_is_faster_than_second_order(self):
		optimize('optimize_test3')
		with open('output_optimized.json') as data_file:
			data = json.load(data_file)
		
		order1 = data[0]
		self.assertEquals(order1['order_id'], 1)
		self.assertEquals(order1['start_time'], 0)
		self.assertEquals(order1['barista_id'], 1)
		
		order2 = data[1]
		self.assertEquals(order2['order_id'], 2)
		self.assertEquals(order2['start_time'], 2)
		self.assertEquals(order2['barista_id'], 2)

	#test is in optimize_test4
	def test_first_order_time_is_first_and_order_is_slower_than_second_order(self):
		optimize('optimize_test4')
		with open('output_optimized.json') as data_file:
			data = json.load(data_file)
		
		order1 = data[0]
		self.assertEquals(order1['order_id'], 2)
		self.assertEquals(order1['start_time'], 2)
		self.assertEquals(order1['barista_id'], 1)
		
		order2 = data[1]
		self.assertEquals(order2['order_id'], 1)
		self.assertEquals(order2['start_time'], 0)
		self.assertEquals(order2['barista_id'], 2)

	#test is in optimize_test5
	def test_first_order_time_is_second_and_order_is_faster_than_second_order(self):
		optimize('optimize_test5')
		with open('output_optimized.json') as data_file:
			data = json.load(data_file)
		
		order1 = data[0]
		self.assertEquals(order1['order_id'], 1)
		self.assertEquals(order1['start_time'], 2)
		self.assertEquals(order1['barista_id'], 1)
		
		order2 = data[1]
		self.assertEquals(order2['order_id'], 2)
		self.assertEquals(order2['start_time'], 1)
		self.assertEquals(order2['barista_id'], 2)

	#test is in optimize_test6
	def test_first_order_time_is_second_and_order_is_slower_than_second_order(self):
		optimize('optimize_test6')
		with open('output_optimized.json') as data_file:
			data = json.load(data_file)
		
		order1 = data[0]
		self.assertEquals(order1['order_id'], 2)
		self.assertEquals(order1['start_time'], 1)
		self.assertEquals(order1['barista_id'], 1)
		
		order2 = data[1]
		self.assertEquals(order2['order_id'], 1)
		self.assertEquals(order2['start_time'], 2)
		self.assertEquals(order2['barista_id'], 2)

	def test_output_metric_file(self):
		optimize('optimize_test7')
		with open('optimized_metric_output.json') as data_file:
			data = json.load(data_file)

		order1 = data[0]
		self.assertEqual(order1['order_id'],2)
		self.assertEqual(order1['start_time'], 1)
		self.assertEqual(order1['barista_id'], 1)
		self.assertEqual(order1['type'], 'tea')
		self.assertEquals(order1['order_time'], 1)

		order2 = data[1]
		self.assertEqual(order2['order_id'],1)
		self.assertEqual(order2['start_time'], 0)
		self.assertEqual(order2['barista_id'], 2)
		self.assertEqual(order2['type'], 'affogato')
		self.assertEqual(order2['order_time'], 0)

		order3 = data[2]
		self.assertEqual(order3['order_id'],4)
		self.assertEqual(order3['start_time'], 4)
		self.assertEqual(order3['barista_id'], 1)
		self.assertEqual(order3['type'], 'tea')
		self.assertEqual(order3['order_time'], 2)

		order4 = data[3]
		self.assertEqual(order4['order_id'],3)
		self.assertEqual(order4['start_time'], 7)
		self.assertEqual(order4['barista_id'], 2)
		self.assertEqual(order4['type'], 'latte')
		self.assertEqual(order4['order_time'], 2)

if __name__ == '__main__':
	print(optimize('input'))
	unittest.main()
	