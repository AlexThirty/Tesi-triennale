# importing modules
import csv
import numpy as np
from matplotlib import pyplot as plt
import statistics
import math
from scipy.special import gamma
from scipy.integrate import dblquad
from scipy import integrate
from anytree import Node
# Qui vengono settate i principali valori

# In questo algoritmo usiamo un paradigma principale, ossia che in ogni stato in cui mi trovo
# Vado a considerare la media degli outcome nel passato che ho ottenuto dallo stesso stato
# Il portafoglio viene aggiornato sia secondo il metodo di Kelly (che tiene conto anche delle covarianze
# e incertezze) e sia secondo il metodo "scelgo quello che mi da mediamente rendimento migliore",
# trascurando cioe le incertezze e le covarianze

# Finestra di tempo che vado a considerare, si usa solo 1 in realta
# Gli altri casi richiederebbero una finestra temporale troppo ampia per diventare efficienti
k = 1

# Portafogli iniziali, il kelly fa riferimento al metodo di kelly
portfolio= 1.
kellyportfolio = 1.
kellyportfolios = []
portfolios = []

# In questo algoritmo ad ogni giorno consideriamo una media e una deviazione standard empirica
# degli ultimi tau giorni (che si settano qua sotto). Gli stati sono invece rappresentati da quanto
# Il rendimento dell'ultima giornata si discosta dal rendimento medio del periodo tau in punti di deviazione standard
s = [-10, -10, -6, -2, -1, -0.5, -0.25, 0, 0.25, 0.5, 1, 2, 6, 10, 10]
tau = 63

# Inizializzo i dizionari e altre variabili utili
di = {}
stot = len(s)
ma = s[stot-2]
outcomes1 = {}
outcomes2 = {}

states = []

for i in range(0, stot-1):
	states.append((s[i], s[i+1]))

# Qui salvero i vari potafogli che mi da il kelly
b1s = []
b2s = []

# Qui si puo settare la frequenza, ossia ogni quanti giorni andiamo a operare
freq = 1


# Importiamo i dati del primo asset dal file CSV

# csv file name
filename = "../Titoli_csv/KO.csv"

# initializing the titles and rows list
titles1 = []
rows1 = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    titles1 = next(csvreader)
    for row in csvreader:
        rows1.append(row)

# csv file name
filename = "../Titoli_csv/IBM.csv"

# initializing the titles and rows list
titles2 = []
rows2 = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    titles2 = next(csvreader)
    for row in csvreader:
        rows2.append(row)

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

# Qui settiamo i vettori con i closing degli asset e quello coi rapporti

asset1 = []
asset2 = []

for i in range(0,(int)(l/freq)):
	asset1.append((float)(rows1[start1+freq*i][5]))
	asset2.append((float)(rows2[start2+freq*i][5]))

l = len(asset1)
assets = []

for i in range(1,l):
	day = []
	day.append(asset1[i]/asset1[i-1])
	day.append(asset2[i]/asset2[i-1])
	assets.append(day)

l = l-1

root = Node(name = "root")

def generateChildren(n):
	for s in states:
		for t in states:
			Node(name=str(s)+"x"+str(t), state1 = s, state2 = t, parent = n, data = 0)
	return n

generateChildren(root)

# Funzione che ottiene lo stato della catena in cui mi trovo
# Restituisce la stringa con cui viene salvato uno stato, semplicemente
# Ogni stato e rappresentato dal rendimento in punti percentuali dei due asset
# separati da una x
# Ogni singolo asset, invece, e rappresentato da un intervallo

def obtainNode(st, en, mu0, sigma0, mu1, sigma1):
	node = root
	w = str
	for t in range(st, en+1):
		if node.children==():
			node = generateChildren(node)
		approx1 = (np.log(assets[t][0])-mu0)/sigma0
		approx2 = (np.log(assets[t][1])-mu1)/sigma1
		for n in node.children:
			if approx1 >= n.state1[0] and approx1 <= n.state1[1] and approx2 >= n.state2[0] and approx2 <= n.state2[1]:
				node = n
	if node.children==():
		node = generateChildren(node)
	return node




