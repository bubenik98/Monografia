####Importar o que precisa
import numpy as np
import random
from Create_Population import *
import time
'''def infection_prob_equation(x):
  P = 1-np.exp()'''

#collision_time = {}    #Conta o tempo em que uma colisão permanece acontecendo

'''def q(x, r, d, epsilon):
  return epsilon/(1+np.exp(r*(x-d)))

def Pedro_Func(collision_group, num_frames_for_hour, frame):                     # Esta é a equação do Pedro
  prob1 = 1
  prob2 = 1
  #print('.')
  p = 0.0001
  Q = 0.008
  Susceptible = collision_group[0][1]
  aux_collision_time = {}
  
  for collision in collision_group:    # É feita uma conversão de unidades te tempo, pois um frame não precisa ser 1 minuto
    Infected = collision[0]
    distance = collision[2]
    prob1 = prob1 * np.exp((-1)*p*q(distance, Infected.dilution_r,Infected.range_d , Infected.Infectivity_epsilon)*12*(60/num_frames_for_hour)*(frame - Susceptible.Collision_time[Infected.identity] + 1)/Q)
    prob2 = prob2 * np.exp((-1)*p*q(distance, Infected.dilution_r,Infected.range_d , Infected.Infectivity_epsilon)*12*(60/num_frames_for_hour)*(frame - Susceptible.Collision_time[Infected.identity])/Q)
    aux_collision_time[Infected.identity] = Susceptible.Collision_time[Infected.identity]
  
  Susceptible.Collision_time = aux_collision_time
  return abs(prob2 - prob1)'''

'''def Union(list1, list2):   #União de conjuntos, mas feito com listas
  for i in list1:
    if not i in list2:
      list2.append(i)
  return list2'''

def solve_collision(collision_set_dict, num_frames_for_day, frame):
  #print(collision_set_dict)


  for key in collision_set_dict:
 
    prob = 0.0003
    #print(prob)
    test = random.random()
    if test <= prob:
      collision_set_dict[key][0][1].Begin_Infection(num_frames_for_day, frame)



def Riley_Func(insiders, num_frames_for_day, integration_time, frame):
  p = 0.005
  Q = 400

  for classroom in list(insiders.keys()):

    prob = 1 - np.exp(len(insiders[classroom]['Infected'])*(-1)*p * 0 * integration_time/ Q)
    #print(prob)
    '''person.Infectivity_epsilon
    Verificar as unidades e a definição correta de person.Infectivity_epsilon ##################################
    Não Esquecer

    .    .     .     .    .   . . . . . . .     .... 

    '''
    
    #print(prob)

      #print(prob)
    for person in insiders[classroom]['Susceptible']:
      test = random.random()
      if test <= prob:
        person.Begin_Infection(num_frames_for_day, frame)
        
  #----------------------------------------------------------------------------------------------------------
  

def detect_collision(p1, p2, R):                  
# Detect the proximity between two persons and returns the validity word and the distance

  if abs(p2.Position[0]-p1.Position[0]) > R:
    validation = 0
  if abs(p2.Position[1]-p1.Position[1]) > R:
    validation = 0
  norm_squared = (p1.Position[1] - p2.Position[1])**2 + (p1.Position[0] - p2.Position[0])**2
  if norm_squared <= R**2:
    validation  = 1
  else:
    validation = 0
  #print(validation)
  return validation, norm_squared


