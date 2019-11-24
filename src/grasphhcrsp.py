#!/usr/bin/env python3

import argparse
import sys





class HhcrspInstance:
    """An instance of the problem HHCRSP

    Attributes:
        nbNodes     Number of nodes in the network; note that the depot is counted as the first(0) and the last(ndNodes-1) node.
        nbVehi      Number of staff members (vehicles).
        nbServi     Number of service types.
        r           Service requirement of each patient.
        DS          Patients,who require double service.
        a           Qualification of staff members.
        x           x-coordinates of the nodes.
        y           y-coordinates of the nodes.
        d           Distance matrix.
        p           Processing time of each service at each patient provided by each staff member.
        mind        Minimal time gap between service activities for double service patients.
        maxd        Maximal time gap between service activities for double service patients.
        e           Beginning of time window.
        l           End of time window.
    """
    def __init__(self, file_path):
        with open(file_path) as f:
            _ = f.readline()
            self.nbNodes = int(f.readline())

            _ = f.readline()
            self.nbVehi = int(f.readline())

            _ = f.readline()
            self.nbServi = int(f.readline())

            _ = f.readline()
            self.r = []
            for i in range(self.nbNodes):
                self.r.append([int(x) for x in f.readline().split()])

            _ = f.readline()
            self.DS = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.a = []
            for i in range(self.nbVehi):
                self.a.append([int(x) for x in f.readline().split()])

            _ = f.readline()
            self.x = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.y = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.d = []
            for i in range(self.nbNodes):
                self.d.append([float(x) for x in f.readline().split()])

            _ = f.readline()
            self.p = []
            for i in range(self.nbNodes * self.nbVehi):
                self.p.append([float(x) for x in f.readline().split()])

            _ = f.readline()
            self.mind = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.maxd = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.e = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.l = [int(x) for x in f.readline().split()]

    def __str__(self):
        return 'nbNodes' + '\n' + \
            str(self.nbNodes) + '\n' + \
            'nbVehi' + '\n' + \
            str(self.nbVehi) + '\n' + \
            'nbServi' + '\n' + \
            str(self.nbServi) + '\n' + \
            'r' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l) ,self.r)) + '\n' + \
            'DS' + '\n' + \
            ' '.join(str(x) for x in self.DS) + '\n' + \
            'a' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l) ,self.a)) + '\n' + \
            'x' + '\n' + \
            ' '.join(str(x) for x in self.x) + '\n' + \
            'y' + '\n' + \
            ' '.join(str(x) for x in self.y) + '\n' + \
            'd' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l) ,self.d)) + '\n' + \
            'p' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l) ,self.p)) + '\n' + \
            'mind' + '\n' + \
            ' '.join(str(x) for x in self.mind) + '\n' + \
            'maxd' + '\n' + \
            ' '.join(str(x) for x in self.maxd) + '\n' + \
            'e' + '\n' + \
            ' '.join(str(x) for x in self.e) + '\n' + \
            'l' + '\n' + \
            ' '.join(str(x) for x in self.l)



class patient:
    timeWindowBegin=0
    timeWindowEnd=0
    requiredServices=0
    doubleservice=0

    def __init__(self, windowB,windowE,requiredserv, isNeedful):
        self.timeWindowBegin = windowB
        self.timeWindowEnd = windowE
        self.requiredServices = requiredserv
        self.doubleservice = isNeedful

class vehicle:
    def __init__(self, givenServices):
        self.services = givenServices





# Type of variable that will hold the time of start and end of a service given to a patient
class serviceTime:
    def __init__(self,start, end):
        self.beg = start
        self.end = end



def howLate(patient,endOfService):
    lateness = endOfService - patient.timeWindowEnd
    if(lateness <= 0):
        return 0
    else:
        return lateness

#============================================================================REVIEW THIS FUNCTION BELOW FOR ME
#Returns both the sum of all late services, and the biggest of all
def AlltheLateness(patients,serviceTimes):

    allLateness=0
    listofLates=[]
    index = 0

    for i in patients:
        late = howLate(i,serviceTimes[index][0].end)        #Gets how late was the service
        allLateness+=late
        listofLates.append(late)

        if(i.isNeedful == 1):                       #if patient requires two services, counts it too
            late = howLate(i,serviceTimes[index][1].end)
            allLateness+=late
            listofLates.append(late)

        index+=1

    return allLateness, max(listofLates), listofLates


