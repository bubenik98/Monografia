from math import ceil
import numpy as np
import random
from Create_Population import *
#import time

def Generate_Schedule(people, classrooms):    # people é um dicionário contendo alunos (Students) e professores (Professors). Cada chave é associada à lista das instâncias da respectiva classe associada
    
    num_students = len(people['Students'])    # numero de alunos
    num_professors = len(people['Professors'])     # Numero de professores
    credits = 24                         # número de créditos/horas-aula que cada aluno deve cumprir (tem que ser par)
    average_students_classroom = 70        # Número médio de estudantes comportados em cada sala (Não é uma cota superior)
    maximum_capacity = 50
    free_time = {}                     # Irá conter um dicionário com os horários livres de cada sala de aula

    for classroom in classrooms:
        free_time[classroom] = {'Mon':[8,10,14,16,19,21], 'Tue':[8,10,14,16,19,21], 'Wed':[8,10,14,16,19,21],'Thu':[8,10,14,16,19,21],'Fri':[8,10,14,16,19,21]}
    
    num_classes_needed = int(np.ceil(num_students/ average_students_classroom) * credits/2)   # Número necessário de aulas para suprir a demanda (Aulas são de 2 créditos/horas)
    num_classes_for_professor = np.ceil(num_classes_needed/num_professors)                  # Número máximo de aulas para cada professor
    
    professor_avaiability = []         # Esta lista conterá listas com os professores e o número de aulas disponíveis para o respectivo professor. É usada para controlar a distribuição de aulas para cada professor
    for prof in people['Professors']:
        professor_avaiability.append([prof, num_classes_for_professor])

    for type_people in people:                 # Inicializa uma agenda básica para todas as instâncias
        for person in people[type_people]:
            person.def_schedule({'Mon':{7:'',8:'',9:'',10:'',11:'',12:'Bandeco',13:'',14:'',15:'',16:'',17:'',18:'Bandeco',19:'',20:'',21:'',22:'',23:''}, 'Tue':{7:'',8:'',9:'',10:'',11:'',12:'Bandeco',13:'',14:'',15:'',16:'',17:'',18:'Bandeco',19:'',20:'',21:'',22:'',23:''}, 'Wed':{7:'',8:'',9:'',10:'',11:'',12:'Bandeco',13:'',14:'',15:'',16:'',17:'',18:'Bandeco',19:'',20:'',21:'',22:'',23:''}, 'Thu':{7:'',8:'',9:'',10:'',11:'',12:'Bandeco',13:'',14:'',15:'',16:'',17:'',18:'Bandeco',19:'',20:'',21:'',22:'',23:''}, 'Fri':{7:'',8:'',9:'',10:'',11:'',12:'Bandeco',13:'',14:'',15:'',16:'',17:'',18:'Bandeco',19:'',20:'',21:'',22:'',23:''}})
        

    class_offered = []    # Será usado para armazenar as aulas que serão oferecidas (possuem um professor disponível para ministrá-la)
    for i in range(num_classes_needed):             # Decide o lugar e horário das aulas e apaga a opção escolhida do dicionário de possibilidades (free_time)
        if len(list(free_time.keys())) != 0:
            classroom = np.random.choice(list(free_time.keys()))
            day = np.random.choice(list(free_time[classroom].keys()))
            hour = np.random.choice(free_time[classroom][day])
            free_time[classroom][day].remove(hour)
            if len(free_time[classroom][day]) == 0:
                del free_time[classroom][day]
            if len(list(free_time[classroom].keys())) == 0:
                del free_time[classroom]

            index = 0
            while professor_avaiability[index][0].Schedule[day][hour] != '' and index < len(professor_avaiability) - 1:     # Essa parte escolhe um professor livre, começando do primeiro e percorrendo a lista até achar. O Último professor, se for o caso, não é verificado aqui se está livre
                index = index + 1
            if professor_avaiability[index][0].Schedule[day][hour] == '':      # Está condição existe apenas para a remota possibilidade de nenhum professor estar livre. No 'While" acima, o último professor da lista é "aceito". Então, verificamos aqui se ele está livre. Caso não esteja, a aula é "cancelada" por falta de docentes
                professor_avaiability[index][1] -= 1
                professor_avaiability[index][0].Schedule[day][hour] = classroom
                professor_avaiability[index][0].Schedule[day][hour + 1] = classroom        # Aula de 2 horas
                if professor_avaiability[index][1] == 0:
                    del professor_avaiability[index]
                class_offered.append([day, hour, classroom, 0])      # [dia da aula, horário da aula, lugar da aula, númer de estudantes matriculados]

    for student in people['Students']:     
        cont_class = 0                         # Número de aulas atribuidas ao aluno
        class_deleted = []                     # Explicado abaixo
        while cont_class <= int(credits/2):
            if len(class_offered) != 0:      # Deve haver aulas disponíveis
                index = random.randint(0,len(class_offered)-1)        # Escolhe uma aula
                day = class_offered[index][0]
                hour = class_offered[index][1]
                classroom = class_offered[index][2]
                if student.Schedule[day][hour] == '':     # A aula é adicionada apenas se o aluno tiver o horário livre
                    cont_class += 1
                    student.Schedule[day][hour] = classroom
                    student.Schedule[day][hour + 1] = classroom
                    class_offered[index][3] += 1
                    if class_offered[index][3] > maximum_capacity:               # Se a aula está lotada, ela é retirada das opções
                        del class_offered[index]
                else:                                     # Se o aluno não está livre, a aula é apagada temporariamente de class_offered e armazenada em class_deleted para posterior recuperação
                    class_deleted.append(class_offered[index])
                    del class_offered[index]
            else:
                cont_class = credits            # Para sair do While, já que não temos mais aulas para esse aluno
        class_offered = class_offered + class_deleted

    
    return None

'''class People():
    def __init__(self):
        self.Schedule = {}
        
class Student(People):
    def __init__(self):
        self.Schedule = {}
class Professor():
    def __init__(self):
        self.Schedule = {}
'''
'''n_alunos = 100000
n_professores = 3000'''
'''people = {'Students':[], 'Professors':[]}
for i in range(n_alunos):
    people['Students'].append(Student())
for j in range(n_professores):
    people['Professors'].append(Professor())
'''
'''num_classes_needed = np.ceil(n_alunos/ 50) * 12   # Número necessário de aulas para suprir a demanda (Aulas são de 2 créditos/horas)
num_classes_for_professor = np.ceil(num_classes_needed/n_professores)
'''
#print(num_classes_for_professor)
'''room = []
for i in range(1000):
    room.append('CB' + str(i))
print(room)
Generate_Schedule(people, room)'''
