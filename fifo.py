import json
import unittest
from pprint import pprint

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
    
#key is the type of drink
#value is tuple
#0th tuple value is brew time
#1st tuple value is profit
drink_map = dict([("tea", [3, 2]), ("latte", [4, 3]), ("affogato", [7, 5])])

retdata = []
b1_time = 0
b2_time = 0

with open('input.json') as data_file:
    data = json.load(data_file)

for i in range(len(data)):
    curr = data[i]
    barista = getBarista(b1_time, b2_time)
    
    if (barista == 1):
        processResult = baristaProcess(curr, barista, b1_time)
        b1_time = processResult[0]
        retdata.append(processResult[1])
    else: 
        processResult = baristaProcess(curr, barista, b2_time)
        b2_time = processResult[0]
        retdata.append(processResult[1])
    
with open('output_fifo.json', 'w') as outfile:
    json.dump(retdata, outfile, indent = 4, sort_keys=True, separators=(',', ':'))


class TestBaristaChosen(unittest.TestCase):
    
    #when both baristas are available, barista 1 is chosen
    def test_barista1chosen(self):
        self.assertEqual(getBarista(0, 0), 1)

    #when barista 1 is available before barista 2, barista 1 is chosen
    def test_barista1chosen(self):
        self.assertEqual(getBarista(0, 1), 1)

    #when barista 2 is available before barista 1, barista 2 is chosen
    def test_barista1chosen(self):
        self.assertEqual(getBarista(1, 0), 2)

class TestDrinkMap(unittest.TestCase):
    
    def test_tea(self):
        self.assertEqual(drink_map['tea'], [3, 2])
    
    def test_latte(self):
        self.assertEqual(drink_map['latte'], [4, 3])

    def test_affogato(self):
        self.assertEqual(drink_map['affogato'], [7, 5])

class TestStartTime(unittest.TestCase):
    
    def test_bIsBigger(self):
        self.assertEqual(getStartTime(0, 1), 1)

    def test_bIsSmaller(self):
        self.assertEqual(getStartTime(1, 0), 1)

class TestIncrementTime(unittest.TestCase):
    
    def test_tea(self):
        self.assertEqual(incrementTime(0, 'tea'), 3)

    def test_latte(self):
        self.assertEqual(incrementTime(0, 'latte'), 4)

    def test_affogato(self):
        self.assertEqual(incrementTime(0, 'affogato'), 7)

if __name__ == '__main__':
    unittest.main()