#Receives a list of visited nodes of ONE CAR and spits the distance list between all of them
#assuming we already have the distance matrix drawed from the instance file.
def buildsDistanceList(visitedNodes):

    i=0
    distances=[]

    while(i<visitedNodes.len() - 1): # <=== doesn't go to the last element
        origin = visitedNodes[i]
        destination = visitedNodes[i+1]
        distances.append(instance.d[origin][destination])
        i+=1

    return distances


# soma dos seguintes fatores seja mínima:  Distâncias percorridas pelos veículos;
# Soma dos atrasos nos atendimentos; Tempo do maior atraso observado na solução.

#listofVehiclesRoutes = List of lists, number of vehicles X maximum number of houses visiteds by a vehicle
#patientsTimes = a list of lists of elements of type serviceTime
def objective(listofVehiclesRoutes , patientsTimes):

    for car in listofVehicles:
        totalDistance += sum(buildsDistanceList( listofVehiclesRoutes[car]) )

    lateness,biggestLate,listlates = AlltheLateness(patientsTimes)

    objectiveValue = totalDistance + latness + biggestLate

    return objectiveValue

########################################## FUNÇÕES QUE CHECAM AS RESTRIÇÕES : #####################################

def outAndBackToGarage(visitedNodes):  #RESTRIÇÃO (5) DO ARTIGO

    firstNode = visitedNodes[0]
    lastNode = visitedNodes[visitedNodes.len()-1]

    xGarage = instance.x[0]
    yGarage = instance.y[0]

    if(instance.x[firstNode] == xGarage and instance.y[firstNode]== yGarage and instance.x[lastNode] == xGarage and instance.y[lastNode]==yGarage):
        return true
    else:
        return false

def TreatmentAfterWindowBegins(serviceTimeList,patientlist): #RESTRIÇÃO (9) DO ARTIGO

    for person in serviceTimeList:      # Para cada linha (pessoa) na tabela de horários de serviços feitos
            if(serviceTimeList[person][0].beg < patientlist[person].timeWindowBegin): #Se horario de inicio do tratamento < começo da janela do paciente
                return false
            elif(patientlist[person].isNeedful==1):             #Se paciente quer 2 serviços
                if(serviceTimeList[person][1].beg < patientlist[person].timeWindowBegin): #checa o segundo horario de tratamento do paciente
                    return false

    return true

def noNegatives(serviceTimeList):      #RESTRIÇÃO (14) DO ARTIGO

    for person in serviceTimeList:
        if(person[0].beg < 0 or person[1].beg <0):    # <======= REVIEW THIS TO ME
            return false

    return true

def timesAreIncreasing(visitedNodes,servicetimes):
    pass
   # TODO

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GRASP-GGCRSP')
    parser.add_argument('-f', dest='file', required=True, help='The instance file.\n')
    parser.add_argument('-o', dest='outfile', help='Output Filename, for best solution and time elapsed')

    args = parser.parse_args()
    out = sys.stdout if args.outfile is None else open(args.outfile, 'w')

    instance = HhcrspInstance(args.file)

    # BUILDING A LIST OF ALL PATIENTS
    listPatients=[]

    for i in range(instance.nbNodes):
        if(i!=0 and i!=instance.nbNodes):
            if (i in instance.DS):
                needy=1
            else:
                needy=0

            newpatient = patient(instance.e[i],instance.l[i],instance.r[i],needy)
            listPatients.append(newpatient)

    rows = instance.nbNodes - 2 # <=== Correto eliminar os nodos garagem? i guess
    columns=2

    serviceTimes = [[ 0 for i in range(columns) ] for j in range(rows)] # <==== Initializing matrix of services given

    # serviceTimes[service1][service2]

    # always pass file=out parameter to print
    # just to test parameter reading
    # print(instance, file=out)

    # TODO everything else
