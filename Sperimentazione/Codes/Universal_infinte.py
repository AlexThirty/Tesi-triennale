# importing modules 
import csv 
import numpy as np
from matplotlib import pyplot as plt
import statistics
import math
from scipy.special import gamma
from scipy.integrate import dblquad
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
freq = 1

# Funzione densita, sia per 2 che per 3 asset usati

def density3(a1,a2):
	return gamma((3./2.))*((a1)**(-0.5))*((a2)**(-0.5))*((1-a1-a2)**(-0.5))/((gamma(0.5))**3)

def density2(a):
	return gamma(1.)*(((float)(a))**(-0.5))*((1.-(float)(a))**(-0.5))/((gamma(0.5))**2)

# NB, qui importiamo 3 asset, il caso da due asset tiene in considerazione i primi 2

# Importiamo i dati del primo asset dal file CSV

# csv file name
filename = "KO.csv"
  
# initializing the titles and rows list 
titles1 = [] 
rows1 = [] 
  
with open(filename, 'r') as csvfile:  
    csvreader = csv.reader(csvfile) 
    titles1 = csvreader.next() 
    for row in csvreader: 
        rows1.append(row)  


# csv file name 
filename = "IBM.csv"
  
# initializing the titles and rows list 
titles2 = [] 
rows2 = [] 

with open(filename, 'r') as csvfile:  
    csvreader = csv.reader(csvfile) 
    titles2 = csvreader.next() 
    for row in csvreader: 
        rows2.append(row) 

# csv file name 
filename = "GE.csv"

# initializing the titles and rows list 
titles3 = [] 
rows3 = [] 

with open(filename, 'r') as csvfile:  
    csvreader = csv.reader(csvfile) 
    titles3 = csvreader.next() 
    for row in csvreader: 
        rows3.append(row)  


# Qua troviamo l'asset con minore periodo e facciamo partire gli altri al punto giusto

l = min(len(rows1), min(len(rows2), len(rows3)))
print(l)
if(len(rows1)!=l):
	start1 = len(rows1)-l
else:
	start1 = 0

if(len(rows2)!=l):
	start2 = len(rows2)-l
else:
	start2 = 0

if(len(rows3)!=l):
	start3 = len(rows3)-l
else:
	start3 = 0


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

# Caso 3 asset

# ~ for i in range(0,l):
	# ~ # Applico esattamente il metodo di Thomas, Cover
	# ~ s3 = 0.
	# ~ for b1 in range(0,100):
		# ~ for b2 in range(0, 100):
			# ~ if(b1+b2<100):
				# ~ s3 = s3 + ((b1/100.+0.01/3)*assets[i][0]+(b2/100.+0.01/3)*assets[i][1]+(1-b1/100.-0.01/3-b2/100.-0.01/3)*assets[i][2])*(0.01**2)*density3(b1/100.+0.01/3,b2/100.+0.01/3)/d3
	# ~ portfolio3 = portfolio3*s3
	# ~ portfolios3.append(portfolio3)
	# ~ print(portfolio3)

# ~ for i in range(0,l):
def fun3(b1,b2,b3):
	S = 1.	
	for j in range(0,l):
		S = S*(assets[j][0]*b1+assets[j][1]*b2+assets[j][2]*b3)
	S = S*gamma((3./2.))*((b1)**(-0.5))*((b2)**(-0.5))*((1-b1-b2)**(-0.5))/((gamma(0.5))**3)
	return S
delta = 1e-4
def bounds_b1():
	return [0,1]
def bounds_b2(b1):
	return [0,1-b1]
def bounds_b3(b1,b2):
	return [0,1-b1-b2]
portfolio3 = integrate.nquad(fun3, [bounds_b3,bounds_b2,bounds_b1])
print portfolio3
portfolios3.append(portfolio3)

# Caso 2 asset

for i in range(0,l):
	print i
	# Applico esattamente il metodo di Thomas, Cover
	s2 = 0.
	for b in range(0,1000):
		s2 = s2 + ((b/1000.+0.0005)*assets[i][0]+(1-b/1000.-0.0005)*assets[i][1])*(0.001)*density2(b/1000.+0.0005)/d2
	portfolio2 = portfolio2*s2
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
plt.plot(range(0,len(portfolios2)), portfolios2)
plt.title("Portafoglio (2 asset) in funzione del tempo")
plt.show()
plt.plot(range(0,len(portfolios2)), portfolios2)
plt.yscale('log')
plt.title("Portafoglio (2 asset) in funzione del tempo, semilog")
plt.show()
plt.plot(range(0,len(dd2)), dd2)
plt.title("Drowdown (2 asset) in funzione del tempo")
plt.show()


# Analisi dei dati, caso 3 asset

wmax3 = 1.
dd3 = []
ddmax3 = 0.
for i in range(0, len(portfolios3)):
	wmax3 = max(wmax3, portfolios3[i])
	dd3.append(1.-portfolios3[i]/wmax3)
	if dd3[i] > ddmax3:
		ddmax3 = dd3[i]
		
cal = []
for i in range(1,len(portfolios3)):
	cal.append(portfolios3[i]/portfolios3[i-1]-1)
mum3 = np.mean(cal)
sdev3 = np.std(cal)

sharpe3 = 16*mum3/(sdev3*(freq**0.5))
calmar3 = 16*mum3/(ddmax3*freq)

mug3 = portfolios3[len(portfolios3)-1]**(1./(len(portfolios3)))-1

print '\n\nCaso dei 3 asset:\n'
print 'Massimo drowdown: ' + str(ddmax3)
print 'Crescita media annua: ' + str(256*mum3/freq)
print 'Deviazione standard annua: ' + str(16*sdev3/(freq**0.5))
print 'Crescita media geometrica: ' + str(mug3)
print 'Sharpe ratio: ' + str(sharpe3)
print 'Calmar ratio: ' + str(calmar3)

print 'Portafoglio finale: ' + str(portfolio3)
plt.plot(range(0,len(portfolios3)), portfolios3)
plt.title("Portafoglio (3 asset) in funzione del tempo")
plt.show()
plt.plot(range(0,len(portfolios3)), portfolios3)
plt.yscale('log')
plt.title("Portafoglio (3 asset) in funzione del tempo, semilog")
plt.show()
plt.plot(range(0,len(dd3)), dd3)
plt.title("Drowdown (3 asset) in funzione del tempo")
plt.show()

# Output dei dati

filename = "Universal_infinite.txt"

file = open(filename, 'w')
file.write("Caso 2 asset:\n\n")
file.write("Massimo drowdown: " + str(ddmax2) + "\n")
file.write("Crescita media annua: " + str(256*mum2/freq) + "\n")
file.write("Deviazione standard annua: " + str(16*sdev2/(freq**0.5)) + "\n")
file.write("Crescita media geometrica: " + str(mug2) + "\n")
file.write("Sharpe ratio: " + str(sharpe2) + "\n")
file.write("Calmar ratio: " + str(calmar2) + "\n")
file.write("Portafoglio finale: " + str(portfolio2) + "\n")

file.write("\n\nCaso 3 asset:\n\n")
file.write("Massimo drowdown: " + str(ddmax3) + "\n")
file.write("Crescita media annua: " + str(256*mum3/freq) + "\n")
file.write("Deviazione standard annua: " + str(16*sdev3/(freq**0.5)) + "\n")
file.write("Crescita media geometrica: " + str(mug3) + "\n")
file.write("Sharpe ratio: " + str(sharpe3) + "\n")
file.write("Calmar ratio: " + str(calmar3) + "\n")
file.write("Portafoglio finale: " + str(portfolio3) + "\n")
