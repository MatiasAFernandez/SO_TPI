# scheduler.py

from collections import deque

class RoundRobinScheduler:
    def __init__(self, quantum):
        self.quantum = quantum      # Time slice for each process
        self.ready_queue = deque()  # Ready queue to store processes in round-robin order
        self.current_time = 0       # Global clock

    def add_process(self, process):
        self.ready_queue.append(process)

    def execute(self):
        # Execute processes in the ready queue using round-robin scheduling
        while self.ready_queue:
            process = self.ready_queue.popleft()  # Get the next process
            print(f"\nTime {self.current_time}: Executing {process}")

            # Calculate how long the process can run for
            run_time = min(self.quantum, process.remaining_time)
            process.remaining_time -= run_time
            self.current_time += run_time  # Update the global clock

            # If the process is done, calculate turnaround and waiting time
            if process.remaining_time == 0:
                process.turnaround_time = self.current_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.burst_time
                print(f"Process {process.pid} completed. Turnaround: {process.turnaround_time}, Waiting: {process.waiting_time}")
            else:
                # Re-add the process to the ready queue if it's not finished
                self.ready_queue.append(process)

            # Print current state of the ready queue
            self.display_ready_queue()

    def display_ready_queue(self):
        print(f"Ready Queue: {[p.pid for p in self.ready_queue]}")
