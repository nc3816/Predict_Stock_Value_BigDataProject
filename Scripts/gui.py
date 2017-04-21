import numpy as np
import scipy as sp
from pandas import *
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com
import rpy2.interactive as r
import csv
import rpy2.robjects.numpy2ri as rpyn
import Normalization as norm
import plotResults as plt
# def readData(filename):
# 	"""Read in samples of a training represented one per line,""" 
# 	print("Loading Data: " + filename) 
# 	samples = []

# 	with open(filename,'r') as testfile:
# 		csv_reader = csv.reader(testfile)
# 		skip = True
# 		for line in csv_reader:
# 			if(skip):
# 				skip = False
# 				continue
# 			if(len(line)!=0):
# 				samples.append([float(line[0]),float(line[1]),float(line[2]),float(line[3])])

# 	print("  completed.\n")
# 	return samples
def readData(filename,model):
	if(model == 2):
		print("model {}".format(model))
		data = norm.readData2(filename)
		data,mean,std = norm.NormalizetheData2(data)

	else :
		print("model = 1")
		data = norm.readData(filename)
		data,mean,std = norm.NormalizetheData(data)
	print(filename)
	print("-----")
	# print("columns top be normalized : {}".format(len(data[0][0])))
	slash = filename.rfind('/')
	ext = filename.rfind('.')
	normfile = filename[slash+1:ext] + "_norm.csv"
	# print("Normalized File : {}".format(normfile))
	with open("../Data/{}".format(normfile), "w") as f:
		    writer = csv.writer(f)
		    writer.writerows(data)
	return data,mean,std


def trainAmodel2(filename):
	# print("File `to be trained : {}".format(filename))
	utils = importr('utils')
	importr('neuralnet')
	ro.r('train <- read.csv(file="'+filename+'",head=FALSE,sep=",")')
	ro.r('colnames(train)<-c("a1","a2","a3","a4","a5","a6","a7","a8","a9","a10","a11","a12","a13")')
	ro.r('a <- train[0:12]')
	ro.r('index <- floor(0.9 * nrow(train))')
	ro.r('set.seed(123)')
	ro.r('trainindex <- sample(seq_len(nrow(train)),size = index)')
	ro.r('testset <- train[-trainindex,]')
	ro.r('test <- tail(train,n=1)')
	ro.r('ts <- testset[0:12]')
	ro.r('print(nrow(ts))')
	# ro.r('print(outp)')
	# ro.r('OR <- c(0,rep(1,7))')
	# ro.r('binary.data <- data.frame(expand.grid(c(0,1), c(0,1), c(0,1)), AND, OR)')
	net = ro.r('net <- neuralnet(a13~a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12,\
							data=train,\
							hidden=c(25),\
							rep = 100,\
							threshold = 0.001,\
							err.fct="sse",\
							linear.output=T)')
	return net

def trainAmodel(filename):
	utils = importr('utils')
	importr('neuralnet')
	ro.r('train <- read.csv(file="'+filename+'",head=FALSE,sep=",")')
	ro.r('colnames(train)<-c("a1","a2","a3","a4")')
	ro.r('a <- train[0:3]')
	ro.r('index <- floor(0.9 * nrow(train))')
	ro.r('set.seed(123)')
	ro.r('trainindex <- sample(seq_len(nrow(train)),size = index)')
	ro.r('testset <- train[-trainindex,]')
	ro.r('test <- tail(train,n=1)')
	ro.r('ts <- testset[0:3]')
	ro.r('print(nrow(ts))')
	# ro.r('print(outp)')
	# ro.r('OR <- c(0,rep(1,7))')
	# ro.r('binary.data <- data.frame(expand.grid(c(0,1), c(0,1), c(0,1)), AND, OR)')
	net = ro.r('net <- neuralnet(a4~a1+a2+a3,\
							data=train,\
							hidden=c(10),\
							rep = 100,\
							threshold = 0.001,\
							err.fct="sse",\
							linear.output=T)')
	return net
