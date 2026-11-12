import os

def read_instance(filepath):
    with open(filepath, "r") as file:
        lines = [int(line.strip()) for line in file if line.strip()]
    num_processors = lines[0]
    num_tasks = lines[1]
    task_times = lines[2:2 + num_tasks]
    return num_processors, num_tasks, task_times

def initial_solution_greedy(num_processors, task_times):
    processor_times = [0] * num_processors
    assignment = [0] * len(task_times) 
    
    for task_id, task_time in enumerate(task_times):
        min_processor_id = processor_times.index(min(processor_times))
        processor_times[min_processor_id] += task_time
        assignment[task_id] = min_processor_id
        
    return assignment, max(processor_times)

def calculate_makespan(num_processors, task_times, assignment):
    processor_times = [0] * num_processors
    for task_id, proc_id in enumerate(assignment):
        processor_times[proc_id] += task_times[task_id]
    return processor_times, max(processor_times)

def tabu_search(num_processors, task_times, initial_assignment, max_iterations=500, tabu_tenure=10):
    best_assignment = list(initial_assignment)
    _, best_cmax = calculate_makespan(num_processors, task_times, best_assignment)
    
    current_assignment = list(initial_assignment)
    
    tabu_list = {} 
    
    for iteration in range(max_iterations):
        processor_times, current_cmax = calculate_makespan(num_processors, task_times, current_assignment)
        
        max_proc_id = processor_times.index(max(processor_times))
        
        bottleneck_tasks = [i for i, p in enumerate(current_assignment) if p == max_proc_id]
        
        best_move = None
        best_move_cmax = float('inf')
        
        for task_id in bottleneck_tasks:
            for target_proc_id in range(num_processors):
                if target_proc_id == max_proc_id:
                    continue
                    
                temp_assignment = list(current_assignment)
                temp_assignment[task_id] = target_proc_id
                _, temp_cmax = calculate_makespan(num_processors, task_times, temp_assignment)
                
                is_tabu = tabu_list.get((task_id, target_proc_id), 0) > iteration
                
                if is_tabu and temp_cmax < best_cmax:
                    is_tabu = False
                    
                if not is_tabu and temp_cmax < best_move_cmax:
                    best_move_cmax = temp_cmax
                    best_move = (task_id, target_proc_id)
        
        if best_move:
            task_id, target_proc_id = best_move
            old_proc_id = current_assignment[task_id]
            
            tabu_list[(task_id, old_proc_id)] = iteration + tabu_tenure
            
            current_assignment[task_id] = target_proc_id
            
            if best_move_cmax < best_cmax:
                best_cmax = best_move_cmax
                best_assignment = list(current_assignment)
        else:
            break
            
    return best_assignment, best_cmax


if __name__ == "__main__":
    filepath = "./instancje/m10n200.txt"
    
    if not os.path.exists(filepath):
        print(f"Brak pliku {filepath} - upewnij się, że ścieżka jest poprawna.")
    else:
        m, n, times = read_instance(filepath)
        
        print("--- Algorytm Zachłanny ---")
        greedy_assignment, greedy_cmax = initial_solution_greedy(m, times)
        print("Cmax (zachłannie):", greedy_cmax)
        
        print("\n--- Tabu Search ---")
        ts_assignment, ts_cmax = tabu_search(m, times, greedy_assignment, max_iterations=500, tabu_tenure=15)
        print("Cmax (Tabu Search):", ts_cmax)
        print("Poprawa:", greedy_cmax - ts_cmax)