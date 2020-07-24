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

sigma1 = 0.001
sigma2 = 0.001
sigma3 = 0.001

# Importiamo i dati del primo asset dal file TXT

filename = "3sKO.txt"
filename1 = 'c' + filename
titles1 = []
rows1 = []

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows1.append(currentline)
  
# txt file name 
filename = "3sIBM.txt"
filename2 = 'c' + filename

# initializing the titles and rows list 
titles2 = [] 
rows2 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows2.append(currentline)
		
# txt file name 
filename = "3sGE.txt"
filename3 = 'c' + filename		

# initializing the titles and rows list 
titles3 = [] 
rows3 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows3.append(currentline)

p1 = []
p2 = []
p3 = []
p1.append(10.)
p2.append(10.)
p3.append(10.)

l1 = len(rows1)
l2 = len(rows2)
l3 = len(rows3)

mu1 = math.log(float(rows1[l1-1][5])/float(rows1[0][5]))/l1
mu2 = math.log(float(rows2[l2-1][5])/float(rows2[0][5]))/l2
mu3 = math.log(float(rows3[l3-1][5])/float(rows3[0][5]))/l3

print mu1
print mu2
print mu3

x1 = []
x2 = []
x3 = []
x1.append(math.log(p1[0]))
x2.append(math.log(p2[0]))
x3.append(math.log(p3[0]))

for i in range(1,l1):
	r1 = np.random.normal(mu1,sigma1)
	r2 = np.random.normal(mu2,sigma2)
	r3 = np.random.normal(mu3,sigma3)
	x1.append(x1[i-1]+r1)
	x2.append(x2[i-1]+r2)
	x3.append(x3[i-1]+r3)
	p1.append(math.exp(x1[i]))
	p2.append(math.exp(x2[i]))
	p3.append(math.exp(x3[i]))

file = open(filename1, "w")
for i in range(0,len(rows1)):
	file.write(str(rows1[i][0])+','+str(rows1[i][1])+','+str(rows1[i][2])+','+str(rows1[i][3])+','+str(rows1[i][4])+','+str(p1[i])+','+str(rows1[i][6]))

file.close()

file = open(filename2, "w")
for i in range(0,len(rows2)):
	file.write(str(rows2[i][0])+','+str(rows2[i][1])+','+str(rows2[i][2])+','+str(rows2[i][3])+','+str(rows2[i][4])+','+str(p2[i])+','+str(rows2[i][6]))
	
file.close()

file = open(filename3, "w")
for i in range(0,len(rows3)):
	file.write(str(rows3[i][0])+','+str(rows3[i][1])+','+str(rows3[i][2])+','+str(rows3[i][3])+','+str(rows3[i][4])+','+str(p3[i])+','+str(rows3[i][6]))
	
file.close()
