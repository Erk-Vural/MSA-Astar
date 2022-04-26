import heapq
import json

json_file_path = "hparam.json"
with open(json_file_path, 'r') as f:
    params = json.load(f)

scores = params['scores']


class PriorityQueue:

    def __init__(self):
        self.q = []
        self.size = 0

    def push(self, node, prev_op, prev_point, cost, prio):
        heapq.heappush(self.q, (prio, (cost, prev_op, prev_point, node)))
        self.size += 1

    def pop(self):
        self.size -= 1
        return heapq.heappop(self.q)

    def empty(self):
        return self.q == []


def find_successors3d(point, m, n, p):
    x, y, z = point
    suc_x, suc_y, suc_z = (x + 1, y, z), (x, y + 1, z), (x, y, z + 1)
    suc_xy, suc_xz, suc_yz = (x + 1, y + 1, z), (x + 1, y, z + 1), (x, y + 1, z + 1)
    suc_xyz = (x + 1, y + 1, z + 1)
    if x == m:
        suc_x, suc_xy, suc_xz, suc_xyz = None, None, None, None
    if y == n:
        suc_y, suc_xy, suc_yz, suc_xyz = None, None, None, None
    if z == p:
        suc_z, suc_xz, suc_yz, suc_xyz = None, None, None, None
    return suc_x, suc_y, suc_z, suc_xy, suc_xz, suc_yz, suc_xyz


def heuristic3d(point, seq1, seq2, seq3, scores):
    x, y, z = point
    m, n, p = len(seq1), len(seq2), len(seq3)
    s_gap = scores.get('gap', 2)
    return (abs(m - x - n + y) + abs(m - x - p + z) + abs(n - y - p + z)) * s_gap


def AStar3d(seq1, seq2, seq3, scores=None):
    m, n, p = len(seq1), len(seq2), len(seq3)
    path = {}
    close_list = [[[0 for _ in range(p + 1)] for _ in range(n + 1)] for _ in range(m + 1)]

    s_match, s_sub, s_gap = scores.get('match', 0), scores.get('sub', 3), scores.get('gap', 2)
    q = PriorityQueue()

    init_point = (0, 0, 0)
    init_op = None
    init_prev = None
    init_cost = 0
    init_prio = heuristic3d(init_point, seq1, seq2, seq3, scores)

    q.push(init_point, init_op, init_prev, init_cost, init_prio)

    opt_res = 0
    goal_point = (m, n, p)
    traverse = 0

    while q.empty() is False:

        cur_prio, (cur_cost, prev_op, prev_point, cur_point) = q.pop()
        x, y, z = cur_point

        if close_list[x][y][z] != 0:
            continue

        traverse += 1

        close_list[x][y][z] = 1

        path[cur_point] = (prev_op, prev_point)

        if cur_point == goal_point:
            opt_res = cur_cost
            break

        suc_x, suc_y, suc_z, \
        suc_xy, suc_xz, suc_yz, \
        suc_xyz = find_successors3d(cur_point, m, n, p)

        if suc_x is not None:
            x, y, z = suc_x

            this_cost = 2 * s_gap
            h = heuristic3d(suc_x, seq1, seq2, seq3, scores)
            g = cur_cost + this_cost
            f = g + h
            q.push(suc_x, 'x', cur_point, g, f)

        if suc_y is not None:
            x, y, z = suc_y

            this_cost = 2 * s_gap
            h = heuristic3d(suc_y, seq1, seq2, seq3, scores)
            g = cur_cost + this_cost
            f = g + h
            q.push(suc_y, 'y', cur_point, g, f)

        if suc_z is not None:
            x, y, z = suc_z

            this_cost = 2 * s_gap
            h = heuristic3d(suc_z, seq1, seq2, seq3, scores)
            g = cur_cost + this_cost
            f = g + h
            q.push(suc_z, 'z', cur_point, g, f)

        if suc_xy is not None:
            x, y, z = suc_xy

            __score_xy = s_match if (seq1[x - 1] == seq2[y - 1]) else s_sub
            this_cost = 2 * s_gap + __score_xy
            h = heuristic3d(suc_xy, seq1, seq2, seq3, scores)
            g = cur_cost + this_cost
            f = g + h
            q.push(suc_xy, 'xy', cur_point, g, f)

        if suc_xz is not None:
            x, y, z = suc_xz

            __score_xz = s_match if (seq1[x - 1] == seq3[z - 1]) else s_sub
            this_cost = 2 * s_gap + __score_xz
            h = heuristic3d(suc_xz, seq1, seq2, seq3, scores)
            g = cur_cost + this_cost
            f = g + h
            q.push(suc_xz, 'xz', cur_point, g, f)

        if suc_yz is not None:
            x, y, z = suc_yz

            __score_yz = s_match if (seq2[y - 1] == seq3[z - 1]) else s_sub
            this_cost = 2 * s_gap + __score_yz
            h = heuristic3d(suc_yz, seq1, seq2, seq3, scores)
            g = cur_cost + this_cost
            f = g + h
            q.push(suc_yz, 'yz', cur_point, g, f)

        if suc_xyz is not None:
            x, y, z = suc_xyz

            __score_xy = s_match if (seq1[x - 1] == seq2[y - 1]) else s_sub
            __score_xz = s_match if (seq1[x - 1] == seq3[z - 1]) else s_sub
            __score_yz = s_match if (seq2[y - 1] == seq3[z - 1]) else s_sub
            this_cost = __score_xy + __score_yz + __score_xz
            h = heuristic3d(suc_xyz, seq1, seq2, seq3, scores)
            g = cur_cost + this_cost
            f = g + h
            q.push(suc_xyz, 'xyz', cur_point, g, f)

    return path, opt_res
