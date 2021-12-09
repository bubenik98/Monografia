import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from Schedule import *
from Move import *
from Detect_colissions import *
from Create_Population import *
from matplotlib.animation import FuncAnimation
import time as tt
from matplotlib.lines import Line2D


'''
Creating necessary classes
'''
class University():
    def __init__(self, Coordinate):
        self.Coordinate = Coordinate
class Institute(University):
    def __init__(self, Coordinate):
        super().__init__(Coordinate)
        self.Area = 0
class Classroom(University):
    def __init__(self, Coordinate):
        super().__init__(Coordinate)
        self.Area = 0
class Restaurant(University):
    def __init__(self, Coordinate):
        super().__init__(Coordinate)
        self.Area = 0

places_dict = {'Bandeco': Restaurant(np.array([0,0])),'IMECC': Institute(np.array([-5,-5])), 'IFGW': Institute(np.array([5,5])), 'CB01': Classroom(np.array([-2,2])), 'CB02': Classroom(np.array([2,2])), 'CB03': Classroom(np.array([2, -2])), 'CB04': Classroom(np.array([4, -4])), 'CB05': Classroom(np.array([-4, 4]))}       
'''
Colocar as estruturas no places_dict
'''
num_students = 250     #Número de estudantes
num_professors = 20   #Número de alunos
num_frames = 4*5*17*49     #Número de frames (Precisa ser múltiplo de 5, de 4 e de 17)
num_weeks = 7
num_frames_for_week = int(num_frames/num_weeks)
num_frames_for_day = int(num_frames_for_week/5)
num_frames_for_hour = int(num_frames_for_day/17)     # 17 é o número de horas presentes na simulação
time_to_run = int(num_frames_for_hour/4)
hours = [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
days = ['Mon', 'Tue', 'Wed', 'Thu','Fri']
People = create_population(num_students, num_professors, num_frames_for_day)
classroom = ['CB01', 'CB02', 'CB03', 'CB04', 'CB05']    #Substitutir pelas salas de aula disponíveis
Generate_Schedule(People, classroom)
#print(People['Professors'][-1].Schedule)
Population = {'S':[], 'E': [], 'I': [], 'R': []}
time_step = 0
#listao = {}
fig, ax = plt.subplots(1,2, figsize = (15 * 1.2, 6 * 1.2))
t = num_frames
archives = []

path = os.getcwd()
path = path[0:len(path) - 10]
print(path)
os.mkdir(path + 'Imagens/')
for frame in range(t):
    start = tt.time()
    day_index = int(frame/num_frames_for_day)
    day_name = days[day_index % 5]
    hour = hours[int((frame - day_index * num_frames_for_day)/num_frames_for_hour)]
    time_step = frame - num_frames_for_day * day_index - num_frames_for_hour * (hour - 7)
    listao = {'x':[], 'y':[], 'color':[]}
    ax[0].clear()
    for place in places_dict:
        ax[0].scatter(places_dict[place].Coordinate[0], places_dict[place].Coordinate[1], c = 'gray', s = 50)
    ax[0].set_xlim(-10, 10)
    ax[0].set_ylim(-10, 10)
    
    for person_class in list(People.keys()):
        for person in People[person_class]:
            movement(person, places_dict, time_step, time_to_run, num_frames_for_hour, day_name, hour, num_frames_for_day, frame)
            
            ax[0].scatter(person.Position[0], person.Position[1], c = person.color, s = 15)
            '''listao['x'].append(person.Position[0])
            listao['y'].append(person.Position[1])
            listao['color'].append(person.color)'''
    ax[0].set_title(day_name + '-' + str(hour) + 'h')
    legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor = 'g', label='Suscetíveis', markersize=5),Line2D([0], [0], marker='o', color='w', markerfacecolor = 'gray', label='Estruturas', markersize=7),
                   Line2D([0], [0], marker='o', color='w', markerfacecolor = 'r', label='Infectados', markersize=5), Line2D([0], [0], marker='o', color='w', markerfacecolor = 'purple', label='Expostos', markersize=5), Line2D([0], [0], marker='o', color='w', markerfacecolor = 'y', label='Recuperados', markersize=5)]
    ax[0].legend(handles=legend_elements)
    name = str(frame) + '.csv'
    pd.DataFrame(listao).to_csv(os.getcwd()[:47] + name, index = False, sep = ';')
    archives.append([os.getcwd()[:47] + name, day_name, str(hour)])

    #print(People['Students'][0].Position)


    Sweep_n_prune(People, 2, time_step, num_frames_for_day, frame)    # Definir o raio mínimo de colisão
    time_step += 1
    time_step = time_step % num_frames_for_hour
    S = 0
    E = 0
    I = 0
    R = 0
    for classe in People:
        for person in People[classe]:
            if person.Infect == 0:
                S += 1
            if person.Infect == 1:
                E += 1
            if person.Infect > 1:
                I += 1
            if person.Infect < 0:
                R += 1
    Population['S'].append(S)
    Population['E'].append(E)
    Population['I'].append(I)
    Population['R'].append(R)
    ax[1].clear()
    time = np.arange(0, frame + 1, 1) / num_frames_for_day
    ax[1].plot(time, Population['S'], label = 'Susceptibles')
    ax[1].plot(time, Population['E'], label = 'Exposed')
    ax[1].plot(time, Population['I'], label = 'Infectious')
    ax[1].plot(time, Population['R'], label = 'Recovered')
    ax[1].legend()
    ax[1].grid(True)
    ax[1].set_xlabel('Day')
    ax[1].set_ylabel('Number of People')
    ax[1].set_title('Infection Evolution')
    ''' l = int(len(time)/4)
    days = np.array([time[l], time[2*l], time[3*l], time[4*l-1]])
    day_label = np.array([int(time[l]/num_frames_for_day), int(time[2*l]/num_frames_for_day), int(time[3*l]/num_frames_for_day), int(time[4*l-1]/num_frames_for_day)])
    ax[1].set_xticks(days, day_label)'''#, labels = np.arange(1, len(days)))
    plt.savefig(path + 'Imagens/' + str(frame) + '.png')
    end = tt.time()
    if frame == 0:
        print((end-start) * t/3600)
print(Population['R'][-1])
pd.DataFrame(Population).to_csv(path + 'Epidemiologia.csv', index = False, sep = ';')
time = np.arange(0, t, 1) / num_frames_for_day
#fig, ax = plt.subplots()
plt.close()
#anim = FuncAnimation(fig, func = Animation, frames = t, fargs = [archives, places_dict], interval = 0.1)
'''plt.plot(time, Population['S'], label = 'Susceptibles')
plt.plot(time, Population['E'], label = 'Exposed')
plt.plot(time, Population['I'], label = 'Infectious')
plt.plot(time, Population['R'], label = 'Recovered')
plt.legend()
plt.grid(True)
plt.xlabel('Day')
plt.ylabel('Number of People')
plt.title('Infection Evolution')
plt.savefig(path + 'Gráfico.png')
plt.close()'''