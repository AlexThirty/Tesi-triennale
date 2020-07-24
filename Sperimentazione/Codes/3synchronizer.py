# Empirical.py
# Metodo basato su frequenze empiriche dei rendimenti

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

# Questo algoritmo utilizza un procedimento suggerito dall'articolo di Algoet,
# Studia l'andamento di due titoli come una catena di Markov a k stati approssimati
# In questo caso ogni stato e rappresentato da un intervallo di punti percentuali del 
# Rendimento di ogni asset
# L'algoritmo trascura le incertezze e le covarianze, quindi il portafoglio ad ogni passo
# e' distribuito tutto su un solo titolo

# Qui vengono settate i principali valori

# Finestra di tempo che vado a considerare, si usa solo 1 in realta
# Gli altri casi richiederebbero una finestra temporale troppo ampia per diventare efficienti
k = 1

# Portafoglio iniziale
portfolio= 1.
portfolios = []
portfolio2 = 1.

# Questi sono gli indicatori degli stati che andiamo a considerare
# Per come e scritto l'algoritmo ci interessano in realta gli intervalli tra questi valori
# Il primo e l'ultimo servono solo per considerare valori estremali
# Questi valori sono da intendersi in punti per mille di rendimento
s = [-1000, -100, -50, -10, -7,-5,-2,-1, 0, 1, 2, 5, 7, 10, 50, 100, 1000]

# Inizializzo il dizionario e variabili utili
di = {}
stot = len(s)
ma = s[stot-2]

# L'algoritmo da un peso base di uno per stati gia visitati, qua si puo
# settare un peso diverso per le transizioni di cui so il numero di occorrenze
peso = 5.

# Qui si puo settare la frequenza, ossia ogni quanti giorni andiamo a operare
freq = 1



# Importiamo i dati del primo asset dal file TXT

filename = "KO.txt"
filename1 = '3s' + filename
titles1 = []
rows1 = []

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows1.append(currentline)
  
# txt file name 
filename = "IBM.txt"
filename2 = '3s' + filename
# initializing the titles and rows list 
titles2 = [] 
rows2 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows2.append(currentline)

# txt file name 
filename = "GE.txt"
filename3 = '3s' + filename
# initializing the titles and rows list 
titles3 = [] 
rows3 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows3.append(currentline)


i = 0
j = 0
k = 0
row1 = []
row2 = []
row3 = []
while i < len(rows1) and j < len(rows2) and k < len(rows3):
	a = dt.strptime(str(rows1[i][0])+":"+str(rows1[i][1]), "%m/%d/%Y:%H:%M")
	b = dt.strptime(str(rows2[j][0])+":"+str(rows2[j][1]), "%m/%d/%Y:%H:%M")
	c = dt.strptime(str(rows3[k][0])+":"+str(rows3[k][1]), "%m/%d/%Y:%H:%M")
	if a == b and b == c:
		row1.append(rows1[i])
		row2.append(rows2[j])
		row3.append(rows3[k])
		print "added" + str(a)
		i = i+1
		j = j+1
		k = k+1
		if i < len(rows1):
			a = dt.strptime(str(rows1[i][0])+":"+str(rows1[i][1]), "%m/%d/%Y:%H:%M")
		if j < len(rows2):
			b = dt.strptime(str(rows2[j][0])+":"+str(rows2[j][1]), "%m/%d/%Y:%H:%M")
		if k < len(rows3):
			c = dt.strptime(str(rows3[k][0])+":"+str(rows3[k][1]), "%m/%d/%Y:%H:%M")
	m = max(a,max(b,c))
	while a < m and i < len(rows1):
		i=i+1
		if i < len(rows1):
			a = dt.strptime(str(rows1[i][0])+":"+str(rows1[i][1]), "%m/%d/%Y:%H:%M")
	while b < m and j < len(rows2):
		j=j+1
		if j < len(rows2):
			b = dt.strptime(str(rows2[j][0])+":"+str(rows2[j][1]), "%m/%d/%Y:%H:%M")
	while c < m and k < len(rows3):
		k=k+1
		if k < len(rows3):
			c = dt.strptime(str(rows3[k][0])+":"+str(rows3[k][1]), "%m/%d/%Y:%H:%M")

print "done"

file = open(filename1, "w")
for i in range(0,len(row1)):
	file.write(str(row1[i][0])+','+str(row1[i][1])+','+str(row1[i][2])+','+str(row1[i][3])+','+str(row1[i][4])+','+str(row1[i][5])+','+str(row1[i][6]))

file.close()

file = open(filename2, "w")
for i in range(0,len(row2)):
	file.write(str(row2[i][0])+','+str(row2[i][1])+','+str(row2[i][2])+','+str(row2[i][3])+','+str(row2[i][4])+','+str(row2[i][5])+','+str(row2[i][6]))
	
file.close()

file = open(filename3, "w")
for i in range(0,len(row3)):
	file.write(str(row3[i][0])+','+str(row3[i][1])+','+str(row3[i][2])+','+str(row3[i][3])+','+str(row3[i][4])+','+str(row3[i][5])+','+str(row3[i][6]))

file.close()