def Sweep_n_prune(People,R, frame_step, num_frames_for_day, frame) -> None:
  """
  This function is responsible to detect all the possible "Collisions" ( pair of people that enter the maximum infectious radius of eachother) in a time complexity better than O(n^2), where n = len(People)
  """ 
  '''

  Para entender está função, favor assistir esse vídeo:
  ->  https://youtu.be/eED4bSkYCB8

  '''


  #Sort people by the x-axis
  New_People = []
  for key in People:
    New_People = New_People + People[key]
  New_People = sorted(New_People, key = lambda x : x.Position[0])
  active = []
  collision_set = {}
  insiders = {}
  aux = {0: 'Susceptible', 2: 'Infected', 3: 'Infected'}


  for i in New_People:
    
    if i.Quarantined == False:
      goal = i.Schedule[i.Time['day_of_week']][i.Time['hour']]
      if goal == '':
        if len(active)>1:
          
          #If there is at least one person in the active list and the interval of all the list coincides
          if np.abs(active[0].Position[0] - i.Position[0]) <= R:
            
            active.append(i)
          # If the new person does not bellong to the currente interval we check all the collisions in the active list
          else:
            #print(active)
            for j in range(len(active)):
              for k in range(j):
                if (active[j].Infect > 1 or active[k].Infect > 1) and not (active[j].Infect > 1 and active[k].Infect > 1 ) and not(active[j].Infect < 0 or active[k].Infect < 0 or active[j].Infect == 1 or active[k].Infect == 1):
                  validation, norm_squared = detect_collision(active[j], active[k], R)
                  if validation == 1:
                    if active[j].Infect > 1:
                     
                      if active[k].identity in collision_set:
                        collision_set[active[k].identity].append((active[j],active[k], np.sqrt(norm_squared)))
                      else:
                        collision_set[active[k].identity] = [(active[j],active[k], np.sqrt(norm_squared))]
                      if not active[j].identity in active[k].Collision_time:
                        active[k].Collision_time[active[j].identity] = frame
                    else:
                      if active[j].identity in collision_set:
                        collision_set[active[j].identity].append((active[k],active[j], np.sqrt(norm_squared)))
                      else:
                        collision_set[active[j].identity] = [(active[k],active[j], np.sqrt(norm_squared))]
                      if not active[k].identity in active[j].Collision_time:
                        active[j].Collision_time[active[k].identity] = frame
            # We then remove the first item of the active list, since all of his possible collsions have been checked
            active.remove(active[0])

            # We now start to remove all the itens of the active list, until the new item is in the interval of someone inside the active list or the active list is empty
            for j in active:
              if np.abs(j.Position[0] - i.Position[0]) <= R or len(active) == 0:
                active.append(i)
                break

              else:
                active.remove(j)
        else:
          active.append(i)
      elif frame_step == 0 and i.Time['hour'] in [8, 10, 12, 14, 16, 18, 19, 21]:       # Frame_step corresponde ao frame entre as horas, como se fosse minutos
        if i.Infect > 1 or i.Infect == 0:
          if not goal in insiders.keys():
            insiders[goal] = {'Susceptible':[], 'Infected':[]}

          insiders[goal][aux[i.Infect]].append(i)      # aux é usado como uma facilidade para saber em qual chave inserir o indivíduo

  if frame_step == 0:
    if i.Time['hour'] in [8,10,14,16,19,21]:      
      Riley_Func(insiders, num_frames_for_day, 2, frame)
    if i.Time['hour'] in [12, 18]:
      Riley_Func(insiders, num_frames_for_day, 1, frame)

  # We can now solve all the collisions
  # for i in collision_set:
  #print(collision_set)
  '''  if collision_set != {}:
    print(collision_set)'''
  solve_collision(collision_set, num_frames_for_day, frame)

  
'''People = {'Students':[], 'Professor': []}
for i in range(100):
  People['Students'].append(Student(0, False, False, {'day_of_week': 'Mon', 'hour': 7}, 20, 5, 15, 9, 0, 10*np.array([random.random(), random.random()]), False, 'IFGW'))

for i in range(100):
  People['Professor'].append(Professor(2, False, False, {'day_of_week': 'Mon', 'hour': 7}, 40, 5, 15, 9, 0, 10*np.array([random.random(), random.random()]), False, 'IFGW'))
for i in range(50):
  Sweep_n_prune(People, 1)

for i in People:
  for j in People[i]:
    print(j.Infect)'''