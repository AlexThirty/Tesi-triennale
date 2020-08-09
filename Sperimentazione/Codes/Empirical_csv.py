# -*- coding: utf-8 -*-
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
from anytree import AnyNode, Node, RenderTree

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
s = [-1000, -1000, -700, -500, -300, -100, -50, -10,  0, 10, 50, 100, 300, 500, 700, 1000, 1000]

# Inizializzo il dizionario e variabili utili
di = {}
stot = len(s)
ma = s[stot-2]
states = []

for i in range(0, stot-1):
	states.append((s[i], s[i+1]))

# L'algoritmo da un peso base di uno per stati gia visitati, qua si puo
# settare un peso diverso per le transizioni di cui so il numero di occorrenze
peso = 5.

# Qui si puo settare la frequenza, ossia ogni quanti giorni andiamo a operare
freq = 21

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

def obtainNode(st, en):
	node = root
	w = str
	for t in range(st, en+1):
		if node.children==():
			node = generateChildren(node)
		approx1 = (int)(assets[t][0]*1000.-1000.)
		approx2 = (int)(assets[t][1]*1000.-1000.)
		for n in node.children:
			if approx1 >= n.state1[0] and approx1 <= n.state1[1] and approx2 >= n.state2[0] and approx2 <= n.state2[1]:
				node = n
	return node


# Algoritmo vero e proprio

# Inizializzo dei contatori per l'analisi finale
indecisioni = 0
primoasset = 0
secondoasset = 0

for i in range(0,l):
	print(i)
	if i > k:
		# Vediamo in che stato mi trovo ora, cioe l'ultima finestra lunga k
		state = obtainNode(i-k, i-1)

		# Prendo dal dizionario le frequenze passate e stimo il valore atteso
		v1 = 0.
		v2 = 0.

		if state.data > 0:
			#print("ci sono già stato\n")
			# Se sono gia stato in questo stato, semplicemente trovo empiricamente
			# Facendo un rapporto di frequenze le probabilita di transizione in ogni altro
			# Stato e calcolo il valore atteso del rendimento
			for n in state.children:
				increment1 = (1. + (n.state1[0] + n.state1[1])/2000.)
				increment2 = (1. + (n.state2[0] + n.state2[1])/2000.)
				#print(increment1)
				#print(increment2)
				if n.data > 0:
					#print("sono già stato nel figlio\n")
					# Se ho già fatto questo passaggio di stato
					v1 = v1 + increment1*(1. + peso*(float)(n.data))/((stot)**2 + peso*(float)(state.data))
					v2 = v2 + increment2*(1. + peso*(float)(n.data))/((stot)**2 + peso*(float)(state.data))
				else:
					#print("non sono mai stato nel figlio\n")
					# Se non ho ancora fatto questo passaggio di stato
					v1 = v1 + increment1*(1.)/((stot)**2 + peso*(float)(state.data))
					v2 = v2 + increment2*(1.)/((stot)**2 + peso*(float)(state.data))
			# Scelgo ora di puntare tutto sull'asset che mi da valore atteso maggiore, sto trascurando le covarianze
			if v1 > v2:
				portfolio = portfolio*assets[i][0]
				primoasset = primoasset + 1
			else:
				if v2 > v1:
					portfolio = portfolio*assets[i][1]
					secondoasset = secondoasset + 1
				else:
					portfolio = portfolio * (0.5*assets[i][0] + 0.5*assets[i][1])
					indecisioni = indecisioni + 1
		else:
			# Se non sono mai stato in questo stato
			portfolio = portfolio * (0.5*assets[i][0] + 0.5*assets[i][1])
			indecisioni = indecisioni + 1

		print(state)

		# A questo punto aggiorno il dizionario degli stati
		state = obtainNode(i-k+1, i)
		state.data = state.data+1

		state = obtainNode(i-k,i)
		state.data = state.data+1

	else:
		# Se e troppo presto
		portfolio = portfolio * (0.5*assets[i][0] + 0.5*assets[i][1])
		indecisioni = indecisioni + 1

	# Aggiornamenti vari
	portfolios.append(portfolio)
	print(portfolio)


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
print(l)
# Stampe varie

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
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale, scala semilogaritmica")
plt.show()
plt.plot(range(0,len(dd)), dd)
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.title("Drowdown")
plt.show()

# Output dei dati

filename = "../Results/Empirical_csv.txt"

file = open(filename, 'w')
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
file.write("Portafogli : \n")
for i in range(0,len(portfolios)):
	file.write(str(portfolios[i]) + "\n")

file.close()
