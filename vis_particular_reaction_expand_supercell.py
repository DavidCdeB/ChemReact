#

# to use in those cases where we want to extract a video and unfortunately the fragment is too long that we have to repeat(( )) the cell to capture those missing atoms. We just need to do this: image = image.repeat((n1, n2, n3)) in both instances:

import re
import os
import sys
from ase.io.trajectory import Trajectory
from ase.io import read
from ase.visualize import view
import numpy as np
import matplotlib.pyplot as plt

def get_reaction(traj_file, time, all_reaction_indices): #, bond):
    traj_file = Trajectory(traj_file)
    traj_file2 = f"{time}fs__bonds.traj"
    traj2 = Trajectory(traj_file2, 'w')

    initial = 0

    # Processing image = initial = 0:
    for i, image in enumerate(traj_file[:initial+1]):
        print (len(image), image)
        image = image.repeat((1, 2, 1))  # here we expand the supercell
        print (len(image), image)
        sub = image[all_reaction_indices]

        L1 = sub.get_cell()[0]
        L2 = sub.get_cell()[1]
        L3 = sub.get_cell()[2]

        center = 0.5 * (L1 + L2 + L3)
        dist_cum = np.zeros(len(sub))
        for j in range(len(sub)):
            pos_atom0 = sub.get_positions()[j]
            V = pos_atom0 - center
            sub.set_positions(sub.get_positions() - V)
            sub.wrap()
            for k in range(len(sub)):
                if k != j:
                    C1 = L1/np.linalg.norm(L1)**2
                    C2 = L2/np.linalg.norm(L2)**2
                    C3 = L3/np.linalg.norm(L3)**2
                    vec = sub.get_positions()[k] - center
                    test = [np.abs(np.dot(vec,C1)), np.abs(np.dot(vec,C2)), np.abs(np.dot(vec,C3))]
                    num=np.amax(test)
                    if num > dist_cum[j]:
                        dist_cum[j]= num
        minimum=np.argmin(dist_cum)

        # using this minimum in image = initial = 0: In principle this is not needed
        sub = image[all_reaction_indices]
        pos_atom0 = sub.get_positions()[minimum]
        V = pos_atom0 - center
        sub.set_positions(sub.get_positions() - V)
        sub.wrap()


    # Processing all images: # restricting the visualization to the interval where reaction occurs:
#   intial = time-70
    initial = 0
    final = len(traj_file) #time+100
#       final = len(self.traj)
#   for i, image in enumerate(traj_file[initial+1:final+1]):
    for i, image in enumerate(traj_file[initial:final+1]):
        image = image.repeat((1, 2, 1)) # here we expand the supercell
        sub2 = image[all_reaction_indices]
        for s in range(len(sub2)):
            dist = 1000
            stat = sub2.get_positions()[s]
            for h in [-1,0,1]:
                for j in [-1,0,1]:
                    for k in [-1,0,1]:
                        tras =  sub2.get_positions()[s] - V
                        pos = tras + h*L1 + j*L2 + k*L3
                        curr_dist = np.linalg.norm(pos-sub.get_positions()[s])
                        if curr_dist < dist :
                            dist = curr_dist
                            stat = pos
            sub2[s].position = stat
        traj2.write(sub2)

# Name of .traj file where to operate:
ruta = os.path.abspath(".")
data = ruta.split("/")

#r = re.compile(".*_Analysis.*")
#auxa = list(filter(r.match, data))
#target = re.findall(r".+?(?=\__)", auxa[0])

#traj_file = "../../../../" + target[0] + ".traj" # global
traj_file = "5869fs__bonds.traj"
print ('traj_file = ', traj_file)

# time where to operate (check Reactions_Open_Table_one_line_per_reaction.pdf) times
time = "5869_SC_1x2x1_v2"

# target indices (check Connected_Open.pdf) indices

# If you need to track several indices, do this:
# 5869_and_5916_and_9770
# t = 5869:
t_5869 = [ 35, 36, 4, 42, 6, 38, 39, 12, 33, 22, 24, 25, 77, 60, 26, 70, 43, 56, 64, 83, 45, 80, 66, 50, 74, 61, 54, 58, 75, 57, 59, 52, 51, 73, 53, 84, 44, 62, 63, 46, 72, 71, 48 ]


all_reaction_indices = list(t_5869)

# Otherwise, just:
#all_reaction_indices = [ , ]

# Calling the function:
get_reaction(traj_file, time, all_reaction_indices)
