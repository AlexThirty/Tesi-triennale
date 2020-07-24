# importing modules 
import csv 
import numpy as np
from matplotlib import pyplot as plt
import statistics
import math
import scipy
from scipy import optimize

# Questo codice esegue l'algoritmo presentato da Gyorfi, Udina e Walk in un articolo
# Ad ogni passo vado a ricercare tramite una finestra scorrevole lunga k, i momenti
# (ciascuno per ogni segmento di lunghezza fissata) in cui una successione di outcome di k
# k giorni si avvicinava di piu' in norma 1 a quella degli ultimi giorni. 
# A questo punto trovo il portafoglio ottimale per queste k sequenze nel passato e lo applico al presente

# Qui vengono settati i principali valori

# Lunghezza del blocco che considero e di cui cerco i vicini nel passato
k = 4

# Lunghezza dei segmenti nel passato, in ciascuno dei quali cerco il vicino
sl = 12			

# Portafoglio di partenza
portfolio = 1.
portfolios = []
portfolio2 = 1.
portfolios2 = []
kellyportfolio = 1.
kellyportfolios = []

# Qui si puo settare la frequenza, ossia ogni quanti giorni andiamo a operare
freq = 21

b1s = []
b2s = []
b3s = []
# Funzione di utilita, calcola la norma di un vettore in k*numero di asset
def norm(vec):
	n = 0.
	for v in vec:
		for d in v:
			n = n + abs(d)**2
	return n**(0.5)

# ~ def norm(vec):
	# ~ n = 0.
	# ~ for v in vec:
		# ~ for d in v:
			# ~ n = n + abs(d)
	# ~ return n

# Importiamo i dati del primo asset dal file CSV

# txt file name 
filename = "s3KO.txt"
  
# initializing the titles and rows list 
titles1 = [] 
rows1 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows1.append(currentline)
  
# txt file name 
filename = "s3IBM.txt"
  
# initializing the titles and rows list 
titles2 = [] 
rows2 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows2.append(currentline)
  
# txt file name 
filename = "s3GE.txt"
  
# initializing the titles and rows list 
titles3 = [] 
rows3 = [] 

with open(filename, "r") as filestream:
	for line in filestream:
		currentline = line.split(",")
		rows3.append(currentline)



# Trovo ora valori utili dell'input e salvo gli incrementi

l = min(len(rows1), min(len(rows2), len(rows3)))
# l = 3650
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

# start = l-3650

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

# Applichiamo il nearest neighbour
# L'algoritmo diventa molto lento quindi in realta ad ogni passo cerco i vicini
# nei segmenti solo dei dieci anni precedenti anche se rimane lento (circa 15 minuti per 10 anni o 1 ora per tutto)
# In ogni giorno verra suddiviso il caso in cui ho una finestra disponibile di almeno 10 anni o no

period = int(2560./freq)

primoasset = 0
secondoasset = 0
terzoasset = 0
indecisioni = 0

