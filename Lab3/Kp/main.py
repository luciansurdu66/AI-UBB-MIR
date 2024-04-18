import time
from models.Backpack import Backpack
from service.Service import Service


def main():
    backpack = Backpack()
    results = []

    numberOfPeople = int(input("Enter the number of people: "))
    maxNumberGenerations = int(input("Enter the maximum number of generations: "))
    mutationProbability = float(input("Enter the mutation probability ([0, 1]): "))
    inputFilename = 'rucsac-200.txt'
    outputFilename = 'rucsac-200-results.txt'

    service = Service(backpack)

    service.readFile(inputFilename)

    for i in range(10):
        startTime = time.time()

        results.append(
            service.evolutionAlgorithm(numberOfPeople, maxNumberGenerations, len(backpack.objects_list), mutationProbability,
                         backpack.max_weight, outputFilename)
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