def PredictTomorrow(mean,stdev):
	ro.r('nn <- compute(net,ts)')
	ro.r('result <- data.frame(actual = testset$a4,prediction = nn$net.result)')
	rs = ro.r('result')
	rs2 = np.asarray(rs)
	actual = rs2[0]
	output = rs2[1]
	graph = []
	for i in range(0,len(actual)):
		#for j in i:
		# print("---{}---{}".format(actual[i]*stdev[-1]+mean[-1],output[i]*stdev[-1]+mean[-1]))
		graph.append([i,actual[i]*stdev[-1]+mean[-1],output[i]*stdev[-1]+mean[-1]])

	# Predicting Tomorrow
	ro.r('nn <- compute(net,test[0:3])')
	rs = ro.r('result <- data.frame(actual = test$a4,prediction = nn$net.result)')
	rs = ro.r('result')
	rs2 = np.asarray(rs)
	actual = rs2[0]
	output = rs2[1]
	for i in range(0,len(actual)):
		#for j in i:
		print("---{}---{}".format(actual[i]*stdev[-1]+mean[-1],output[i]*stdev[-1]+mean[-1]))
		return output[i]*stdev[-1]+mean[-1],graph
def PredictTomorrow2(mean,stdev):
	ro.r('nn <- compute(net,ts)')
	ro.r('result <- data.frame(actual = testset$a13,prediction = nn$net.result)')
	rs = ro.r('result')
	rs2 = np.asarray(rs)
	actual = rs2[0]
	output = rs2[1]
	graph = []
	for i in range(0,len(actual)):
		#for j in i:
		# print("---{}---{}".format(actual[i]*stdev[-1]+mean[-1],output[i]*stdev[-1]+mean[-1]))
		graph.append([i,actual[i]*stdev[-1]+mean[-1],output[i]*stdev[-1]+mean[-1]])

	# Predicting Tomorrow
	ro.r('nn <- compute(net,test[0:12])')
	rs = ro.r('result <- data.frame(actual = test$a13,prediction = nn$net.result)')
	rs = ro.r('result')
	rs2 = np.asarray(rs)
	actual = rs2[0]
	output = rs2[1]
	for i in range(0,len(actual)):
		#for j in i:
		print("---{}---{}".format(actual[i]*stdev[-1]+mean[-1],output[i]*stdev[-1]+mean[-1]))
		return output[i]*stdev[-1]+mean[-1],graph
def checkRequirement():
	ro.r('if(length(setdiff("neuralnet",rownames(installed.packages())))) { \
						install.packages("neuralnet") }')
def mainFunction(filePath,model):
	print("model : {}".format(model))
	print("FILE : {}".format(filePath))
	if model == 2:
		print("callpredict2")
		data,mean,stdev = readData(filePath,model)
		checkRequirement()
		ext = filePath.rfind('.')
		normfile = filePath[:ext] + "_norm.csv"

		net = trainAmodel2(normfile)
		tomorrow,graph = PredictTomorrow2(mean,stdev)
		print("Tomorrow's Price will be : {}".format(tomorrow))
		plt.plotSamples(graph,'Performance of the model on the Loaded Data')
		return tomorrow
	else :
		print("call predict 1")
		data,mean,stdev = readData(filePath,model)
		checkRequirement()
		ext = filePath.rfind('.')
		normfile = filePath[:ext] + "_norm.csv"

		net = trainAmodel(normfile)
		tomorrow,graph = PredictTomorrow(mean,stdev)
		print("Tomorrow's Price will be : {}".format(tomorrow))
		plt.plotSamples(graph,'Performance of the model on the Loaded Data')
		return tomorrow



def main():
	mainFunction('../Data/data_1_days.csv')
	# utils.install_packages('DirichletReg')
	# utils.install_packages('neuralnet')
	# print("Main")
	# ro.r('x=c()')
	# ro.r('x[1]=22')
	# ro.r('x[2]=44')
	# print(ro.r('x'))
	# #[1] 22 44
	# print(ro.r['x'])
	# #[1] 22 44

if __name__ == '__main__' :
	main()
