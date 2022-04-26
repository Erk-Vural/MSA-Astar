from run_algorithms import run_Astar3d
from util.load_data import load_data

if __name__ == '__main__':
    query3, database = load_data()

    run_Astar3d(query3, database)
