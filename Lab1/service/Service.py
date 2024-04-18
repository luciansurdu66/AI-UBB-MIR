import random
import time
from models.Backpack import Backpack
from models.Item import Object

class Service:
    def __init__(self, backpack: Backpack):
        self.__backpack = backpack

    @property
    def backpack(self):
        return self.__backpack

    @backpack.setter
    def backpack(self, new_backpack):
        self.__backpack = new_backpack

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

    def showFileContent(self, file_name):
        self.readFile(file_name)

        print(f'Content {file_name}: ')

        for object in self.backpack.objects_list:
            print(object.__str__())
        print(self.backpack.max_weight)

    @staticmethod
    def createRandomSolution(nr_objects):
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
        if self.__solutionWeight(solution) <= self.__backpack.max_weight:
            return True
        else:
            return False

    def getSolutionFitness(self, solution):
        solutionFitness = 0

        for i in range(len(solution)):
            if solution[i] == 1:
                solutionFitness += int(
                    self.__backpack.objects_list[i].value)

        return solutionFitness

    def getBestSolution(self, solutions_list):
        bestSolutions = []
        fitnessList = self.__getListOfFitness(solutions_list)

        for solution in solutions_list:
            if self.getSolutionFitness(solution) == max(fitnessList):
                bestSolutions.append(solution)

        if len(bestSolutions) == 1:
            return bestSolutions[0]
        else:
            return self.__getSolutionWithMinWeight(bestSolutions)

    def getAverageFitness(self, solutions_list):
        fitnessList = self.__getListOfFitness(solutions_list)

        averageFitness = sum(fitnessList) // len(fitnessList)

        return averageFitness

    def getWorstFitness(self, solutions_list):
        return min(self.__getListOfFitness(solutions_list))

    def __getSolutionWithMinWeight(self, solutions_list):
        weightList = []
        for solution in solutions_list:
            weightList.append(self.__solutionWeight(solution))

        for solution in solutions_list:
            if self.__solutionWeight(solution) == min(weightList):
                return solution

    def __solutionWeight(self, solution):
        totalWeight = 0

        for i in range(len(solution)):
            if solution[i] == 1:
                totalWeight += int(self.__backpack.objects_list[i].weight)

        return totalWeight

    def __getListOfFitness(self, solutions_list):
        fitnessList = []

        for solution in solutions_list:
            fitnessList.append(self.getSolutionFitness(solution))

        return fitnessList

    @staticmethod
    def createListOfObjects(nr_objects):
        objectsList = []

        for i in range(nr_objects):
            object = Object()
            value = int(input(f'Enter the value of the object {i+1}: '))
            weight = int(input(f'Enter the weight of the object {i+1}: '))
            object.value = value
            object.weight = weight
            objectsList.append(object)

        return objectsList

    def randomSearchWithSpecifiedData(self, k, nr_objects):
        validSolutions = []
        list_best_solution = []

        startTime = time.time()
        for j in range(10):
            for i in range(k):
                solution = self.createRandomSolution(nr_objects).copy()

                print(solution)
                print("solution: " + str(self.validateSolution(solution)))
                print("fitness: " + str(self.getSolutionFitness(solution)))
                print("weight: " + str(self.__solutionWeight(solution)))

                if self.validateSolution(solution):
                    validSolutions.append(solution)
            if len(validSolutions) != 0:
                best_solution = self.getBestSolution(validSolutions).copy()
                list_best_solution.append(self.getSolutionFitness(best_solution))
        print("best: " + str(max(list_best_solution)))
        print("average: " + str(sum(list_best_solution) // len(list_best_solution)))
        print("worst: " + str(min(list_best_solution)))

        endTime = time.time()

        if len(validSolutions) != 0:
            best_solution = self.getBestSolution(
                validSolutions).copy()
            average_fitness = self.getAverageFitness(
                validSolutions)
            worstFitness = self.getWorstFitness(
                validSolutions)

            print("\n")
            print(f'----- seconds {endTime - startTime} -------')
            print("\n")
            print(f'Best solution: {best_solution}, \n having'
                  f' the fitness: {self.getSolutionFitness(best_solution)} \n'
                  f' and the weight: {self.__solutionWeight(best_solution)} ')
            print("\n")
            print(f'Average fitness is: {average_fitness} ')
            print("\n")
            print(f'Worst fitness is: {worstFitness} ')
        else:
            print("There is no valid solution!")

    def randomSearchWithFileData(self, k, nr_objects):
        valid_solutions = []
        list_best_solutions = []

        startTime = time.time()
        for _ in range(10):
            for _ in range(k):
                solution = self.createRandomSolution(nr_objects).copy()

                print(solution)
                print("solution: " + str(self.validateSolution(solution)))
                print("fitness: " + str(self.getSolutionFitness(solution)))
                print("weight: " + str(self.__solutionWeight(solution)))

                if self.validateSolution(solution):
                    valid_solutions.append(solution)

            if len(valid_solutions) != 0:
                bestSolution = self.getBestSolution(valid_solutions).copy()
                list_best_solutions.append(self.getSolutionFitness(bestSolution))
        print("best: " + str(max(list_best_solutions)))
        print("average: " + str(sum(list_best_solutions) // len(list_best_solutions)))
        print("worst: " + str(min(list_best_solutions)))

        endTime = time.time()

        if len(valid_solutions) != 0:
            best_solution = self.getBestSolution(
                valid_solutions).copy()
            average_fitness = self.getAverageFitness(
                valid_solutions)
            worst_fitness = self.getWorstFitness(
                valid_solutions)

            print("\n")
            print(f'----- seconds {endTime - startTime} -------')
            print("\n")
            print(f'Best solution: {best_solution}, \n having'
                  f' the fitness: {self.getSolutionFitness(best_solution)} \n'
                  f' and the weight: {self.__solutionWeight(best_solution)} ')

            print("\n")
            print(f'Average fitness is: {average_fitness} ')
            print("\n")
            print(f'Worst fitness is: {worst_fitness} ')

        else:
            print("There is no valid solution!")

    def __createNeighbours(self, solution):
        neighbours = []

        for i in range(len(solution)):
            neighbour = solution.copy()
            neighbour[i] = self.__changeBit(solution[i])
            neighbours.append(neighbour)
        return neighbours

    def __changeBit(self, bit):
        if bit == 1:
            return 0
        return 1

    def nextAscentHillClimbing(self, k, nr_objects):
        best_solution = None
        best_fitness = -1
        evaluations = 0
        list_best_solution = []

        solution = self.createRandomSolution(nr_objects).copy()
        while evaluations < k:
            neighbours = self.__createNeighbours(solution)
            for neighbour in neighbours:
                evaluations += 1
                if evaluations >= k:
                    break
                if self.getSolutionFitness(neighbour) > self.getSolutionFitness(solution) and self.validateSolution(neighbour):
                    solution = neighbour.copy()
                    break
            elimport java.util.*;

public class Main {
    public static int computeSpeed(List<Integer> lights) {
        double maxSpeed = Double.POSITIVE_INFINITY;
        for (int i = 0; i < lights.size(); i += 2) {
            int distance = lights.get(i);
            int cycleTime = lights.get(i + 1);
            // Calculate the speed needed to reach the light before it turns red
            double speed = (double) distance / cycleTime;
            if (speed < maxSpeed) {
                maxSpeed = speed;
            }
        }
        // If maxSpeed is still its initial value, return 0, because it's impossible to go through all the lights while they're green.
        // Otherwise, return maxSpeed, rounded down to the nearest integer, because the speed must be an integer.
        // Also, ensure that the speed does not exceed the maximum speed limit of 100 km/h.
        return maxSpeed == Double.POSITIVE_INFINITY ? 0 : Math.min(100, (int) Math.floor(maxSpeed));
    }

    public static void main(String[] args) {
        List<Integer> lights = Arrays.asList(100, 10, 200, 10);
        int maxSpeed = computeSpeed(lights);
        System.out.println("Maximum speed: " + maxSpeed + " km/h");
    }
}se:
                break
            if best_solution is None or self.getSolutionFitness(solution) > best_fitness:
                best_solution = solution.copy()
                print(best_solution)
                print("solution: " + str(self.validateSolution(best_solution)))
                print("fitness: " + str(self.getSolutionFitness(best_solution)))
                print("weight: " + str(self.__solutionWeight(best_solution)))
                best_fitness = self.getSolutionFitness(best_solution)
            list_best_solution.append(best_fitness)
        print("\n-----------------\n")
        print(f"best: {max(list_best_solution)}")
        print(f"average: {sum(list_best_solution) // len(list_best_solution)}")
        print(f"worst: {min(list_best_solution)}")
        print(list_best_solution)
        return best_solution