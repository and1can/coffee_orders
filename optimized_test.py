import optimized as opt
import json
import unittest

class TestProcess(unittest.TestCase):

	def test_process_baristaOrderMaintained_When_Two_Orders_are_of_same_type(self):
		barista1, barista2 = opt.process({"order_id":1, "order_time":1, "type":"affogato"},{"order_id":2, "order_time":2, "type":"affogato"} )
		#print('barista1: ', barista1)
		self.assertEquals(barista1['order_id'], 1)
		self.assertEquals(barista2['order_id'], 2)

	def test_first_order_slower_than_second(self):
		barista1, barista2 = opt.process({"order_id":1, "order_time":1, "type":"affogato"},{"order_id":2, "order_time":2, "type":"latte"} )
		self.assertEquals(barista1['order_id'], 2)
		self.assertEquals(barista2['order_id'], 1)

	def test_first_order_faster_than_second(self):
		barista1, barista2 = opt.process({"order_id":1, "order_time":1, "type":"tea"},{"order_id":2, "order_time":2, "type":"latte"} )
		self.assertEquals(barista1['order_id'], 1)
		self.assertEquals(barista2['order_id'], 2)

class TestDrinkMap(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(opt.drink_map['tea'], [3, 2])
	
	def test_latte(self):
		self.assertEqual(opt.drink_map['latte'], [4, 3])

	def test_affogato(self):
		self.assertEqual(opt.drink_map['affogato'], [7, 5])

class TestGetStartTime(unittest.TestCase):
	
	def test_order_time_greater_than_barista_available_time(self):
		self.assertEqual(opt.getStartTime(0, 1), 1)

	def test_order_time_less_than_barista_available_time(self):
		self.assertEqual(opt.getStartTime(1, 0), 1)

class TestIncrementTime(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(opt.incrementTime(0, 'tea'), 3)

	def test_latte(self):
		self.assertEqual(opt.incrementTime(0, 'latte'), 4)

	def test_affogato(self):
		self.assertEqual(opt.incrementTime(0, 'affogato'), 7)

class TestBaristaProcess(unittest.TestCase):

	def test_barista1_order_time_greater_than_barista_availability(self):
		btime, order = opt.baristaProcess({"order_id":1, "order_time":1, "type":"affogato"}, 1, 0)
		self.assertEqual(btime, 8)
		self.assertEquals(order['barista_id'], 1)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_greater_than_barista_availability(self):
		btime, order = opt.baristaProcess({"order_id":1, "order_time":1, "type":"tea"}, 2, 0)
		self.assertEqual(btime, 4)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_less_than_barista_availability(self):
		btime, order = opt.baristaProcess({"order_id":1, "order_time":0, "type":"latte"}, 2, 2)		
		self.assertEqual(btime, 6)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 2)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_same_as_barista_availability(self):
		btime, order = opt.baristaProcess({"order_id":1, "order_time":2, "type":"latte"}, 2, 2)
		self.assertEqual(btime, 6)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 2)
		self.assertEquals(order['order_id'], 1)

class TestCalcWaitTime(unittest.TestCase):

	def test_tea_immediate(self):
		difference = opt.calcWaitTime({"order_id":1, "order_time":1, "type":"tea"}, {"barista_id":1, "start_time":1, "type":"tea"})
		self.assertEquals(difference, 3)

	def test_tea_delay(self):
		difference = opt.calcWaitTime({"order_id":1, "order_time":1, "type":"tea"}, {"barista_id":1, "start_time":2, "type":"tea"})
		self.assertEquals(difference, 4)

	def test_latte_immediate(self):
		difference = opt.calcWaitTime({"order_id":1, "order_time":2, "type":"latte"}, {"barista_id":1, "start_time":2, "type":"latte"})
		self.assertEquals(difference, 4)

	def test_latte_delay(self):
		difference = opt.calcWaitTime({"order_id":1, "order_time":2, "type":"latte"}, {"barista_id":1, "start_time":3, "type":"latte"})
		self.assertEquals(difference, 5)

	def test_affogato_immediate(self):
		difference = opt.calcWaitTime({"order_id":1, "order_time":3, "type":"affogato"}, {"barista_id":1, "start_time":3, "type":"affogato"})
		self.assertEquals(difference, 7)

	def test_affogato_delay(self):
		difference = opt.calcWaitTime({"order_id":1, "order_time":3, "type":"affogato"}, {"barista_id":1, "start_time":4, "type":"affogato"})
		self.assertEquals(difference, 8)

class TestOptimize(unittest.TestCase):

	#test is in optimize_test1
	def test_same_order_time_first_order_is_faster_than_second(self):
		opt.optimize('optimized_tests/optimize_test1')
		with open('output_files/output_optimized.json') as data_file:
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
		opt.optimize('optimized_tests/optimize_test2')
		with open('output_files/output_optimized.json') as data_file:
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
		opt.optimize('optimized_tests/optimize_test3')
		with open('output_files/output_optimized.json') as data_file:
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
		opt.optimize('optimized_tests/optimize_test4')
		with open('output_files/output_optimized.json') as data_file:
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
		opt.optimize('optimized_tests/optimize_test5')
		with open('output_files/output_optimized.json') as data_file:
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
		opt.optimize('optimized_tests/optimize_test6')
		with open('output_files/output_optimized.json') as data_file:
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
		opt.optimize('optimized_tests/optimize_test7')
		with open('output_files/optimized_metric_output.json') as data_file:
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
	unittest.main()