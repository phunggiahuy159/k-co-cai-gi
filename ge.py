import random
from time import time as tm

# Input
def InputFromFile(filepath):
    f = open(filepath, 'r')
    N, Q = map(int, f.readline().strip("\n").split())
    pred = []
    for _ in range(Q):
        pred.append(tuple(map(int, f.readline().strip("\n").split())))
    d = [0] + list(map(int, f.readline().strip("\n").split()))
    M = int(f.readline().strip("\n"))
    s = [0] + list(map(int, f.readline().strip("\n").split()))
    K = int(f.readline().strip("\n"))
    c = [[0 for i in range(M+1)] for j in range(N+1)]
    for _ in range(K):
        task, team, cost = map(int, f.readline().strip("\n").split())
        c[task][team] = cost
    f.close()
    return N, Q, pred, d, M, s, K, c

# Topological Sort implementation
def TopologicalSort(N, pred):
    edge = [set() for i in range(N+1)]
    in_degree = [0 for i in range(N+1)]
    for u, v in pred:
        edge[u].add(v)
        in_degree[v] += 1
    zero_in_degree = []
    for i in range(1, N+1):
        if in_degree[i] == 0:
            zero_in_degree = [i] + zero_in_degree
    topo = []
    while len(zero_in_degree) > 0:
        node = zero_in_degree[-1]
        zero_in_degree.pop()
        topo.append(node)
        for u in edge[node]:
            in_degree[u] -= 1
            if in_degree[u] == 0:
                zero_in_degree = [u] + zero_in_degree
    return topo

# Read the input
N, Q, pred, d, M, s, K, c = InputFromFile('test.txt')

max_cost = sum([sum(c[i]) for i in range(N+1)])

# Initialize the available list, where available[i] is list of teams that can do task i
available = [[] for i in range(N+1)]
for i in range(1, N+1):
    for j in range(1, M+1):
        if c[i][j] > 0:
            available[i].append(j)

before = [set() for i in range(N+1)]
after = [set() for i in range(N+1)]

for u, v in pred:
    after[u].add(v)
    before[v].add(u)

class Individual:
    def __init__(self, l):
        self.l = list(l)
        self.index = self.GetIndex()
        self.evaluation = 0

    def GetEvaluation(self, Print=False):
        scheduled = 0
        tmp_s = s[:]
        tmp_time = [0 for i in range(N+1)]
        tmp_completed = [0 for i in range(N+1)]
        for task in self.l:
            if tmp_completed[task] == -1:
                for i in after[task]:
                    tmp_completed[i] = -1
                continue
            teams = [(max(tmp_s[i], tmp_time[task]), c[task][i], i) for i in available[task]]
            if len(teams) == 0:
                tmp_completed[task] = -1
                for i in after[task]:
                    tmp_completed[i] = -1
                continue
            index = 0
            for i in range(len(teams)):
                if teams[i] < teams[index]:
                    index = i
            team = teams[index][2]
            tmp_completed[task] = team
            scheduled += 1
            tmp_time[task] = max(tmp_s[team], tmp_time[task])
            tmp_s[team] = tmp_time[task] + d[task]
            for i in after[task]:
                tmp_time[i] = max(tmp_time[i], tmp_time[task] + d[task])
        total_time = 0
        total_cost = 0
        for i in range(1, N+1):
            if tmp_completed[i] not in {-1, 0}:
                total_time = max(total_time, tmp_time[i] + d[i])
                total_cost += c[i][tmp_completed[i]]
        
        if Print:
            ans = ""
            f = open('output.txt', 'w')
            ans = ans + str(scheduled) + "\n"
            for i in range(1, N+1):
                if tmp_completed[i] not in {-1, 0}:
                    # print(i, tmp_completed[i], tmp_time[i])
                    ans = ans + str(i) + " " + str(tmp_completed[i]) + " " + str(tmp_time[i]) + "\n"
            f.write(ans)
            f.close()
        self.evaluation = (total_time, total_cost)
        return self.evaluation
    
    def Evaluation(self):
        if self.evaluation != 0:
            return self.evaluation
        return self.GetEvaluation()

    def GetIndex(self):
        index = [0 for i in range(N+1)]
        for i in range(len(self.l)):
            index[self.l[i]] = i
        return index

    def GetNeighbor(self, task):
        left = -1
        right = N
        for t in before[task]:
            left = max(left, self.index[t])
        for t in after[task]:
            right = min(right, self.index[t])
        BeforeIndex = self.index[task]
        if left+1 >= right-1:
            return self
        AfterIndex = random.randint(left+1, right-1)
        new_l = self.l[:]
        if BeforeIndex < AfterIndex:
            tmp = new_l[BeforeIndex]
            i = BeforeIndex
            while i < AfterIndex:
                new_l[i] = new_l[i+1]
                i += 1
            new_l[AfterIndex] = tmp
        elif BeforeIndex > AfterIndex:
            tmp = new_l[BeforeIndex]
            i = BeforeIndex
            while i > AfterIndex:
                new_l[i] = new_l[i-1]
                i -= 1
            new_l[AfterIndex] = tmp
        return Individual(new_l)
    
    def Mutation(self, p_m = 0.05):
        state = Individual(self.l)
        for task in set(range(1, N+1)):
            p = random.random()
            if p < p_m:
                state = state.GetNeighbor(task)
        return state

    # Like mother like daughter, like father like son
    def BornDaughter(self, other, k1, k2):
        daughter = []
        visited = [False for i in range(N+1)]
        for i in range(k1+1):
            daughter.append(self.l[i])
            visited[self.l[i]] = True
        ind = 0
        for i in range(k1+1, k2+1):
            while visited[other.l[ind]]:
                ind += 1
            daughter.append(other.l[ind])
            visited[other.l[ind]] = True
        ind = k1 + 1
        for i in range(k2+1, N):
            while visited[self.l[ind]]:
                ind += 1
            daughter.append(self.l[ind])
            visited[self.l[ind]] = True
        return Individual(daughter)


    def BornSon(self, other, k1, k2):
        # Shaded like dad, unshaded like mom
        return other.BornDaughter(self, k1, k2)
    
    def Crossover(self, other, k1, k2):
        daughter = self.BornDaughter(other, k1, k2)
        son = self.BornSon(other, k1, k2)
        return daughter, son


