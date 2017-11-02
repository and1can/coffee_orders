import metric
import unittest

class TestMetricCalc(unittest.TestCase):

	def test_no_tea_one_latte_and_two_affogatos(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait, \
		tea_percent_comp, latte_percent_comp, affogato_percent_comp \
		 = metric.metricCalc('metric_tests/metric_test1', 'metric_tests/metric_input1')
		self.assertEquals(tea_avg_wait, 0)
		self.assertEquals(latte_avg_wait, 4)
		self.assertEquals(affogato_avg_wait, 17/float(2))
		self.assertEquals(tea_percent_comp, 0)
		self.assertEquals(latte_percent_comp, 1)
		self.assertEquals(affogato_percent_comp, 1)
		
	def test_no_latte_one_affogato_and_two_teas(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait, \
		tea_percent_comp, latte_percent_comp, affogato_percent_comp \
		= metric.metricCalc('metric_tests/metric_test2','metric_tests/metric_input2')
		self.assertEquals(tea_avg_wait, 9/float(2))
		self.assertEquals(latte_avg_wait, 0)
		self.assertEquals(affogato_avg_wait, 7)
		self.assertEquals(tea_percent_comp, 1)
		self.assertEquals(latte_percent_comp, 0)
		self.assertEquals(affogato_percent_comp, 1)

	def test_no_affogato_one_tea_and_two_lattes(self):
		tea_avg_wait, latte_avg_wait, affogato_avg_wait, \
		tea_percent_comp, latte_percent_comp, affogato_percent_comp \
		= metric.metricCalc('metric_tests/metric_test3' ,'metric_tests/metric_input3')
		self.assertEquals(tea_avg_wait, 6)
		self.assertEquals(latte_avg_wait, 4)
		self.assertEquals(affogato_avg_wait, 0)
		self.assertEquals(tea_percent_comp, 1)
		self.assertEquals(latte_percent_comp, 1)
		self.assertEquals(affogato_percent_comp, 0)




if __name__ == '__main__':
	unittest.main()
