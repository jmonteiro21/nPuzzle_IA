import numpy as np
import copy 
from timeit import default_timer as timer

n = 4

class node():
    def __init__(self, pieces_list = [], matrix = [], parent = None, f=0, g=0, h=0, mis=0):
        self.pieces_list = pieces_list
        self.matrix = matrix
        self.f = f
        self.g = g
        self.h = h
        self.mis = mis
        self.parent = parent

    def create_matrix(self, list):
        self.matrix = np.zeros((n,n))
        index = 0
        for i in range(4):
            for j in range(4):
                self.matrix[i][j] = list[index]
                index += 1
        # print(self.matrix)


    def isGoal(self):
        # print(self.matrix)
        return np.array_equal(self.matrix, goal.matrix)
    

    def findBlank(self):
        for i in range(n):
                for j in range(n):
                    if self.matrix[i][j] == 0:
                        return i, j


    def genChildren(self):
            x, y = self.findBlank()
            newMatrices = []
            if (x + 1) < n: #moving blank down / moving a tile up
                new = copy.deepcopy(self.matrix)
                new[x][y] = new[x+1][y]
                new[x+1][y] = 0
                newMatrices.append(new)
            if (y + 1) < n:  # moving blank right / moving a tile left
                new = copy.deepcopy(self.matrix)
                new[x][y]=new[x][y+1]
                new[x][y+1]= 0
                newMatrices.append(new)
            if (x - 1) > -1: #moving blank up / moving a tile down
                new = copy.deepcopy(self.matrix)
                new[x][y] = new[x-1][y]
                new[x-1][y] = 0
                newMatrices.append(new)
            if (y - 1) > -1: # moving blank left / moving a tile right
                new = copy.deepcopy(self.matrix)
                new[x][y] = new[x][y - 1]
                new[x][y-1] = 0
                newMatrices.append(new)
            ret = []
            for matrix in newMatrices: #create children nodes
                child = node()
                child.matrix = matrix
                child.parent = self
                # print(child.g)
                child.manhattan()
                # print(child.g)
                ret.append(child)
            return ret


    def manhattan(self):
        # print("dakjdwadwkj")
        sum = 0
        # print(self.matrix)
        if np.array_equal(self.matrix, start.matrix):
            for i in range(n):
                for j in range(n):
                    if self.matrix[i][j] == 0:
                        continue
                    else:
                        x, y = findGoal(self.matrix[i][j], goal)
                        sum += abs(x - i) + abs(y - j)
            self.h = sum
            self.g = 0
            self.f = sum
        else:
            for i in range(n):
                for j in range(n):
                    if self.matrix[i][j] == 0:
                        continue
                    else:
                        x, y = findGoal(self.matrix[i][j], goal)
                        sum += abs(x - i) + abs(y - j)
            self.h = sum
            self.g = self.parent.g + 1
            self.f = self.g + sum


    def misplaced(self):
        total = 0
        for i in range(n):
            for j in range(n):
                if (self.matrix[i][j] != 0) and (self.matrix[i][j] != goal.matrix[i][j]):
                    total += 1
        self.mis = total


    def print_matrix(self):
        # for i in range(n):
        #     print(int(self.matrix[i][0]), int(self.matrix[i][1]), int(self.matrix[i][2]), int(self.matrix[i][3])) 
        for i in range(n):
            b = ""
            for j in range(n):
                b += str(int(self.matrix[i][j])) + '\t'
            print(b)
        print("---------------------------")





def solvability(start_list):
    inversions = 0
    for i in range(len(start_list)):
        inversions_temp = 0
        for j in range(i+1, len(start_list)):
            if start_list[i] > start_list[j] and start_list[j]!=0:
                inversions_temp += 1
        inversions += inversions_temp
    for i in range(len(start_list)):
        if start_list[i] == 0:
            if (i > -1 and i < 4) or (i > 8 and i < 13):
                if inversions % 2 != 0:
                    return True
            else:
                if inversions % 2 == 0: 
                    return True
    return False






def astar_manhattan():
    open_list = []
    closed_list = []
    # print(start.matrix)
    open_list.append(start)
    while(len(open_list) > 0):
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if(current_node.isGoal()):
            path = []
            current = current_node
            while(current is not None):
                path.append(current)
                current = current.parent
            return path[::-1]
        children = current_node.genChildren()
        for child in children:
            for closed_child in closed_list:
                if(np.array_equal(child.matrix, closed_child.matrix)):
                    continue
            # print(child)
            child.manhattan()
            for open_child in open_list:
                if(np.array_equal(open_child.matrix, child.matrix) and child.g > open_child.g):
                    continue
            open_list.append(child)



