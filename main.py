#This project implements three CPU scheduling algorithms:
# 1. FCFS (First-Come, First-Served)
# 2. SJF (Shortest Job First)
# 3. RR (Round Robin)

# Imports the 'sys' module to interact with the system, such as reading from standard input.
import sys

# Defines the Process class to represent a process with its properties.
class Process:
    # The constructor initializes a new Process object.
    def __init__(self, arrival_time, burst_time, pid):
        # The time the process arrives in the system.
        self.arrival_time = arrival_time
        # The total CPU time required for the process.
        self.burst_time = burst_time
        # The remaining execution time of the process. Initially, it's equal to the burst_time.
        self.remaining_time = burst_time
        # The time at which the process finishes its execution.
        self.completion_time = 0
        # The total time from arrival to completion.
        self.turnaround_time = 0
        # The total time the process spent waiting in the ready queue.
        self.waiting_time = 0
        # The time from arrival until the first time the process is executed. -1 indicates it hasn't run yet.
        self.response_time = -1
        # The process ID, used for tie-breaking in some algorithms.
        self.pid = pid

# Function to calculate the average metrics for a set of processes.
def calculate_metrics(processes):
    # Gets the number of processes in the list.
    num_processes = len(processes)
    # Avoids division by zero if there are no processes.
    if num_processes == 0:
        return 0.0, 0.0, 0.0

    # Calculates the total sum of turnaround, response, and waiting times.
    # These metrics should have already been calculated by the scheduling algorithms.
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    total_response_time = sum(p.response_time for p in processes)
    total_waiting_time = sum(p.waiting_time for p in processes)

    # Calculates the average of each metric.
    avg_turnaround_time = total_turnaround_time / num_processes
    avg_response_time = total_response_time / num_processes
    avg_waiting_time = total_waiting_time / num_processes

    # Returns the average metrics as a tuple.
    return avg_turnaround_time, avg_response_time, avg_waiting_time

# Implements the FCFS (First-Come, First-Served) scheduling algorithm.
def fcfs(processes_data):
    # Creates a list of Process objects from the input data.
    processes = [Process(p[0], p[1], idx) for idx, p in enumerate(processes_data)]
    if not processes:
        return 0.0, 0.0, 0.0
    # Sorts the processes strictly by their arrival time.
    processes.sort(key=lambda x: x.arrival_time)

    # Initializes the current simulation time.
    current_time = 0
    # Iterates over the already sorted processes.
    for p in processes:
        # If the CPU is idle (current time < process arrival time),
        # advance the time to the moment the process arrives.
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        # The first time a process runs is now.
        # Response time = start time - arrival time.
        p.response_time = current_time - p.arrival_time
        # Completion time = start time + burst duration.
        p.completion_time = current_time + p.burst_time
        # Turnaround time = completion time - arrival time.
        p.turnaround_time = p.completion_time - p.arrival_time
        # Waiting time = turnaround time - burst duration.
        p.waiting_time = p.turnaround_time - p.burst_time
        # Updates the current time to the process's completion time.
        current_time = p.completion_time

    # Calculates and returns the average metrics.
    return calculate_metrics(processes)

# Implements the non-preemptive SJF (Shortest Job First) scheduling algorithm.
def sjf(processes_data):
    # Creates process objects.
    processes = [Process(p[0], p[1], idx) for idx, p in enumerate(processes_data)]
    if not processes:
        return 0.0, 0.0, 0.0

    current_time = 0
    completed_processes = 0
    n = len(processes)

    # Ready queue for processes that have already arrived.
    ready_queue = []
    # List of processes that have not yet arrived, sorted by arrival time.
    unarrived_processes = sorted(processes, key=lambda x: x.arrival_time)
    unarrived_idx = 0

    # Simulates execution as long as there are processes to complete.
    while completed_processes < n:
        # Adds processes that have arrived to the ready queue.
        while unarrived_idx < n and unarrived_processes[unarrived_idx].arrival_time <= current_time:
            ready_queue.append(unarrived_processes[unarrived_idx])
            unarrived_idx += 1

        # If the ready queue is empty, the CPU is idle.
        if not ready_queue:
            # If there are still processes to arrive, advance the time to the next arrival.
            if unarrived_idx < n:
                current_time = unarrived_processes[unarrived_idx].arrival_time
                continue
            # If all processes have arrived and the queue is empty, the simulation ends.
            else:
                break

        # Sorts the ready queue by the shortest burst time.
        # In case of a tie, uses arrival time (FCFS) and then PID as a tie-breaker.
        ready_queue.sort(key=lambda x: (x.burst_time, x.arrival_time, x.pid))

        # Selects the process with the shortest burst time from the queue.
        shortest_job = ready_queue.pop(0)

        # If the response time hasn't been set yet, set it.
        if shortest_job.response_time == -1:
            shortest_job.response_time = current_time - shortest_job.arrival_time

        # Executes the process until its completion (non-preemptive).
        current_time += shortest_job.burst_time
        shortest_job.completion_time = current_time

        # Calculates the process's metrics.
        shortest_job.turnaround_time = shortest_job.completion_time - shortest_job.arrival_time
        shortest_job.waiting_time = shortest_job.turnaround_time - shortest_job.burst_time

        completed_processes += 1

    # Sorts the list of processes back by PID to ensure consistent output.
    processes.sort(key=lambda x: x.pid)
    return calculate_metrics(processes)


