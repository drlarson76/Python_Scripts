# RandomWalk2

# Predicts the occurrence percentage of traveleing more than 4 blocks
#   if turn direction is random at each intersection.


import random

def random_walk_2(n):
    """Return coordinates after 'n' block random walk."""
    x, y = 0, 0
    for i in range(n):
        (dx, dy) = random.choice([(0,1), (0, -1), (1, 0), (-1, 0)])
        x += dx
        y += dy
    return(x,y)

number_of_walks = 1000 # Number of Trials for each walk length.

#for walk_length in range(1,31):
print("'No transport' means less than 4 blocks from start.")
for walk_length in [30, 100, 1000, 10000]:  # Walk lengths in blockes.
    no_transport = 0 # Number of walks 4 or less blocks from home
    for i in range(number_of_walks):
        (x, y) = random_walk_2(walk_length)
        distance = abs(x) + abs(y)
        if distance <= 4:
            no_transport += 1
    no_transport_percentage = float(no_transport) / number_of_walks
    
    print("Walk size = ", walk_length, " blocks. ", 
          round(100*no_transport_percentage,3), "% no transport" )
            
