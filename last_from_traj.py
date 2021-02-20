"""Simplest way to save the last images of a trajectory in another trajectory.

Run python last_from_traj.py <filename> <number of images>

Where <filename> is the trajectory file that you want to slice and
<number of images> is the last number of structures in the original
trajectory you want to extract.

"""
from ase.io import write
from ase.io.trajectory import Trajectory
import sys


def save_last_images(fname, no_images):
    traj = Trajectory(fname)
    write(f'last_{no_images}.traj', traj[-no_images:])

def save_from_one_image_to_end(fname, image, rootname):
    traj = Trajectory(fname)
    write(f'{rootname}_from_{image}_to_end.traj', traj[image:])

def extract_images(fname, first, last):
    traj = Trajectory(fname)
    write(f'image_{first}-{last}.traj', traj[first:last])

#if __name__ == "__main__":
#   traj_file = sys.argv[1]
#   no_images = int(sys.argv[2])
#   save_last_images(traj_file, no_images)

#traj_file = sys.argv[1]
#print (len(traj_file))
fname = "../R3-R39.traj"
rootname = fname.split('.traj')[0].split('/')[-1]
#traj_file = Trajectory(fname)
#print (fname, rootname, traj_file)
#sys.exit()

# For the ADF packmol reactants approach, i.e. generating the R1-1959fs-R24__Analysis stuff:
#save_from_one_image_to_end(fname, int(3267), rootname)

# For extracting last 10ps trajectory, for analysis of reactions: - Part 1:
last = 10000
save_last_images(fname, int(last))

# Part 2: Printing a shift_time, that consists of [len(Trajectory(fname)) - 10ps]
#traj_file = Trajectory(fname)
#shift_time = len(traj_file) - int(last)

