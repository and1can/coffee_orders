import json
import unittest
from fifo import simulateCafeDay
from optimized import optimize
import matplotlib.pylab as plt


def metricCalc(file_name, input_name):
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

	with open(input_name + '.json') as data_file:
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
	
	

	plt.bar(orders_map.keys(), orders_map.values())
	plt.show()

	tea_percent_comp = 0
	latte_percent_comp = 0
	affogato_percent_comp = 0
	
	print('tea_comp: ', tea_count, 'latte_comp: ', latte_count, 'affogato_comp: ', affogato_count)
	#calculate the average percentage of orders completed fore ach
	#type of drink. also make sure not to divide by zero 
	if (tea_total != 0):
		tea_percent_comp = tea_count / float(tea_total)
	
	if (latte_total != 0):
		latte_percent_comp = latte_count / float(latte_total)

	if (affogato_total != 0):
		affogato_percent_comp = affogato_count / float(affogato_total)

	print('tea_total: ', tea_total, 'latte_total: ', latte_total, 'affogato_total', affogato_total)

	return (tea_avg_wait, latte_avg_wait, affogato_avg_wait, tea_percent_comp, \
		latte_percent_comp, affogato_percent_comp)



class TestMetricCalc(unittest.TestCase):

	def test_no_tea_one_latte_and_two_affogatos(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait, \
		tea_percent_comp, latte_percent_comp, affogato_percent_comp \
		 = metricCalc('fifo_solution/metric_tests/metric_test1', 'fifo_solution/metric_tests/metric_input1')
		self.assertEquals(tea_avg_wait, 0)
		self.assertEquals(latte_avg_wait, 4)
		self.assertEquals(affogato_avg_wait, 17/float(2))
		self.assertEquals(tea_percent_comp, 0)
		self.assertEquals(latte_percent_comp, 1)
		self.assertEquals(affogato_percent_comp, 1)
		
	def test_no_latte_one_affogato_and_two_teas(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait, \
		tea_percent_comp, latte_percent_comp, affogato_percent_comp \
		= metricCalc('fifo_solution/metric_tests/metric_test2','fifo_solution/metric_tests/metric_input2')
		self.assertEquals(tea_avg_wait, 9/float(2))
		self.assertEquals(latte_avg_wait, 0)
		self.assertEquals(affogato_avg_wait, 7)
		self.assertEquals(tea_percent_comp, 1)
		self.assertEquals(latte_percent_comp, 0)
		self.assertEquals(affogato_percent_comp, 1)

	def test_no_affogato_one_tea_and_two_lattes(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait, \
		tea_percent_comp, latte_percent_comp, affogato_percent_comp \
		= metricCalc('fifo_solution/metric_tests/metric_test3' ,'fifo_solution/metric_tests/metric_input3')
		self.assertEquals(tea_avg_wait, 6)
		self.assertEquals(latte_avg_wait, 4)
		self.assertEquals(affogato_avg_wait, 0)
		self.assertEquals(tea_percent_comp, 1)
		self.assertEquals(latte_percent_comp, 1)
		self.assertEquals(affogato_percent_comp, 0)




if __name__ == '__main__':
	#unittest.main()

	print('simulation Fifo')
	print(simulateCafeDay('poisson_mean_50_47_samples_equal_prob_types_of_drinks'))
	print('fifo metric: ')
	print(metricCalc('fifo_metric_output', 'input'))
	print('simulation Optimized')
	print(optimize('input'))
	print('optimized metric: ')
	print(metricCalc('optimized_metric_output', 'input'))

