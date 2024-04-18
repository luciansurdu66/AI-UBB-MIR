import time
from service.service import Service


def main():
    results = []

    # numberOfPeople = int(input("Enter the number of people: "))
    # maxNumberGenerations = int(input("Enter the maximum number of generations: "))
    # mutationProbability = float(input("Enter the mutation probability ([0, 1]): "))
    numberOfPeople = 100
    maxNumberGenerations = 500
    mutationProbability = 0.85
    inputFilename = "cities.txt"
    outputFilename = "cities_results.txt"

    service = Service()

    cities = service.readFile(inputFilename)

    for i in range(10):
        startTime = time.time()

        results.append(
            service.evolutionAlgorithm(numberOfPeople, maxNumberGenerations, cities, mutationProbability,
                        outputFilename)
        )

        endTime = time.time() - startTime

    bestIndividual = service.getBestIndividual(results)
    avgFitness = service.getAverageFitness(results)

    service.writeToFile(outputFilename,
                                "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                                "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    service.writeToFile(outputFilename,
                                f"numberOfPeople: {numberOfPeople}   maxNumberGenerations: {maxNumberGenerations}  mutationProbability: {mutationProbability}"
                                f" best: {bestIndividual[1]}  average: {avgFitness}  timp: {endTime}")

    service.writeToFile(outputFilename,
                                "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "
                                "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


main()