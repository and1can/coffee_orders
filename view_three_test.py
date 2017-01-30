import unittest
import view_three as vt

class TestDrinkMap(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(vt.drink_map['tea'], [3, 2])
	
	def test_latte(self):
		self.assertEqual(vt.drink_map['latte'], [4, 3])

	def test_affogato(self):
		self.assertEqual(vt.drink_map['affogato'], [7, 5])

class TestStartTime(unittest.TestCase):
	
	def test_order_time_greater_than_barista_available_time(self):
		self.assertEqual(vt.getStartTime(0, 1), 1)

	def test_order_time_less_than_barista_available_time(self):
		self.assertEqual(vt.getStartTime(1, 0), 1)

class TestIncrementTime(unittest.TestCase):
	
	def test_tea(self):
		self.assertEqual(vt.incrementTime(0, 'tea'), 3)

	def test_latte(self):
		self.assertEqual(vt.incrementTime(0, 'latte'), 4)

	def test_affogato(self):
		self.assertEqual(vt.incrementTime(0, 'affogato'), 7)

class TestCalcWaitTime(unittest.TestCase):

	def test_tea_immediate(self):
		difference = vt.calcWaitTime({"order_id":1, "order_time":1, "type":"tea"}, {"barista_id":1, "start_time":1, "type":"tea"})
		self.assertEquals(difference, 3)

	def test_tea_delay(self):
		difference = vt.calcWaitTime({"order_id":1, "order_time":1, "type":"tea"}, {"barista_id":1, "start_time":2, "type":"tea"})
		self.assertEquals(difference, 4)

	def test_latte_immediate(self):
		difference = vt.calcWaitTime({"order_id":1, "order_time":2, "type":"latte"}, {"barista_id":1, "start_time":2, "type":"latte"})
		self.assertEquals(difference, 4)

	def test_latte_delay(self):
		difference = vt.calcWaitTime({"order_id":1, "order_time":2, "type":"latte"}, {"barista_id":1, "start_time":3, "type":"latte"})
		self.assertEquals(difference, 5)

	def test_affogato_immediate(self):
		difference = vt.calcWaitTime({"order_id":1, "order_time":3, "type":"affogato"}, {"barista_id":1, "start_time":3, "type":"affogato"})
		self.assertEquals(difference, 7)

	def test_affogato_delay(self):
		difference = vt.calcWaitTime({"order_id":1, "order_time":3, "type":"affogato"}, {"barista_id":1, "start_time":4, "type":"affogato"})
		self.assertEquals(difference, 8)


class TestBaristaProcess(unittest.TestCase):

	def test_barista1_order_time_greater_than_barista_availability(self):
		btime, order = vt.baristaProcess({"order_id":1, "order_time":1, "type":"affogato"}, 1, 0)
		self.assertEqual(btime, 8)
		self.assertEquals(order['barista_id'], 1)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_greater_than_barista_availability(self):
		btime, order = vt.baristaProcess({"order_id":1, "order_time":1, "type":"tea"}, 2, 0)
		self.assertEqual(btime, 4)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_less_than_barista_availability(self):
		btime, order = vt.baristaProcess({"order_id":1, "order_time":0, "type":"latte"}, 2, 2)		
		self.assertEqual(btime, 6)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 2)
		self.assertEquals(order['order_id'], 1)

	def test_barista2_order_time_same_as_barista_availability(self):
		btime, order = vt.baristaProcess({"order_id":1, "order_time":2, "type":"latte"}, 2, 2)
		self.assertEqual(btime, 6)
		self.assertEquals(order['barista_id'], 2)
		self.assertEquals(order['start_time'], 2)
		self.assertEquals(order['order_id'], 1)

class TestSortOrders(unittest.TestCase):

	def test_three_different_types(self):
		o1 = {"order_id":1, "order_time":1, "type":"affogato"}
		o2 = {"order_id":2, "order_time":1, "type":"tea"}
		o3 = {"order_id":3, "order_time":1, "type":"latte"}
		fast, med, slow = vt.sort_orders(o1, o2, o3)
		self.assertEquals(fast['order_id'], 2)
		self.assertEquals(fast['type'], 'tea')
		self.assertEquals(med['order_id'], 3)
		self.assertEquals(med['type'], 'latte')
		self.assertEquals(slow['order_id'], 1)
		self.assertEquals(slow['type'], 'affogato')

class TestProcessOrder(unittest.TestCase):

	def test_valid_order(self):
		b_time = 0
		barista = 1
		order = {"order_id":2, "order_time":1, "type":"affogato"}
		wait_time = 1
		profit = 10
		num_of_orders = 1
		valid, output, wait_time, profit, num_of_orders, b_time, order = vt.processOrder(b_time, barista, \
			order, wait_time, profit, num_of_orders)
		self.assertEquals(valid, True)
		self.assertEquals(output['order_id'], 2)
		self.assertEquals(output['barista_id'], 1)
		self.assertEquals(output['start_time'], 1)
		self.assertEquals(wait_time, 8)
		self.assertEquals(profit, 15)
		self.assertEquals(b_time, 8)
		self.assertEquals(order['order_id'], 2)
		self.assertEquals(order['barista_id'], 1)
		self.assertEquals(order['start_time'], 1)
		self.assertEquals(order['type'], 'affogato')

	def test_invalid_order(self):
		b_time = 99
		barista = 1
		order = {"order_id":2, "order_time":1, "type":"affogato"}
		wait_time = 1
		profit = 10
		num_of_orders = 1
		valid, output, wait_time, profit, num_of_orders, b_time, order = vt.processOrder(b_time, barista, \
			order, wait_time, profit, num_of_orders)
		self.assertEquals(valid, False)

if __name__ == '__main__':
	unittest.main()