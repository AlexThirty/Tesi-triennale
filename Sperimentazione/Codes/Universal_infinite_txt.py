# importing modules 
import csv 
import numpy as np
import math
from scipy.special import gamma
from scipy.integrate import quad
from scipy import integrate

# Questo algoritmo esegue, con un integrale approssimato, il procedimento del portafoglio universale
# cosi come si trova sul libro di Thomas-Cover

# Qui vengono settati i principali valori

# Portafogli iniziali
portfolio2 = 1.
portfolios2 = []
portfolio3 = 1.
portfolios3 = []

# Inizializzazioni varie
s2 = 0.
s3 = 0.

# Qui si puo settare la frequenza, ossia ogni quanti giorni andiamo a operare
freq = 256

# Funzione densita, sia per 2 che per 3 asset usati

def density3(a1,a2):
	return gamma((3./2.))*((a1)**(-0.5))*((a2)**(-0.5))*((1-a1-a2)**(-0.5))/((gamma(0.5))**3)

def density2(a):
	return gamma(1.)*(((float)(a))**(-0.5))*((1.-(float)(a))**(-0.5))/((gamma(0.5))**2)

# NB, qui importiamo 3 asset, il caso da due asset tiene in considerazione i primi 2

# Importiamo i dati del primo asset dal file TXT

filename = "sKO.txt"

titles1 = []
rows1 = []

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows1.append(currentline)
  
# txt file name 
filename = "sIBM.txt"
  
# initializing the titles and rows list 
titles2 = [] 
rows2 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows2.append(currentline)
  
# Qua troviamo l'asset con minore periodo e facciamo partire gli altri al punto giusto

l = min(len(rows1), len(rows2))
print(l)

if(len(rows1)!=l):
	start1 = len(rows1)-l
else:
	start1 = 0

if(len(rows2)!=l):
	start2 = len(rows2)-l
else:
	start2 = 0

print start1
print start2

# Qui creiamo il vettore degli asset

asset1 = []
asset2 = []
asset3 = []
for i in range(0,(int)(l/freq)):
	asset1.append((float)(rows1[start1+freq*i][5]))
	asset2.append((float)(rows2[start2+freq*i][5]))
	asset3.append((float)(rows3[start3+freq*i][5]))

l = len(asset1)
assets = []

for i in range(1, l):
	day = []
	day.append(asset1[i]/asset1[i-1])
	day.append(asset2[i]/asset2[i-1])
	day.append(asset3[i]/asset3[i-1])
	assets.append(day)

l = l-1

# Siccome facciamo un integrale approssimato troviamo anzitutto quando vale l'integrale totale

# Caso 3 asset


for b1 in range(0,100):
	for b2 in range(0, 100):
		if(b1+b2<100):
			s3 = s3 + (0.01**2)*density3(b1/100.+0.01/3,b2/100.+0.01/3)

# Caso 2 asset

for b in range(0,1000):
	s2 = s2 + (0.001)*density2(b/1000.+0.0005)

d2 = (float)(s2)
d3 = (float)(s3)

# Ora risolviamo il problema vero e proprio
# Lavoriamo con 2 asset

def fun2(x, n):
		S = 1.
		for j in range(0, int(n)):
			S = S*(assets[j][0]*x+assets[j][1]*(1-x))
		S = S*density2(x)
		return S

for i in range(0,10000):
	print i
	# Applico esattamente il metodo di Thomas, Cover
	pas = i
	portfolio2 = quad(fun2, 0, 1, args=(pas))[0]
	print portfolio2
	portfolios2.append(portfolio2)

# Vari plotting

# Analisi dei dati, caso 2 asset

wmax2 = 1.
dd2 = []
ddmax2 = 0.
for i in range(0, len(portfolios2)):
	wmax2 = max(wmax2, portfolios2[i])
	dd2.append(1.-portfolios2[i]/wmax2)
	if dd2[i] > ddmax2:
		ddmax2 = dd2[i]
		
cal = []
for i in range(1,len(portfolios2)):
	cal.append(portfolios2[i]/portfolios2[i-1]-1)
mum2 = np.mean(cal)
sdev2 = np.std(cal)

sharpe2 = 16*mum2/(sdev2*(freq**0.5))
calmar2 = 16*mum2/(ddmax2*freq)

mug2 = portfolios2[len(portfolios2)-1]**(1./(len(portfolios2)))-1

print 'Caso dei 2 asset\n'
print 'Massimo drowdown: ' + str(ddmax2)
print 'Crescita media annua: ' + str(256*mum2/freq)
print 'Deviazione standard annua: ' + str(16*sdev2/(freq**0.5))
print 'Crescita media geometrica: ' + str(mug2)
print 'Sharpe ratio: ' + str(sharpe2)
print 'Calmar ratio: ' + str(calmar2)

print 'Portafoglio finale: ' + str(portfolio2)

# Output dei dati

filename = "Universal_infinite2.txt"

file = open(filename, 'w')
file.write("Caso 2 asset:\n\n")
file.write("Massimo drowdown: " + str(ddmax2) + "\n")
file.write("Crescita media annua: " + str(256*mum2/freq) + "\n")
file.write("Deviazione standard annua: " + str(16*sdev2/(freq**0.5)) + "\n")
file.write("Crescita media geometrica: " + str(mug2) + "\n")
file.write("Sharpe ratio: " + str(sharpe2) + "\n")
file.write("Calmar ratio: " + str(calmar2) + "\n")
file.write("Portafoglio finale: " + str(portfolio2) + "\n")
for i in range(0, len(portfolios2)):
	file.write(str(portfolios2[i])+"\n")

