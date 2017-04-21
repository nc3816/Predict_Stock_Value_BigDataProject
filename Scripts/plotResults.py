
from pylab import *
import csv

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
			samples.append([float(line[0]),float(line[1]),float(line[2])])

	print("  completed.\n")
	return samples


def plotSamples( samples,title):	
	'''
	receives statices and creates a plot
	'''
	x = [i for i in range(0,len(samples))]
	yTarget = [s[1] for s in samples]
	yOutput = [s[2] for s in samples]
	line, = plt.plot(x, yTarget, lw=1, label="Target")
	line, = plt.plot(x, yOutput, lw=1, label="Output")
	plt.legend()
	plt.title(" {}".format(title) )
	# plt.savefig("{} ".format(title))
	plt.show()
	return plt

def main():
	for i in range(1,11):
		samples = readData("../Results/stock_{}_days_test_score_idents.csv".format(i))
		plotSamples(samples,i)
	for i in range(1,11):
		samples = readData("../Results/stock2_{}_days_test_score_idents.csv".format(i))
		plotSamples(samples,i+10)


if __name__=="__main__":
	main()