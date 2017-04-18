import os 
import timeit

for lambdaval in range(0,85,5):
	for hidden in range(30,80,10):
		print(lambdaval,hidden)
		os.system("python nnScript.py %s %s"%(str(lambdaval),str(hidden)))
