path_query = "./data/MSA_query.txt"
path_database = "./data/MSA_database.txt"


def load_query():
    query3 = []
    with open(path_query, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            else:
                query3.append(line[:-1])
    return query3


def load_base():
    database = []
    with open(path_database, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            else:
                database.append(line[:-1])
    return database


def load_data():
    query3 = load_query()
    database = load_base()
    return query3, database
