from service.Service import Service
from models.Backpack import Backpack
from models.Item import Object
import time

backpack = Backpack()

def menuRandomSearch():
    while True:
        print("1. Specified data")
        print("2. File data")
        print("3. Back")

        option = int(input("Choose option:"))
        if option == 1:
            print(option)

            service = Service(backpack)

            nrObjects = int(input("Enter the number of objects: "))
            backpackWeight = int(
                input("Enter the maximum weight accepted by the backpack: "))
            backpack.max_weight = backpackWeight
            backpack.objects_list = Service.createListOfObjects(nrObjects)

            k = int(
                input("Enter the number of random solutions to generate: "))
            service.randomSearchWithSpecifiedData(k, nrObjects)

        elif option == 2:
            service = Service(backpack)

            fileName = input("Enter the filename: ")
            service.showFileContent(fileName)

            k = int(
                input("Enter the number of random solutions to generate: "))
            service.randomSearchWithFileData(k, backpack.nr_objects)
        elif option == 3:
            break

        else:
            print("Command not found. Try again!")

def menuNAHC():
    while True:
        print("1. Specified data")
        print("2. File data")
        print("3. Back")

        option = int(input("Choose option:"))
        if option == 1:

            service = Service(backpack)

            nrObjects = int(input("Enter the number of objects: "))
            backpackWeight = int(
                input("Enter the maximum weight accepted by the backpack: "))
            backpack.max_weight = backpackWeight
            backpack.objects_list = Service.createListOfObjects(nrObjects)

            startTime = time.time()

            k = int(input("Enter the number of evaluations: "))
            solution = service.nextAscentHillClimbing(
                k, nrObjects)
            print("\nSolution:")
            print(solution)
            print("fitness: " + str(service.getSolutionFitness(solution)))

            endTime = time.time()

            print("\n")
            print(f'----- seconds {endTime - startTime} -------')

        elif option == 2:
            service = Service(backpack)

            fileName = input("Enter the filename: ")
            service.readFile(fileName)

            startTime = time.time()

            k = int(input("Enter the number of evaluations: "))
            solution = service.nextAscentHillClimbing(
                k, backpack.nr_objects)
            print("\nSolution: ")
            print(solution)
            print("fitness: " + str(service.getSolutionFitness(solution)))

            endTime = time.time()

            print("\n")
            print(f'----- seconds {endTime - startTime} -------')

        elif option == 3:
            break

        else:
            print("Command not found. Try again!")

def showMenu():
    while True:

        print("1. Random search")
        print("2. NAHC")
        print("3. Exit")

        option = int(input("Choose option:"))
        if option == 1:
            menuRandomSearch()

        elif option == 2:
            menuNAHC()
            print(option)

        elif option == 3:
            break

        else:
            print("Command not found. Try again!")
            
showMenu()