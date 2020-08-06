import time


class MWDSGraph:
    vertex_weight = {}
    edges = {}

    def __init__(self, n):
        self.vertices_count = n

    def get_vertices(self):
        return range(self.vertices_count)

    def add_vertex(self, u, weight):
        self.edges[u] = set()
        self.vertex_weight[u] = weight

    def add_edge(self, u, v):
        self.edges[u].add(v)
        self.edges[v].add(u)

    def get_edges(self):
        for u in self.get_vertices():
            for v in self.edges[u].keys():
                yield u, v

    def get_N1(self, v):
        return self.edges[v]

    def get_N1_for_set(self, A):
        N1 = set()
        for v in A:
            N1.update(self.get_N1(v))
        return N1

    def get_N2(self, v):
        N2 = set()
        for u_1 in self.get_N1(v):
            N2.add(u_1)
            for u2 in self.get_N1(u_1):
                N2.add(u2)
        return N2


class CC2FS:
    def __init__(self, graph: MWDSGraph, cutoff_time):
        self.graph = graph
        self.cutoff_time = cutoff_time
        self.S = set()
        self.S_star = set()
        self.conf_change = set(self.graph.get_vertices())  # CC2_RULE1
        self.forbid_list = set()
        self.freq = [1 for _ in range(graph.vertices_count)]
        self.score_f = [0 for _ in range(graph.vertices_count)]
        self.age = [0 for _ in range(graph.vertices_count)]
        self.covered_vertices = set()

    def init_greedy(self):
        while self.get_uncovered_vertices_count() != 0:
            vertices = set(self.graph.get_vertices()).difference(self.S)
            coverage = [(v, len(self.graph.edges[v].difference(self.covered_vertices))) for v in vertices]
            coverage = sorted(coverage, key=lambda p: p[0], reverse=True)
            v = coverage[0][0]
            if v not in self.S:
                self.add_to_S(v)

    def update_score_f(self):
        for v in self.graph.get_vertices():
            if v in self.S:
                sum_freq_c2 = sum([self.freq[u] for u in self.get_c2(v)])
                self.score_f[v] = - sum_freq_c2 / self.graph.vertex_weight[v]
            else:  # not in S
                sum_freq_c1 = sum([self.freq[u] for u in self.get_c1(v)])
                self.score_f[v] = sum_freq_c1 / self.graph.vertex_weight[v]

    def get_c1(self, v):
        return self.graph.get_N1(v).difference(self.graph.get_N1_for_set(self.S))

    def get_c2(self, v):
        S_u = self.S.copy()
        S_u.remove(v)
        return self.graph.get_N1(v).difference(self.graph.get_N1_for_set(S_u))

    def get_uncovered_vertices_count(self):
        return self.graph.vertices_count - len(self.covered_vertices)

    @staticmethod
    def get_solution_weight(S):
        return sum([social_net.vertex_weight[v] for v in S])

    def get_vertex_with_highest_score_f(self, ignore_forbid_list):
        self.update_score_f()
        vertices = self.S
        if not ignore_forbid_list:
            vertices = set(vertices).difference(self.forbid_list)
        if len(vertices) > 0:
            scores = sorted(zip(vertices, self.score_f), key=lambda p: p[1], reverse=True)
            v_s = scores[0]
            i = 1
            while i < len(scores) and scores[i][1] == v_s[1]:
                if self.age[scores[i][0]] < self.age[v_s[0]]:
                    v_s = scores[i]
                i += 1
            return v_s[0]
        else:
            return None

    def get_v_from_CCV2(self):
        scores = [(v, self.score_f[v]) for v in self.conf_change.difference(self.S)]
        if len(scores) == 0:
            return None
        scores = sorted(scores, key=lambda p: p[1], reverse=True)
        v_s = scores[0]
        i = 1
        while i < len(scores) and scores[i][1] == v_s[1]:
            if self.age[scores[i][0]] > self.age[v_s[0]]:
                v_s = scores[i]
            i += 1
        return v_s[0]

    def CC2_RULE2(self, v):
        for u in self.graph.get_N2(v):
            self.conf_change.add(u)
        self.conf_change.remove(v)

    def CC2_RULE3(self, v):
        for u in self.graph.get_N2(v):
            self.conf_change.add(u)

    def update_freq(self):
        for v in social_net.get_vertices():
            if v not in self.covered_vertices:
                self.freq[v] += 1

    def add_to_S(self, v):
        self.S.add(v)
        self.age[v] = 0
        self.update_NS()

    def remove_from_S(self, v):
        self.S.remove(v)
        self.age[v] = 0
        self.update_NS()

    def update_NS(self):
        self.covered_vertices = self.graph.get_N1_for_set(self.S).union(self.S)

    def increase_age(self):
        for v in self.graph.get_vertices():
            self.age[v] += 1

    def find_solution(self):
        self.init_greedy()
        self.S_star = self.S.copy()
        while time.time_ns() < self.cutoff_time:
        #while True:
            if self.get_uncovered_vertices_count() == 0:
                if self.get_solution_weight(self.S) < self.get_solution_weight(self.S_star):
                    self.S_star = self.S.copy()
                v = self.get_vertex_with_highest_score_f(ignore_forbid_list=True)
                self.remove_from_S(v)
                self.CC2_RULE2(v)
                continue
            v = self.get_vertex_with_highest_score_f(ignore_forbid_list=False)
            if v is not None:
                self.remove_from_S(v)
                self.CC2_RULE2(v)
            self.forbid_list.clear()
            while self.get_uncovered_vertices_count() > 0:
                v = self.get_v_from_CCV2()
                if v is None:
                    break
                self.add_to_S(v)
                self.CC2_RULE3(v)
                self.forbid_list.add(v)
                self.update_freq()

    def print_solution(self, name_mapping):
        print(len(self.S_star))
        cost = 0
        for v in self.S_star:
            # print(name_mapping[v])
            cost += self.graph.vertex_weight[v]
        print(cost)


vertex_count = int(input())
start = time.time_ns()
social_net = MWDSGraph(vertex_count)
names2int = {}
int2names = {}

for i in range(vertex_count):
    line = input().split()
    names2int[line[0]] = i
    int2names[i] = line[0]
    social_net.add_vertex(i, int(line[1]))

m = int(input())
for i in range(m):
    line = input().split()
    social_net.add_edge(names2int[line[0]], names2int[line[1]])


time_delta = 4 * (10 ** 8)
cutoff_time = 2
if social_net.vertices_count == 300:
    cutoff_time = 5
cutoff_time = start + cutoff_time * (10 ** 9) - time_delta

algorithm = CC2FS(social_net, cutoff_time)
algorithm.find_solution()
algorithm.print_solution(int2names)
