#!/usr/bin/env python3

import argparse
import sys
from functools import reduce
import random
import math
from copy import copy





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
    def __init__(self, windowB,windowE,requiredserv, isNeedful):
        self.timeWindowBegin = windowB
        self.timeWindowEnd = windowE
        self.requiredServices = requiredserv
        self.doubleservice = isNeedful

class vehicle:
    def __init__(self, givenServices):
        self.services = givenServices

class carService:
    def __init__(self,patient,service,b,e):
        self.patient = patient
        self.service = service
        self.start = b
        self.end = e




# Type of variable that will hold the time of start and end of a service given to a patient
class serviceTime:
    def __init__(self,start, end):
        self.beg = start
        self.end = end
        

def howLate(carService,numNodes, patientlist):

    if carService != None:
        if carService.patient != 0 and carService.patient != numNodes -1:
            lateness = carService.end - patientlist[carService.patient].timeWindowEnd
            if(lateness>0):
                return lateness
    return 0

#============================================================================REVIEW THIS FUNCTION BELOW FOR ME
#Returns both the sum of all late services, and the biggest of all
def allTheLateness(matrix, numNodes, patientList):
    allServices = reduce(lambda x,y: x+y, matrix,[])
    listOfLates= map(lambda x: howLate(x,numNodes,patientList), allServices)

    return sum(listOfLates), max(listOfLates)


#Receives a list of visited nodes of ONE CAR and spits the distance list between all of them
#assuming we already have the distance matrix drawed from the instance file.
def buildsDistanceList(visitedNodes,instance):

    i=0
    distances=[]

    while(i<visitedNodes.len() - 1): # <=== doesn't go to the last element
        origin = visitedNodes[i].node
        destination = visitedNodes[i+1].node
        distances.append(instance.d[origin][destination])
        i+=1

    return distances


def getProcessingTime(instance,patientIdx,vehicleIdx,serviceIdx):
    return instance.p[patientIdx*instance.nbVehi+vehicleIdx][serviceIdx]

def buildCarServiceMatrix(instance,patientList,routes):
    timesMatrix = []
    for vehicleIdx,route in enumerate(routes):
        times = [0]*instance.nbNodes
        for i in range(1,len(route)):
            times[i] = times[i-1] + getProcessingTime(instance,route[i][0],vehicleIdx,route[i][1])
        timesMatrix.append(times)

    carServiceMatrix = [[None]*instance.nbNodes for _ in range(instance.nbVehi)]
    for vehicleIdx,route in enumerate(routes):
        for i in range(1,len(route)-1):
            cs = carService(patientList[patientIdx],route[i][1],timesMatrix[vehicleIdx][route[i][0]],timesMatrix[vehicleIdx][route[i][0]]+getProcessingTime(instance,route[i][0],vehicleIdx,route[i][1]))
            carServiceMatrix[vehicleIdx][route[i][0]] = cs


def canItServeIt(vehicle,patient,service,instance): # ============ REVIEW THIS FUNCTION PLS

    if(instance.a[vehicle][service] == patient.requiredServices[service]):
            return true

    return false




def whoServedit(listofAllroutes, nservices, npatients):


    whoservedit = [[ -1 for i in range(nservices) ] for j in range(npatients)]

    for index,car in enumerate(listofAllroutes):
        for service in car:
            if(service.node!=0 and service.node != npatients-1):
                whoservedit[service.node][service.service] = index

    return whoservedit





# soma dos seguintes fatores seja mínima:  Distâncias percorridas pelos veículos;
# Soma dos atrasos nos atendimentos; Tempo do maior atraso observado na solução.

#listofVehiclesRoutes = List of lists, number of vehicles X maximum number of houses visiteds by a vehicle
#patientsTimes = a list of lists of elements of type serviceTime
def objective(instance, carServiceMatrix, patientList):

    for car in carServiceMatrix:
        totalDistance += sum(buildsDistanceList(car, instance))

    lateness,biggestLate = allTheLateness(carServiceMatrix, instance.nbNodes, patientList)

    objectiveValue = totalDistance + latness + biggestLate

    return objectiveValue

########################################## FUNÇÕES QUE CHECAM AS RESTRIÇÕES : #####################################

def outAndBackToGarage(visitedNodes):  #RESTRIÇÃO (5) DO ARTIGO

    firstNode = visitedNodes[0].node
    lastNode = visitedNodes[visitedNodes.len()-1].node

    xGarage = instance.x[0]
    yGarage = instance.y[0]

    if(instance.x[firstNode] == xGarage and instance.y[firstNode]== yGarage and instance.x[lastNode] == xGarage and instance.y[lastNode]==yGarage):
        return True
    else:
        return False

def TreatmentAfterWindowBegins(Allrouteslist,patientlist):

    for route in Allrouteslist:
        for service in route:
            if(patientlist[service.node] != None):
                if(service.start < patientlist[service.node].timeWindowBegin):
                return False
    return True

def noNegatives(Allrouteslist, numbernodes):      #RESTRIÇÃO (14) DO ARTIGO

    for route in Allrouteslist:
        for serv in route:
            if(serv.node != 0 and serv.node != numbernodes-1 and serv != None):
                if(serv.start <0):
                    return False


    return True

#checa uma linha da matriz de solução       RESTRIÇÃO (8) <====MELHORAR C DISTANCIAS
def timesAreIncreasing(visitedNodes):

    tempoanterior = 0
    nodoanterior=0

    for service in visitedNodes:
        if(service != None):
            if(service.start < tempoanterior):
                return False
            tempoanterior = service.start
            nodoanterior = service.node


    return True

