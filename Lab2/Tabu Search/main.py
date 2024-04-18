import time
from models.Backpack import Backpack
from service.Service import Service

backpack = Backpack()

def show_menu():
    while True:
        print("1. Specified data")
        print("2. File data")
        print("3. Exit")

        option = input("Choose an option: ")
        if option == "1":
            service = Service(backpack)
            backpack_content = [10, (7, 20), (15, 50), (20, 140), (14, 81), (5, 50), (13, 100), (11, 25), (20, 45),
                                           (21, 73), (1, 10), 489]    

            backpack.nr_objects = backpack_content[0]
            backpack.max_weight = backpack_content[-1]
            backpack.objects_list = service.createListOfObjects(backpack_content)

            max_iterations = int(input("Enter the maximum number of iterations: "))
            max_tabu_iterations = int(input("Enter the number of tabu iterations: "))
            tabu_search_results = []

            start_time = time.time()

            for _ in range(10):
                tabu_search_results.append(service.tabuSearch(backpack.nr_objects, max_iterations, max_tabu_iterations))

            print(tabu_search_results)
            solution = service.getBestSolution(tabu_search_results)
            avg_fitness = service.getAverageFitness(tabu_search_results)
            worst_fitness = service.getWorstFitness(tabu_search_results)

            end_time = time.time()

            print("\n")
            print(f'----- seconds {end_time - start_time} -------')
            print(f'Best solution: {solution} \n'
                  f'having the fitness '
                  f'{service.getSolutionFitness(solution)}.')
            print("\n")
            print(f'Average fitness: {avg_fitness} ')
            print("\n")
            print(f'Worst fitness: {worst_fitness} ')

        elif option == "2":

            service = Service(backpack)

            numeFisier = input("File name: ")
            service.readFile(numeFisier)

            max_iterations = int(input("Enter the maximum number of iterations: "))
            max_tabu_iterations = int(input("Enter the number of tabu iterations: "))
            tabu_search_results = []

            startTime = time.time()

            for i in range(10):
                tabu_search_results.append(service.tabuSearch(backpack.nr_objects, max_iterations, max_tabu_iterations))

            for _ in tabu_search_results:
                print(_ )
            solution = service.getBestSolution(tabu_search_results)
            avg_fitness = service.getAverageFitness(tabu_search_results)
            worst_fit = service.getWorstFitness(tabu_search_results)

            endTime = time.time()

            print("\n")
            print(f'----- seconds {endTime - startTime} -------')
            print(f'Best solution: {solution} \n'
                  f'having the fitness '
                  f'{service.getSolutionFitness(solution)}.')
            print("\n")
            print(f'Average fitness: {avg_fitness} ')
            print("\n")
            print(f'Worst fitness: {worst_fit} ')

        elif option == '3':
            break

        else:
            print("Command not found. Try again!! ")


show_menu()