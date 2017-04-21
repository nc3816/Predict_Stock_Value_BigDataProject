import mysql.connector
import csv
from mysql.connector import errorcode
import sys
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
def getCompanies():
	l = []
	try:
		cnx = connect("root","rasa","project_database")
		cursor = cnx.cursor()
		
		cursor.execute("Select * from companies ")
		row = cursor.fetchone()
		while row is not None :
			l.append(row[1])
			row = cursor.fetchone()
		cnx.commit()
	except mysql.connector.Error as err:
		print(err.msg)
		print("----")

	return l
def add_company(company):
	cnx = connect("root","rasa","project_database")
	try:
		print("Inserting new Company : {}".format(company))
		print("INSERT INTO `project_database`.`companies` (`c_name`) VALUES ('{}')\
".format(\
				company))
		cursor = cnx.cursor()

		cursor.execute("INSERT INTO `project_database`.`companies` (`c_name`) VALUES ('{}')\
".format(\
				company))

		cnx.commit()


		#ID = ??????



	except mysql.connector.Error as err:
		print(err.msg)
		print("----")

		return None

def add_data_to_Company(company,samples):
	company = getCompanyID(company)
	cnx = connect("root","rasa","project_database")
	try:
		print("Insert Data to Table : {}".format(company))
		cursor = cnx.cursor()
		for s in samples:
			# print(s)
			# print("####")
			cursor.execute("INSERT INTO historic_data(\
				`c_id`,`open`,`high`,`low`,`close`,`volume`,`adj_close`) \
				Values({},'{}','{}','{}','{}','{}','{}')".format(\
					company,s[0],s[1],s[2],s[3],s[4],s[5]))

		cnx.commit()
	except mysql.connector.Error as err:
		print(err.msg)
		print("----")
def getCompanyID(company):
	try:
		cnx = connect("root","rasa","project_database")
		cursor = cnx.cursor()
		
		cursor.execute("Select c_id from companies \
			where c_name ='{}' ".format(company))
		return int(cursor.fetchone()[0])
	except mysql.connector.Error as err:
		print(err.msg)
		print("----")

def getCompanyData(company):
	l = []
	try:
		cnx = connect("root","rasa","project_database")
		cursor = cnx.cursor()
			
		cursor.execute("Select `open`,`high`,`low`,`close`,`volume`,`adj_close` \
							from historic_data h, companies c\
							where c.c_id =h.c_id and \
							c.c_name =  '{}' ".format(company))
		row = cursor.fetchone()
		while row is not None :
			l.append([float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5])])
			row = cursor.fetchone()
		cnx.commit()
	except mysql.connector.Error as err:
		print(err.msg)
		print("----")

	return l

	
def connect(user,psw,db):
	cnx = False
	try:
		cnx = mysql.connector.connect(user=user,\
	                                database=db,
	                                password = psw,\
	                                host = '127.0.0.1')	
	except mysql.connector.Error as err:
		print(err.msg)
		print("----")
	return cnx

if __name__ == '__main__':
	#cnx = connect('root','rasa','project_database')
	# da = readData('../Data/Apple.csv')
	# print(da[0])
	# add_data_to_Company(3,da)
	# print(getCompanies())	
	#print(getCompanyData('facebook'))
	print(getCompanyID('Google'))