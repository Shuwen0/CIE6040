
import sys


class Node():
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action


# Please finish this stack function for DFS
class StackFrontier():

    def __init__(self):
        """
        define an empty frontier
        """
        self.frontier = []

    def add(self, node):
        """
        adds node  to the frontier
        """ 
           
        self.frontier.append(node)

    def contains_state(self,state):
        """
        checks if the frontier contains a particular state
        """    
        for node in self.frontier:
            if state == node.state:
                return node
            
        return False

    def empty(self):
        """
        check whether the frontier is empty or not
        """    
        return len(self.frontier) == 0

    def remove(self):
        """
        remove node to the frontier based on stack structure
        """    
        return self.frontier.pop()


# Please finish this queue function for BFS
class QueueFrontier(StackFrontier):
    def remove(self):
        """
        remove node to the frontier based on queue structure
        """    
        if not self.empty():
            return self.frontier.pop(0)

class Maze():
    def __init__(self,filename):

        # Read file and set height and width of maze 
        with open(filename) as f:
            contents = f.read()

        # validate start and goal
        if contents.count("A") !=1:
            raise Exception("maze must have exactly one start point")

        if contents. count("B") !=1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = [] # 2D list: height, width
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A": # start
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j] == "B": # end
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == " ": # okay to proceed
                        row.append(False)
                    else:
                        row.append(True) # blocked
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("▊", end="") # walls
                elif (i,j) == self.start:
                    print("A", end="")
                elif (i,j) == self.goal:  
                    print("B", end="")
                elif solution is not None and (i ,j) in solution:
                    print("*", end="") # the step included in solution
                else:
                    print(" ", end="") # the path not taken
            print()
        print()

    def neighbors(self,state):
        '''return a list of tuples of (action, (r,c))'''
        row, col = state

        # All possible actions
        candidates = [
            ("up", (row -1, col)),
            ("down", (row+1, col)),
            ("left", (row, col -1)),
            ("right", (row, col +1))
        ]

        # Ensure action are valid 
        result = []
        for action, (r,c) in candidates:
            try:
                if not self.walls[r][c] and (r >= 0) and (c >= 0): # self.walls[r][c] == True --> blocked; assume positive index!
                    result.append((action, (r,c)))
            except IndexError:
                continue
        return result

    # plese finish the solve function that help the machine to figure out how to actually get from point A to point B
    def solve(self, method="BFS"):
        """ 
        Finds a solution to maze, if one exists, default method is 'DFS'.
        :param: method: string, 'DFS' or 'BFS', default is 'DFS'
        """
        

        if method == 'DFS':
            frontier = StackFrontier()
        else:
            frontier = QueueFrontier()
            

        # ================================= DFS =========================================
        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state = self.start, parent = None, action = None)

        # Initialize a solution as a stack
        frontier = StackFrontier()
        frontier.add(start)

        self.explored = []

        while (frontier.contains_state(self.goal) == False) and (frontier.empty() == False):
            
            current_node = frontier.remove()
            self.explored.append(current_node.state)
            self.num_explored += 1
            if len(self.neighbors(current_node.state)) != 0:
                for (action, state) in self.neighbors(current_node.state):
                    if (state not in self.explored) and (not frontier.contains_state(state)):
                        frontier.add(Node(state, current_node, action))
                        if state == self.goal:
                            break
                    
        if frontier.contains_state(self.goal):
            self.solution = []
            goal_node = frontier.contains_state(self.goal)
            current_node = goal_node
            while current_node.parent != None:
                self.solution.append(current_node.state)
                current_node = current_node.parent
            
            self.solution = [[], self.solution]
                

                    


    def output_image(self, filename, show_solution = True, show_explored= False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a black canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height *cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40,40,40)

                # Start
                elif (i,j) == self.start:
                    fill = (255, 0 ,0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0,171,28)


                #Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220,235,113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212,97,85)
                
                # Empty cell
                else:
                    fill = (237, 240, 252)


                # Draw cell
                draw.rectangle(
                    ([ ( j*cell_size + cell_border,  i*cell_size + cell_border ),
                       ( (j+1)*cell_size - cell_border, (i+1)*cell_size - cell_border  ) ]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) !=2:
    sys.exit("Usage: python maze.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png")
# m.output_image("maze.png", show_explored = True)

# debug
# print(len(m.explored))
# print(len(set(m.explored)))
# walls = 0
# for (r,c) in m.explored:
#     if m.walls[r][c]:
#         walls += 1
# print(walls)
# print(m.explored)

    













        



            


