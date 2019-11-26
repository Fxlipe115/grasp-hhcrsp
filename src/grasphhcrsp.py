#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l), self.r)) + '\n' + \
            'DS' + '\n' + \
            ' '.join(str(x) for x in self.DS) + '\n' + \
            'a' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l), self.a)) + '\n' + \
            'x' + '\n' + \
            ' '.join(str(x) for x in self.x) + '\n' + \
            'y' + '\n' + \
            ' '.join(str(x) for x in self.y) + '\n' + \
            'd' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l), self.d)) + '\n' + \
            'p' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l), self.p)) + '\n' + \
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

    late=0
    listlates=[0]

    for car in matrix:
        for carserv in car:
            if(carserv.patient!=0 and carserv.patient != -1):
                late=carserv.end - patientList[carserv.patient].timeWindowEnd
                if late > 0:
                    listlates.append(late)

    return sum(listlates), max(listlates)


#Receives a list of visited nodes of ONE CAR and spits the distance list between all of them
#assuming we already have the distance matrix drawed from the instance file.
def buildsDistanceList(visitedNodes,instance):

    i=0
    distances=[]

    while(i<len(visitedNodes) - 1): # <=== doesn't go to the last element
        origin = visitedNodes[i].patient
        destination = visitedNodes[i+1].patient
        distances.append(instance.d[origin][destination])
        i+=1

    return distances


def getProcessingTime(instance,patientIdx,vehicleIdx,serviceIdx):
    return instance.p[patientIdx*instance.nbVehi+vehicleIdx][serviceIdx]

def buildCarServiceMatrix(instance,patientList,routes): #<========= felipe
    newmatrix = [[ carService(-1,-1,-1,-1) for i in range(instance.nbNodes) ] for j in range(instance.nbVehi)]

    indexlinha=0
    indexcoluna=0

    tempofinalanterior=0            #route[0][0] = [nodo,serviço] #route[0][1] = [nodo1,serviço1]

    for indexlinha,car in enumerate(routes):
        for indexcoluna,service in enumerate(car):
            newmatrix[indexlinha][indexcoluna].patient = service[0]
            newmatrix[indexlinha][indexcoluna].service = service[1]

            #print(service," ############################")
            #print(newmatrix[indexlinha][indexcoluna].patient, " FOR CAR", indexcoluna)
            if indexcoluna != 0 and indexcoluna!= len(routes[indexlinha])-1 and indexcoluna < len(routes[indexlinha])-1:
                newmatrix[indexlinha][indexcoluna].start = tempofinalanterior + instance.d[routes[indexlinha][indexcoluna][0]][routes[indexlinha][indexcoluna-1][0]]
                if newmatrix[indexlinha][indexcoluna].start < patientList[indexcoluna].timeWindowBegin:
                    newmatrix[indexlinha][indexcoluna].start = patientList[indexcoluna].timeWindowBegin
                newmatrix[indexlinha][indexcoluna].end = newmatrix[indexlinha][indexcoluna].start + getProcessingTime(instance,routes[indexlinha][indexcoluna][0],indexlinha,routes[indexlinha][indexcoluna][1])
                tempofinalanterior = newmatrix[indexlinha][indexcoluna].end
            else:
                newmatrix[indexlinha][indexcoluna].start = -1
                newmatrix[indexlinha][indexcoluna].end = -1

    #print(newmatrix[1][2].patient)
    return newmatrix


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

    totalDistance=0
    for car in carServiceMatrix:
        totalDistance += sum(buildsDistanceList(car, instance))

    lateness,biggestLate = allTheLateness(carServiceMatrix, instance.nbNodes, patientList)

    objectiveValue = totalDistance + lateness + biggestLate

    return objectiveValue

########################################## FUNÇÕES QUE CHECAM AS RESTRIÇÕES : #####################################