for n in range(0, l):
	print(n)
	if n <= period:
		segments = (int)(math.floor((n-1)/sl))
	else:
		segments = (int)(math.floor(period/sl))
	li = []
	ind = 0
	if(n>2*sl+1):
		Ni = []
		# Guardo tra i vari segmenti della divisione e cerco i portafogli piu' vicini
		if n <= period:
			for i in range(1, segments+1):
				mi = 1e10
				for j in range(((i-1)*sl+k), (i*sl)):
					li = []
					for g in range(j-k, j):
						li.append(np.subtract(assets[g],assets[g+n-j]))
					nor = norm(li)
					if(nor<mi):
						mi = nor
						ind = j
				Ni.append(ind)
		else:
			for i in range(1, segments+1):
				mi = 1e10
				for j in range((n-period)+((i-1)*sl+k), (n-period)+(i*sl)):
					li = []
					for g in range(j-k, j):
						li.append(np.subtract(assets[g],assets[g+n-j]))
					nor = norm(li)
					if(nor<mi):
						mi = nor
						ind = j
				Ni.append(ind)
				
		# Trovo ora il miglior modo di suddividere il mio portafoglio
		prod1 = 1.
		prod2 = 1.
		prod3 = 1.
		def fu(vect):
			su = 1.
			for i in Ni:
				su = su*(vect[0]*assets[i][0]+vect[1]*assets[i][1]+vect[2]*assets[i][2])
			return -su
		
		# Massimizzo grazie a una libreria di python
		
		boun=((0,1),(0,1),(0,1))		
		constr={'type': 'eq', 'fun': lambda x: x[0]+x[1]+x[2]-1}
		
		prov = scipy.optimize.minimize(fun = fu, x0 =(1/3,1/3,1/3), method='SLSQP',bounds=boun, constraints=constr)
		
		
		# Applichiamo il Kelly ai valori in Ni
		# Kelly
		outcomes1 = []
		outcomes2 = []
		outcomes3 = []
		
		for i in Ni:
			outcomes1.append(assets[i][0])
			outcomes2.append(assets[i][1])
			outcomes3.append(assets[i][2])
		
		me1 = np.mean(outcomes1)-1
		me2 = np.mean(outcomes2)-1
		me3 = np.mean(outcomes3)-1
		
		cov_mat = np.stack((outcomes1,outcomes2, outcomes3), axis = 0)
		cov = np.cov(cov_mat)
		
		
		# Trovo i coefficienti del kelly
		if(np.linalg.det(cov) == 0):
			print "singular\n"
			C = np.linalg.pinv(cov)
		else:
			C = np.linalg.inv(cov)
		b = np.array([me1, me2, me3])
		f = C.dot(b)
			
		# Sistemo i coefficienti del kelly
		if f[0] > 0 and f[1] > 0 and f[2] > 0:
			if f[0] + f[1] + f[2] >= 1:
				b1 = f[0]/(f[0]+f[1]+f[2])
				b2 = f[1]/(f[0]+f[1]+f[2])
				b3 = f[2]/(f[0]+f[1]+f[2])
			else:
				b1 = f[0]
				b2 = f[1]
				b3 = f[2]
		if f[0] > 0 and f[1] <= 0 and f[2]<= 0:
			if f[0] > 1:
				b1 = 1.
			else:
				b1 = f[0]
			b2 = 0.
			b3 = 0.
		
		if f[1] > 0 and f[0] <= 0 and f[2]<= 0:
			if f[1] > 1:
				b2 = 1.
			else:
				b2 = f[1]
			b1 = 0.
			b3 = 0.
			
		if f[2] > 0 and f[0] <= 0 and f[1]<= 0:
			if f[2] > 1:
				b3 = 1.
			else:
				b3 = f[2]
			b1 = 0.
			b2 = 0.
		
		if f[0] > 0 and f[1] > 0 and f[2] <= 0:
			if f[0] + f[1] >= 1:
				b1 = f[0]/(f[0]+f[1])
				b2 = f[1]/(f[0]+f[1])
			else:
				b1 = f[0]
				b2 = f[1]
			
			b3 = 0.
		if f[0] > 0 and f[2] > 0 and f[1] <= 0:
			if f[0] + f[2] >= 1:
				b1 = f[0]/(f[0]+f[2])
				b3 = f[2]/(f[0]+f[2])
			else:
				b1 = f[0]
				b3 = f[2]
			
			b2 = 0.	
		if f[1] > 0 and f[2] > 0 and f[0] <= 0:
			if f[2] + f[1] >= 1:
				b3 = f[2]/(f[2]+f[1])
				b2 = f[1]/(f[2]+f[1])
			else:
				b3 = f[2]
				b2 = f[1]
			
			b1 = 0.
		if f[1] <= 0 and f[0] <= 0 and f[2] <= 0:
			b1 = 0.
			b2 = 0.
			b3 = 0.
		
		b1s.append(b1)
		b2s.append(b2)
		b3s.append(b3)
		
		# Approssimazione al primo ordine
		prod1 = 1.
		prod2 = 1.
		prod3 = 1.
		for i in Ni:
			prod1 = prod1*assets[i][0]
			prod2 = prod1*assets[i][1]
			prod3 = prod1*assets[i][2]
		best = max(prod1, max(prod2,prod3))
		if prod1 == best:
			if prod2 == best:
				if prod3 == best:
					indecisioni = indecisioni +1
					portfolio2 = portfolio2*(assets[n][0]/3.+assets[n][1]/3.+assets[n][2]/3.)
				else:
					portfolio2 = portfolio2*(assets[n][0]/2.+assets[n][1]/2.)
					indecisioni = indecisioni+1
			else:
				if prod3 == best:
					portfolio2 = portfolio2*(assets[n][0]/2.+assets[n][2]/2.)
					indecisioni = indecisioni +1
				else:
					primoasset = primoasset + 1
					portfolio2 = portfolio2*(assets[n][0])
		else:
			if prod2 == best:
				if prod3 == best:
					indecisioni = indecisioni +1
					portfolio2 = portfolio2*(assets[n][1]/2.+assets[n][2]/2.)
				else:
					portfolio2 = portfolio2*(assets[n][1])
					secondoasset = secondoasset+1
			else:
				if prod3 == best:
					portfolio2 = portfolio2 * assets[n][2]
					terzoasset= terzoasset+1
		portfolios2.append(portfolio2)
		
		# Trovo i coefficienti del metodo base
		pro1 = prov.x[0]/(prov.x[0]+prov.x[1]+prov.x[2])
		pro2 = prov.x[1]/(prov.x[0]+prov.x[1]+prov.x[2])
		pro3 = prov.x[2]/(prov.x[0]+prov.x[1]+prov.x[2])
		
		# Aggiorno il portafoglio
		portfolio = portfolio*(assets[n][0]*pro1+assets[n][1]*pro2+assets[n][2]*pro3)
		portfolios.append(portfolio)
		
		kellyportfolio = kellyportfolio * (assets[n][0]*b1 + assets[n][1]*b2 + assets[n][2]*b3 + 1.*(1.-b1-b2-b3))
		kellyportfolios.append(kellyportfolio)
		#print(portfolio)
	else:
		portfolio2 = portfolio2 * (assets[n][0]/3. + assets[n][1]/3. + assets[n][2]/3.)
		kellyportfolio = kellyportfolio * (assets[n][0]/3. + assets[n][1]/3. + assets[n][2]/3.)
		portfolio = portfolio * (assets[n][0]/3. + assets[n][1]/3. + assets[n][2]/3.)
		portfolios.append(portfolio)
		portfolios2.append(portfolio2)
		kellyportfolios.append(kellyportfolio)
	
	print portfolio
	print portfolio2
	print kellyportfolio