class Population:
    def __init__(self, population=[]):
        self.population = population[:]
        self.PopulationSize = 100

    def NewPopulation(self, new_population):
        self.population.clear()
        for individual in new_population:
            self.population.append(individual)
    
    def InitialPopulation(self, individual: Individual):
        self.population.append(individual)
        while len(self.population) < self.PopulationSize:
            new_individual = individual.Mutation(1)
            self.population.append(new_individual)
    
    def GetFitness(self, individual: Individual):
        return individual.Evaluation()

    def Selection(self):
        new_population = []
        self.population.sort(key = lambda individual: individual.Evaluation())
        best_individuals = [self.population[i] for i in range(self.PopulationSize) if self.population[i].Evaluation() == self.population[0].Evaluation()]
        for i in range(50*self.PopulationSize//100):
            r = random.randint(0, len(best_individuals) - 1)
            new_population.append(best_individuals[r])
        while len(new_population) < self.PopulationSize:
            i = 0
            j = 0
            while i == j:
                i = random.randint(0, self.PopulationSize - 1)
                j = random.randint(0, self.PopulationSize - 1)
            FirstFighter = self.population[i]
            SecondFighter = self.population[j]
            if self.GetFitness(FirstFighter) < self.GetFitness(SecondFighter):
                new_population.append(FirstFighter)
            else:
                new_population.append(SecondFighter)
        return Population(new_population)

    def Crossover(self, p_c=0.5):
        remaining = set(range(0, len(self.population)))
        while len(remaining) > 0:
            mum = 0
            dad = 0
            for i in remaining:
                mum = i
                break
            remaining.remove(i)
            for j in remaining:
                dad = j
                break
            remaining.remove(j)
            mother = self.population[mum]
            father = self.population[dad]
            p = random.random()
            if p < p_c:
                k1 = random.randint(0, N-2)
                k2 = random.randint(k1+1, N-1)
                daughter, son = mother.Crossover(father, k1, k2)
                self.population[mum] = daughter
                self.population[dad] = son

    def Mutation(self, p_m=0.05):
        for i in range(len(self.population)):
            self.population[i] = self.population[i].Mutation(p_m)
    
    def GetBestIndividual(self):
        max_fitness = (float('inf'), float('inf'))
        best_individual = None
        for individual in self.population:
            if self.GetFitness(individual) < max_fitness:
                best_individual = individual
                max_fitness = self.GetFitness(individual)
        return best_individual

class GeneticAlgorithm:
    def __init__(self):
        pass

    def Solve(self, l, time_limit=30):
        population = Population()
        population.InitialPopulation(Individual(l))
        ans = None
        min_evaluation = (float('inf'), float('inf'))
        step = 0
        t = tm()
        while tm() - t < time_limit:
            step += 1
            population = population.Selection()
            population.Crossover()
            population.Mutation()
            best_individual = population.GetBestIndividual()
            if best_individual.Evaluation() < min_evaluation:
                ans = best_individual
                min_evaluation = best_individual.Evaluation()
                print(f"Step: {step}, best individual: {best_individual.Evaluation()}, runtime: {(tm() - t)*1000} ms")
        
        print(min_evaluation)
        ans.GetEvaluation(True)
    
l = TopologicalSort(N, pred)
solver = GeneticAlgorithm()
solver.Solve(l, time_limit=30)

