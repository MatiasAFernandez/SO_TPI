# simulation.py

from process import Process
from memory import MemoryManager
from scheduler import RoundRobinScheduler

class Simulation:
    def __init__(self, quantum):
        self.memory_manager = MemoryManager()  # Manage memory partitions
        self.scheduler = RoundRobinScheduler(quantum)  # Manage CPU scheduling
        self.process_list = []  # All processes
        self.finished_processes = []  # Track completed processes

    def load_processes(self, file_path):
        # Load processes from a file (ID, size, arrival time, burst time)
        with open(file_path, 'r') as file:
            for line in file:
                pid, size, arrival, burst = map(int, line.split())
                process = Process(pid, size, arrival, burst)
                self.process_list.append(process)

    def run(self):
        # Simulate the process of loading, scheduling, and executing processes
        for process in sorted(self.process_list, key=lambda p: p.arrival_time):
            print(f"\nProcess {process.pid} arrived at time {process.arrival_time}")
            
            # Try to allocate memory for the process
            if self.memory_manager.allocate(process):
                print(f"Memory allocated to Process {process.pid}")
                self.scheduler.add_process(process)
            else:
                print(f"Memory allocation failed for Process {process.pid}")

            # Display memory partitions
            self.memory_manager.display_partitions()

        # Run the scheduler to execute the processes
        self.scheduler.execute()

        # Output final report after all processes are done
        self.generate_report()

    def generate_report(self):
        print("\nSimulation complete. Final Report:")
        total_turnaround = 0
        total_waiting = 0
        for process in self.process_list:
            total_turnaround += process.turnaround_time
            total_waiting += process.waiting_time
            print(f"Process {process.pid}: Turnaround Time={process.turnaround_time}, Waiting Time={process.waiting_time}")

        print(f"\nAverage Turnaround Time: {total_turnaround / len(self.process_list)}")
        print(f"Average Waiting Time: {total_waiting / len(self.process_list)}")

