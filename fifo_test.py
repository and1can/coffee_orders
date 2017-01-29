import fifo 
import json
import unittest

class TestBaristaChosen(unittest.TestCase):
	
	#when both baristas are available, barista 1 is chosen
	def test_barista1chosen(self):
		self.assertEqual(fifo.getBarista(0, 0), 1)

	#when barista 1 is available before barista 2, barista 1 is chosen
	def test_barista1chosen(self):
		self.assertEqual(fifo.getBarista(0, 1), 1)

	#when barista 2 is available before barista 1, barista 2 is chosen
	def test_barista2chosen(self):
		self.assertEqual(fifo.getBarista(1, 0), 2)

class TestDrinkMap(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(fifo.drink_map['tea'], [3, 2])
	
	def test_latte(self):
		self.assertEqual(fifo.drink_map['latte'], [4, 3])

	def test_affogato(self):
		self.assertEqual(fifo.drink_map['affogato'], [7, 5])

class TestStartTime(unittest.TestCase):
	
	def test_order_time_greater_than_barista_available_time(self):
		self.assertEqual(fifo.getStartTime(0, 1), 1)

	def test_order_time_less_than_barista_available_time(self):
		self.assertEqual(fifo.getStartTime(1, 0), 1)

class TestIncrementTime(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(fifo.incrementTime(0, 'tea'), 3)

	def test_latte(self):
		self.assertEqual(fifo.incrementTime(0, 'latte'), 4)

	def test_affogato(self):
		self.assertEqual(fifo.incrementTime(0, 'affogato'), 7)

class TestCalcWaitTime(unittest.TestCase):

	def test_tea_immediate(self):
		difference = fifo.calcWaitTime({"order_id":1, "order_time":1, "type":"tea"}, {"barista_id":1, "start_time":1, "type":"tea"})
		self.assertEquals(difference, 3)

	def test_tea_delay(self):
		difference = fifo.calcWaitTime({"order_id":1, "order_time":1, "type":"tea"}, {"barista_id":1, "start_time":2, "type":"tea"})
		self.assertEquals(difference, 4)

	def test_latte_immediate(self):
		difference = fifo.calcWaitTime({"order_id":1, "order_time":2, "type":"latte"}, {"barista_id":1, "start_time":2, "type":"latte"})
		self.assertEquals(difference, 4)

	def test_latte_delay(self):
		difference = fifo.calcWaitTime({"order_id":1, "order_time":2, "type":"latte"}, {"barista_id":1, "start_time":3, "type":"latte"})
		self.assertEquals(difference, 5)

	def test_affogato_immediate(self):
		difference = fifo.calcWaitTime({"order_id":1, "order_time":3, "type":"affogato"}, {"barista_id":1, "start_time":3, "type":"affogato"})
		self.assertEquals(difference, 7)

	def test_affogato_delay(self):
		difference = fifo.calcWaitTime({"order_id":1, "order_time":3, "type":"affogato"}, {"barista_id":1, "start_time":4, "type":"affogato"})
		self.assertEquals(difference, 8)


class TestBaristaProcess(unittest.TestCase):

	def test_barista1_order_time_greater_than_barista_availability(self):
		btime, order = fifo.baristaProcess({"order_id":1, "order_time":1, "type":"affogato"}, 1, 0)
		self.assertEqual(btime, 8)
		self.assertEquals(order['barista_id'], 1)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_greater_than_barista_availability(self):
		btime, order = fifo.baristaProcess({"order_id":1, "order_time":1, "type":"tea"}, 2, 0)
		self.assertEqual(btime, 4)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_less_than_barista_availability(self):
		btime, order = fifo.baristaProcess({"order_id":1, "order_time":0, "type":"latte"}, 2, 2)		
		self.assertEqual(btime, 6)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 2)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_same_as_barista_availability(self):
		btime, order = fifo.baristaProcess({"order_id":1, "order_time":2, "type":"latte"}, 2, 2)
		self.assertEqual(btime, 6)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 2)
		self.assertEquals(order['order_id'], 1)

class TestSimulateCafeDay(unittest.TestCase):
	
	def test_barista_both_available_at_same_time_two_orders_have_same_order_time(self):
		fifo.simulateCafeDay('fifo_tests/fifo_test1')
		with open('output_files/output_fifo.json') as data_file:
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
		fifo.simulateCafeDay('fifo_tests/fifo_test2')
		with open('output_files/output_fifo.json') as data_file:
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
		fifo.simulateCafeDay('fifo_tests/fifo_test3')
		with open('output_files/output_fifo.json') as data_file:
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
		fifo.simulateCafeDay('fifo_tests/fifo_test4')
		with open('output_files/output_fifo.json') as data_file:
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
		fifo.simulateCafeDay('fifo_tests/fifo_test5')
		with open('output_files/output_fifo.json') as data_file:
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
		profit, num_of_orders, percent_of_orders, average_wait_time, _ = fifo.simulateCafeDay('fifo_tests/input_test1')
		with open('output_files/output_fifo.json') as data_file:
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
		profit, num_of_orders, percent_of_orders, average_wait_time, _ = fifo.simulateCafeDay('fifo_tests/input_test1')
		self.assertEquals(profit, 12)
		self.assertEquals(num_of_orders, 4)
		self.assertEquals(percent_of_orders, 0.8)
		self.assertEquals(average_wait_time, 24/float(4))
	
	def test_BaristaNotAbleToProcessOrderUntilAfterTis100(self):
		profit, num_of_orders, percent_of_orders, average_wait_time, _ = fifo.simulateCafeDay('fifo_tests/input_test2')
		self.assertEquals(profit, 10)
		self.assertEquals(num_of_orders, 3)
		self.assertEquals(percent_of_orders, 0.6)
		self.assertEquals(average_wait_time, 16/float(3))

	def test_output_metric_file(self):
		fifo.simulateCafeDay('fifo_tests/input_test3')
		with open('output_files/fifo_metric_output.json') as data_file:
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
	unittest.main()