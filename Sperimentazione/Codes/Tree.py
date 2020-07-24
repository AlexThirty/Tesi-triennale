# importing modules 
import csv 
import numpy as np
from matplotlib import pyplot as plt
import statistics
import math
from scipy.special import gamma
from scipy.integrate import dblquad
from scipy import integrate

# Questo algoritmo sfrutta un procedimento suggerito dall'articolo di Algoet
# che si basa sull'algoritmo di Lempel-Ziv, ad ogni passo aggiorno l'albero
# di struttura tipico di tale algoritmo. Le probabilita di transizione sono date
# dal rapporto tra le dimensioni dei sottoalberi rispetto alla dimensione del nodo attuale
# Gli stati sono rappresentati da un intervallo di punti percentuali di rendimento dei due asset
# Viene quindi calcolato il valore atteso dell'outcome e scelto il titolo migliore
# Trascuro quindi le incertezze e le covarianze

# Qui vengono settate i principali valori

# Finestra di tempo che vado a considerare, si usa solo 1 in realta
# Gli altri casi richiederebbero una finestra temporale troppo ampia per diventare efficienti
k = 1

# Inizializzo i portafogli
portfolio= 1.
portfolios = []
portfolio2 = 1.

# Questi sono gli indicatori degli stati che andiamo a considerare
# Per come e scritto l'algoritmo ci interessano in realta gli intervalli tra questi valori
# Il primo e l'ultimo servono solo per considerare valori estremali
# Questi valori sono da intendersi in punti per mille di rendimento
s = [-10000, -100, -50, -10, -5, 0, 5, 10, 50, 100, 10000]

# Inizializzo il dizionario e variabili utili
di = {}
stot = len(s)
ma = s[stot-2]

# L'algoritmo da un peso base di uno per stati gia visitati, qua si puo
# settare un peso diverso per le transizioni di cui so il numero di occorrenze
peso = 10.

# Qui si puo settare la frequenza, ossia ogni quanti giorni andiamo a operare
freq = 21	

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

# Funzione che ottiene lo stato della catena in cui mi trovo
# Restituisce la stringa con cui viene salvato uno stato, semplicemente
# Ogni stato e rappresentato dal rendimento in punti percentuali dei due asset
# separati da una x
# Ogni singolo asset, invece, e rappresentato da un intervallo

def obtainword(st, en):
	w = ''
	for t in range(st, en+1):
		if t == st:
			approx = (int)(assets[t][0]*1000.-1000.)
			for a in range(1, stot):
				if approx <= s[a]:
					if a == 1:
						w = '<' + str(s[1]) + '%'
					else:
						if a == stot-1:
							w = '>' + str(s[a-1]) + '%'
						else:
							w = str(s[a-1]) + 'to' + str(s[a]) + '%'
					break
			approx = (int)(assets[t][1]*1000.-1000.)
			for a in range(1, stot):
				if approx <= s[a]:
					if a == 1:
						w = w + 'x' + '<' + str(s[1]) + '%'
					else:
						if a == stot-1:
							w = w + 'x' + '>' + str(s[a-1]) + '%'
						else:
							w = w + 'x' + str(s[a-1]) + 'to' + str(s[a]) + '%'
					break
		else:
			approx = (int)(assets[t][0]*1000.-1000.)
			for a in range(1, stot):
				if approx <= s[a]:
					if a == 1:
						w = w + ' ' + '<' + str(s[1]) + '%'
					else:
						if a == stot-1:
							w = w + ' ' + '>' + str(s[a-1]) + '%'
						else:
							w = w + ' ' + str(s[a-1]) + 'to' + str(s[a]) + '%'
					break
			approx = (int)(assets[t][1]*1000.-1000.)
			for a in range(1, stot):
				if approx <= s[a]:
					if a == 1:
						w = w + 'x' + '<' + str(s[1]) + '%'
					else:
						if a == stot-1:
							w = w + 'x' + '>' + str(s[a-1]) + '%'
						else:
							w = w + 'x' + str(s[a-1]) + 'to' + str(s[a]) + '%'
					break
	return w		