def outAndBackToGarage(visitedNodes):  #RESTRIÇÃO (5) DO ARTIGO

    firstNode = visitedNodes[0].node
    lastNode = visitedNodes[len(visitedNodes)-1].node

    xGarage = instance.x[0]
    yGarage = instance.y[0]

    if(instance.x[firstNode] == xGarage and instance.y[firstNode]== yGarage and instance.x[lastNode] == xGarage and instance.y[lastNode]==yGarage):
        return True
    else:
        return False


def geraPendentes(matriz,listadepacientes,numser):

    pendentes=[]

    for paciente in range(len(matriz)):
        for service in range(numser):
            if(listadepacientes[paciente]!= None and listadepacientes[paciente].requiredServices[service]==1 and matriz[paciente][service]==-1):
                pendentes.append([paciente,service])

    return pendentes

#recebe lista de serviços pendentes, numero de veiculos e a lista dos serviços dos veiculos
def geraRCL(pendentes, nveiculos, servicosveiculos,patientlist,instance):
    rcl = []
    for services in pendentes:
      #  print(services[0],"AAAAAAAAAAAAAAAAAAAAAAAA")
        for i in range(nveiculos):
            if (servicosveiculos[i][services[1]] == 1):
                rcl.append([i,services[0],services[1],custo(instance, services[0],i,services[1])]) #carro serviço nodo custo

    return rcl


def custo(instance,patient,vehic,service):
    return getProcessingTime(instance,patient,vehic,service)

    
    #   #Critério de Ordenação: Pacientes cujo final da janela de tempo ocorre mais cedo primeiro

def selectsCandidate(rcl, alpha):
    considerados = math.ceil(len(rcl) * alpha)
    rcl.sort(key=lambda x: x[3])

    return rcl[random.randrange(0,considerados)]

def commonServices(veiculo1,veiculo2,instance):
    common=[]

#    for i in range(instance.nbServi):
#        if(instance.a[veiculo1][i] == 1 and instance.a[veiculo2][i]==1):
#            common.append(i)

    return list(set(map(lambda x: x[1],veiculo1)).intersection(set(map(lambda x: x[1],veiculo2))))

#PENDENTES = (id paciente, id serviço)
#RCL = (id veículo, id paciente, id serviço, custo de atribuição na rota)

def greedyRandomizedAlgortithm(alpha,matrix,patientlist,instance):
    nveiculos = instance.nbVehi

    #TODOS CARROS SAEM DA GARAGEM:
    rotas=[[] for _ in range(nveiculos)]

    for i in range(nveiculos):
        rotas[i].append([0,-1])

    pendentes = geraPendentes(matrix,patientlist,instance.nbServi)
    pendentes.sort(key=lambda x: patientlist[x[0]].timeWindowEnd )


    while(len(pendentes) > 0):
        rcl = geraRCL(pendentes,instance.nbVehi,instance.a, patientlist,instance)

        chosen = selectsCandidate(rcl,alpha)

        rotas[chosen[0]].append([chosen[1], chosen[2]]) #rotas[veiculo escolhido].append(paciente escolhido, serviço escolhido)
        matrix[chosen[1]][chosen[2]] = chosen[0]

        pendentes.remove([chosen[1],chosen[2]])     # Retira dos pendentes, o (paciente,serviço) que foi selecionado

    for i in range(nveiculos):              #TODOS VEICULOS VOLTAM PRA GARAGEM
        rotas[i].append([0,-1])

    #print(rotas)

    return rotas


def swapPatients(route1,route2,service):
    patient1Idx = list(map(lambda x: x[1], route1)).index(service)
    patient2Idx = list(map(lambda x: x[1], route2)).index(service)

    route1[patient1Idx],route2[patient2Idx] = route2[patient2Idx],route1[patient1Idx]


