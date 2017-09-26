import os
import filecmp
import math

def getData(filename):
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys will come from the first row in the data.

#Note: The column headings will not change from the
#test cases below, but the the data itself will
#change (contents and size) in the different test
#cases.

	myFile = open(filename, 'r')
	keys = myFile.readline().strip().split(",")
	theDataList = []

	for element in myFile.readlines():
		dataDict = {}
		dataList = element.strip().split(",")
		index = 0
		for key in keys:
			dataDict[key] = dataList[index]
			index += 1
		theDataList.append(dataDict)

	return theDataList

#Sort based on key/column
def mySort(data,col):
#Input: list of dictionaries
#Output: Return a string of the form firstName lastName
	sortedList = sorted(data, key = lambda k: k[col])
	return sortedList[0]['First'] + " " + sortedList[0]['Last']

#Create a histogram
def classSizes(data):
# Input: list of dictionaries
# Output: Return a list of tuples ordered by
# ClassName and Class size, e.g
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]

	snrCount = 0
	jnrCount = 0
	sophCount = 0
	freshCount = 0
	countlist = []

	for element in data:
		if element['Class'] == 'Senior':
			snrCount += 1
		elif element['Class'] == 'Junior':
			jnrCount += 1
		elif element['Class'] == 'Sophomore':
			sophCount += 1
		elif element['Class'] == 'Freshman':
			freshCount += 1
	countlist.append(("Senior", snrCount))
	countlist.append(("Junior", jnrCount))
	countlist.append(("Sophomore", sophCount))
	countlist.append(("Freshman", freshCount))

	return sorted(countlist, reverse = True, key = lambda k: k[1])

# Find the most common day of the year to be born
def findDay(a):
# Input: list of dictionaries
# Output: Return the day of month (1-31) that is the
# most often seen in the DOB

	DOBdict = {}
	valueList = []
	for element in a:
		dayOfMonth = element['DOB'].split('/')[1]
		if dayOfMonth not in DOBdict.keys():
			DOBdict[dayOfMonth] = 1
		else:
			DOBdict[dayOfMonth] += 1
	return int(sorted(DOBdict, reverse = True, key = DOBdict.get)[0])

# Find the average age (rounded) of the Students
def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of students rounded
# to nearest integer

	ages = []
	birthDates = []
	currentDate = [9, 30, 2017]
	age = 0

	# gather data in list of lists (int form)
	for person in a:
		temp = []
		for item in person['DOB'].split('/'):
			temp.append(int(item))
		birthDates.append(temp)

	# calculate each age and put ages in list 'ages'
	for birthdate in birthDates:
		# year hasn't happened yet
		if birthdate[2] > currentDate[2]:
			age = 0
		# year is this year
		elif birthdate[2] == currentDate[2]:
			# month hasn't happened yet
			if birthdate[0] > currentDate[0]:
				age = 0
			else:
				# day hasn't happened yet
				if birthdate[1] > currentDate[1]:
					age = 0
				else:
					age = 1
		# year is in the past
		elif birthdate[2] < currentDate[2]:
			# birthday month hasn't happened this year yet
			if birthdate[0] > currentDate[0]:
				age = currentDate[2] - birthdate[2]	+ 1
			# birthday is happening this month
			elif birthdate[0] == currentDate[0]:
				# birthday day hasn't happened this year yet
				if birthdate[1] > currentDate[1]:
					age = currentDate[2] - birthdate[2]	+ 1
				# birthday day is today or already happened
				elif birthdate[1] <= currentDate[1]:
					age = currentDate[2] - birthdate[2]
		ages.append(age)

	return int(sum(ages) / len(ages))

#Similar to mySort, but instead of returning single
#Student, all of the sorted data is saved to a csv file.
def mySortPrint(a,col,fileName):
#Input: list of dictionaries, key to sort by and output file name
#Output: None

	csv = open(fileName, 'w')

	sortedList = sorted(a, key = lambda k: k[col])
	for element in sortedList:
		temp = []
		for value in element.values():
			temp.append(value)
		row = ",".join(temp[:3])
		csv.write(row + "\n")

	csv.close()
	return None


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ",end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),40)
	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',15)
	total += test(mySort(data2,'First'),'Adam Rocha',15)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',15)
	total += test(mySort(data2,'Last'),'Elijah Adams',15)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',15)
	total += test(mySort(data2,'Email'),'Orli Humphrey',15)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],10)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],10)

	print("\nThe most common day of the year to be born is:")
	total += test(findDay(data),13,10)
	total += test(findDay(data2),26,10)

	print("\nThe average age is:")
	total += test(findAge(data),39,10)
	total += test(findAge(data2),41,10)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,10)


	print("Your final score is: ",total)
# Standard boilerplate to call the main() function that tests all your code.
if __name__ == '__main__':
    main()
