# importing modules 
import csv 
import numpy as np
from matplotlib import pyplot as plt
import statistics
import math
from scipy.special import gamma
from scipy.integrate import dblquad
from scipy import integrate
from datetime import datetime as dt


# Importiamo i dati del primo asset dal file TXT

filename = "Titoli_txt/AAPL.txt"
fil = filename.split('/')
filename1 = 's' + fil[1]
titles1 = []
rows1 = []

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows1.append(currentline)
  
# txt file name 
filename = "Titoli_txt/GE.txt"
fil = filename.split('/')
filename2 = 's' + fil[1]

# initializing the titles and rows list 
titles2 = [] 
rows2 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows2.append(currentline)

i = 0
j = 0
row1 = []
row2 = []
while i < len(rows1) and j < len(rows2):
	a = dt.strptime(str(rows1[i][0])+":"+str(rows1[i][1]), "%m/%d/%Y:%H:%M")
	b = dt.strptime(str(rows2[j][0])+":"+str(rows2[j][1]), "%m/%d/%Y:%H:%M")
	if a == b:
		row1.append(rows1[i])
		row2.append(rows2[j])
		print "added" + str(a)
		i = i+1
		j = j+1
		if i < len(rows1):
			a = dt.strptime(str(rows1[i][0])+":"+str(rows1[i][1]), "%m/%d/%Y:%H:%M")
		if j < len(rows2):
			b = dt.strptime(str(rows2[j][0])+":"+str(rows2[j][1]), "%m/%d/%Y:%H:%M")
	while a < b and i < len(rows1):
		i=i+1
		if i < len(rows1):
			a = dt.strptime(str(rows1[i][0])+":"+str(rows1[i][1]), "%m/%d/%Y:%H:%M")
	while b < a and j < len(rows2):
		j=j+1
		if j < len(rows2):
			b = dt.strptime(str(rows2[j][0])+":"+str(rows2[j][1]), "%m/%d/%Y:%H:%M")

print "done"

file = open(filename1, "w")
for i in range(0,len(row1)):
	file.write(str(row1[i][0])+','+str(row1[i][1])+','+str(row1[i][2])+','+str(row1[i][3])+','+str(row1[i][4])+','+str(row1[i][5])+','+str(row1[i][6]))

file.close()

file = open(filename2, "w")
for i in range(0,len(row2)):
	file.write(str(row2[i][0])+','+str(row2[i][1])+','+str(row2[i][2])+','+str(row2[i][3])+','+str(row2[i][4])+','+str(row2[i][5])+','+str(row2[i][6]))
	
file.close()
