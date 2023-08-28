import pygame, sys


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra Algorithm")
ROWS = 50

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width  # calculating x/y coordinate given row/col and width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    def get_pos(self):             # get-pos method called on Spot-obj
        return self.row, self.col  # return row, col
    def is_closed(self):
        return self.color == RED   # retusn boolean based condition
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE
    def make_closed(self):   # changes attribute
        self.color = RED
    def make_open(self):
        self.color = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))  # this method is called on spot-obj

    def update_neighbors(self, grid):     # method is called on every spot-obj, uses its attributes
        self.neighbors = []   # add spot-obj to self.neighbors if neighbor is blank
        if self.row < self.total_rows-1 and not grid[self.row + 1][self.col].is_barrier():   # down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():   # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col + 1].is_barrier():   # right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():   # left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def get_click_pos(pos, rows, width):
    gap = width // rows    # gap = width of cubes
    y, x = pos          # pos = mouse-click-position

    row = y // gap
    col = x // gap
    return row, col  # returns row/col of mouse-click-position

def draw_grid(win, rows, width):
    gap = width // rows   # gap = distance between each line
    for i in range(rows):  # horizontal lines, (0, 3*gap), (width, 3*gap)
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))  # drawing line(win,color,(x,y),(x,y))
        for j in range(rows):  # vertical lines, (3*gap, 0), (3*gap, width)
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))
def draw(win, grid, rows, width):
    #win.fill(WHITE)

    for row in grid:     # grid is made up of lists, for every list-row in grid
        for spot in row: # for spot-obj in list-row
            spot.draw(win)  # calling draw method on spot-obj, draws colors

    draw_grid(win, rows, width)
    pygame.display.update()

def make_grid(rows, width):
    grid = []               # grid is made of lists with spot-objects
    gap = width // rows     # gap = width of cube
    for i in range(rows):   # for every row
        grid.append([])    # append empty list-row to grid
        for j in range(rows):  # for every spot in empty list-row
            spot = Node(i, j, gap, rows)   # spot-obj, passing(row, col, width, total_rows)
            grid[i].append(spot)         # append spot-obj to list-row i in grid

    return grid

def reconstruct_path(from_list, start, end):
	if end == start:
		return
	end.make_path()
	reconstruct_path(from_list, start, from_list[end])

def min_distance(dis, visited_nodes):  # given current DFS-dict and visted-nodes-dict
    min_node = next(iter(dis))    # min-node = next-item-in-iterator-DFS
    for node in dis:    # for evrey node-obj in DFS-dict
        if dis[node] < dis[min_node] and not visited_nodes[node]:   # if DFS(node-obj) less-than DFS(min-node) and node-obj hasn't been visited
            min_node = node                                         # setting min-node = cur-node-obj
    return min_node
    
def dijkstra_algorithm(draw, grid, start, end, win):
    dis = {node: float("inf") for row in grid for node in row}      # DFS = {node-obj:initally-infinity} each key is node-obj each value is DFS
    visited_nodes = {node: False for row in grid for node in row}   # visited-nodes = {node-obj:initally-false} each key is node-obj each value is t/f if it has been visited
    dis[start] = 0                                                  # setting DFS(start-node-obj) to zero
    from_list = {}

    while any(visited_nodes):                # any returns true if any item in iterable are true
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = min_distance(dis, visited_nodes)   # cur-node-obj = min-dis(), calling min-dis func

        if current == end:                      # if cur-node-obj equals end-node-obj
            reconstruct_path(from_list, start, end)  # calling recontruct path func
            start.make_start()
            end.make_end()
            return 
        for neighbor in current.neighbors:   # for neighbor-node-obj in cur-node-obj.neighbors-attribute
            temp_dis = dis[current] + 1      # temp-dis = DFS[cur-node-obj] +1, plus one because all edges are length 1
            if dis[neighbor] > temp_dis:     # if DFS(neighbor-node-obj) greater-than temp-dis
                dis[neighbor] = temp_dis     # setting DFS(neighbor-node-obj) equal to temp-dis
                from_list[neighbor] = current   # from  list
        
        current.make_open()
        current.draw(win)
        start.make_start()
        start.draw(win)
        visited_nodes[current] = True
        pygame.display.update()

def main(win, width):

    grid = make_grid(ROWS, width)
    source = None
    end = None
    run = True
    while run:
        draw(win, grid, ROWS, width)
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, ROWS, width)
                print("clciked: " + str(col))
                node = grid[row][col]
                if not source and node != end:   # creates start-spot
                        source = node         # start = spot-obj
                        source.make_start()   # sets start-spot-obj color to orange

                elif not end and node != source:  # creates end-spot
                    end = node                  # end = spot-obj
                    end.make_end()           # sets end-spot-obj to turquoise

                elif node != end and node != source:  # creates barrier-spots
                    node.make_barrier()

            if pygame.mouse.get_pressed()[0] and keys_pressed[pygame.K_z]:       # if right-mouse is clicked for erase
                    pos = pygame.mouse.get_pos()  # gets x,y position of mouse
                    row, col = get_click_pos(pos, ROWS, width)  # calling method returns row, col
                    node = grid[row][col]
                    node.reset()       # sets self.color = WHITE
                    if node == source:
                        source = end
                    elif node == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and source and end:
                    for row in grid:
                        for node in row:   # for every spot-obj in grid
                            node.update_neighbors(grid)  # call update_neighbors method on spot-obj pass grid
                    x = lambda: draw(win, grid, ROWS, WIDTH)
                    dijkstra_algorithm(x, grid, source, end, win)

    pygame.quit()

main(WIN, WIDTH)
