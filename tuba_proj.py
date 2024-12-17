import heapq

def parse_input():
    N, Q = map(int, input().split())  # Number of tasks and precedence constraints
    precedence = [tuple(map(int, input().split())) for _ in range(Q)]
    durations = list(map(int, input().split()))
    M = int(input())  # Number of teams
    start_times = list(map(int, input().split()))
    K = int(input())  # Number of cost entries
    costs = [tuple(map(int, input().split())) for _ in range(K)]
    return N, Q, precedence, durations, M, start_times, K, costs

# Objective function to evaluate a solution
import random

# Function to evaluate the cost and total time of a solution
def evaluate_solution(solution, costs, durations):
    total_cost = sum(costs.get((task, team), float('inf')) for task, team in solution)
    total_time = sum(durations[task] for task, _ in solution)
    return total_cost, total_time

# Function to generate neighbors with only valid task-team assignments
def generate_neighbors(current_solution, tasks, valid_teams, costs):
    neighbors = []
    for idx, (task, team) in enumerate(current_solution):
        for new_team in valid_teams:  # Only consider valid teams
            if (task, new_team) in costs:  # Ensure the task-team pair has valid costs
                new_solution = current_solution[:]
                new_solution[idx] = (task, new_team)  # Swap team assignment
                neighbors.append(new_solution)
    return neighbors

# Tabu search implementation
def tabu_search(N, M, durations, start_times, costs, precedence, max_iterations=100, tabu_tenure=5):
    # Extract valid teams from costs
    valid_teams = set(j for _, j, _ in costs)
    tasks = list(range(N))

    # Initialize a feasible solution with valid task-team assignments
    solution = [(task, min(valid_teams)) for task in tasks]  # Assign the first valid team to all tasks
    best_solution = solution[:]
    best_cost, best_time = evaluate_solution(solution, costs, durations)

    tabu_list = []
    iteration = 0

    while iteration < max_iterations:
        neighbors = generate_neighbors(solution, tasks, valid_teams, costs)
        neighbors = [n for n in neighbors if n not in tabu_list]  # Remove tabu neighbors

        # Evaluate all valid neighbors
        neighbor_costs = [(neighbor, *evaluate_solution(neighbor, costs, durations)) for neighbor in neighbors]
        neighbor_costs.sort(key=lambda x: (x[1], x[2]))  # Sort by cost, then by time

        # Choose the best neighbor
        if neighbor_costs:
            solution, cost, time = neighbor_costs[0]

            if cost < best_cost or (cost == best_cost and time < best_time):
                best_solution, best_cost, best_time = solution[:], cost, time

            tabu_list.append(solution)
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)

        iteration += 1

    return best_solution, best_cost, best_time

# Main function to read input and call the tabu search
def main():
    # Sample Input (Replace with actual input reading as needed)
    N, Q = 3, 2  # Tasks and precedence constraints
    precedence = [(0, 1), (1, 2)]  # Task 1 depends on Task 0, Task 2 depends on Task 1
    durations = [10, 20, 15]  # Durations of tasks
    M = 3  # Number of teams
    start_times = [0, 5, 10]  # Teams' availability times
    K = 6  # Number of cost mappings
    costs_input = [
        (0, 0, 10), (0, 1, 15), (1, 1, 20), (1, 2, 25), (2, 0, 30), (2, 2, 35)
    ]

    # Build costs dictionary
    costs = {(i, j): c for i, j, c in costs_input}

    # Run Tabu Search
    best_solution, best_cost, best_time = tabu_search(N, M, durations, start_times, costs, precedence)

    # Print Results
    print("Best Solution (Task-Team Assignments):")
    for task, team in best_solution:
        print(f"Task {task} -> Team {team}")
    print(f"Total Cost: {best_cost}")
    print(f"Total Time: {best_time}")

if __name__ == "__main__":
    main()
