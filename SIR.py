import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
def func(t, x, R_0, gamma):
    S = x[0]
    I = x[1]
    R = x[2]
    beta = R_0 * gamma
    N = S + I + R
    dS = -beta * I * S / N
    dI = beta * I * S / N - gamma * I
    dR = gamma * I
    return dS, dI, dR
gamma = 1/14
R_0 = 4
time = 360
interval = np.arange(0, time)

y = solve_ivp(lambda t, x: func(t, x, R_0, gamma), (0, time), y0 = (200e6 - 1, 1,0), t_eval = interval )

plt.plot(y.t, y.y[0]/1e6, label = 'Susceptible')
plt.plot(y.t, y.y[1]/1e6, label = 'Infected')
plt.plot(y.t, y.y[2]/1e6, label = 'recovered')
plt.legend()
plt.grid(True)
plt.xlabel('Dias')
plt.ylabel('Milhões de pessoas')
plt.title('Modelo SIR')
plt.savefig('Graph_Mono.png')
plt.show()
