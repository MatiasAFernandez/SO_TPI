# memory.py

class Partition:
    def __init__(self, pid, start_address, size):
        self.id = pid                    # Partition ID
        self.start_address = start_address  # Starting memory address
        self.size = size                 # Size of the partition
        self.process_assigned = None     # Process assigned to this partition
        self.internal_fragmentation = 0  # Internal fragmentation

    def assign_process(self, process):
        self.process_assigned = process.pid
        self.internal_fragmentation = self.size - process.size

    def free_partition(self):
        self.process_assigned = None
        self.internal_fragmentation = 0

    def __repr__(self):
        return (f"Partition({self.id}, Start={self.start_address}, Size={self.size}K, "
                f"Process={self.process_assigned}, Fragmentation={self.internal_fragmentation}K)")

class MemoryManager:
    def __init__(self):
        # Memory partitions (ID, start address, size)
        self.partitions = [
            Partition(1, 0, 100),    # Reserved for OS
            Partition(2, 100, 250),  # Large jobs
            Partition(3, 350, 150),  # Medium jobs
            Partition(4, 500, 50)    # Small jobs
        ]

    def allocate(self, process):
        # Apply Worst-Fit algorithm to find the largest partition that can fit the process
        worst_partition = None
        for partition in self.partitions:
            if partition.process_assigned is None and partition.size >= process.size:
                if worst_partition is None or partition.size > worst_partition.size:
                    worst_partition = partition
        
        if worst_partition:
            worst_partition.assign_process(process)
            return True  # Allocation successful
        return False  # Allocation failed (no suitable partition)

    def release(self, process_id):
        # Free the partition assigned to the process
        for partition in self.partitions:
            if partition.process_assigned == process_id:
                partition.free_partition()

    def display_partitions(self):
        # Display memory partitions and their current state
        for partition in self.partitions:
            print(partition)