def allServicesDone(patientlist,servedBy):

    index=0
    for patient in patientList:
        if patient != None:
            for i in range(nbServi):
                if(patient.requiredServices[i]==1 and servedBy[index][i] == -1):
                    return False
        index+=1

    return True

def geraPendentes(matriz,listadepacientes):

    pendentes=[]

    for i,paciente in enumerate(matriz):
        for servico in range(len(paciente)):
            if listadepacientes[i].requiredServices[servico]==1 and paciente[servico]==-1:
                pendentes.append([paciente,servico])

    return pendentes

#recebe lista de serviços pendentes, numero de veiculos e a lista dos serviços dos veiculos
def geraRCL(pendentes, nveiculos, servicosveiculos):
    rcl = []
    for services in pendentes:
        for i in range(nveiculos):
            if (servicosveiculos[i][services[1]] == 1):
                rcl.append([i,pendentes[0],pendentes[1],custo()]) #carro serviço nodo custo

    return rcl

def custo():
    pass
    #TODO

def selectsCandidate(rcl, alpha):
    considerados = math.ceil(rcl.length() * alpha)
    rcl.sort(key=lambda x: x[3])

    return rcl[random.randrange(0,considerados)]

def commonServices(veiculo1,veiculo2,instance):
    common=[]
    
    for i in range(instance.nbServi):
        if(instance.a[veiculo1][i] == 1 and instance.a[veiculo2][i]==1):
            common.append(i)

    return common

#PENDENTES = (id paciente, id serviço)
#RCL = (id veículo, id paciente, id serviço, custo de atribuição na rota)

def greedyRandomizedAlgortithm(alpha,matrix,patientlist,instance,nveiculos):

    #TODOS CARROS SAEM DA GARAGEM:


    rotas=[[] for _ in range(nveiculos)]

    for i in range(nveiculos):
        rotas[i].append([0,-1])

    pendentes = geraPendentes(matrix,patientlist) 

    while(pendentes.len() > 0):
        rcl = geraRCL(pendentes,instance.nbVehi,instance.a)

        chosen = selectsCandidate(rcl,alpha)

        rotas[chosen[0]].append([chosen[1], chosen[2]]) #rotas[veiculo escolhido].append(paciente escolhido, serviço escolhido)
        matrix[chosen[1]][chosen[2]] = t[0]

        pendentes.remove([chosen[1],chosen[2]])     # Retira dos pendentes, o (paciente,serviço) que foi selecionado
    
    for i in range(nveiculos):              #TODOS VEICULOS VOLTAM PRA GARAGEM
        rotas[i].append([0,-1])

    return rotas

def swapPatients(route1,route2,service):
    patient1Idx = list(map(lambda x: x[1], route1)).index(service)
    patient2Idx = list(map(lambda x: x[1], route2)).index(service)

    route1[patient1Idx],route2[patient2Idx] = route2[patient2Idx],route1[patient1Idx]

def isFeasible(S):
    # TODO
    return True

def repairSolution(S):
    # TODO
    return S

def f(S):
    # TODO
    return float('inf')

def localSearch(self,instance,patientList,routes,numberOfNeighbours):
    number_of_neighbours = 30

    carServiceMatrix = buildCarServiceMatrix(instance,patientList,routes)
    current_state = copy(routes)

    def generate_Neighbours(numberOfNeighbours, routes):
        new_neighbours = []
        for i in range(0,numberOfNeighbours):
            new_weights = list(weights)
            for j in range(len(new_weights)):
                randomChance = random.randint(0,2)
                if(randomChance==0):
                    new_weights[j]-=tiny_disturbance
                elif(randomChance==1):
                    new_weights[j]+=tiny_disturbance

            if(new_weights not in new_neighbours):
                new_neighbours.append(new_weights)
        return new_neighbours


    episode=0
    iteration=0
    data=[]
    score_current = objective(instance, carServiceMatrix, patientList)
    best_episode=-1
    for i in range(1):
        neighbours = generate_Neighbours(number_of_neighbours,weights)
        best_neighbour = current_state
        score_best_neighbour = objective(instance, carServiceMatrix, patientList)
        episode+=1
        best_score = score_current
        for current_neighbour in neighbours:
            carServiceMatrix = buildCarServiceMatrix(instance,patientList,current_state)
            cur_score = objective(instance, carServiceMatrix, patientList)
            if cur_score < score_best_neighbour:
                best_neighbour = current_neighbour
                best_score = cur_score
                best_episode=episode
                data.append((iteration,episode,score_best_neighbour))
            episode+=1
        if score_best_neighbour > score_current:
            current_state = best_neighbour
        iteration+=1

    return current_state

def GRASP(maxIter, alpha):
    score = float('inf')
    for i in range(maxIter):
        S = greedyRandomizedAlgortithm(alpha)
        if not isFeasible(S):
            S = repairSolution(S)
        S = localSearch(S)
        if f(S) < score:
            solution = S
            score = f(S)

    return solution





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
        newpatient = None
        if i!=0 and i!=instance.nbNodes-1:
            if i+1 in instance.DS:
                needy=1
            else:
                needy=0
            newpatient = patient(instance.e[i],instance.l[i],instance.r[i],needy)
        elif i==0 or i== instance.nbNodes-1:
            newpatient = None #REVIEW
        listPatients.append(newpatient)



    rows = instance.nbNodes
    columns=2

    serviceTimes = [[ 0 for i in range(columns) ] for j in range(rows)] # <==== Initializing matrix of services given
    serviceTimes[0] = None # <==== NODOS GARAGEM
    serviceTimes[rows-1] = None

    # serviceTimes[service1][service2]




    # always pass file=out parameter to print
    # just to test parameter reading
    # print(instance, file=out)

    # TODO everything else
