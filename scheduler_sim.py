import os
import copy


class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = 0


def get_input_manual():
    processes = []
    print("\n--- Manual Input Mode ---")
    print()
    try:
        n = int(input("Enter number of processes: "))
        print()
        for i in range(n):
            print(f"Enter details for Process {i + 1}:")
            arrival = int(input("- Arrival Time: "))
            burst = int(input("- Burst Time: "))
            print()
            processes.append(Process(f"P{i + 1}", arrival, burst))
    except ValueError:
        print("Invalid input. Please enter integers.")
        return []
    return processes


def get_input_from_file():
    processes = []
    print("\n--- File Input Mode ---")
    filename = input("Enter filename (e.g., input.txt): ").strip()

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return []

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            process_count = 1
            for line in lines:
                # Remove whitespace and split by space or comma
                parts = line.replace(',', ' ').split()

                # Skip empty lines
                if not parts:
                    continue

                # Expecting at least 2 numbers: Arrival and Burst
                if len(parts) >= 2:
                    try:
                        arrival = int(parts[0])
                        burst = int(parts[1])
                        processes.append(
                            Process(f"P{process_count}", arrival, burst))
                        process_count += 1
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
                        continue

        print(
            f"Successfully loaded {len(processes)} processes from {filename}.")
        return processes

    except Exception as e:
        print(f"Error reading file: {e}")
        return []


def print_table(processes, mode_name, exec_order):
    print("=" * 65)
    print(f"Mode: {mode_name}")
    print("=" * 65)
    print(f"Process Execution Order: {'->'.join(exec_order)}")
    print("-" * 65)

    # Table Header
    print(f"{'Process':<10} {'Arrival':<10} {'Burst':<10} {'Finish':<10} {'Turnaround':<12} {'Waiting':<10}")

    total_turnaround = 0
    total_waiting = 0

    for p in processes:
        print(f"{p.pid:<10} {p.arrival_time:<10} {p.burst_time:<10} {p.finish_time:<10} {p.turnaround_time:<12} {p.waiting_time:<10}")
        total_turnaround += p.turnaround_time
        total_waiting += p.waiting_time

    avg_turnaround = total_turnaround / len(processes) if processes else 0
    avg_waiting = total_waiting / len(processes) if processes else 0

    print("-" * 65)
    print(f"[{mode_name.split()[0]} Summary]")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print("=" * 65)
    print("\n")


def calculate_fcfs(processes):
    if not processes:
        return

    # Sort by Arrival Time
    sorted_processes = sorted(processes, key=lambda x: x.arrival_time)

    current_time = 0
    exec_order = []

    for p in sorted_processes:
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        p.start_time = current_time
        p.finish_time = p.start_time + p.burst_time

        # Formulas from source [17, 18]
        p.turnaround_time = p.finish_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        current_time = p.finish_time
        exec_order.append(p.pid)

    print_table(sorted_processes, "First-Come First-Served (FCFS)", exec_order)


def calculate_sjf(processes):
    if not processes:
        return

    n = len(processes)
    remaining_processes = sorted(processes, key=lambda x: x.arrival_time)
    completed_processes = []
    exec_order = []

    current_time = 0

    if remaining_processes and current_time < remaining_processes[0].arrival_time:
        current_time = remaining_processes[0].arrival_time

    while len(completed_processes) < n:
        # Find ready processes (Arrival <= Current Time)
        ready_queue = [
            p for p in remaining_processes if p.arrival_time <= current_time]

        if not ready_queue:
            if remaining_processes:
                current_time = remaining_processes[0].arrival_time
                continue

        # Select shortest burst time
        shortest_job = min(ready_queue, key=lambda x: x.burst_time)

        shortest_job.start_time = current_time
        shortest_job.finish_time = current_time + shortest_job.burst_time

        # Formulas from source [17, 18]
        shortest_job.turnaround_time = shortest_job.finish_time - shortest_job.arrival_time
        shortest_job.waiting_time = shortest_job.turnaround_time - shortest_job.burst_time

        current_time = shortest_job.finish_time
        exec_order.append(shortest_job.pid)
        completed_processes.append(shortest_job)
        remaining_processes.remove(shortest_job)

    print_table(completed_processes,
                "Shortest Job First (SJF) - Non Preemptive", exec_order)


def main():
    print("CPU SCHEDULING SIMULATOR (FCFS & SJF)")
    print("1. Manual Input (Type in console)")
    print("2. Read from File (.txt)")

    choice = input("Select input method (1 or 2): ").strip()

    input_data = []

    if choice == '1':
        input_data = get_input_manual()
    elif choice == '2':
        input_data = get_input_from_file()
    else:
        print("Invalid selection.")
        return

    if not input_data:
        print("No processes to schedule.")
        return

    # Deep copy to ensure fresh data for each algorithm
    data_for_fcfs = copy.deepcopy(input_data)
    data_for_sjf = copy.deepcopy(input_data)

    calculate_fcfs(data_for_fcfs)
    calculate_sjf(data_for_sjf)


if __name__ == "__main__":
    main()
