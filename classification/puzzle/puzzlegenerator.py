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
def hill_climb(node_matrix, iterations):
    """
    Hill climbing algorithm to optimize a given, unsolved node matrix.
    Returns a solved (BFS'd) node matrix.
    """
    reset_matrix(node_matrix)
    index = len(node_matrix)
    for iteration in range(iterations):
        step_matrix = create_step_matrix(node_matrix)
        temp_matrix = create_node_matrix(step_matrix)

        temp_matrix = random_step_change(temp_matrix, index)

        bfs(node_matrix)
        bfs(temp_matrix)
        node_eval = get_eval_from_nodes(node_matrix)
        temp_eval = get_eval_from_nodes(temp_matrix)

        # If new evaluation function is better, then node matrix becomes new one
        # Node matrix's depth and visited are reset so you can run solve again
        if temp_eval >= node_eval:
            node_matrix = temp_matrix
            reset_matrix(node_matrix)
        else:
            reset_matrix(node_matrix)
    bfs(node_matrix)
    return node_matrix

def random_restart(node_matrix, iterations, restarts):
    """
    Implements hill climbing algorithm on multiple randomly generated matrices.
    Number of new randoms = number of restarts.
    Returns the optimized matrix, unsolved
    """
    reset_matrix(node_matrix)
    index = len(node_matrix)

    for restart in range(restarts):
        print "Random restart hill climb iteration: ", iterations, "..."
        print "Number of random restarts: " , restart, "..."
        current_matrix = hill_climb(node_matrix,iterations)
        new_matrix = create_node_matrix(generate_matrix(index))
        new_matrix = hill_climb(new_matrix,iterations)

        current_eval = get_eval_from_nodes(current_matrix)
        new_eval = get_eval_from_nodes(new_matrix)

        if new_eval >= current_eval:
            current_matrix = new_matrix
            reset_matrix(current_matrix)
        else:
            reset_matrix(current_matrix)
    #bfs(current_matrix)            #This was needed in original, but not now
    return current_matrix
    
def get_eval_from_nodes(node_matrix):
    """
    Returns the evaluation function of a solved node matrix.
    """
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
def random_step_change(nodes, index):
    #Select random matrix spot, can't change node_matrix[index-1][index-1]
    row = randint(0, index-1)
    col = randint(0, index-1)
    while row == index - 1 and col == index -1:
        row = randint(0, index-1)
        col = randint(0, index-1)
    nodes[row][col].steps = randint(1, max(index-row-1, row, index-col-1, col))

    #Must regenerate children for changed index:
    nodes[row][col].children[:]=[]
    nodes[row][col].get_up(nodes)
    nodes[row][col].get_down(nodes)
    nodes[row][col].get_left(nodes)
    nodes[row][col].get_right(nodes)

    return nodes
def create_step_matrix(nodes):
    """
    Returns an integer matrix with values from the .steps field of a node matrix.
    """
    step_matrix = []
    index = len(nodes)

    for i in range(index):
        step_matrix.append([])
        for j in range(index):
            step_matrix[i].append(nodes[i][j].steps)

    return step_matrix

