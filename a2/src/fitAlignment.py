#!/usr/bin/env python

import sys

if (len(sys.argv) != 2):
	sys.exit();

fastaFile = sys.argv[1]
sequenceA = ''
sequenceB = ''
sequenceScanned = 0

# open file and save sequences
with open(fastaFile, 'r') as file:
	for line in file:
		if (line.strip().startswith(">")):
			if (sequenceScanned == 0):
				sequenceScanned = 1
			elif (sequenceScanned == 1):
				sequenceScanned = 2
		elif (line.strip()):
			cleanedLine = line.strip().rstrip("\r\n").replace(" ","")
			if (sequenceScanned == 1):
				sequenceA += cleanedLine
			elif (sequenceScanned == 2):
				sequenceB += cleanedLine
			

m = 1
mm = -1
id = -1

# create matrices
lengthA = len(sequenceA)
lengthB = len(sequenceB)

# had to +1 since [0,0] is empty (well 0)
M = []
for i in xrange(0,lengthA+1):
	column = []
	for j in xrange(0,lengthB+1):
		column.append(0)
	M.append(column)
 
# find values for matrices
for i in xrange(1, lengthA+1):
	for j in xrange(1, lengthB+1):
		isMatch = -1
		if (sequenceA[i-1] == sequenceB[j-1]):
			isMatch = 1
		M[i][j] = max([M[i-1][j-1] + isMatch, M[i-1][j] -1, M[i][j-1] - 1])

# get location of max score end
maxI = lengthA
maxJ = max(M[lengthA])
for i in xrange(0,lengthB+1):
	if (M[lengthA][i] == maxJ):
		maxJ = i
		break

S = ""
T = ""

currI = maxI
currJ = maxJ

while (currI > 0 and currJ > 0):
	isMatch = -1
	if (sequenceA[currI-1] == sequenceB[currJ-1]):
		isMatch = 1

	if (M[currI][currJ] == M[currI - 1][currJ] -1):
		S = str(sequenceA[currI-1]) + S
		T = "-" + T
		currI -= 1
	elif (M[currI][currJ] == M[currI][currJ-1] - 1):
		S = "-" + S
		T = str(sequenceB[currJ-1]) + T
		currJ -= 1
	else:
		S = str(sequenceA[currI-1]) + S
		T = str(sequenceB[currJ-1]) + T
		currI -= 1
		currJ -= 1

print(M[maxI][maxJ])
print(S)
print(T)