# Analisi dei dati

wmax = 1.
dd = []
ddmax = 0.
for i in range(0, len(portfolios)):
	wmax = max(wmax, portfolios[i])
	dd.append(1.-portfolios[i]/wmax)
	if dd[i] > ddmax:
		ddmax = dd[i]
		
cal = []
for i in range(1,len(portfolios)):
	cal.append(portfolios[i]/portfolios[i-1]-1)
mum = np.mean(cal)
sdev = np.std(cal)

sharpe = 16*mum/(sdev*(freq**0.5))
calmar = 16*mum/(ddmax*freq)

mug = portfolios[len(portfolios)-1]**(1./(len(portfolios)))-1

# Analisi dei dati per il kelly

kellywmax = 1.
kellydd = []
kellyddmax = 0.
for i in range(0, len(kellyportfolios)):
	kellywmax = max(kellywmax, kellyportfolios[i])
	kellydd.append(1.-kellyportfolios[i]/kellywmax)
	if kellydd[i] > kellyddmax:
		kellyddmax = kellydd[i]
		
cal = []
for i in range(1,len(kellyportfolios)):
	cal.append(kellyportfolios[i]/kellyportfolios[i-1]-1)
kellymum = np.mean(cal)
kellysdev = np.std(cal)

kellysharpe = 16*kellymum/(kellysdev*(freq**0.5))
kellycalmar = 16*kellymum/(kellyddmax*freq)

kellymug = kellyportfolios[len(kellyportfolios)-1]**(1./(len(kellyportfolios)))-1

# Analisi dei dati per l'appross al primo ordine

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

# Stampe varie

print 'Standard\n'
print 'Massimo drowdown: ' + str(ddmax)
print 'Crescita media annua: ' + str(256*mum/freq)
print 'Deviazione standard annua: ' + str(16*sdev/(freq**0.5))
print 'Crescita media geometrica: ' + str(mug)
print 'Sharpe ratio: ' + str(sharpe)
print 'Calmar ratio: ' + str(calmar)

print 'Portafoglio finale: ' + str(portfolio)
plt.plot(range(0,len(portfolios)), portfolios)
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale per il metodo NN")
plt.show()
plt.plot(range(0,len(portfolios)), portfolios)
plt.yscale('log')
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale per il metodo NN, scala semilogaritmica")
plt.show()
plt.plot(range(0,len(dd)), dd)
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.title("Drowdown per il metodo NN")
plt.show()

