import json
import unittest


def metricCalc(file_name):
	tea_count = 0
	latte_count = 0
	affogato_count = 0
	tea_wait_time = 0
	latte_wait_time = 0
	affogato_wait_time = 0

	tea_avg_wait = 0
	latte_avg_wait = 0
	affogato_avg_wait = 0

	with open(file_name + '.json') as data_file:
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
	return (tea_avg_wait, latte_avg_wait, affogato_avg_wait)


class TestMetricCalc(unittest.TestCase):

	def test_no_tea_one_latte_and_two_affogatos(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait = metricCalc('metric_tests/metric_test1')
		self.assertEquals(tea_avg_wait, 0)
		self.assertEquals(latte_avg_wait, 4)
		self.assertEquals(affogato_avg_wait, 17/float(2))
		
	def test_no_latte_one_affogato_and_two_teas(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait = metricCalc('metric_tests/metric_test2')
		self.assertEquals(tea_avg_wait, 9/float(2))
		self.assertEquals(latte_avg_wait, 0)
		self.assertEquals(affogato_avg_wait, 7)

	def test_no_affogato_one_tea_and_two_lattes(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait = metricCalc('metric_tests/metric_test3')
		self.assertEquals(tea_avg_wait, 6)
		self.assertEquals(latte_avg_wait, 4)
		self.assertEquals(affogato_avg_wait, 0)

if __name__ == '__main__':
	#unittest.main()

	print('fifo metric: ')
	print(metricCalc('fifo_metric_output'))