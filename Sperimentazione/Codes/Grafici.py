from matplotlib import pyplot as plt
import numpy as np
portfolios = []
freq = 1

filename = "Tree_txt.txt"
f = open(filename, 'r')
for x in f:
	portfolios.append((float)(x))
	

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

sharpe = 20*mum/(sdev*(freq**0.5))
calmar = 20*mum/(ddmax*freq)

mug = portfolios[len(portfolios)-1]**(1./(len(portfolios)))-1




plt.plot(range(0,len(portfolios)*freq, freq), portfolios, 'b', label='Giornaliero')
plt.title("Capitale")
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.show()
plt.plot(range(0,len(portfolios)*freq, freq), portfolios, 'b', label='Giornaliero')
plt.yscale('log')
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale, scala semilogaritmica")
plt.show()
plt.plot(range(0,len(dd)*freq, freq), dd, 'b', label='Giornaliero')
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.title("Drowdown")
plt.show()

filename = "Prove_random/Tree_txt_new.txt"

file = open(filename, 'w')
file.write("Massimo drowdown: " + str(ddmax) + "\n")
file.write("Crescita media giornaliera: " + str(400*mum/freq) + "\n")
file.write("Deviazione standard giornaliera: " + str(20*sdev/(freq**0.5)) + "\n")
file.write("Crescita media geometrica: " + str(mug) + "\n")
file.write("Sharpe ratio: " + str(sharpe) + "\n")
file.write("Calmar ratio: " + str(calmar) + "\n")
file.write("Portafoglio finale: " + str(portfolios[len(portfolios)-1]) + "\n")
file.write("Portafogli : \n")
for i in range(0,len(portfolios)):
	file.write(str(portfolios[i]) + "\n")

file.close()
