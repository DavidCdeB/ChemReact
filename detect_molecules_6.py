import numpy as np
from ase.visualize import view
from ase.io import read
from ase.neighborlist import NeighborList
from scipy import sparse
import collections
from collections import Counter
from ase.io.trajectory import Trajectory
import multiprocessing
import sys
import itertools

import os, fnmatch
import re
from ase.db import connect

# Name of .traj file where to operate:
#ruta = os.path.abspath(".")
#data = ruta.split("/")

#r = re.compile(".*_Analysis.*")
#auxa = list(filter(r.match, data))
#target = re.findall(r".+?(?=\__)", auxa[0])
#traj_file = "./" + target[0] + ".traj" # global 

# Automated way of finfing the name of .traj file where to operate:
def find(pattern, path):
    result = []
    for files in os.listdir(path):
        if fnmatch.fnmatch(files, pattern):
            result.append(files)
    return result

target = find('*.traj', '.')
if len(target) > 1:
    print ('There is more than one *.traj in this folder. Please specify')
    sys.exit()

traj_file = target[0]
print (traj_file)

def process_image(image_number):

    traj = Trajectory(traj_file)

    Trajectory_Fragments = []
    Trajectory_Fragments_for_view = []

    atoms = traj[image_number]

    syms = atoms.get_chemical_symbols()

    cutoff_dict = {'Al': 1, 'Cl': 1.7, 'H': .37, 'O': 1, 'N': 1, 'C': 1}

    cutoffs = [cutoff_dict[s.symbol] for s in atoms]

    nl = NeighborList(cutoffs, skin=0, self_interaction=False, bothways=False)
    nl.update(atoms)
    mat = nl.get_connectivity_matrix(sparse=False)
    Cl_indices = np.array([a.index for a in atoms if a.symbol == 'Cl'])
    for i in Cl_indices:
        for j in range(len(atoms)):
            if syms[j] != 'Al':
                mat[i, j] = 0
                mat[j, i] = 0
 
    n_components, component_list = sparse.csgraph.connected_components(mat)
 
    All_fragments = []
    All_fragments_for_view = []
    for i in range(n_components):
    #   view(atoms[np.where(component_list == i)[0]])

        fragments_for_view = atoms[np.where(component_list == i)[0]]
        fragments = atoms[np.where(component_list == i)[0]].get_chemical_formula()
    
        All_fragments.append(fragments)
        All_fragments_for_view.append(fragments_for_view)
 
    Trajectory_Fragments.append(All_fragments)
    Trajectory_Fragments_for_view.append(All_fragments_for_view)

    dict_fragments = Counter(All_fragments)


    # N-Dimensional list of lists -> 1D list, so that counter works properly!
    flat_Trajectory_Fragments = [item for sublist in Trajectory_Fragments for item in sublist]
    flat_Trajectory_Fragments_for_view = [item for sublist in Trajectory_Fragments_for_view for item in sublist]

    # to remove duplicates:
    from collections import defaultdict
    formula_dct = defaultdict(list)
    All_chemical_formula_in_flat_Trajectory_Fragments_for_view = []
    for i in flat_Trajectory_Fragments_for_view:
        chemical_formula_in_flat_Trajectory_Fragments_for_view = i.get_chemical_formula()
        formula_dct[chemical_formula_in_flat_Trajectory_Fragments_for_view].append(i)
        All_chemical_formula_in_flat_Trajectory_Fragments_for_view.append(chemical_formula_in_flat_Trajectory_Fragments_for_view)

    """Save a trajectory of the fragments:  """
#   for formula, images in formula_dct.items():
#       traj = Trajectory(formula + ".traj", mode="w")
#       for img in images:
#           traj.write(img)

    u, indices = np.unique(All_chemical_formula_in_flat_Trajectory_Fragments_for_view, return_index=True)

    res_list = [flat_Trajectory_Fragments_for_view[i] for i in indices] 

    """Save a database:  """
#   if os.path.exists("./species.db"):
#       os.remove("./species.db")
#   else:
#       print('File does not exists')

#   outdb = connect('./species.db')
#   for i in res_list:
#       print ('i to view = ', i.get_chemical_formula())
#       outdb.write(i)
  
    """
    to show an overview of the database: 'ase db species.db'
    to view a fragment of the database:  'ase gui species.db@<id>'
    to show complete list: 'ase db species.db  --limit=0'
    """
    """ partition the trajectory:
        `ase convert R3-R19.traj@:1000 -o 1ps.traj`
        from t=209fs to t=210fs: `ase convert -n 209:211 R3-R19.traj   209-210ps.traj`
    """


    dict_Trajectory_Fragments = Counter(flat_Trajectory_Fragments)

    f = open('molecules_found.dat.%d' % image_number, 'w')
    total_fragments = sum(dict_Trajectory_Fragments.values())
    for chemical_symbol, number in sorted(dict_Trajectory_Fragments.items(), reverse=True, key=lambda item: item[1]):
         print("{:>15} = {:>2}  {:3.20f} %".format(chemical_symbol, number, (number/total_fragments)*100.), file=f)
    f.close()
    return dict_Trajectory_Fragments

def main():
    TimeStep_ps = 0.001

    traj = Trajectory(traj_file)

    N_images = len(traj)

    import subprocess
    subprocess.check_call("for i in molecules_found.dat.*; do rm -Rf $i; done", shell=True)

    pool = multiprocessing.Pool(processes=24)
#   res = pool.map(process_image, range(9))
    res = pool.map(process_image, range(N_images))

    # If the number of molecules_found.dat.* files is very very large (i.e. the trajectory is large), this cat command can saturate and give error: /bin/cat: Argument list too long
#   output = subprocess.check_output("cat molecules_found.dat.*  |  awk '{print $1}' | sort  | uniq", shell=True)
    # so we just substitute it by a for loop:

    output = subprocess.check_output("for f in molecules_found.dat.* ; do cat $f >> all_molecules_found.dat; done", shell=True)
    output = subprocess.check_output("cat all_molecules_found.dat  |  awk '{print $1}' | sort  | uniq", shell=True)
    LABELS=[x.decode('utf-8') for x in output.splitlines()]

    time_series=collections.defaultdict(list)
    time_series_count=collections.defaultdict(list)
    for step, moldict in enumerate(res):
        total_fragments = sum(moldict.values())
        for mol in LABELS:
            try:
                concentration = (moldict[mol]/total_fragments)*100
                counts = moldict[mol]
            except KeyError:
                concentration = 0
                counts = 0

            time_series[mol].append(concentration)
            time_series_count[mol].append(counts)

    for key, val in time_series.items():
        # If 1st time is 1ps: 
#       time = np.arange(TimeStep_ps, (N_images+1)*1E-3, TimeStep_ps)
        # If 1st time is 0ps: 
        time = np.arange(0, (N_images)*1E-3, TimeStep_ps)
        output = np.vstack((val, time)).T
        np.savetxt(key+".txt", output)

    for key, val in time_series_count.items():
        # If 1st time is 1ps: 
#       time = np.arange(TimeStep_ps, (N_images+1)*1E-3, TimeStep_ps)
        # If 1st time is 0ps: 
        time = np.arange(0, (N_images)*1E-3, TimeStep_ps)
        output = np.vstack((val, time)).T
        np.savetxt(key+".count.txt", output)

    # Don't need 40K number of files; only all_molecules_found.dat for scatter.py to work.
    # you can get /usr/bin/rm: Argument list too long, so
    subprocess.check_call("for i in molecules_found.dat.*; do rm -Rf $i; done", shell=True)


if __name__ == "__main__":
    main()
