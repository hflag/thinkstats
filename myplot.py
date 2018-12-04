import survey
import Pmf
import matplotlib.pyplot as plt
import numpy as np


table = survey.Pregnancies()
table.readRecords(data_dir='data')

firsts_babies = survey.Pregnancies()
others_babies = survey.Pregnancies()

for r in table.records:
    if r.outcome != 1:
        continue
    if r.birthord == 1:
        firsts_babies.addRecord(r)
    else:
        others_babies.addRecord(r)

firsts_prglengths = [r.prglength for r in firsts_babies.records]
others_prglengths = [r.prglength for r in others_babies.records]

firts_hist = Pmf.Hist(firsts_prglengths)
others_hist = Pmf.Hist(others_prglengths)

times1, values1 = firts_hist.render()
times2, values2 = others_hist.render()
times2 = np.array(times2)


plt.bar(times1, values1, width=0.45)
plt.bar(times2+0.45, values2, width=0.45)
plt.show()
