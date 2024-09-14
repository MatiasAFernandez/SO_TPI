# main.py

from simulation import Simulation

if __name__ == "__main__":
    quantum = 3  # Time slice for Round-Robin
    simulator = Simulation(quantum)

    # Load processes from file (e.g., input/processes.txt)
    simulator.load_processes("input/processes.txt")

    # Run the simulation
    simulator.run()
