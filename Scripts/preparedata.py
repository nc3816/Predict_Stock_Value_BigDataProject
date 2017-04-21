import csv
from pylab import *
import numpy as np
import DB_Activities as db
def readData(filename):
	"""Read in samples of a training represented one per line,""" 
	print("Loading Data: " + filename) 
	samples = []

	with open(filename,'r') as testfile:
		csv_reader = csv.reader(testfile)
		skip = True
		for line in csv_reader:
			if(skip):
				skip = False
				continue
			samples.append([float(line[1]),float(line[2]),float(line[3]),float(line[4]),float(line[5]),float(line[6])])

	print("  completed.\n")

	return samples
	
def readDataDB(company):
	samples = db.getCompanyData(company)
	return samples


def generateData(samples,d):
	"""
	This function creates data set for the stock market. It finds average, minimum and maximum
	price in the last d days and average of todays prices will be the output

	:param d: specifies number of days to be used, (last d days)
	:params samples: is the data that we extract feature from

	:return : a new dataset with our new features which is 3 input one output
	:rtype: a list of list
	"""
	data = []
	for i in range(0,len(samples)-d):
		highest = float("-inf")
		lowest = float("inf")
		average = 0
		summ = 0
		for j in range(i,i+d):
			# finding the lowest price
			if (samples[j][3]<lowest):
				lowest = samples[j][3]
			# finding the highest price
			if (samples[j][2]>highest):
				highest = samples[j][2]
			# finding the lowest price
			if (samples[j][1]<lowest):
				lowest = samples[j][1]
			# finding the highest price
			if (samples[j][1]>highest):
				highest = samples[j][1]
			# finding the lowest price
			if (samples[j][2]<lowest):
				lowest = samples[j][2]
			# finding the highest price
			if (samples[j][2]>highest):
				highest = samples[j][2]
			# finding the average price 
			summ = summ + samples[j][0] + samples[j][1] + samples[j][2] + samples[j][3]
		average = summ/4.0*d
		price = (samples[i+d][0]+samples[i+1][1]+samples[i+1][2]+samples[i+1][3])/4.0
		data.append([lowest,highest,average,price])
	with open("../Data/data_"+str(d)+"_days.csv", "w") as f: #,encoding = 'utf_8',newline='') as f:
		    writer = csv.writer(f)
		    writer.writerows(data)
	return data 
def generateData2(samples,d):
	"""
	This function creates data set for the stock market. It finds average, minimum and maximum
	price in the last d days and average of todays prices will be the output

	:param d: specifies number of days to be used, (last d days)
	:params samples: is the data that we extract feature from

	:return : a new dataset with our new feates which is 3 input one output
	:rtype: a list of list
	"""
	data = []
	for i in range(0,len(samples)-d):
		
		row  = []
		for j in range(i,i+d):
			highest = float("-inf")
			lowest = float("inf")
			average = 0
			# finding the lowest price
			if (samples[j][3]<lowest):
				lowest = samples[j][3]
			# finding the highest price
			if (samples[j][2]>highest):
				highest = samples[j][2]
			# finding the lowest price
			if (samples[j][1]<lowest):
				lowest = samples[j][1]
			# finding the highest price
			if (samples[j][1]>highest):
				highest = samples[j][1]
			# finding the lowest price
			if (samples[j][2]<lowest):
				lowest = samples[j][2]
			# finding the highest price
			if (samples[j][2]>highest):
				highest = samples[j][2]
			# finding the average price 
			avg = (samples[j][0] + samples[j][1] + samples[j][2] + samples[j][3]) / 4.0
			row = np.hstack((row,[lowest,highest,avg]))
		price = (samples[i+d][0]+samples[i+d][1]+samples[i+d][2]+samples[i+d][3]) / 4.0
		data.append(np.hstack((row,price)))
	with open("../Data/data2_"+str(d)+"_days.csv", "w") as f: #,encoding = 'utf_8',newline='') as f:
			writer = csv.writer(f)
			writer.writerows(data)
	return data 


def main():
	samples = readData("../Data/data.csv")
	# creating different dataset with different value for d
	# which is using the last d days.
	for i in range(1,11):
		print(i)
		data = generateData(samples,i)
		data2 = generateData2(samples,i)
		# plotSamples(data,i)
		with open("../Data/data_"+str(i)+"_days.csv", "w") as f: #,encoding = 'utf_8',newline='') as f:
		    writer = csv.writer(f)
		    writer.writerows(data)
	    
		with open("../Data/data2_"+str(i)+"_days.csv", "w") as f: #,encoding = 'utf_8',newline='') as f:
			writer = csv.writer(f)
			writer.writerows(data2)
if __name__ == "__main__":
	main()