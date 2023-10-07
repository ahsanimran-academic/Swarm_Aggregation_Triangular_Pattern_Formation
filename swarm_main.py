import numpy as np
import matplotlib.pyplot as plt
import math
import random
from celluloid import Camera



iteration_number = 50000
swarms = 6

swarm_distance = np.zeros((swarms, swarms, iteration_number))

#randomize swarm postion initialization
swarm_position = np.zeros((swarms, 2, iteration_number))
for i in range(swarms):
    for j in range(2):
        swarm_position[i,j,0] = random.randint(0,100)


# initialize delta for all pairs
delta = np.zeros((6,6))
d = 0.05
delta[0,1] = d
delta[0,2] = d
delta[1,2] = d
delta[0,4] = d/2
delta[0,3] = d/2
delta[0,5] = math.sqrt((d)**2-(d/2)**2)
delta[1,4] = d/2
delta[1,5] = d/2
delta[1,3] = math.sqrt((d)**2-(d/2)**2)
delta[2,5] = d/2
delta[2,3] = d/2
delta[2,4] = math.sqrt((d)**2-(d/2)**2)
delta[3,4] = d/2
delta[3,5] = d/2
delta[4,5] = d/2

for i in range(6):
    for j in range(6):
        if delta[i,j] == 0:
            delta[i,j] = delta[j,i]
            
# initialize a, b, c for all pairs             
a = np.zeros((6,6))            
b = np.zeros((6,6))
c = np.zeros((6,6))            

for i in range(6):
    for j in range(6):
        if i == j:
            a[i,j] = 0
        else:
            a[i,j] = 0.1

for i in range(6):
    for j in range(6):
        if i == j:
            c[i,j] = 0
        else:
            c[i,j] = 0.2  

# computing b using a,c and delta for all pairs
for i in range(6):
    for j in range(6):
        if i != j:
            b[i,j] = a[i,j] * (math.exp((delta[i,j]**2)/c[i,j]))

# updating swarm_position
f = np.zeros((swarms, swarms, 2))

def compute_distance(pos_i, pos_j):
    dis = math.sqrt((pos_i[0] - pos_j[0])**2 + (pos_i[1] - pos_j[1])**2)
    return dis

for iteration in range(1,iteration_number):
    for i in range(swarms):
        for j in range(swarms):
            if i != j:
                dis = compute_distance(swarm_position[i,:,iteration-1], swarm_position[j,:,iteration-1])
                swarm_distance[i,j,iteration-1] = dis
                f[i,j,:] = -(swarm_position[i,:,iteration-1] - swarm_position[j,:,iteration-1])* (a[i,j] - b[i,j]* math.exp(-dis**2/c[i,j]))          
        f_i1 = np.sum(f[i,:,0])
        f_i2 = np.sum(f[i,:,1])
        f_i = np.zeros((2,))
        f_i[0,] = f_i1
        f_i[1,] = f_i2
        swarm_position[i,:,iteration] = swarm_position[i,:,iteration-1] + f_i
    if f_i.all()>= 0 and f_i.all()<=0.001:
         break
        

plt.scatter(swarm_position[:,0,iteration],swarm_position[:,1,iteration])


#creating gif 
camera = Camera(plt.figure())
for i in range(200, swarm_position.shape[2], 30):
    plt.scatter(swarm_position[:,0,i],swarm_position[:,1,i], s=500)
    camera.snap()
animation = camera.animate(blit=True)
animation.save('output.gif')

# fig = plt.figure()
# ax = plt.subplot(111)
# ax.scatter(swarm_position[:,0,iteration],swarm_position[:,1,iteration], s=50, c = 'green')
# plt.title('Iteration {:02d}'.format(iteration))
# fig.savefig('plot_{:02d}.png'.format(iteration))