# Questa funzione aggiorna l'albero, ogni nodo avra infatti come valore
# Al suo interno la dimensione del suo sottoalbero: ogni volta quindi che continuo
# A muovermi all'interno di esso senza ripartire dalla radice (come nell'algoritmo di 
# Lempel-Ziv) vado ad aggiornare tutti i nodi della successione di stati che sto considerando

def aggiornaalbero(st, en):
	w = ''
	for t in range(st, en+1):
		if t == st:
			approx = (int)(assets[t][0]*1000.-1000.)
			for a in range(1, stot):
				if approx <= s[a]:
					if a == 1:
						w = '<' + str(s[1]) + '%'
					else:
						if a == stot-1:
							w = '>' + str(s[a-1]) + '%'
						else:
							w = str(s[a-1]) + 'to' + str(s[a]) + '%'
					break
			approx = (int)(assets[t][1]*1000.-1000.)
			for a in range(1, stot):
				if approx <= s[a]:
					if a == 1:
						w = w + 'x' + '<' + str(s[1]) + '%'
					else:
						if a == stot-1:
							w = w + 'x' + '>' + str(s[a-1]) + '%'
						else:
							w = w + 'x' + str(s[a-1]) + 'to' + str(s[a]) + '%'
					break
			di[w] = di[w]+1
		else:
			approx = (int)(assets[t][0]*1000.-1000.)
			for a in range(1, stot):
				if approx <= s[a]:
					if a == 1:
						w = w + ' ' + '<' + str(s[1]) + '%'
					else:
						if a == stot-1:
							w = w + ' ' + '>' + str(s[a-1]) + '%'
						else:
							w = w + ' ' + str(s[a-1]) + 'to' + str(s[a]) + '%'
					break
			approx = (int)(assets[t][1]*1000.-1000.)
			for a in range(1, stot):
				if approx <= s[a]:
					if a == 1:
						w = w + 'x' + '<' + str(s[1]) + '%'
					else:
						if a == stot-1:
							w = w + 'x' + '>' + str(s[a-1]) + '%'
						else:
							w = w + 'x' + str(s[a-1]) + 'to' + str(s[a]) + '%'
					break
			di[w] = di[w]+1


# Algoritmo vero e proprio

# Inizializzo dei contatori utili per l'analisi
indecisioni = 0
primoasset = 0
secondoasset = 0

# Il primo giorno non so nulla, mi mantengo equilibrato
portfolio = portfolio*(assets[0][0]*0.5 + assets[0][1]*0.5)
portfolios.append(portfolio)
indecisioni = indecisioni + 1

# Lo stato '' (stringa vuota) rappresenta la radice dell'albero
# Come valore al suo interno dovra avere il numero di giorni
di[''] = 1

state = obtainword(0,0)
di[state] = 1

state = ''

# La variabile profondity serve solamente come aiuto pratico per richiamare
# La funzione che aggiorna i valori dell'albero
profondity = 0