def reset_matrix(node_matrix):
    """
    Reset a node matrix's depth and visited fields to -1 and 0, respectively.
    """
    index = len(node_matrix)
    for i in range(index):
        for j in range(index):
            node_matrix[i][j].visited = 0
            node_matrix[i][j].depth = -1

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
    """
    Returns a string matrix of depth values. Converts int depths to strings.
    """
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
    """
    Creates a random matrix of square size index.
    """
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
        print "Creating unoptimized training puzzleset..."
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

    for i in range(trainingOptimized):
        print "Creating optimized training puzzle set..."
        matrix = generate_matrix(index)
        node_matrix = create_node_matrix(matrix)

        #Applies random restart algorithm to the given node matrix.
        #Each hill climb algorithm iterates 1000 times, while there are i amount of restarts.
        #This allows for a bunch of solutions at different optimization levels.
        node_matrix = random_restart(node_matrix, randint(50, 100), randint(1, 10))

        start_ms = round(time() * 1000)
        bfs(node_matrix) #Solves the node matrix
        end_ms = round(time() * 1000) - start_ms
        elapsed = str(end_ms)
        
        string_matrix = generate_string_matrix(node_matrix)
        eval_function = str(get_eval_from_nodes(node_matrix)) #Get evaluation function from solved node matrix

        writer.write_puzzle(matrix, '../data/puzzledata/trainingpuzzles')
        writer.write_eval(eval_function, '../data/puzzledata/trainingpuzzlelabels')
        writer.write_time(elapsed, '../data/puzzledata/trainingpuzzletimes')
    for i in range(valid):
        print "Creating unoptimized validation puzzle set..."
        matrix = generate_matrix(index) #create random matrix (this is integer 2d list)
        node_matrix = create_node_matrix(matrix) #create node matrix

        start_ms = int(round(time() * 1000))
        bfs(node_matrix) #Solves the node matrix
        end_ms = int(round(time() * 1000)) - start_ms
        elapsed = str(end_ms)
        
        string_matrix = generate_string_matrix(node_matrix)
        eval_function = str(get_eval_from_nodes(node_matrix)) #Get evaluation function from solved node matrix

        writer.write_puzzle(matrix, '../data/puzzledata/validationpuzzles')
        writer.write_eval(eval_function, '../data/puzzledata/validationpuzzlelabels')
        writer.write_time(elapsed, '../data/puzzledata/validationpuzzletimes')

    for i in range(validOptimized):
        print "Creating optimized validation puzzle set..."
        matrix = generate_matrix(index)
        node_matrix = create_node_matrix(matrix)

        #Applies random restart algorithm to the given node matrix.
        #Each hill climb algorithm iterates 1000 times, while there are i amount of restarts.
        #This allows for a bunch of solutions at different optimization levels.
        node_matrix = random_restart(node_matrix, randint(50, 100), randint(1, 10))

        start_ms = round(time() * 1000)
        bfs(node_matrix) #Solves the node matrix
        end_ms = round(time() * 1000) - start_ms
        elapsed = str(end_ms)
        
        string_matrix = generate_string_matrix(node_matrix)
        eval_function = str(get_eval_from_nodes(node_matrix)) #Get evaluation function from solved node matrix

        writer.write_puzzle(matrix, '../data/puzzledata/validationpuzzles')
        writer.write_eval(eval_function, '../data/puzzledata/validationpuzzlelabels')
        writer.write_time(elapsed, '../data/puzzledata/validationpuzzletimes')
    for i in range(test):
        print "Creating unoptimized test puzzle set..."
        matrix = generate_matrix(index) #create random matrix (this is integer 2d list)
        node_matrix = create_node_matrix(matrix) #create node matrix

        start_ms = int(round(time() * 1000))
        bfs(node_matrix) #Solves the node matrix
        end_ms = int(round(time() * 1000)) - start_ms
        elapsed = str(end_ms)
        
        string_matrix = generate_string_matrix(node_matrix)
        eval_function = str(get_eval_from_nodes(node_matrix)) #Get evaluation function from solved node matrix

        writer.write_puzzle(matrix, '../data/puzzledata/testpuzzles')
        writer.write_eval(eval_function, '../data/puzzledata/testpuzzlelabels')
        writer.write_time(elapsed, '../data/puzzledata/testpuzzletimes')

    for i in range(testOptimized):
        print "Creating optimized test puzzle set..."
        matrix = generate_matrix(index)
        node_matrix = create_node_matrix(matrix)

        #Applies random restart algorithm to the given node matrix.
        #Each hill climb algorithm iterates 1000 times, while there are i amount of restarts.
        #This allows for a bunch of solutions at different optimization levels.
        node_matrix = random_restart(node_matrix, randint(50, 100), randint(1, 10))

        start_ms = round(time() * 1000)
        bfs(node_matrix) #Solves the node matrix
        end_ms = round(time() * 1000) - start_ms
        elapsed = str(end_ms)
        
        string_matrix = generate_string_matrix(node_matrix)
        eval_function = str(get_eval_from_nodes(node_matrix)) #Get evaluation function from solved node matrix

        writer.write_puzzle(matrix, '../data/puzzledata/testpuzzles')
        writer.write_eval(eval_function, '../data/puzzledata/testpuzzlelabels')
        writer.write_time(elapsed, '../data/puzzledata/testpuzzletimes')

        

if __name__ == "__main__":
    main()