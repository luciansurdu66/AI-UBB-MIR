import random
import math
from models.City import City

class Service:
    
    def read_file(self):
        cities = []
        lines = []
        
        f = open("data/cities.txt", "r")
        file_lines = f.readlines()
        
        for line in file_lines:
            lines.append(line.strip())
            
        for properties in lines:
            city = City()
            city.index = int(properties.split(" ")[0])
            city.x = int(properties.split(" ")[1])
            city.y = int(properties.split(" ")[2])
            cities.append(city)
        return cities
    
    def distance_between_cities(self, city1, city2):
        return math.sqrt((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2)
    
    def create_random_solution(self):
        cities = self.read_file()
        random.shuffle(cities)
        return cities
    
    def get_total_distance(self, cities):
        total_distance = 0
        for i in range(len(cities) - 1):
            total_distance += self.distance_between_cities(cities[i], cities[i + 1])
        total_distance += self.distance_between_cities(cities[-1], cities[0])
        return total_distance
    
    def create_neighbour_using_2swap(self, solution):
        new_solution = solution.copy()
        index1 = random.randint(0, len(new_solution) - 1)
        index2 = random.randint(0, len(new_solution) - 1)
        while index1 == index2:
            index2 = random.randint(0, len(new_solution) - 1)
        new_solution[index1], new_solution[index2] = new_solution[index2], new_solution[index1]
        return new_solution
    
    def get_best_solution(self, solutions_list):
        fitnessesList = self.get_list_of_fitness(solutions_list)

        for solution in solutions_list:
            if self.get_total_distance(solution) == min(fitnessesList):
                return solution

    def getAverageFitness(self, solutions_list):
        fitnessesList = self.get_list_of_fitness(solutions_list)

        avgFitness = sum(fitnessesList) // len(fitnessesList)

        return avgFitness

    def get_list_of_fitness(self, solutions_list):
        fitnessesList = []

        for solution in solutions_list:
            fitnessesList.append(self.get_total_distance(solution))

        return fitnessesList

    def travelling_salesman_problem(self, initial_temp, nr_iterations, cooling_rate, min_temperature):
        temperature = initial_temp

        c = self.create_random_solution()
        best = c

        evaluateBest = self.get_total_distance(best)
        evaluateC = self.get_total_distance(c)

        while temperature > min_temperature:

            initialIterationsNumber = nr_iterations
            while initialIterationsNumber:
                x = self.create_neighbour_using_2swap(c)
                evaluateX = self.get_total_distance(x)

                delta = evaluateX - evaluateC

                if delta < 0:
                    c = x
                elif round(random.uniform(0, 0.99), 2) < math.exp(-delta/temperature):
                    c = x

                if evaluateBest > evaluateC:
                    best = c

                initialIterationsNumber -= 1

            temperature *= cooling_rate
        return best