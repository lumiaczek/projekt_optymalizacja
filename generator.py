import random

num_processors = int(input("Podaj liczbę procesorów: "))
num_tasks = int(input("Podaj liczbę zadań: "))
task_time_min = int(input("Podaj minimalny czas trwania zadania: "))
task_time_max = int(input("Podaj maksymalny czas trwania zadania: "))

with open("./instancje/generated.txt", "w") as file:
    file.writelines(f"{str(num_processors)}\n{str(num_tasks)}\n")

    for i in range(num_tasks):
        random_task_time = str(random.randrange(task_time_min, task_time_max))
        file.write(f"{random_task_time}\n")