# Algoritmo vero e proprio

indecisioni = 0
primoasset = 0
secondoasset = 0

for i in range(0,l):
	print(i)
	if i > tau:

		# Trovo varianze e medie empiriche negli ultimi tau giorni
		cal = []
		for j in range(i-tau, i):
			cal.append(np.log(assets[j][0]))
		sigma0 = np.std(cal)
		mu0 = np.mean(cal)
		cal = []
		for j in range(i-tau, i):
			cal.append(np.log(assets[j][1]))
		sigma1 = np.std(cal)
		mu1 = np.mean(cal)


		# Vediamo in che stato mi trovo ora
		state = obtainNode(i-k, i-1, mu0, sigma0, mu1, sigma1)

		# Prendo dal dizionario le frequenze passate e stimo il valore atteso
		v1 = 0.
		v2 = 0.

		# Troviamo il portafoglio aggiornato, lo facciamo sia con una Kelly che standard


		if state.data > 0:
			# Se sono gia stato in questo stato nel passato
			# Prendiamo le medie degli outcome per questo stato nel passato
			me1 = np.mean(outcomes1[state])-1
			me2 = np.mean(outcomes2[state])-1

			# Calcoliamo la correlazione o la matrice di covarianza

			# ~ for j in range(i-tau, i):
				# ~ cal.append(((assets[j][0]-1)*(assets[j][1]-1)))
			# ~ #rho = np.mean(cal)/(sigma0*sigma1)
			# ~ rho = np.mean(cal)

			cal1 = []
			cal2 = []
			for j in range(i-tau ,i):
				cal1.append(assets[j][0])
				cal2.append(assets[j][1])
			cov_mat = np.stack((cal1,cal2), axis = 0)
			cov = np.cov(cov_mat)

			# Trovo i coefficienti del kelly
			C = np.linalg.inv(cov)
			b = np.array([me1, me2])
			f = C.dot(b)

			# Sistemo i coefficienti del kelly
			if f[0] > 0 and f[1] > 0:
				if f[0] + f[1] >= 1:
					b1 = f[0]/(f[0]+f[1])
					b2 = f[1]/(f[0]+f[1])
				else:
					b1 = f[0]
					b2 = f[1]
			if f[0] > 0 and f[1] <= 0:
				if f[0] > 1:
					b1 = 1
				else:
					b1 = f[0]
				b2 = 0
			if f[1] > 0 and f[0] <= 0:
				if f[1] > 1:
					b2 = 1
				else:
					b2 = f[1]
				b1 = 0
			if f[1] <= 0 and f[0] <= 0:
				b1 = 0
				b2 = 0

			b1s.append(b1)
			b2s.append(b2)

			# Qua uso decido su quale asset puntare per il metodo che trascura le incertezze
			if me1 > me2:
				primoasset = primoasset + 1
				portfolio = portfolio*assets[i][0]
			else:
				if me2 > me1:
					secondoasset = secondoasset + 1
					portfolio = portfolio*assets[i][1]
				else:
					indecisioni = indecisioni + 1
					portfolio = portfolio * (0.5*assets[i][0] + 0.5*assets[i][1])

			# Aggiorno il portafoglio kelly
			kellyportfolio = kellyportfolio*(b1*assets[i][0] + b2*assets[i][1]) + kellyportfolio*(1.-b1-b2)

		else:
			# Se non sono mai stato in questo stato
			portfolio = portfolio * (0.5*assets[i][0] + 0.5*assets[i][1])
			kellyportfolio = kellyportfolio * (0.5*assets[i][0] + 0.5*assets[i][1])
			indecisioni = indecisioni + 1

		# A questo punto aggiorno il dizionario degli stati

		# Trovo varianze e medie empiriche
		cal = []
		for j in range(i-tau+1, i+1):
			cal.append(np.log(assets[j][0]))
		sigma0 = np.std(cal)
		mu0 = np.mean(cal)
		cal = []
		for j in range(i-tau+1, i+1):
			cal.append(np.log(assets[j][1]))
		sigma1 = np.std(cal)
		mu1 = np.mean(cal)

		# Prendo l'ultimo k stato

		state = obtainNode(i-k+1, i, mu0, sigma0, mu1, sigma1)
		print(state)
		state.data = state.data + 1

		# Aggiundo al dizionario che salva gli outcomes per ogni stato

		if state in outcomes1:
			outcomes1[state].append(assets[i][0])
		else:
			outcomes1[state] = []
			outcomes1[state].append(assets[i][0])

		if state in outcomes2:
			outcomes2[state].append(assets[i][1])
		else:
			outcomes2[state] = []
			outcomes2[state].append(assets[i][1])

	else:
		# Se e troppo presto
		portfolio = portfolio * (0.5*assets[i][0] + 0.5*assets[i][1])
		kellyportfolio = kellyportfolio * (0.5*assets[i][0] + 0.5*assets[i][1])
		indecisioni = indecisioni + 1

	# Aggiornamenti vari
	portfolios.append(portfolio)
	kellyportfolios.append(kellyportfolio)
	#print(kellyportfolio)
	#print(portfolio)


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