def localSearch(instance,patientList,routes,numberOfNeighbours):
    


    current_state = copy(routes)
    carServiceMatrix = buildCarServiceMatrix(instance,patientList,routes)
    score_current = objective(instance, carServiceMatrix, patientList)

    episode=0
    iteration=0
    data=[]
    best_episode=-1

    def generate_Neighbours(S,numberOfNeighbours, routes, instancia, nveiculos,patientlist):

        new_neighbours = []
        for i in range(0,numberOfNeighbours):

            copiarotas = copy(routes)

            commonServ=[]

            while(len(commonServ) < 1):
                car1 = random.randrange(nveiculos)
                car2 = random.randrange(nveiculos)

                if(car1==car2):
                    car2 = random.randrange(nveiculos)

                commonServ = commonServices(copiarotas[car1],copiarotas[car2],instancia)
            #print(commonServ)
            #print(copiarotas[car1],copiarotas[car2])

            servico=random.randrange(len(commonServ))

            swapPatients(copiarotas[car1],copiarotas[car2],commonServ[servico])


            teste = buildCarServiceMatrix(instance,patientlist,copiarotas)

            if copiarotas not in new_neighbours:
                new_neighbours.append(copiarotas)

        return new_neighbours


    for i in range(1):

        #print("Generating Neighbours\n")
        neighbours = generate_Neighbours(routes,numberOfNeighbours,current_state,instance,instance.nbVehi,patientList)
  #      best_neighbour = current_state
  #      score_best_neighbour = objective(instance, carServiceMatrix, patientList)
  #      episode+=1
  #      best_score = score_current
        for current_neighbour in neighbours:
            carServiceMatrix = buildCarServiceMatrix(instance,patientList,current_neighbour) #Monta matriz do vizinho
            neighbourScore = objective(instance, carServiceMatrix, patientList) #Calcula Score do vizinho
            if neighbourScore < score_current:
                #print("Someone was better\n")
                current_state = copy(current_neighbour)
                score_current = neighbourScore
            #    best_episode=episode
            #    data.append((iteration,episode,score_best_neighbour))
            #episode+=1
        #if score_best_neighbour > score_current:
        #    current_state = best_neighbour
        #iteration+=1

    return current_state

def initialSolution(instance):
    ncarros = instance.nbVehi
    nPacientes = instance.nbNodes



def GRASP(maxIter, alpha, patientList, instance):

    score = float('inf')
    bestSolution=[]
    bestScore = 10000

    for i in range(maxIter):

        patientServiceMatrix = [[ -1 for i in range(columns) ] for j in range(rows)]

        S = greedyRandomizedAlgortithm(alpha, patientServiceMatrix, patientList, instance) #Solução inicial gulosa
        greedyServiceMatrix = buildCarServiceMatrix(instance,patientList,S) #Monta tempos
        greedyScore = objective(instance,greedyServiceMatrix,patientList)

        if(greedyScore < bestScore):
            bestSolution = copy(S)
            bestScore = greedyScore

        S = localSearch(instance,patientList,S,50)
        ServiceMatrix = buildCarServiceMatrix(instance,patientList,S)    #objective(instance, carServiceMatrix, patientList):
        newscore = objective(instance,ServiceMatrix,patientList)
                                                    #def buildCarServiceMatrix(instance,patientList,routes):
        if newscore < bestScore:
            bestSolution = copy(S)
            bestScore = newscore

    return bestSolution,bestScore





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GRASP-GGCRSP')
    parser.add_argument('-f', dest='file', required=True, help='The instance file.\n')
    parser.add_argument('-o', dest='outfile', help='Output Filename, for best solution and time elapsed')
    parser.add_argument('-x', dest='repetitions', help='Output Filename, for best solution and time elapsed')
    parser.add_argument('-a', dest='alpha', help='Output Filename, for best solution and time elapsed')

    random.seed()
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
    columns= instance.nbServi

    result,score=GRASP(int(args.repetitions),float(args.alpha),listPatients,instance)
    print(score)

     # <==== Initializing matrix of services given


    # serviceTimes[service1][service2]




    # always pass file=out parameter to print
    # just to test parameter reading
    # print(instance, file=out)

    # TODO everything else