for i in range(1,l):
	print(i)
	
	# Aggiornamento dei valori del dizionario per l'ultimo outcome
	agg = ''
	di[agg] = di[agg]+1
	
	if profondity > 0:
		aggiornaalbero(i-profondity, i-1)
	
	# Stima dei valori attesi basandosi sulle dimensioni dei sottoalberi
	
	v1 = 0.
	v2 = 0.
	
	if state == '':
		# Caso in cui mi trovo nella radice
		for a in range(0,stot):
			for b in range(0,stot):
				if a == 0:
					increment1 = (1. + s[1]/1000.)
					newstate = state + '<' + str(s[1]) + '%'
				else:
					if a == stot-1:
						increment1 = (1. + s[a-1]/1000.)
						w = '>' + str(s[a-1]) + '%'
					else:
						increment1 = (1. + (s[a-1]+s[a])/2000.)
						newstate = state + str(s[a-1]) + 'to' + str(s[a]) + '%'
				if b == 0:
					increment2 = (1. + s[1]/1000.)
					newstate = newstate + 'x' + '<' + str(s[1]) + '%'
				else:
					if b == stot-1:
						increment2 = (1. + s[b-1]/1000.)
						w = '>' + str(s[b-1]) + '%'
					else:
						increment2 = (1. + (s[b-1]+s[b])/2000.)
						newstate = newstate + 'x' + str(s[b-1]) + 'to' + str(s[b]) + '%'
				if newstate in di:
					# Se ho gia fatto questo passaggio prima
					v1 = v1 + increment1*(1. + peso*(float)(di[newstate]))/((stot)**2 + peso*(float)(di[state]))
					v2 = v2 + increment2*(1. + peso*(float)(di[newstate]))/((stot)**2 + peso*(float)(di[state]))
				else:
					# Se non c'e mai stata questa transizione di stati
					v1 = v1 + increment1*(1.)/((stot)**2 + peso*(float)(di[state]))
					v2 = v2 + increment2*(1.)/((stot)**2 + peso*(float)(di[state]))
	else:
		# Caso in cui non mi trovo nella radice
		for a in range(0,stot):
			for b in range(0,stot):
				if a == 0:
					increment1 = (1. + s[1]/1000.)
					newstate = state + ' ' + '<' + str(s[1]) + '%'
				else:
					if a == stot-1:
						increment1 = (1. + s[a-1]/1000.)
						w = '>' + str(s[a-1]) + '%'
					else:
						increment1 = (1. + (s[a-1]+s[a])/2000.)
						newstate = state + ' ' + str(s[a-1]) + 'to' + str(s[a]) + '%'
				if b == 0:
					increment2 = (1. + s[1]/1000.)
					newstate = newstate + 'x' + '<' + str(s[1]) + '%'
				else:
					if b == stot-1:
						increment2 = (1. + s[b-1]/1000.)
						w = '>' + str(s[b-1]) + '%'
					else:
						increment2 = (1. + (s[b-1]+s[b])/2000.)
						newstate = newstate + 'x' + str(s[b-1]) + 'to' + str(s[b]) + '%'
				if newstate in di:
					# Se ho gia fatto questo passaggio prima
					v1 = v1 + increment1*(1. + peso*(float)(di[newstate]))/((stot)**2 + peso*(float)(di[state]))
					v2 = v2 + increment2*(1. + peso*(float)(di[newstate]))/((stot)**2 + peso*(float)(di[state]))
				else:
					# Se non c'e mai stata questa transizione di stati
					v1 = v1 + increment1*(1.)/((stot)**2 + peso*(float)(di[state]))
					v2 = v2 + increment2*(1.)/((stot)**2 + peso*(float)(di[state]))
	
	# Scelta e aggiornamento del portafoglio, sto scegliendo l'asset che mi da valore atteso empirico maggiore, trascurando le covarianze
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
	
	# Aggiornamento della profondita, in base a se sto aggiungendo un nuovo nodo 
	# o sto muovendomi ancora nell'albero, come secondo Lempel-Ziv
	state = obtainword(i-profondity,i)
	if state in di:
		profondity = profondity + 1
	else:
		di[state] = 1
		state = ''
		profondity = 0
	
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

print 'Massimo drowdown: ' + str(ddmax)
print 'Crescita media annua: ' + str(256*mum/freq)
print 'Deviazione standard annua: ' + str(16*sdev/(freq**0.5))
print 'Crescita media geometrica: ' + str(mug)
print 'Sharpe ratio: ' + str(sharpe)
print 'Calmar ratio: ' + str(calmar)
print 'Primo: ' + str(primoasset)
print 'Secondo: ' + str(secondoasset)
print 'Indecisioni: ' + str(indecisioni)

print 'Portafoglio finale: ' + str(portfolio)
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
plt.title("Drowndown")
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.show()

# Output dei dati

filename = "Tree.txt"

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