print '\n\nPrimo Ordine\n'
print 'Massimo drowdown: ' + str(ddmax2)
print 'Crescita media annua: ' + str(256*mum2/freq)
print 'Deviazione standard annua: ' + str(16*sdev2/(freq**0.5))
print 'Crescita media geometrica: ' + str(mug2)
print 'Sharpe ratio: ' + str(sharpe2)
print 'Calmar ratio: ' + str(calmar2)
print 'Primo: ' + str(primoasset)
print 'Secondo: ' + str(secondoasset)
print 'Terzo: ' + str(terzoasset)
print 'Indecisioni: ' + str(indecisioni)

print 'Capitale finale: ' + str(portfolio2)
plt.plot(range(0,len(portfolios2)), portfolios2)
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale per il metodo NN al primo ordine")
plt.show()
plt.plot(range(0,len(portfolios2)), portfolios2)
plt.yscale('log')
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale per il metodo NN al primo ordine, scala semilogaritmica")
plt.show()
plt.plot(range(0,len(dd2)), dd2)
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.title("Drowdown per il metodo NN al primo ordine")
plt.show()


print '\n\nKelly\n'
print 'Massimo drowdown: ' + str(kellyddmax)
print 'Crescita media annua: ' + str(256*kellymum/freq)
print 'Deviazione standard annua: ' + str(16*kellysdev/(freq**0.5))
print 'Crescita media geometrica: ' + str(kellymug)
print 'Sharpe ratio: ' + str(kellysharpe)
print 'Calmar ratio: ' + str(kellycalmar)

print 'Portafoglio finale: ' + str(kellyportfolio)
plt.plot(range(0,len(kellyportfolios)), kellyportfolios)
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale per il metodo NN con Kelly")
plt.show()
plt.plot(range(0,len(kellyportfolios)), kellyportfolios)
plt.yscale('log')
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale per il metodo NN con Kelly, scala semilogaritmica")
plt.show()
plt.plot(range(0,len(kellydd)), kellydd)
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.title("Drowdown per il metodo NN con Kelly")
plt.show()
# Output dei dati

filename = "NN.txt"

file = open(filename, 'w')
file.write("Standard\n")
file.write("Massimo drowdown: " + str(ddmax) + "\n")
file.write("Crescita media annua: " + str(256*mum/freq) + "\n")
file.write("Deviazione standard annua: " + str(16*sdev/(freq**0.5)) + "\n")
file.write("Crescita media geometrica: " + str(mug) + "\n")
file.write("Sharpe ratio: " + str(sharpe) + "\n")
file.write("Calmar ratio: " + str(calmar) + "\n")
file.write("Portafoglio finale: " + str(portfolio) + "\n")


file.write("\n\nPrimo ordine\n")
file.write("Massimo drowdown: " + str(ddmax2) + "\n")
file.write("Crescita media annua: " + str(256*mum2/freq) + "\n")
file.write("Deviazione standard annua: " + str(16*sdev2/(freq**0.5)) + "\n")
file.write("Crescita media geometrica: " + str(mug2) + "\n")
file.write("Sharpe ratio: " + str(sharpe2) + "\n")
file.write("Calmar ratio: " + str(calmar2) + "\n")
file.write("Ho scelto il primo asset " + str(primoasset) + " volte\n")
file.write("Ho scelto il secondo asset " + str(secondoasset) + " volte\n")
file.write("Ho scelto il terzo asset " + str(terzoasset) + " volte\n")
file.write("Sono stato indeciso " + str(indecisioni) + " volte\n")
file.write("Portafoglio finale: " + str(portfolio2) + "\n")

file.write("\n\nKelly\n")
file.write("Massimo drowdown: " + str(kellyddmax) + "\n")
file.write("Crescita media annua: " + str(256*kellymum/freq) + "\n")
file.write("Deviazione standard annua: " + str(16*kellysdev/(freq**0.5)) + "\n")
file.write("Crescita media geometrica: " + str(kellymug) + "\n")
file.write("Sharpe ratio: " + str(kellysharpe) + "\n")
file.write("Calmar ratio: " + str(kellycalmar) + "\n")
file.write("Portafoglio finale: " + str(kellyportfolio) + "\n")
for i in range(0,len(portfolios)):
	file.write(str(portfolios[i]) + "\n")

file.close()
