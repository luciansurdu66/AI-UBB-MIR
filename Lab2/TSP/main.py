import time
from service.service import Service

service = Service()
tsp_results = []

start_time = time.time()

for _ in range(10):
    result = service.travelling_salesman_problem(10000, 50, 0.99, 0.001)
    tsp_results.append(result)
    
def get_solution_indexes(solution):
    indexes = []
    for city in solution:
        indexes.append(city.index)
    return indexes

best = service.get_best_solution(tsp_results)
avg_fitness = service.getAverageFitness(tsp_results)

end_time = time.time()

print("\n")
print(f'----- seconds {end_time - start_time} -------')
print(f'Best solution: {get_solution_indexes(best)}' +"\n" +'having the fitness '
      f'{service.get_total_distance(best)}.')
print("\n")
print(f'Average fitness: {avg_fitness} ')