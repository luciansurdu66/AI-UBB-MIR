from models.City import City
import math
import random
import sys
import itertools
import time
import matplotlib.pyplot as plt


class Service:
    def readFile(self, file_name):
        cities = []
        fileLinesList = []

        f = open("data/" + file_name, "r")
        fileLines = f.readlines()

        for line in fileLines:
            fileLinesList.append(line.split())

        for properties in fileLinesList:
            city = City()
            city.index = properties[0]
            city.x_coord = properties[1]
            city.y_coord = properties[2]
            cities.append(city)
        return cities

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

    def createRandomSolution(self, cities):
        random.shuffle(cities)

        return cities

    def getDistanceBetweenCities(self, city_1, city_2):
        return int(math.sqrt((int(city_2.x_coord) - int(city_1.x_coord)) ** 2 +
                             (int(city_2.y_coord) - int(city_1.y_coord)) ** 2))

    def getTotalDistance(self, solution):
        totalDistance = 0

        for i in range(0, len(solution) - 1):
            totalDistance += self.getDistanceBetweenCities(
                solution[i], solution[i+1])

        totalDistance += self.getDistanceBetweenCities(
            solution[-1], solution[0])
        return totalDistance

    def createNeighbourUsing2Swap(self, solution):
        index_1 = random.randint(0, len(solution) - 1)

        while True:
            index_2 = random.randint(0, len(solution) - 1)

            if index_1 != index_2:
                break

        cityIndex1 = solution[index_1]
        solution[index_1] = solution[index_2]
        solution[index_2] = cityIndex1

        return solution

    def getEndOfInterval(self, number, set):
        largeSet = max(set)

        for element in set:
            if element >= number and element < largeSet:
                largeSet = element

        index = set.index(largeSet)

        return index

    def getBestIndividual(self, population):
        min_fitness = sys.maxsize
        best = []

        for individ in population:
            if individ[1] <= min_fitness:
                min_fitness = individ[1]
                best.append((individ[0], individ[1]))

        return best[-1]

    def getAverageFitness(self, population):
        fitnessList = [individual[1] for individual in population]

        avgFitness = sum(fitnessList) // len(fitnessList)

        return avgFitness

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

    # ---------EVOLUTIONARY ALGORITHM OPERATIONS-----------

    def initializePopulation(self, numberOfPeople, nrObjects):
        population = []

        for i in range(numberOfPeople):
            individ = self.createRandomSolution(nrObjects)
            population.append((individ, self.getTotalDistance(individ)))

        return population

    # TURNIR SELECTION

    def turnirSelection(self, numberOfPeople, population):
        parents = []

        for i in range(numberOfPeople):
            index1 = random.randint(0, numberOfPeople - 1)

            while True:
                index2 = random.randint(0, numberOfPeople - 1)

                if index1 != index2:
                    break

            if population[index1][1] <= population[index2][1]:
                parents.append(population[index1])
            else:
                parents.append(population[index2])

        return parents

    # CROSSING WITH TWO CUT POINTS ORDER CROSSOVER

    def crossingParents(self, cities, parents):
        p_x = []

        for i in range(len(parents) // 2):

            crossedIndivi1 = []
            crossedIndivid2 = []
            orderParent1 = []
            orderParent2 = []
            descendent1 = []
            descendent2 = []

            cutPoint1 = random.randint(1, len(cities) - 2)
            cutPoint2 = random.randint(cutPoint1 + 1, len(cities) - 1)
            index1 = random.randint(0, len(parents) - 1)

            while True:
                index2 = random.randint(0, len(parents) - 1)

                if index1 != index2:
                    break

            parent1 = parents[index1][0]
            parent2 = parents[index2][0]

            for index in range(cutPoint1, cutPoint2):
                crossedIndivi1.insert(index, parent1[index])
                crossedIndivid2.insert(index, parent2[index])

            for j in range(cutPoint2, len(cities)):
                orderParent1.append(parent1[j])
                orderParent2.append(parent2[j])

            for m in range(0, cutPoint2):
                orderParent1.append(parent1[m])
                orderParent2.append(parent2[m])

            for oras in orderParent1:
                if oras not in crossedIndivid2:
                    descendent2.append(oras)

            for oras in orderParent2:
                if oras not in crossedIndivi1:
                    descendent1.append(oras)

            p = 0
            for x in range(cutPoint2, len(cities)):
                crossedIndivi1.insert(x, descendent1[p])
                crossedIndivid2.insert(x, descendent2[p])
                p += 1

            for n in range(0, cutPoint1):
                crossedIndivi1.insert(n, descendent1[p])
                crossedIndivid2.insert(n, descendent2[p])
                p += 1

            p_x.append((crossedIndivi1, self.getTotalDistance(crossedIndivi1)))
            p_x.append(
                (crossedIndivid2, self.getTotalDistance(crossedIndivid2)))

        return p_x

    def crossingParents1cut(self, cities, parents):
        p_x = []

        for i in range(len(parents) // 2):

            crossedIndivi1 = []
            crossedIndivid2 = []
            orderParent1 = []
            orderParent2 = []
            descendent1 = []
            descendent2 = []

            cutPoint1 = random.randint(1, len(cities) - 2)
            index1 = random.randint(0, len(parents) - 1)

            while True:
                index2 = random.randint(0, len(parents) - 1)

                if index1 != index2:
                    break

            parent1 = parents[index1][0]
            parent2 = parents[index2][0]

            for j in range(cutPoint1, len(cities)):
                orderParent1.append(parent1[j])
                orderParent2.append(parent2[j])

            for m in range(0, cutPoint1):
                orderParent1.append(parent1[m])
                orderParent2.append(parent2[m])

            for oras in orderParent1:
                if oras not in crossedIndivid2:
                    descendent2.append(oras)

            for oras in orderParent2:
                if oras not in crossedIndivi1:
                    descendent1.append(oras)

            p = 0
            for x in range(cutPoint1, len(cities)):
                crossedIndivi1.insert(x, descendent1[p])
                crossedIndivid2.insert(x, descendent2[p])
                p += 1

            for n in range(0, cutPoint1):
                crossedIndivi1.insert(n, descendent1[p])
                crossedIndivid2.insert(n, descendent2[p])
                p += 1

            p_x.append((crossedIndivi1, self.getTotalDistance(crossedIndivi1)))
            p_x.append(
                (crossedIndivid2, self.getTotalDistance(crossedIndivid2)))

        return p_x

    def offspringCrossingMutation(self, p_x, mutationProbability):
        p_m = []
        crossingSolution = []

        for element in p_x:
            isChanged = False

            q = round(random.random(), 2)

            if q < mutationProbability:
                crossingSolution = self.createNeighbourUsing2Swap(element[0])
                isChanged = True

            if isChanged:
                p_m.append(
                    (crossingSolution, self.getTotalDistance(crossingSolution)))
            else:
                p_m.append(element)

        return p_m

    def scrambleMutation(self, p_x, mutationProbability):
        p_m = []
        for element in p_x:
            if random.random() < mutationProbability:
                index2 = random.randint(2, len(element[0]) - 1)
                index1 = random.randint(0, len(element[0]) - index2)
                subset = element[0][index1:index1 + index2]
                random.shuffle(subset)
                crossingSolution = element[0][:index1] + subset + element[0][index1 + index2:]
            else:
                crossingSolution = element[0]
            p_m.append((crossingSolution, self.getTotalDistance(crossingSolution)))
        return p_m
    

    def proportionalFitnessSelectionSurvivors(self, populationList, crossingList, mutationList):
        individsList = list(itertools.chain(
            populationList, crossingList, mutationList))
        random.shuffle(individsList)

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

    def evolutionAlgorithm(self, numberOfPeople, maxNumberGenerations, cities, mutationProbability, outputFile):
        graph = []
        startTime = time.time()
        currentGeneration = 0

        population = self.initializePopulation(numberOfPeople, cities)

        while currentGeneration < maxNumberGenerations:
            parents = self.turnirSelection(numberOfPeople, population)

            p_x = self.crossingParents(cities, parents)

            p_m = self.scrambleMutation(p_x, mutationProbability)

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
