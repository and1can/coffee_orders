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
				
			
	with open('output_fifo' + '.json', 'w') as outfile:
		json.dump(retdata, outfile, indent = 4, sort_keys=True, separators=(',', ':'))

	with open('fifo_metric_output' + '.json', 'w') as outfile:
		json.dump(metricData, outfile, indent = 4, sort_keys=True, separators=(',', ':'))
	return profit, num_of_order, (num_of_order / float(len(data))), \
	(wait_time / float(num_of_order)), (barista_avail)
	#return 'profit: ' + str(profit), 'num of order: ' +  str(num_of_order), 'percent of order: ' + str(num_of_order / float(len(data))), 'average wait_time: ' + str(wait_time / float(num_of_order)), 'times both baristas available at same time: ' + str(barista_avail)


class TestBaristaChosen(unittest.TestCase):
	
	#when both baristas are available, barista 1 is chosen
	def test_barista1chosen(self):
		self.assertEqual(getBarista(0, 0), 1)

	#when barista 1 is available before barista 2, barista 1 is chosen
	def test_barista1chosen(self):
		self.assertEqual(getBarista(0, 1), 1)

	#when barista 2 is available before barista 1, barista 2 is chosen
	def test_barista2chosen(self):
		self.assertEqual(getBarista(1, 0), 2)

