import csv
import pickle
import math
from pylab import *
import numpy as np
def readData2(filename):
	"""Read in samples of a training represented one per line,""" 
	print("Loading Data: " + str(filename) )
	samples = []

	with open(filename,'r') as testfile:
		csv_reader = csv.reader(testfile)
		skip = True
		for line in csv_reader:
			if(skip):
				skip = False
				continue
			else:
				# print(line)
				if len(line)>0:
					samples.append([[float(l) for l in line[:-1]],float(line[-1])])

	print("  completed.\n")
	return samples

def readData(filename):
	"""Read in samples of a training represented one per line,""" 
	print("Loading Data: " + str(filename) )
	samples = []

	with open(filename,'r') as testfile:
		csv_reader = csv.reader(testfile)
		skip = True
		for line in csv_reader:
			if(skip):
				skip = False
				continue
			else:
				# print(line)
				if len(line)>0:
					samples.append([[float(line[0]),float(line[1]),float(line[2])],float(line[3])])

	print("  completed.\n")
	return samples

def plot(lines,title,xlabel,ylabel):	
	'''
	receives statices and creates a plot
	'''
	x = [i for i in range(0,len(lines[0]))]
	i = 0
	for l in lines:
		line, = plt.plot(x, l, lw=2, label=title[i])
		i += 1
	#line, = plt.plot(x, actual, lw=1, label="Real Stock Price")

	plt.legend(bbox_to_anchor=(1,0.2))
	plt.title("Stock Price Predictino using RNN")
	#plt.savefig()
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.show()


def NormalizetheData(data):
	mean = 0.0
	stdev = 0.0
	newdata = []
	total = [0.0, 0.0, 0.0, 0.0]
	mean = [0.0, 0.0, 0.0, 0.0]
	stdev = [0.0, 0.0, 0.0, 0.0]
	for i in data:
		inp = i[0]
		o = i[1]
		# print(i)
		# print(inp[0])
		total[0] += inp[0]
		total[1] += inp[1]
		total[2] += inp[2]
		total[3] += o
	mean[0] = total[0]/len(data)
	mean[1] = total[1]/len(data)
	mean[2] = total[2]/len(data)
	mean[3] = total[3]/len(data)

	for i in data:
		inp = i[0]
		o = i[1]
		stdev[0] += math.pow(inp[0]-mean[0],2)
		stdev[1] += math.pow(inp[1]-mean[1],2)
		stdev[2] += math.pow(inp[2]-mean[2],2)
		stdev[3] += math.pow(o-mean[3],2)
	stdev[0] = math.sqrt(stdev[0]/4)
	stdev[1] = math.sqrt(stdev[1]/4)
	stdev[2] = math.sqrt(stdev[2]/4)
	stdev[3] = math.sqrt(stdev[3]/4)
	for i in data:
		inp = i[0]
		o = i[1]
		temp = []
		temp.append((inp[0]-mean[0])/stdev[0])
		temp.append((inp[1]-mean[1])/stdev[1])
		temp.append((inp[2]-mean[2])/stdev[2])
		temp.append((o-mean[3])/stdev[3])
		newdata.append(temp)
	return newdata,mean,stdev
def NormalizetheData2(data):
	# print("File to be normalized : {}".format(data))
	mean = 0.0
	stdev = 0.0
	newdata = []
	print(data[0])
	total = [0.0 for i in data[0][0]]
	mean = [0.0 for i in data[0][0]]
	stdev = [0.0 for i in data[0][0]]
	print(len(total))
	for i in data:
		inp = i[0]
		o = i[1]
		# print(i)
		# print(inp[0])
		for j in range (0,len(inp)):
			total[j] += inp[j]
		total[-1] += o

	for j in range(0,len(inp)):
		mean[j] = total[j]/len(data)
	mean[-1] = total[-1]/len(data)

	for i in data:
		inp = i[0]
		o = i[1]
		for j in range(0,len(inp)):
			stdev[j] += math.pow(inp[j]-mean[j],2)
		stdev[-1] += math.pow(o-mean[-1],2)
	for j in range(0,len(inp)):
		stdev[j] = math.sqrt(stdev[j]/13)
	
	for i in data:
		inp = i[0]
		o = i[1]
		temp = []
		for j in range(0,len(inp)):
			temp.append((inp[j]-mean[j])/stdev[j])
		temp.append((o-mean[-1])/stdev[-1])
		newdata.append(temp)
	return newdata,mean,stdev
# data = readData('../Data/data_1_days.csv')
# # print(data[1])
# data2,a,b = NormalizetheData(data)
# print("normalized")
# with open("../Data/data_1_days_norm.csv", "w") as f:
# 		    writer = csv.writer(f)
# 		    writer.writerows(data2)
# print(data2)
# ds = SupervisedDataSet(3,1)
# testds = SupervisedDataSet(3,1)
# tf = open('data_6_days.csv','r')

# for line in tf.readlines():
# 	data = [float(x) for x in line.strip().split(',') if x != '']
# 	indata =  tuple(data[:3])
# 	outdata = tuple(data[3:])
# 	ds.addSample(indata,outdata)
	
# training = SupervisedDataSet(3,1)
# testing = SupervisedDataSet(3,1)
# i = 0
# normdata,mean,stdev = NormalizetheData(list(ds))
# print(mean)
# print(stdev)
# for d in normdata:
# 	i += 1
# 	if (i <=633):
# 		training.addSample(tuple(d[:3]),tuple(d[3:]))
# 	else:
# 		testing.addSample(tuple(d[:3]),tuple(d[3:]))

# n = buildNetwork(training.indim,10,10,training.outdim,recurrent=True)
# t = BackpropTrainer(n,dataset=training,learningrate=0.005,momentum=0.005,verbose=True)
# Error = []
# # t.trainOnDataset(training,1000)
# # t.testOnData(verbose=True)
# for i in range(10000):
# 	print("Epoch : "+str(i))
# 	Error.append( t.train() )
# with open("RNN_Model", 'w') as modelFile:
# 	pickle.dump(n, modelFile)
# with open("RNN_Trainer", 'w') as modelFile:
# 	pickle.dump(t, modelFile)

# # print("##############")
# # with open("RNN_Model") as modelfile:
# # 	n = pickle.load(modelfile)
# # with open("RNN_Trainer") as modelfile:
# # 	t = pickle.load(modelfile)
# # print(len(testing))
# actual = []
# output = []
# for i in testing :
# 	#print(i)
# 	#data = [float(x) for x in i.strip().split(',') if x != '']
# 	#print(i[0])
# 	predicted = n.activate(i[0])
# 	print(predicted*stdev[3]+mean[3])
# 	print("Correct : {}".format(i[1]*stdev[3]+mean[3]))
# 	actual.append(i[1]*stdev[3]+mean[3])
# 	output.append(predicted*stdev[3]+mean[3])
# plot([actual,output],["Actual Stock Price","Predicited Stock Price"],"Prediciton day","Stock Price")
# plot([Error],["Error"],"Epoch","Total Error")
