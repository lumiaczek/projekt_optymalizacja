def task_scheduling_greedy(filepath):
    with open(filepath, "r") as file:
        lines = [int(line.strip()) for line in file if line.strip()]

    num_processors = lines[0]
    num_tasks = lines[1]
    task_times = lines[2:2 + num_tasks]

    processor_times = [0] * num_processors

    for task_time in task_times:
        min_processor_id = processor_times.index(min(processor_times))
        
        processor_times[min_processor_id] += task_time

    cmax = max(processor_times)

    print("Minimalna długość cmax (zachłannie):", cmax)


if __name__ == "__main__":
    task_scheduling_greedy("./adam/random_instance2.txt")
