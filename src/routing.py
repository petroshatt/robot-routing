import json
import numpy
import sys
import collections
from random import choice

global json_data

#Parse json file
def pars_json(file):
    
  f = open(file)
  
  data = json.load(f)

  f.close()

  return data


possible_alg = ['BFS', 'A', 'B']

json_data = pars_json("../data/json_rout.json")

x_grid = json_data["grid_x"]
y_grid = json_data["grid_y"]


#Grid with zeros
grid = [ ["0"] * y_grid for _ in range(x_grid)]

#Assign "1" to grid for obstacles
for i in range(len(json_data["obstacle"])):
	assign_obs_x = json_data["obstacle"][i][0]
	assign_obs_y = json_data["obstacle"][i][1]
	grid[assign_obs_y - 1][assign_obs_x - 1] = "1"

#Start point and assign "S" to grid for start
start_x = json_data["start_point"][0]
start_y = json_data["start_point"][1]
start_p = (start_x, start_y)

grid[start_y - 1][start_x - 1] = "S"

#End point and assign "E" to grid for end
end_x = json_data["end_point"][0]
end_y = json_data["end_point"][1]
end_p = (end_x, end_y)

grid[end_y - 1][end_x - 1] = "E"

print()
print(numpy.matrix(grid))
print()

ALG_FLAG = sys.argv[1]


def randAlg():

  path = []
  curr_x = start_x
  curr_y = start_y
  curr_p = (curr_x, curr_y)

  while (curr_p != (end_x, end_y)):

    #Excluded moves
    excl = []

    #Exclude moves because of grid limits
    if curr_y <= 1:
      excl.append(1)
    if curr_y >= y_grid:
      excl.append(2)
    if curr_x <=1:
      excl.append(3)
    if curr_x >= x_grid:
      excl.append(4)

    #Exclude moves because of obstacles
    try:
      if grid[curr_y+1-1][curr_x-1] == "1":
        excl.append(2)
    except:
      pass

    try:
      if grid[curr_y-1-1][curr_x-1] == "1":
        excl.append(1)
    except:
      pass

    try:
      if grid[curr_y-1][curr_x+1-1] == "1":
        excl.append(4)
    except:
      pass

    try:
      if grid[curr_y-1][curr_x-1-1] == "1":
        excl.append(3)
    except:
      pass

    #Check if every move is excluded - meaning no moves available - then terminate
    if 1 in excl and 2 in excl and 3 in excl and 4 in excl:
      break

    #Algorithm B - Random navigation with path memory
    if ALG_FLAG == "B":

      while True:

        #Choose random move from the valid ones
        move = choice([i for i in range(1,5) if i not in excl]) #1-UP 2-DOWN 3-LEFT 4-RIGHT

        #Update next point based on move
        if move == 1:
          next_x = curr_x
          next_y = curr_y-1
          next_p = (next_x, next_y)
        elif move == 2:
          next_x = curr_x
          next_y = curr_y+1
          next_p = (next_x, next_y)
        elif move == 3:
          next_x = curr_x-1
          next_y = curr_y
          next_p = (next_x, next_y)
        elif move == 4:
          next_x = curr_x+1
          next_y = curr_y
          next_p = (next_x, next_y)

        if len(path) > 0:
          if next_p == path[-1]: #Checks just the previous point
          #if next_p in path:    #Checks every previous point
            if len(excl) == 3:    
              break
          else:
            break
        else:
          break

    #Algorithm A - completely random navigation
    elif ALG_FLAG == "A":

      #Choose random move from the valid ones
      move = choice([i for i in range(1,5) if i not in excl]) #1-UP 2-DOWN 3-LEFT 4-RIGHT

      #Update next point based on move
      if move == 1:
        next_x = curr_x
        next_y = curr_y-1
        next_p = (next_x, next_y)
      elif move == 2:
        next_x = curr_x
        next_y = curr_y+1
        next_p = (next_x, next_y)
      elif move == 3:
        next_x = curr_x-1
        next_y = curr_y
        next_p = (next_x, next_y)
      elif move == 4:
        next_x = curr_x+1
        next_y = curr_y
        next_p = (next_x, next_y)

    #Append point on path list
    path.append(curr_p)

    #Update point - next is now current
    curr_x = next_x
    curr_y = next_y
    curr_p = next_p

  #Append last point
  path.append(curr_p)
  print(path)
  print()


def bfs(grid, start):

    wall, clear, goal = "1", "0", "E"
    width, height = x_grid, y_grid

    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y-1][x-1] == goal:
            print(path)
            print()
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))


# def initJSON():

#   init_json_str = json.dumps({
#     "xdimension": x_grid,
#     "ydimension": y_grid,
#     "grid_size": 25,
#     "label": "Robot Emulator",
#     "obstacle": [],
#     "robots": [],
#     "robots_movements": [],
#     "exits": [],
#     "end": "false"
#   })


# def pathToJSON():

#   json_str = json.dumps({"robots_movements":[{
#     "robot_name": str(sys.argv[2]),
#     "line_color": "("+ str(sys.argv[3]) + ")",
#     "move":[]}
#     ]})

#   print(json_str)



if __name__ == "__main__":

  if ALG_FLAG in possible_alg:
    print("Algorithm " + ALG_FLAG + " is executed." + "\n")

    #Algorithm B - Random navigation with path memory
    if ALG_FLAG == "BFS":
      bfs(grid, start_p)

    else:
      randAlg()

  else:
    print("Incorrent argument." + "\n")

  #pathToJSON()