# Stampe varie

print('Standard\n')
print('Massimo drowdown: ' + str(ddmax))
print('Crescita media annua: ' + str(256*mum/freq))
print('Deviazione standard annua: ' + str(16*sdev/(freq**0.5)))
print('Crescita media geometrica: ' + str(mug))
print('Sharpe ratio: ' + str(sharpe))
print('Calmar ratio: ' + str(calmar))
print('Primo: ' + str(primoasset))
print('Secondo: ' + str(secondoasset))
print('Indecisioni: ' + str(indecisioni))

print('Portafoglio finale: ' + str(portfolio))
plt.plot(range(0,len(portfolios)), portfolios)
plt.title("Capitale")
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.show()
plt.plot(range(0,len(portfolios)), portfolios)
plt.yscale('log')
plt.title("Capitale, scala semilogaritmica")
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.show()
plt.plot(range(0,len(dd)), dd)
plt.title("Drowdown")
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.show()

print('\n\nKelly\n')
print('Massimo drowdown: ' + str(kellyddmax))
print('Crescita media annua: ' + str(256*kellymum/freq))
print('Deviazione standard annua: ' + str(16*kellysdev/(freq**0.5)))
print('Crescita media geometrica: ' + str(kellymug))
print('Sharpe ratio: ' + str(kellysharpe))
print('Calmar ratio: ' + str(kellycalmar))

print('Portafoglio finale: ' + str(kellyportfolio))
plt.plot(range(0,len(kellyportfolios)), kellyportfolios)
plt.title("Capitale con Kelly")
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.show()
plt.plot(range(0,len(kellyportfolios)), kellyportfolios)
plt.yscale('log')
plt.title("Capitale con Kelly, scala semilogaritmica")
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.show()
plt.plot(range(0,len(kellydd)), kellydd)
plt.title("Drowdown con Kelly")
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.show()


# Output dei dati su file

filename = "../Results/Empirical3_csv.txt"

file = open(filename, 'w')
file.write("Standard\n")
file.write("Massimo drowdown: " + str(ddmax) + "\n")
file.write("Crescita media annua: " + str(256*mum/freq) + "\n")
file.write("Deviazione standard annua: " + str(16*sdev/(freq**0.5)) + "\n")
file.write("Crescita media geometrica: " + str(mug) + "\n")
file.write("Sharpe ratio: " + str(sharpe) + "\n")
file.write("Calmar ratio: " + str(calmar) + "\n")
file.write("Ho scelto il primo asset " + str(primoasset) + " volte\n")
file.write("Ho scelto il secondo asset " + str(secondoasset) + " volte\n")
file.write("Sono stato indeciso " + str(indecisioni) + " volte\n")
file.write("Portafoglio finale: " + str(portfolio) + "\n")

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