class TestDrinkMap(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(drink_map['tea'], [3, 2])
	
	def test_latte(self):
		self.assertEqual(drink_map['latte'], [4, 3])

	def test_affogato(self):
		self.assertEqual(drink_map['affogato'], [7, 5])

class TestStartTime(unittest.TestCase):
	
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

class TestSimulateCafeDay(unittest.TestCase):
	
	def test_barista_both_available_at_same_time_two_orders_have_same_order_time(self):
		simulateCafeDay('fifo_test1')
		with open('output_fifo.json') as data_file:
			data = json.load(data_file)

		order1 = data[0]
		self.assertEqual(order1['order_id'], 1)
		self.assertEqual(order1['start_time'], 0)
		self.assertEqual(order1['barista_id'], 1)

		order2 = data[1]
		self.assertEqual(order2['order_id'],2)
		self.assertEqual(order2['start_time'], 0)
		self.assertEqual(order2['barista_id'], 2)

	def test_barista_both_available_at_same_time_two_orders_have_different_order_time(self):
		simulateCafeDay('fifo_test2')
		with open('output_fifo.json') as data_file:
			data = json.load(data_file)

		order1 = data[0]
		self.assertEqual(order1['order_id'], 1)
		self.assertEqual(order1['start_time'], 1)
		self.assertEqual(order1['barista_id'], 1)

		order2 = data[1]
		self.assertEqual(order2['order_id'],2)
		self.assertEqual(order2['start_time'], 0)
		self.assertEqual(order2['barista_id'], 2)

	def test_barista1_busy_barista2_available(self):
		simulateCafeDay('fifo_test3')
		with open('output_fifo.json') as data_file:
			data = json.load(data_file)

		order1 = data[0]
		self.assertEqual(order1['order_id'], 1)
		self.assertEqual(order1['start_time'], 0)
		self.assertEqual(order1['barista_id'], 1)

		order2 = data[1]
		self.assertEqual(order2['order_id'],2)
		self.assertEqual(order2['start_time'], 0)
		self.assertEqual(order2['barista_id'], 2)

		order2 = data[2]
		self.assertEqual(order2['order_id'],3)
		self.assertEqual(order2['start_time'], 3)
		self.assertEqual(order2['barista_id'], 2)

	def test_barista2_busy_barista1_available(self):
		simulateCafeDay('fifo_test4')
		with open('output_fifo.json') as data_file:
			data = json.load(data_file)

		order1 = data[0]
		self.assertEqual(order1['order_id'], 1)
		self.assertEqual(order1['start_time'], 0)
		self.assertEqual(order1['barista_id'], 1)

		order2 = data[1]
		self.assertEqual(order2['order_id'],2)
		self.assertEqual(order2['start_time'], 0)
		self.assertEqual(order2['barista_id'], 2)

		order2 = data[2]
		self.assertEqual(order2['order_id'],3)
		self.assertEqual(order2['start_time'], 3)
		self.assertEqual(order2['barista_id'], 1)

	def test_both_baristas_busy(self):
		simulateCafeDay('fifo_test5')
		with open('output_fifo.json') as data_file:
			data = json.load(data_file)

		order1 = data[0]
		self.assertEqual(order1['order_id'], 1)
		self.assertEqual(order1['start_time'], 0)
		self.assertEqual(order1['barista_id'], 1)

		order2 = data[1]
		self.assertEqual(order2['order_id'],2)
		self.assertEqual(order2['start_time'], 0)
		self.assertEqual(order2['barista_id'], 2)

		order2 = data[2]
		self.assertEqual(order2['order_id'],3)
		self.assertEqual(order2['start_time'], 3)
		self.assertEqual(order2['barista_id'], 1)

	#test if the given test from prompt works
	def test_simulateCafeDay(self):
		profit, num_of_orders, percent_of_orders, average_wait_time, _ = simulateCafeDay('input_test1')
		with open('output_fifo.json') as data_file:
			data = json.load(data_file)

		order1 = data[0]
		self.assertEqual(order1['order_id'],1)
		self.assertEqual(order1['start_time'], 0)
		self.assertEqual(order1['barista_id'], 1)

		order2 = data[1]
		self.assertEqual(order2['order_id'],2)
		self.assertEqual(order2['start_time'], 1)
		self.assertEqual(order2['barista_id'], 2)

		order3 = data[2]
		self.assertEqual(order3['order_id'],3)
		self.assertEqual(order3['start_time'], 4)
		self.assertEqual(order3['barista_id'], 2)

		order4 = data[3]
		self.assertEqual(order4['order_id'],4)
		self.assertEqual(order4['start_time'], 7)
		self.assertEqual(order4['barista_id'], 1)

	def test_metrics(self):
		profit, num_of_orders, percent_of_orders, average_wait_time, _ = simulateCafeDay('input_test1')
		self.assertEquals(profit, 12)
		self.assertEquals(num_of_orders, 4)
		self.assertEquals(percent_of_orders, 0.8)
		self.assertEquals(average_wait_time, 24/float(4))
	
	def test_BaristaNotAbleToProcessOrderUntilAfterTis100(self):
		profit, num_of_orders, percent_of_orders, average_wait_time, _ = simulateCafeDay('input_test2')
		self.assertEquals(profit, 10)
		self.assertEquals(num_of_orders, 3)
		self.assertEquals(percent_of_orders, 0.6)
		self.assertEquals(average_wait_time, 16/float(3))

	def test_output_metric_file(self):
		simulateCafeDay('input_test3')
		with open('fifo_metric_output.json') as data_file:
			data = json.load(data_file)

		order1 = data[0]
		self.assertEqual(order1['order_id'],1)
		self.assertEqual(order1['start_time'], 0)
		self.assertEqual(order1['barista_id'], 1)
		self.assertEqual(order1['type'], 'affogato')
		self.assertEquals(order1['order_time'], 0)

		order2 = data[1]
		self.assertEqual(order2['order_id'],2)
		self.assertEqual(order2['start_time'], 1)
		self.assertEqual(order2['barista_id'], 2)
		self.assertEqual(order2['type'], 'tea')
		self.assertEqual(order2['order_time'], 1)

		order3 = data[2]
		self.assertEqual(order3['order_id'],3)
		self.assertEqual(order3['start_time'], 4)
		self.assertEqual(order3['barista_id'], 2)
		self.assertEqual(order3['type'], 'latte')
		self.assertEqual(order3['order_time'], 2)

		order4 = data[3]
		self.assertEqual(order4['order_id'],4)
		self.assertEqual(order4['start_time'], 7)
		self.assertEqual(order4['barista_id'], 1)
		self.assertEqual(order4['type'], 'tea')
		self.assertEqual(order4['order_time'], 2)

	
if __name__ == '__main__':
	print(simulateCafeDay('poisson_mean_50_47_samples_equal_prob_types_of_drinks'))
	#unittest.main()

	
