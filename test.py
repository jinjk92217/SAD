#!/bin/python

import os

r = 50
l = 1000
e = 0.0001
a = 28.0
k = 0.1

# for _r in range(50,301,50):
# 	for seed in [1,3,119,1000,24000]:
# 		cmd = "python ./Main.py PRAAG " + str(_r) + " " + str(l) + " " + str(e) + " " +  str(a) + " " + str(k) +" " + str(seed)
# 		os.system(cmd)


# for _l in range(500,3001,500):
# 	for seed in [1,3,119,1000,24000]:
# 		cmd = "python ./Main.py PRAAG " + str(r) + " " + str(_l) + " " + str(e) + " " +  str(a) + " " + str(k) +" " + str(seed)
# 		os.system(cmd)


# for _a in range(20,51,10):
# 	for seed in [1,3,119,1000,24000]:
# 		cmd = "python ./Main.py PRAAG " + str(r) + " " + str(l) + " " + str(e) + " " +  str(_a) + " " + str(k) +" " + str(seed)
# 		os.system(cmd)


# for _k in range(0,21,5):
# 	_k = _k*1.0/100
# 	for seed in [1,3,119,1000,24000]:
# 		cmd = "python ./Main.py PRAAG " + str(r) + " " + str(l) + " " + str(e) + " " +  str(a) + " " + str(_k) +" " + str(seed)
# 		os.system(cmd)						


for seed in [1,3,119,1000,24000]:
	cmd = "python ./Main.py PRAAG " + str(r) + " " + str(l) + " " + str(e) + " " +  str(a) + " " + str(k) +" " + str(seed)
	os.system(cmd)						


# for seed in [1,3,119,1000,24000]:
# 	cmd = "python ./Main.py CUSUM " + str(seed)
# 	os.system(cmd)						