# Implements the RR (Round Robin) scheduling algorithm with a fixed quantum.
def rr(processes_data, quantum=2): # Quantum is 2, as specified in the project.
    # Creates process objects.
    processes = [Process(p[0], p[1], idx) for idx, p in enumerate(processes_data)]
    if not processes:
        return 0.0, 0.0, 0.0
    n = len(processes)
    current_time = 0
    completed_processes = 0

    # Ready queue using a list, which behaves like a queue (FIFO).
    q = []
    # List of unarrived processes for control.
    unarrived_processes = sorted(processes, key=lambda x: x.arrival_time)
    unarrived_idx = 0
    # Set to track PIDs in the queue and avoid duplicates.
    in_queue_pids = set()

    # Sets the initial simulation time to the arrival time of the first process.
    if unarrived_processes:
        current_time = unarrived_processes[0].arrival_time
    else:
        return 0.0, 0.0, 0.0

    while completed_processes < n:
        # Adds processes that have arrived up to 'current_time' to the ready queue.
        while unarrived_idx < n and unarrived_processes[unarrived_idx].arrival_time <= current_time:
            p = unarrived_processes[unarrived_idx]
            if p.pid not in in_queue_pids:
                q.append(p)
                in_queue_pids.add(p.pid)
            unarrived_idx += 1

        # If the ready queue is empty, advance the time to the next arrival.
        if not q:
            if unarrived_idx < n:
                current_time = unarrived_processes[unarrived_idx].arrival_time
            else:
                break
            continue

        # Gets the next process from the queue (FIFO behavior).
        p = q.pop(0)
        in_queue_pids.remove(p.pid)

        # Sets the response time the first time the process is executed.
        if p.response_time == -1:
            p.response_time = current_time - p.arrival_time

        # Determines the execution time for the quantum or until the burst ends.
        execute_time = min(quantum, p.remaining_time)
        current_time += execute_time
        p.remaining_time -= execute_time

        # Adds processes that arrived during this quantum's execution.
        while unarrived_idx < n and unarrived_processes[unarrived_idx].arrival_time <= current_time:
            new_p = unarrived_processes[unarrived_idx]
            if new_p.pid not in in_queue_pids:
                q.append(new_p)
                in_queue_pids.add(new_p.pid)
            unarrived_idx += 1

        # If the process hasn't finished, put it back at the end of the queue.
        if p.remaining_time > 0:
            if p.pid not in in_queue_pids:
                q.append(p)
                in_queue_pids.add(p.pid)
        # If the process has finished, calculate its metrics and increment the counter.
        else:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            completed_processes += 1

    # Sorts the list of processes back by PID for consistent output.
    processes.sort(key=lambda x: x.pid)
    return calculate_metrics(processes)

# Helper function to format the output with a comma as the decimal separator.
def format_output(label, metrics):
    """Formats the output string with a comma as the decimal separator."""
    # Formats each metric with one decimal place and replaces the dot with a comma.
    t = f"{metrics[0]:.1f}".replace('.', ',')
    r = f"{metrics[1]:.1f}".replace('.', ',')
    w = f"{metrics[2]:.1f}".replace('.', ',')
    # Returns the formatted string.
    return f"{label} {t} {r} {w}"

# Main function to orchestrate reading the input, running the algorithms, and printing the output.
def main():
    processes_data = []

    # The filename the program will try to open.
    # Make sure this file is in the same folder as the .py script.
    filename = "input.txt"

    try:
        # Tries to open the file. If it's not found, the exception will be caught.
        with open(filename, 'r') as f:
            for line in f:
                try:
                    # The input consists of pairs of integers.
                    arrival, duration = map(int, line.split())
                    processes_data.append((arrival, duration))
                except ValueError:
                    # Continues reading if the line is invalid.
                    continue
    except FileNotFoundError:
        # If the file is not found, inform the user and exit the program.
        print(f"Error: The file '{filename}' was not found. Make sure it's in the same folder as the script.")
        return

    # If the list of processes is empty, there is nothing to schedule.
    if not processes_data:
        print("No valid processes found in the file. Exiting.")
        return

    # Executes each algorithm and stores its metrics.
    fcfs_metrics = fcfs(processes_data)
    sjf_metrics = sjf(processes_data)
    rr_metrics = rr(processes_data)

    # Prints the formatted output for each algorithm.
    print(format_output("FCFS:", fcfs_metrics))
    print(format_output("SJF:", sjf_metrics))
    print(format_output("RR:", rr_metrics))

if __name__ == "__main__":
    main()