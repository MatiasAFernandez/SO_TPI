# process.py

class Process:
    def __init__(self, pid, size, arrival_time, burst_time):
        self.pid = pid                 # Process ID
        self.size = size               # Process size in KB
        self.arrival_time = arrival_time  # Time the process arrives in the system
        self.burst_time = burst_time    # CPU burst time
        self.remaining_time = burst_time  # Time left for execution
        self.waiting_time = 0           # Time the process spends waiting
        self.turnaround_time = 0        # Total time from arrival to completion

    def __repr__(self):
        return f"Process({self.pid}, Size={self.size}K, Arrival={self.arrival_time}, Burst={self.burst_time})"
