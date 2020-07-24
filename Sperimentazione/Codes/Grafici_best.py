from matplotlib import pyplot as plt
portfoliosg = []
portfolioss = []
portfoliosm = []
freq1 = 1
freq2 = 63
freq3 = 256

filename = "Universal_infinite2_best/giorn.txt"
f = open(filename, 'r')
for x in f:
	portfoliosg.append((float)(x))
	
filename = "Universal_infinite2_best/trimes.txt"
f = open(filename, 'r')
for x in f:
	portfolioss.append((float)(x))

filename = "Universal_infinite2_best/ann.txt"
f = open(filename, 'r')
for x in f:
	portfoliosm.append((float)(x))


wmaxg = 1.
ddg = []
ddmaxg = 0.
for i in range(0, len(portfoliosg)):
	wmaxg = max(wmaxg, portfoliosg[i])
	ddg.append(1.-portfoliosg[i]/wmaxg)
	if ddg[i] > ddmaxg:
		ddmaxg = ddg[i]

wmaxs = 1.
dds = []
ddmaxs = 0.
for i in range(0, len(portfolioss)):
	wmaxs = max(wmaxs, portfolioss[i])
	dds.append(1.-portfolioss[i]/wmaxs)
	if dds[i] > ddmaxs:
		ddmaxs = dds[i]

wmaxm = 1.
ddm = []
ddmaxm = 0.
for i in range(0, len(portfoliosm)):
	wmaxm = max(wmaxm, portfoliosm[i])
	ddm.append(1.-portfoliosm[i]/wmaxm)
	if ddm[i] > ddmaxm:
		ddmaxm = ddm[i]






plt.plot(range(0,len(portfoliosg)*freq1, freq1), portfoliosg, 'b', label='Giornaliero')
plt.plot(range(0,len(portfolioss)*freq2, freq2), portfolioss, 'g', label='Trimestrale')
plt.plot(range(0,len(portfoliosm)*freq3, freq3), portfoliosm, 'r', label='Annuale')
plt.title("Capitale")
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.legend()
plt.show()
plt.plot(range(0,len(portfoliosg)*freq1, freq1), portfoliosg, 'b', label='Giornaliero')
plt.plot(range(0,len(portfolioss)*freq2, freq2), portfolioss, 'g', label='Trimestrale')
plt.plot(range(0,len(portfoliosm)*freq3, freq3), portfoliosm, 'r', label='Annuale')
plt.yscale('log')
plt.ylabel('Capitale: S_t')
plt.xlabel('Periodo di investimento: t')
plt.title("Capitale, scala semilogaritmica")
plt.legend()
plt.show()
plt.plot(range(0,len(ddg)*freq1, freq1), ddg, 'b', label='Giornaliero')
plt.plot(range(0,len(dds)*freq2, freq2), dds, 'g', label='Trimestrale')
plt.plot(range(0,len(ddm)*freq3, freq3), ddm, 'r', label='Annuale')
plt.ylabel('Drowdown: dd(t)')
plt.xlabel('Periodo di investimento: t')
plt.title("Drowdown")
plt.legend()
plt.show()
