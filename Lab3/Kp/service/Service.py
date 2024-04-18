import time
import random
import itertools
import sys
from models.Backpack import Backpack
from models.Item import Object
import matplotlib.pyplot as plt


class Service:
    def __init__(self, backpack: Backpack):
        self.__backpack = backpack

    @property
    def backpack(self):
        return self.__backpack

    @backpack.setter
    def backpack(self, new_backpack):
        self.__backpack = new_backpack

    # FILE OPERATIONS

    def readFile(self, file_name):
        fileLinesList = []

        f = open("data/" + file_name, "r")
        fileLines = f.readlines()

        self.backpack.nr_objects = int(fileLines[0])
        self.backpack.max_weight = int(fileLines[-1])

        for line in fileLines:
            fileLinesList.append(line.split())

        listOfProperties = fileLinesList[1:-1]

        for properties in listOfProperties:
            object = Object()
            object.position = properties[0]
            object.value = properties[1]
            object.weight = properties[2]
            self.backpack.objects_list.append(object)

    def writeToFile(self, fileName, text):
        with open("data/" + fileName, "a") as f:
            f.write(text)
            f.write("\n")

    def saveSolutionToFile(self, fileName, bestIndividual, avgFitness, n, m, p, time):
        self.writeToFile(fileName, self.getSplitter())

        self.writeToFile(fileName,
                         self.formatSolutionToFile(bestIndividual, avgFitness, n, m, p, time))

        self.writeToFile(fileName, self.getSplitter())

    def getSplitter(self):
        return "------------------------------------------------------------------------------------------------"
               

    def formatSolutionToFile(self, bestIndividual, avgFitness, n, m, p, time):

        tableHeader = "|population    |generations  |mutation probability     |value best" \
            "  |value average        |time                     "

        solutionFormat = ""
        index = 0
        n_str = str(n)
        m_str = str(m)
        p_str = str(p)

        vb_str = str(bestIndividual[1])
        va_str = str(avgFitness)
        t_str = str(time)

        values = [n_str, m_str, p_str, vb_str, va_str, t_str]

        i = 0
        while i < len(tableHeader):

            if tableHeader[i] == "|":
                solutionFormat += tableHeader[i]
                for j in range(len(values[index])):
                    solutionFormat += values[index][j]
                i += len(values[index])
                index += 1

            else:
                solutionFormat += " "

            i += 1

        solutionFormat += "|"

        return solutionFormat

    # LOGIC OPERATIONS

    def createRandomSolution(self, nr_objects):
        solution = []

        for i in range(nr_objects):
            n = random.randint(0, 1)
            solution.append(n)

        return solution

    def createValidRandomSolution(self, nr_objects):
        while True:
            solution = self.createRandomSolution(nr_objects)
            if self.validateSolution(solution):
                return solution

    def validateSolution(self, solution):
        if self.solutionWeight(solution) <= self.__backpack.max_weight:
            return True
        else:
            return False

    def getSolutionFitness(self, solution):
        solutionFitness = 0

        for i in range(len(solution)):
            if solution[i] == 1:
                solutionFitness += int(self.__backpack.objects_list[i].value)

        return solutionFitness

    def __changeBit(self, bit):
        if bit == 1:
            return 0
        return 1

    def getEndOfInterval(self, number, set):
        largeSet = max(set)

        for element in set:
            if element >= number and element < largeSet:
                largeSet = element

        index = set.index(largeSet)

        return index

    def getBestIndividual(self, population):
        max_fitness = - sys.maxsize
        best = []

        for individ in population:
            if individ[1] >= max_fitness:
                max_fitness = individ[1]
                best.append((individ[0], individ[1]))

        return best[-1]

    def getAverageFitness(self, population):
        fitnessList = [individual[1] for individual in population]

        avgFitness = sum(fitnessList) // len(fitnessList)

        return avgFitness

    def solutionWeight(self, solution):
        totalWeight = 0

        for i in range(len(solution)):
            if solution[i] == 1:
                totalWeight += int(self.__backpack.objects_list[i].weight)

        return totalWeight

    def getListOfFitness(self, solutions_list):
        fitnessList = []

        for solution in solutions_list:
            fitnessList.append(self.getSolutionFitness(solution))

        return fitnessList

    def getSolutionWithMinWeight(self, solutions_list):
        weightList = []
        for solution in solutions_list:
            weightList.append(self.__solutionWeight(solution))

        for solution in solutions_list:
            if self.__solutionWeight(solution) == min(weightList):
                return solution

    def convertFromSolutionInvalidToValid(self, invalidSolution, maxWeight):

        weight = self.solutionWeight(invalidSolution)
        copyOfinvalidSolution = invalidSolution.copy()

        while weight > maxWeight:

            index = random.randint(0, len(invalidSolution) - 1)

            if invalidSolution[index] == 1:

                copyOfinvalidSolution[index] = 0
                weight -= int(self.__backpack.objects_list[index].weight)

        validSolution = copyOfinvalidSolution.copy()

        return validSolution

    # GRAPHICAL OPERATIONS

    def createGraph(self, results, numberOfPeople, maxNumberGenerations):

        t = []
        bestIndividual = []
        avgFitness = []

        for res in results:
            t.append(res[0])
            bestIndividual.append(res[1])
            avgFitness.append(res[2])

        plt.plot(t, bestIndividual, label="best", marker="o")
        plt.plot(t, avgFitness, label="average", marker="*")
        plt.xlabel('generations-axis')
        plt.ylabel('values-axis')
        plt.title(
            f'Results for: N = {numberOfPeople} and M = {maxNumberGenerations}')
        plt.legend()
        plt.show()
        plt.close()

    # EVOLUTIONARY ALGORITHM OPERATIONS

    def initializePopulation(self, numberOfPeople, nrObjects):
        population = []

        for i in range(numberOfPeople):
            individ = self.createValidRandomSolution(nrObjects)
            population.append((individ, self.solutionWeight(individ)))

        return population

    # TURNIR SELECTION- Se aleg aleator numberOfPeople cromozomi -> se alege cel mai performant
    def turnirSelection(self, numberOfPeople, population):
        parents = []

        for _ in range(numberOfPeople):
            index1 = random.randint(0, numberOfPeople - 1)

            while True:
                index2 = random.randint(0, numberOfPeople - 1)

                if index1 != index2:
                    break

            if population[index1][1] >= population[index2][1]:
                parents.append(population[index1])
            else:
                parents.append(population[index2])

        return parents

    # CROSSING WITH A SINGLE CUT POINT

    def crossingParents(self, population, nrObjects, parents, maxWeight):
        p_x = []

        for _ in range(len(population) // 2):

            crossedIndivid1 = []
            crossedIndivid2 = []

            cutPoint = random.randint(1, nrObjects)

            index1 = random.randint(0, len(population) - 1)

            while True:
                index2 = random.randint(0, len(population) - 1)

                if index1 != index2:
                    break

            individ_1 = parents[index1][0]
            individ_2 = parents[index2][0]

            for j in range(nrObjects):

                if j < cutPoint:
                    crossedIndivid1.append(individ_1[j])
                    crossedIndivid2.append(individ_2[j])
                else:
                    crossedIndivid1.append(individ_2[j])
                    crossedIndivid2.append(individ_1[j])

            if self.solutionWeight(crossedIndivid1) <= self.__backpack.max_weight:
                p_x.append(
                    (crossedIndivid1, self.getSolutionFitness(crossedIndivid1)))
            else:
                solution = self.convertFromSolutionInvalidToValid(crossedIndivid1,
                                                                  maxWeight)
                p_x.append((solution, self.getSolutionFitness(solution)))

            if self.solutionWeight(crossedIndivid2) <= self.__backpack.max_weight:
                p_x.append(
                    (crossedIndivid2, self.getSolutionFitness(crossedIndivid2)))
            else:
                solution = self.convertFromSolutionInvalidToValid(crossedIndivid2,
                                                                  maxWeight)
                p_x.append((solution, self.getSolutionFitness(solution)))

        return p_x
    

    def offspringCrossingMutationStrong(self, nrObjects, p_x, mutationProbability, maxWeight):
        p_m = []
        crossingSolutions = [p_x[index][0]
                             for index in range(len(p_x))]

        for i in range(len(p_x)):

            for j in range(nrObjects):

                q = round(random.random(), 2)

                if q < mutationProbability:
                    self.__changeBit(crossingSolutions[i][j])

            if self.solutionWeight(crossingSolutions[i]) <= self.__backpack.max_weight:
                p_m.append(
                    (crossingSolutions[i], self.getSolutionFitness(crossingSolutions[i])))
            else:
                solution = self.convertFromSolutionInvalidToValid(crossingSolutions[i],
                                                                  maxWeight)
                p_m.append((solution, self.getSolutionFitness(solution)))

        return p_m
    

    def offspringCrossingMutationWeak(self, nrObjects, p_x, mutationProbability, maxWeight):
        p_m = []
        crossingSolutions = [p_x[index][0]
                             for index in range(len(p_x))]

        for i in range(len(p_x)):

            for j in range(nrObjects):

                q = round(random.random(), 2)

                if q < mutationProbability:
                    crossingSolutions[i][j] = random.randint(0, 1)


            if self.solutionWeight(crossingSolutions[i]) <= self.__backpack.max_weight:
                p_m.append(
                    (crossingSolutions[i], self.getSolutionFitness(crossingSolutions[i])))
            else:
                solution = self.convertFromSolutionInvalidToValid(crossingSolutions[i],
                                                                  maxWeight)
                p_m.append((solution, self.getSolutionFitness(solution)))

        return p_m
    
    # def elitisticSelectionSurvivors(self, populationList, crossingList, mutationList):
    #     individsList = list(itertools.chain(populationList, crossingList, mutationList))
    #     individsList.sort()
    #     individsList = list(individsList for individsList, _ in itertools.groupby(individsList))

    #     oldGeneration = sorted(individsList, key=lambda individ: individ[1])
    #     newGeneration = []
    #     for i in range(len(populationList)):
    #         newGeneration.append(oldGeneration[i])
    #     return newGeneration


    def proportionalFitnessSelectionSurvivors(self, populationList, crossingList, mutationList):
        individsList = list(itertools.chain(populationList, crossingList, mutationList))
        random.shuffle(individsList)
        individsList.sort()
        individsList = list(individsList for individsList, _ in itertools.groupby(individsList))

        survivorsPopulation = []
        p = []
        qList = []

        F = 0
        for i in range(len(individsList)):
            F += individsList[i][1]

        for j in range(len(individsList)):
            p.append(individsList[j][1] / F)

        for k in range(len(individsList)):
            q = 0
            for m in range(k + 1):
                q += p[m]

            qList.append(q)

        for m in range(len(populationList)):
            g = round(random.random(), 2)

            if 0 <= g <= qList[0]:
                survivorsPopulation.append(individsList[0])
            else:
                index = self.getEndOfInterval(g, qList)
                survivorsPopulation.append(individsList[index])

        return survivorsPopulation

    def evolutionAlgorithm(self, numberOfPeople, maxNumberGenerations, nrObjects, mutationProbability,
                           maxWeight, outputFile):
        graph = []
        startTime = time.time()
        currentGeneration = 0

        population = self.initializePopulation(numberOfPeople, nrObjects)

        while currentGeneration < maxNumberGenerations:
            parents = self.turnirSelection(numberOfPeople, population)

            p_x = self.crossingParents(
                population, nrObjects, parents, maxWeight)


            p_m = self.offspringCrossingMutationStrong(
                nrObjects, p_x, mutationProbability, maxWeight)
            
            # p_m = self.offspringCrossingMutationWeak(
            #     nrObjects, p_x, mutationProbability, maxWeight)

            population = self.proportionalFitnessSelectionSurvivors(
                population, p_x, p_m)
            

            currentGeneration += 1

            bestIndividual = self.getBestIndividual(population)
            avgFitness = self.getAverageFitness(population)
            graph.append([currentGeneration, bestIndividual[1], avgFitness])

        endTime = time.time() - startTime
        # self.createGraph(graph, numberOfPeople, maxNumberGenerations)
        bestIndividual = self.getBestIndividual(population)
        avgFitness = self.getAverageFitness(population)

        self.saveSolutionToFile(outputFile, bestIndividual, avgFitness, numberOfPeople,
                                maxNumberGenerations, mutationProbability, endTime)
        return bestIndividual
