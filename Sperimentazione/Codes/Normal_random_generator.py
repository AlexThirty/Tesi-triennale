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

# Importiamo i dati del primo asset dal file TXT

filename = "sKO.txt"
filename1 = 'c' + filename
titles1 = []
rows1 = []

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows1.append(currentline)
  
# txt file name 
filename = "sIBM.txt"
filename2 = 'c' + filename

# initializing the titles and rows list 
titles2 = [] 
rows2 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows2.append(currentline)

p1 = []
p2 = []
p1.append(10.)
p2.append(10.)

l1 = len(rows1)
l2 = len(rows2)

mu1 = math.log(float(rows1[l1-1][5])/float(rows1[0][5]))/l1
mu2 = math.log(float(rows2[l1-1][5])/float(rows2[0][5]))/l2

print mu1
print mu2

x1 = []
x2 = []
x1.append(math.log(p1[0]))
x2.append(math.log(p2[0]))

for i in range(1,l1):
	r1 = np.random.normal(mu1,sigma1)
	r2 = np.random.normal(mu2,sigma2)
	x1.append(x1[i-1]+r1)
	x2.append(x2[i-1]+r2)
	p1.append(math.exp(x1[i]))
	p2.append(math.exp(x2[i]))


file = open("waste.txt", "w")
for i in range(0,len(rows1)):
	file.write(str(rows1[i][0])+','+str(rows1[i][1])+','+str(rows1[i][2])+','+str(rows1[i][3])+','+str(rows1[i][4])+','+str(p1[i])+','+str(rows1[i][6]))

file.close()

file = open(filename2, "w")
for i in range(0,len(rows2)):
	file.write(str(rows2[i][0])+','+str(rows2[i][1])+','+str(rows2[i][2])+','+str(rows2[i][3])+','+str(rows2[i][4])+','+str(p2[i])+','+str(rows2[i][6]))
	
file.close()