def astar_misplaced():
    open_list = []
    closed_list = []
    # print(start.matrix)
    open_list.append(start)
    while(len(open_list) > 0):
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if(current_node.isGoal()):
            path = []
            current = current_node
            while(current is not None):
                path.append(current)
                current = current.parent
            return path[::-1]
        children = current_node.genChildren()
        for child in children:
            for closed_child in closed_list:
                if(np.array_equal(child.matrix, closed_child.matrix)):
                    continue
            # print(child)
            child.misplaced()
            for open_child in open_list:
                if(np.array_equal(open_child.matrix, child.matrix) and child.mis > open_child.mis):
                    continue
            open_list.append(child)


def BFS():
    queue = []
    queue.append(start)
    queue.append(0)
    visited_nodes = []
    while(len(queue) != 0):
        node = queue.pop(0)
        depth_node = queue.pop(0)
        visited_nodes.append(node)
        # print("Nós já visitados:", len(visited_nodes),"Nós por visitar:", len(queue), "Profundidade do Nó a ser analisado:", depth_node)
        if(node.isGoal()):
            path = []
            while(node != None):
                path.insert(0, node)
                node = node.parent
            return path
        children = node.genChildren()
        for child in children:
            if(child not in visited_nodes):
                queue.append(child)
                queue.append(depth_node+1)
                visited_nodes.append(child)


def IDFS():
    depth = 1
    bottom_reached = False  
    while not bottom_reached:
        path, bottom_reached = IDFSRec(start, 0, depth)
        if path is not None:
            return path
        depth += 1
        # print("Profundidade máxima:", depth)
    return None


def IDFSRec(node, current_depth, max_depth):
    if node.isGoal():
        print("Solucão encontrada")
        print("Profundidade da solução:", current_depth)
        path = []
        while(node != None):
            path.insert(0, node)
            node = node.parent
        return path, True
    children = node.genChildren()
    if current_depth == max_depth:
        return None, False
    bottom_reached = True
    for child in children:
        result, bottom_reached_rec = IDFSRec(child, current_depth + 1, max_depth)
        if result is not None:
            return result, True
        bottom_reached = bottom_reached and bottom_reached_rec
    return None, bottom_reached


def DFS():
    stack = []
    stack.insert(0, 0)
    stack.insert(0, start)
    visited_nodes = []
    while(len(stack) != 0):
        node = stack.pop(0)
        depth_node = stack.pop(0)
        visited_nodes.append(node)
        print(node.matrix)
        # print("Nós já visitados:", len(visited_nodes),"Nós por visitar:", len(stack), "Profundidade do Nó a ser analisado:", depth_node)
        if(node.isGoal()):
            path = []
            while(node != None):
                path.insert(0, node.matrix)
                node = node.parent
            return path
        children = node.genChildren()
        for child in children:
            if(child not in visited_nodes):
                stack.insert(0, depth_node+1)
                stack.insert(0, child)
                visited_nodes.append(child)




start = node()
goal = node()
    
def get_input():
        global strategy, start_list, goal_list, start, goal, method
        start_list = list(map(int, input("Posição inicial: ").split()))
        goal_list = list(map(int, input("Posição final: ").split()))
        start.create_matrix(start_list)
        goal.create_matrix(goal_list)
        method = input("Escolha uma destas estratégias de busca (DFS, BFS, IDFS, A*-misplaced, A*-Manhattan, Greedy-misplaced, Greedy-Manhattan): ")



def findGoal(num, goal):
    for i in range(n):
        for j in range(n):
            if goal.matrix[i][j] == num:
                return i, j



get_input()

if not solvability(start_list):
    print("Configuraão inicial não leva à configuração final proposta")
else:
    path = []
    if method == "DFS":
        start_time = timer()
        path = DFS()
        end_time = timer()
    elif method == "BFS":
        start_time = timer()
        path = BFS()
        end_time = timer()
    elif method == "IDSF":
        start_time = timer()
        path = IDFS()
        end_time = timer()
    elif method == "A*-misplaced":
        start_time = timer()
        path = astar_misplaced()
        end_time = timer()
    elif method == "A*-Manhattan":
        start_time = timer()
        path = astar_manhattan()
        end_time = timer()
    elif method == "Greedy-misplaced":
        start_time = timer()
        print(BFS())
        end_time = timer()
    elif method == "Greedy-misplaced":
        start_time = timer()
        print(BFS())
        end_time = timer()
    else:
        print("Por favor escolha uma estratégia de pesquisa válida")
    for matrix in path:
        matrix.print_matrix()
    print(f"Profundidade: {len(path)-1}")
    print(f"Tempo demorado: {round(end_time-start_time, 3)} segundos")

