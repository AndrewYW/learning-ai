import sys
import numpy as np
from random import randint
from time import time
import writer
import Queue

class Node:
    def __init__(self, matrix, x, y):
        self.matrix = matrix
        self.steps = int(matrix[x][y])
        self.visited = 0
        self.depth = -1
        self.children = []
        self.index = len(matrix)
        self.x = x
        self.y = y
    
    def get_depth(self):
        return str(self.depth)
    def get_up(self, nodes):
        up = self.x - self.steps
        if up >= 0:
            self.children.append(get_node(nodes, up, self.y))
    def get_down(self, nodes):
        down = self.x + self.steps
        if down < self.index:
            self.children.append(get_node(nodes, down, self.y))
    def get_left(self, nodes):
        left = self.y - self.steps
        if left >= 0:
            self.children.append(get_node(nodes, self.x, left))
    def get_right(self, nodes):
        right = self.y + self.steps
        if right < self.index:
            self.children.append(get_node(nodes, self.x, right))

def get_node(nodes, x, y):
    return nodes[x][y]
    
def bfs(node_matrix):
    """
    BFS function
    Adjusts node fields in a given node matrix:
    Visited, depth
    """
    q = Queue.Queue()
    q.put(node_matrix[0][0])
    node_matrix[0][0].depth = 0
    while not q.empty():
        node = q.get()
        if node.visited == 0:
            node.visited = 1
            depth = node.depth
            for item in node.children:
                q.put(item)
                if item.depth == -1:
                    item.depth = depth + 1
def get_eval_from_nodes(node_matrix):
    index = len(node_matrix[0])
    if node_matrix[index-1][index-1].depth == -1:
        eval = 0
        for i in range(index):
            for j in range(index):
                if node_matrix[i][j].depth == -1:
                    eval -= 1
        return eval
    else:
        return node_matrix[index-1][index-1].depth

def create_node_matrix(matrix):
    """
    Creates a matrix of nodes given an integer matrix
    """
    index = len(matrix[0])
    node_matrix = []
    for i in range(index):
        node_matrix.append([])
        for j in range(index):
            node_matrix[i].append(Node(matrix, i, j))
    for row in node_matrix:
        for node in row:
            if not node.steps == 0:
                node.get_up(node_matrix)
                node.get_down(node_matrix)
                node.get_left(node_matrix)
                node.get_right(node_matrix)
    return node_matrix
def generate_string_matrix(node_matrix):
    index = len(node_matrix[0])
    string_matrix = [['' for x in range(index)] for y in range(index)]
    for i in range(index):
        for j in range(index):
            if node_matrix[i][j].depth == -1:
                string_matrix[i][j] = 'X'
            else:
                string_matrix[i][j] = str(node_matrix[i][j].depth)

    return string_matrix
def generate_matrix(index):
    matrix = np.empty([index, index], dtype=int)
    for i in range(index):
        for j in range(index):
            if((i == index -1) and (j == index - 1)):
                matrix[i][j] = 0
            else:
                matrix[i][j] = randint(
                    1, max(index - (i + 1), i, index - (j + 1), j))

    return matrix
def main():
    index = int(input('Puzzle index:\n'))
    training = int(input('Number of random training puzzles:\n'))
    trainingOptimized = int(input('Number of optimized training puzzles:\n'))
    valid = int(input('Number of validation puzzles:\n'))
    validOptimized = int(input('Number of optimized validation puzzles:\n'))
    test = int(input('Number of test puzzles:\n'))
    testOptimized = int(input('Number of optimized test puzzles:\n'))

    for i in range(training):
        matrix = generate_matrix(index) #create random matrix (this is integer 2d list)
        node_matrix = create_node_matrix(matrix) #create node matrix

        start_ms = int(round(time() * 1000))
        bfs(node_matrix) #Solves the node matrix
        end_ms = int(round(time() * 1000)) - start_ms
        elapsed = str(end_ms)
        
        string_matrix = generate_string_matrix(node_matrix)
        eval_function = str(get_eval_from_nodes(node_matrix)) #Get evaluation function from solved node matrix

        writer.write_puzzle(matrix, '../data/puzzledata/trainingpuzzles')
        writer.write_eval(eval_function, '../data/puzzledata/trainingpuzzlelabels')
        writer.write_time(elapsed, '../data/puzzledata/trainingpuzzletimes')

        """
        for line in string_matrix:
            print line
        print 'Eval function: ', eval_function
        print elapsed, ' ms'
        """
        


    """
    Generate random puzzles
    Create node matrices
    Solve node matrices, tracking time
    Get evaluation function
    Store 
    """
        

if __name__ == "__main__":
    main()