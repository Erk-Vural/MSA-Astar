from util.trace_path import resolve_path3d
from MSA_AS import AStar3d
from tqdm import tqdm
import time
import json

json_file_path = "hparam.json"
with open(json_file_path, 'r') as f:
    params = json.load(f)

scores = params['scores']


def run_Astar3d(query3, database):
    count = 1
    start = time.time()
    len_data = len(database)

    best_seq1 = ""
    best_seq2 = ""
    best_seq1_a = ""
    best_seq2_a = ""
    best_query_a = ""

    filename = "./results/AStar3d_res.txt"
    filename_opt = "./results/AStar3d_opt.txt"

    with open(filename, 'w') as f1:
        with open(filename_opt, 'w') as f2:
            for query in query3:
                best_score = float('inf')
                for i in tqdm(range(len_data)):
                    for j in range(i + 1, len_data):
                        start_each = time.time()
                        seq1 = database[i]
                        seq2 = database[j]
                        path, score = AStar3d(query, seq1, seq2, scores)
                        query_a, seq1_a, seq2_a = resolve_path3d(query, seq1, seq2, path)
                        end = time.time()

                        if score <= best_score:
                            best_score = score
                            best_seq1 = seq1
                            best_seq2 = seq2
                            best_query_a = query_a
                            best_seq1_a = seq1_a
                            best_seq2_a = seq2_a

                        count += 1

                        content = "Query: %s\nSeq1:  %s\nSeq2:  %s\nScore: %d\nTime Expired: %.6f second\n" % (
                            query_a, seq1_a, seq2_a, score, (end - start_each)
                        )
                        f1.write(content + '\n')
                content = "Query: %s\nSeq1:  %s\nSeq2:  %s\nScore: %d\nTotal Time Expired: %.6f " \
                          "second\nALIGNED:\n%s\n%s\n%s\n" % (
                              query, best_seq1, best_seq2, best_score, (end - start),
                              best_query_a, best_seq1_a, best_seq2_a)
                f2.write(content + '\n')
