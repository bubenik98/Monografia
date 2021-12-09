import random
import numpy as np

'''
-> Parâmetros people.infect
    -> 0 = Suscetível
    -> 1 = Exposto
    -> 2 = Sintomático
    -> 3 = Assintomático
    -> -1 = Recuperado
    -> -2 = Morto
'''


class people():
    def __init__(self, Infect, Vaccinated, Quarantined, Time, Age, Death_Period, Position, Imune, Institute, identity):
        self.Infect = Infect
        self.Vaccinated = Vaccinated
        self.Quarantined  = Quarantined
        self.Time = Time
        self.Age = Age
        self.Collision_time = {}
        self.Incubation_Period = -1
        self.Death_Period = Death_Period
        self.Recover_Period = -1
        self.Death_Period = -1
        self.Infectivity_epsilon = None
        self.Position = Position
        self.Imune = Imune
        self.Institute = Institute
        self.Schedule = None
        self.identity = identity
        self.dilution_r = None
        self.range_d = None
        self.Prob_to_Die = None
        self.color =  {0:"Green", 1: 'purple' , 2:"Red", 3:"blue", -1:'yellow', -2:'black' }[self.Infect]

    def def_schedule(self, schedule):
        self.Schedule = schedule

    def Att_color(self):
        if self.Quarantined:
            self.color = 'white'
        else:
            self.color =  {0:"Green", 1: 'purple' , 2:"Red", 3:"blue", -1:'yellow', -2:'black' }[self.Infect]

    def Att_Position(self, velocity, day, hour, num_frames_for_day, frame):
        
        prob_Quarentine = 0     # Definir a eficiencia da quarentena
        #v = np.linalg.norm(velocity)
        aux = self.Position + velocity
        #print(np.linalg.norm(aux - self.Position))
        self.Position = aux
        self.Time['day_of_week'] = day
        self.Time['hour'] = hour
        if self.Recover_Period == frame:
            self.Infect = -1
            self.Quarentined = False
            self.Att_color()        
            '''elif self.Death_Period == frame:
            self.Infect == -2
            self.Quarentined = False
            self.Att_color()'''
        elif self.Incubation_Period == frame:
            if random.random() >= self.Prob_to_Die:      #Chance de morrer
                time = np.random.gamma(16.2, 0.56)
                self.Recover_Period = np.round(time * num_frames_for_day) + frame
                if random.random() <= 1:              #Sintomático ou assintomático (Não sei as probabilidades)
                    self.Infect = 2
                    if random.random() < prob_Quarentine:
                        self.Quarentined = True       # Não altero posição, por que o indivíduo se torna uma entidade neutra
                else:
                    self.Infect = 3

            else:
                time = np.random.lognormal(2.84, 0.58)
                self.Death_Period = np.round(time * num_frames_for_day) + frame    #Calculo o horário se mudar de estado por que achei mais fácil. Não que mude algo...
                self.Infect = 2
            
                if random.random() < prob_Quarentine:
                    self.Quarentined = True
            self.Att_color()

    def Begin_Infection(self, num_frames_for_day, frame):
        self.Infect = 1
        #self.Infectivity_epsilon = np.log(1-np.random.gamma(1.88, 0.008))/np.log(0.999306)  #Função gamma - Parâmetros definidos pelo Pedro
        #self.dilution_r = abs(np.random.normal(5, 2))      ### Tirar o abs
        #self.range_d = abs(np.random.normal(1, 0.3))
        time = np.random.lognormal(1.5, 0.6)
        self.Incubation_Period = np.round(time * num_frames_for_day) + frame
        self.Prob_to_Die = 0 # 0.0000457*np.exp(0.08952*self.Age)
        self.Att_color()
class Student(people):
    def __init__(self, Infect, Vaccinated, Quarantined, Time, Age, Death_Period, Position, Imune, Institute, identity):
        super().__init__(Infect, Vaccinated, Quarantined, Time, Age, Death_Period, Position, Imune, Institute, identity)
class Professor(people):
    def __init__(self, Infect, Vaccinated, Quarantined, Time, Age, Death_Period, Position, Imune, Institute, identity):
        super().__init__(Infect, Vaccinated, Quarantined, Time, Age, Death_Period, Position, Imune, Institute, identity)

def create_population(n_students, n_professor, num_frames_for_day):

    People = {'Students':[], 'Professors': []}

    for i in range(n_students - 1):
        People['Students'].append(Student(0, False, False, {'day_of_week': 'Mon', 'hour': 7}, 20, 5, 5*np.array([random.random(), random.random()]), False, np.random.choice(['IFGW', 'IMECC']), str(i)))
    People['Students'].append(Student(2, False, False, {'day_of_week': 'Mon', 'hour': 7}, 20, 5, np.array([random.random(), random.random()]), False, np.random.choice(['IFGW', 'IMECC']), str(i)))
    People['Students'][-1].Recover_Period = np.round(np.random.gamma(16.2, 0.56) * num_frames_for_day)
    #People['Students'][-1].Infectivity_epsilon = np.log(1-np.random.gamma(1.88, 0.008))/np.log(0.999306)
    #People['Students'][-1].dilution_r = abs(np.random.normal(5, 2))
    #People['Students'][-1].range_d = abs(np.random.normal(1, 0.3))
    People['Students'][-1].Prob_to_Die = 0
    #print(num_frames_for_day)
    #print(People['Students'][0].Incubation_Period)
    for i in range(n_professor):
        People['Professors'].append(Professor(0, False, False, {'day_of_week': 'Mon', 'hour': 7}, 40, 5, 5*np.array([random.random(), random.random()]), False, np.random.choice(['IFGW', 'IMECC']), str(n_students*i)))
    
    return People
