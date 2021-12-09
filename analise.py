'''
----------------------------------------------------------------------------------------------------------
Usado para criar um vídeo, após rodar a simulação (arquivo Main.py)
----------------------------------------------------------------------------------------------------------
'''


import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import os

def f(x, a, b):
    return a * x + b

path = os.getcwd()
path = path[0:len(path) - 20]
path = os.path.join(path, 'Simulações')
path = os.path.join(path, 'p = 0.0003, q = 100')
print(os.listdir(path))
file_name = 'Epidemiologia.csv'
file = os.path.join(path,file_name)
df = pd.read_csv(file, sep = ';')
#print(df)
I = np.log(df['I'].values)
time = np.arange(0, len(I), 1)/(17*4*4)
plt.plot(time, I, '--', label = '100 partículas virais por hora')
I = I[:1500]
time = np.arange(0, len(I), 1)/(17*4*4)
popt, pcov = curve_fit(f, time, I, p0 = [9, 0])
print(popt[0]*9+1)
#plt.plot(time, f(time, popt[0], popt[1]), 'r', label = 'linear fit')

path = os.getcwd()
path = path[0:len(path) - 20]
path = os.path.join(path, 'Simulações')
path = os.path.join(path, 'p = 0.0003, q = 50')
print(os.listdir(path))
file_name = 'Epidemiologia.csv'
file = os.path.join(path,file_name)
df = pd.read_csv(file, sep = ';')
#print(df)
I = np.log(df['I'].values)
time = np.arange(0, len(I), 1)/(17*4*4)
plt.plot(time, I, '--', label = '50 partículas virais por hora')
I = I[:1500]
time = np.arange(0, len(I), 1)/(17*4*4)
popt, pcov = curve_fit(f, time, I, p0 = [9, 0])
print(popt[0]*9+1)
#plt.plot(time, f(time, popt[0], popt[1]), 'r', label = 'linear fit2')

path = os.getcwd()
path = path[0:len(path) - 20]
path = os.path.join(path, 'Simulações')
path = os.path.join(path, 'p = 0.0003, q = 0')
print(os.listdir(path))
file_name = 'Epidemiologia.csv'
file = os.path.join(path,file_name)
df = pd.read_csv(file, sep = ';')
#print(df)
I = np.log(df['I'].values)
time = np.arange(0, len(I), 1)/(17*4*4)
plt.plot(time, I, '--', label = '0 partículas virais por hora')
I = I[:1500]
time = np.arange(0, len(I), 1)/(17*4*4)
popt, pcov = curve_fit(f, time, I, p0 = [9, 0])
print(popt[0]*9+1)
#plt.plot(time, f(time, popt[0], popt[1]), 'r', label = 'linear fit')

plt.xlabel('Day')
plt.ylabel('Infectious - logarithmic scale')
plt.title('Infection Evolution')
plt.grid(True)
plt.legend()
plt.savefig(path + '/Fit R_0 teste.png')

plt.show()
