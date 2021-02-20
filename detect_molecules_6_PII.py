from ase.db import connect
import re
import os, fnmatch
import itertools
import sys
import multiprocessing
from ase.io.trajectory import Trajectory
from collections import defaultdict
from collections import Counter
import collections
from scipy import sparse
from ase.neighborlist import NeighborList
from ase.io import read
from ase.visualize import view
import numpy as np
import matplotlib.pyplot as plt
from functools import partial

#from visualize_reaction import ViewReaction
#from centering_tree import ViewReaction
#from centering_min import ViewReaction


# Name of .traj file where to operate:
#ruta = os.path.abspath(".")
#data = ruta.split("/")

#r = re.compile(".*_Analysis.*")
#auxa = list(filter(r.match, data))
#target = re.findall(r".+?(?=\__)", auxa[0])
#traj_file = "./" + target[0] + ".traj" # global 

#print (traj_file)


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


#sys.exit()

#traj_file = "./1900fs.traj"
#traj_file = "/home/energy/dcabu/long_paths/Correct_rho/1.5_Salt__1_Ur/Al2Cl7-__AlCl2Ur2+/NaCl/23.08.2019/SC_2x2x2/make_ok_poscar_and_potcar/AIMD/Restart_1/650K_2_300K/R3-R19__Analysis_working_indices/R3-R19.traj"
#traj_file = '900fs.traj'


# Grabbing the name of this .traj file - components.npz will adquire this name: 
traj_name = traj_file.rsplit('/')[-1].rsplit('.')[0]

dict_labels = {
        'C2H8AlCl2N4O2'       : '$[$AlCl$_{2}$(ur)$_{2}]^{+}$',
        'Al2Cl7'              : '$[$Al$_{2}$Cl$_{7}]^{-}$',
        'AlCl4'               : '$[$AlCl$_{4}]^{-}$',
        'C2H8Al2Cl5N4O2'      : '$[$Al$_{2}$Cl$_{5}$(ur)$_{2}]^{+}$',
        'C2H8Al4Cl12N4O2'     : '$[$Al$_{4}$Cl$_{12}$(ur)$_{2}]$',
        'C2H8Al3Cl8N4O2'      : '$[$Al$_{3}$Cl$_{8}$(ur)$_{2}]^{+}$',
        'C2H8Al3Cl9N4O2'      : '$[$Al$_{3}$Cl$_{9}$(ur)$_{2}]$',
        'CH4AlCl3N2O'         : '$[$AlCl$_{3}$(ur)$]$',
        'CH4Al2Cl6N2O'        : '$[$Al$_{2}$Cl$_{6}$(ur)$]$',
        'C2H8Al5Cl15N4O2'     : '$[$Al$_{5}$Cl$_{15}$(ur)$_{2}]$',
        'C3H12AlClN6O3'       : '$[$AlCl(ur)$_{3}]^{2+}$',  #x
        'H'                   : 'H',
        'CH3Al3Cl9N2O'        : 'CH$_{3}$Al$_{3}$Cl$_{9}$N$_{2}$O',
        'Cl'                  : 'Cl',
        'CH4Al3Cl9N2O'        : '$[$Al$_{3}$Cl$_{9}$(ur)$]$',
        'AlCl3'               : '$[$AlCl$_{3}]$',
        'CH4N2O'              : 'ur',
        'CH5N2O'              : 'CH$_{5}$N$_{2}$O',
        'C2H7Al2Cl5N4O2'      : 'C$_{2}$H$_{7}$Al$_{2}$Cl$_{5}$N$_{4}$O$_{2}$',
        'CH3Al2Cl6N2O'        : 'CH$_{3}$Al$_{2}$Cl$_{6}$N$_{2}$O',
        'CH4AlCl2N2O'         : '$[$AlCl$_{2}$(ur)$]^{+}$',
        'Al3Cl10'             : '$[$Al$_{3}$Cl$_{10}]^{-}$',
        'C2H7Al3Cl8N4O2'      : 'C$_{2}$H$_{7}$Al$_{3}$Cl$_{8}$N$_{4}$O$_{2}$',
        'C3H11Al2Cl4N6O3'     : 'C$_{3}$H$_{11}$Al$_{2}$Cl$_{4}$N$_{6}$O$_{3}$',
        'C2H8Al6Cl19N4O2'     : '$[$Al$_{6}$Cl$_{19}$(ur)$_{2}]^{-}$',
        'Al4Cl14'             : '$[$Al$_{4}$Cl$_{14}]^{2-}$',
        'C2H8Al2Cl6N4O2'      : '$[$Al$_{2}$Cl$_{6}$(ur)$_{2}]$',

# others:
 'C4H16Al4Cl10N8O4'  : '$[$Al$_{4}$Cl$_{10}$(ur)$_{4}]^{2+}$',
 'C4H16Al5Cl13N8O4'  : '$[$Al$_{5}$Cl$_{13}$(ur)$_{4}]^{2+}$',
 'C4H16Al6Cl17N8O4'  : '$[$Al$_{6}$Cl$_{17}$(ur)$_{4}]^{+}$',
 'C4H16Al7Cl21N8O4'  : '$[$Al$_{7}$Cl$_{21}$(ur)$_{4}]$',
 'C3H12Al4Cl11N6O3'  : '$[$Al$_{4}$Cl$_{11}$(ur)$_{3}]^{+}$',
 'C4H16Al5Cl14N8O4'  : '$[$Al$_{5}$Cl$_{14}$(ur)$_{4}]^{+}$',
 'C3H12Al5Cl15N6O3'  : '$[$Al$_{5}$Cl$_{15}$(ur)$_{3}]$',
 'C3H12Al2Cl4N6O3'   : '$[$Al$_{2}$Cl$_{4}$(ur)$_{3}]^{2+}$',
 'C2H8Al6Cl18N4O2'   : '$[$Al$_{6}$Cl$_{18}$(ur)$_{2}]$',
 'C4H16Al3Cl7N8O4'   : '$[$Al$_{3}$Cl$_{7}$(ur)$_{4}]^{2+}$',
 'C2H8AlClN4O2'      : '$[$AlCl(ur)$_{2}]^{2+}$',
 'C3H12Al3Cl7N6O3'   : '$[$Al$_{3}$Cl$_{7}$(ur)$_{3}]^{2+}$',
 'C5H20Al3Cl6N10O5'  : '$[$Al$_{3}$Cl$_{6}$(ur)$_{5}]$',
 'C2H8Al2Cl4N4O2'    : '$[$Al$_{2}$Cl$_{4}$(ur)$_{2}]^{2+}$',
 'C3H12Al5Cl14N6O3'  : '$[$Al$_{5}$Cl$_{14}$(ur)$_{3}]^{+}$',  # added Sept-2020
 'C2H8Al4Cl11N4O2'   : '$[$Al$_{4}$Cl$_{11}$(ur)$_{2}]^{+}$'  # added Sept-2020
}

class Detect(object):
    def __init__(self, traj, cutoff_dict,
                 saved_components_file=f"components_traj_{traj_name}.npz"):
        atoms = traj[0]
        self.cutoffs = [cutoff_dict[s.symbol] for s in atoms]
        self.save_file = saved_components_file
        self.syms = atoms.get_chemical_symbols()
        self.Cl_indices = np.array(
            [a.index for a in atoms if a.symbol == 'Cl'])
        self.Al_indices = np.array(
            [a.index for a in atoms if a.symbol == 'Al'])

        self.nl = NeighborList(self.cutoffs, skin=0,
                               self_interaction=False, bothways=True)

        self.initial_components = None
        self.traj = [a for a in traj]
        self.atoms = atoms
        self.molecule_information = {}
        self.open_reactions = {}
        self.closed_reactions = []
        self.reaction_indices = []
        self.distinct_indices = []
        self.distinct_strings = []
        self.distinct_counts = []
        self.broken_bonds = []

        self._initialize(atoms)
        self.parse_trajectory()

    def _initialize(self, atoms):
        cl = self.get_component_list(atoms)[0]
        self.initial_components = cl

        for Al_idx in self.Al_indices:
            fragment = self.get_fragment(Al_idx, cl)
            self.molecule_information[Al_idx] = [
                (0, self.get_formula(fragment))]

    def parse_trajectory(self):
        if os.path.isfile(self.save_file) and os.stat(self.save_file).st_size > 0:
            components, matrices = load_components_file(self.save_file)
            self.traj_components = components
            self.connectivity_matrices = matrices
        else:
            pool = multiprocessing.Pool(processes=24)
            pm = pool.map(self.get_component_list, self.traj)
            pool.close()
            pool.join()

            components, matrices = zip(*pm)

            self.traj_components = components
            self.connectivity_matrices = matrices
            save_components_file(self.save_file, components, matrices)

    def get_fragment(self, idx, component_list):
        return np.where(component_list == component_list[idx])[0]

    def get_formula(self, fragment):
        if self.atoms[fragment].get_chemical_formula() in dict_labels:
            return dict_labels[self.atoms[fragment].get_chemical_formula()]
        else:
            return self.atoms[fragment].get_chemical_formula()

    def get_component_list(self, atoms):
        self.nl.update(atoms)
        mat = self.nl.get_connectivity_matrix(sparse=False)

        for i in self.Cl_indices:
            for j in range(len(atoms)):
                if self.syms[j] != 'Al':
                    mat[i, j] = 0
                    mat[j, i] = 0

        return sparse.csgraph.connected_components(mat)[1], mat


    # for the visualization of the reaction:  
    def get_reaction(self, time, all_reaction_indices): #, bond):
        traj_file2 = f"{time}fs__bonds.traj"
        traj2 = Trajectory(traj_file2, 'w')

        initial = 0

        # Processing image = initial = 0:
        for i, image in enumerate(self.traj[:initial+1]):
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
        intial = time-70
        final = time+100
#       final = len(self.traj)
        for i, image in enumerate(self.traj[initial+1:final+1]):
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



    def follow(self):
        previous_components = self.initial_components
#       All_counts = []
#       All_distinct_R = []
#       All_distinct_s_R = []
#       All_distinct_P = []
#       All_distinct_s_P = []
        for count, component_list in enumerate(self.traj_components):
            diff = component_list - previous_components
            if any(diff):
                print('Reaction took place at', count)

                reactant_dict = {}
                for Al_idx in self.Al_indices:
                    fragment = self.get_fragment(
                        Al_idx, previous_components)
                    reactant_dict[Al_idx] = (
                        self.get_formula(fragment), fragment)

                product_dict = {}
                for Al_idx in self.Al_indices:
                    fragment = self.get_fragment(Al_idx, component_list)
                    product_dict[Al_idx] = (
                        self.get_formula(fragment), fragment)

                reacted_idx = []
                reactants = []
                products = []
                all_indices_of_reaction = set()
                all_indx_R = []
                all_indx_P = []
                for Al_idx in self.Al_indices:
                    reac = reactant_dict[Al_idx][0]
                    prod = product_dict[Al_idx][0]
                    if reac != prod:
                        print(Al_idx, f'changed from {reac} to {prod}')
                        self.molecule_information[Al_idx].append((count, prod))
                        reactants.append(reac)
                        products.append(prod)
                        reacted_idx.append(Al_idx)
                        # Add the indices from the fragment belonging
                        # to this Al index to all the indices of all
                        # the fragments in this reaction
                        all_indices_of_reaction |= set(
                            reactant_dict[Al_idx][1])

                        alla_R = reactant_dict[Al_idx]#[1]
                        all_indx_R.append(alla_R)

                        alla_P = product_dict[Al_idx]#[1]
                        all_indx_P.append(alla_P)
#                       print ('alla R = ', alla_R)
#                       print ('alla P = ', alla_P)
                        all_indices_of_reaction |= set(product_dict[Al_idx][1])
                all_reaction_idx = sorted(all_indices_of_reaction)
                print('All indices of this reaction: ',
                      all_reaction_idx)
#               print ('all_indices_of_reaction_R = ', all_indx_R)
#               print ('all_indices_of_reaction_P = ', all_indx_P)

                np.set_printoptions(threshold=sys.maxsize) # print all np arrays

################### specific indices for reactants : distinct_R
#                   specific reactants string: distinct_s_R. for strings you may have same formula for two different array indices, so:
                ns_R = [i[1] for i in all_indx_R]

                distinct_R_strs_indx = list()
                distinct_R = list()
                for indx_M, M in enumerate(ns_R):
                    if any(np.array_equal(M, N) for N in distinct_R):
                        continue
                    distinct_R.append(M)
                    distinct_R_strs_indx.append(indx_M)
                print ('distinct indices Reactants = ', distinct_R)

                distinct_s_R = [all_indx_R[j][0] for j in distinct_R_strs_indx]
                print ('distinct strings Reactants = ', distinct_s_R)


################### specific indices for products:
#                   specific products string: distinct_s_P:

                ns_P = [i[1] for i in all_indx_P]

                distinct_P_strs_indx = list()
                distinct_P = list()
                for indx_M, M in enumerate(ns_P):
                    if any(np.array_equal(M, N) for N in distinct_P):
                        continue
                    distinct_P.append(M)
                    distinct_P_strs_indx.append(indx_M)
                print ('distinct indices Products = ', distinct_P)

                distinct_s_P = [all_indx_P[j][0] for j in distinct_P_strs_indx]
                print ('distinct strings Products = ', distinct_s_P)

                cm = self.connectivity_matrices

#               np.set_printoptions(threshold=sys.maxsize)

                diff_cm = cm[count] - cm[count - 1]

                # Is diff_cm symmetric ?
                # diff_cm is symmetric if all elements of (diff_cm - diff_cm.T) are zero. (T=transpose)
                # If not, the matrix is not symmetric.
                if not np.all(diff_cm - diff_cm.T == 0):
                    print(f"diff_cm between {count}fs and {count -1}fs is not symmetric. Either cm[count] or cm[count- 1], of both, are non symmetric. Use bothways=True")
                    sys.exit()

#               broken_indices = np.ravel(np.where(diff_cm < 0))
                # which indices are broken in the lower trianguar of diff_cm ?
                broken_indices = np.argwhere(np.tril(diff_cm) < 0)
                print('The bond between the following indices broke: ',
                      broken_indices)

#               broken_indices_vis = [[all_reaction_idx.index(i) for i in elmt]\
#                                     for elmt in broken_indices] # sometimes breaks. commented
#               print('.... for visualization: ',
#                     broken_indices_vis)

#               formed_indices = np.ravel(np.where(diff_cm > 0))
                # which indices are broken in the lower trianguar of diff_cm ?
                formed_indices = np.argwhere(np.tril(diff_cm) > 0)
                print('The bond between the following indices formed: ',
                      formed_indices)

#               formed_indices_vis = [[all_reaction_idx.index(i) for i in elmt]\
#                                     for elmt in formed_indices] # sometimes breaks. commented.
#               print('.... for visualization: ',
#                     formed_indices_vis)

                # Save the time of reaction, all indices and broken
                # indices to easier process the specific reaction
                # later
                self.reaction_indices.append((count, all_reaction_idx,
                                              broken_indices, formed_indices))
                self.distinct_indices.append((distinct_R, distinct_P)) 
                self.distinct_strings.append((distinct_s_R, distinct_s_P)) 
                self.distinct_counts.append((count)) 
                # visualize the reaction (expensive part):
#               self.get_reaction(count, all_reaction_idx) #, broken_indices)

                reactant_str = ', '.join(sorted(list(set(reactants))))
                product_str = ', '.join(sorted(list(set(products))))
                reaction_str = f'{reactant_str} -> {product_str}'
                opposite_reaction = f'{product_str} -> {reactant_str}'
                # A reaction should be identified by both Aluminium
                # indices and reaction species.
                reacts = tuple(reacted_idx + [opposite_reaction])
#               print ('self.open_reactions.keys() = ', self.open_reactions.keys())
#               print ('self.open_reactions  = ', self.open_reactions)
#               print ('reacts = ', reacts)
#               print ('self.reaction_indices = ', self.reaction_indices)
                if reacts in self.open_reactions.keys():
                    # It is now a closed reaction!?!
                    lifetime = count - self.open_reactions[reacts][0]
                    tot_reaction_str = opposite_reaction + ' -> ' + \
                        reaction_str.split(' -> ')[-1]

                    lst = [i[0] for i in self.reaction_indices]
                    indx = lst.index(self.open_reactions[reacts][0])

################### BEGIN calculating distances for closed reactions, parallelized:
                    iterable = self.traj[self.open_reactions[reacts][0]-1 : count+1]
                    pool = multiprocessing.Pool()

                    broken_past = self.reaction_indices[indx][2]
                    if np.array_equal(broken_past, formed_indices):
                        if formed_indices.size != 0 :
                            max_fr_v = []
                            min_fr_v = []
                            func = partial(calculate_distances, formed_indices)
                            res = pool.map(func, iterable)

                            pool.close()
                            pool.join()
                            for i in range(np.shape(res)[1]):
                                aux_max = max([row[i] for row in res])
                                aux_min = min([row[i] for row in res])
                                max_fr_v.append(aux_max)
                                min_fr_v.append(aux_min)
                            max_br = max_fr_v
                            min_br = min_fr_v
                        else:
                            max_fr_v = []
                            min_fr_v = []
                            max_br = max_fr_v
                            min_br = min_fr_v


                    if not np.array_equal(broken_past, formed_indices):
                        print ("broken_past and formed_indices are different")
                        if formed_indices.size != 0:
                            max_fr_v = []
                            min_fr_v = []
                            all_res = []
                            for image in iterable:
                                res = [image.get_distance(row[0], row[1], mic=True) \
                                       for row in formed_indices]
                                all_res.append(res)

                            for i in range(np.shape(all_res)[1]):
                                aux_max = max([row[i] for row in all_res])
                                aux_min = min([row[i] for row in all_res])
                                max_fr_v.append(aux_max)
                                min_fr_v.append(aux_min)
                        if formed_indices.size == 0:
                            max_fr_v = []
                            min_fr_v = []

                        if broken_past.size != 0:
                            max_br = []
                            min_br = []
                            all_res = []
                            for image in iterable:
                                res = [image.get_distance(row[0], row[1], mic=True) \
                                       for row in broken_past]
                                all_res.append(res)

                            for i in range(np.shape(all_res)[1]):
                                aux_max = max([row[i] for row in all_res])
                                aux_min = min([row[i] for row in all_res])
                                max_br.append(aux_max)
                                min_br.append(aux_min)
                        if broken_past.size == 0:
                            max_br = []
                            min_br = []

                    formed_past = self.reaction_indices[indx][3]
                    if np.array_equal(formed_past, broken_indices):
                        if broken_indices.size != 0 :
                            max_br_v = []
                            min_br_v = []
                            func = partial(calculate_distances, broken_indices)
                            res = pool.map(func, iterable)

                            pool.close()
                            pool.join()
                            for i in range(np.shape(res)[1]):
                                aux_max = max([row[i] for row in res])
                                aux_min = min([row[i] for row in res])
                                max_br_v.append(aux_max)
                                min_br_v.append(aux_min)
                            max_fr = max_br_v
                            min_fr = min_br_v
                        else:
                            max_br_v = []
                            min_br_v = []
                            max_fr = max_br_v
                            min_fr = min_br_v

                    if not np.array_equal(formed_past, broken_indices):
                        print ("formed_past and broken_indices are different")
                        if broken_indices.size != 0:
                            max_br_v = []
                            min_br_v = []
                            all_res = []
                            for image in iterable:
                                res = [image.get_distance(row[0], row[1], mic=True) \
                                       for row in broken_indices]
                                all_res.append(res)

                            for i in range(np.shape(all_res)[1]):
                                aux_max = max([row[i] for row in all_res])
                                aux_min = min([row[i] for row in all_res])
                                max_br_v.append(aux_max)
                                min_br_v.append(aux_min)
                        if broken_indices.size == 0:
                            max_br_v = []
                            min_br_v = []

                        if formed_past.size != 0:
                            max_fr = []
                            min_fr = []
                            all_res = []
                            for image in iterable:
                                res = [image.get_distance(row[0], row[1], mic=True) \
                                       for row in formed_past]
                                all_res.append(res)

                            for i in range(np.shape(all_res)[1]):
                                aux_max = max([row[i] for row in all_res])
                                aux_min = min([row[i] for row in all_res])
                                max_fr.append(aux_max)
                                min_fr.append(aux_min)
                        if formed_past.size == 0:
                            max_fr = []
                            min_fr = []

                    pool.close()
                    pool.join()
################### END calculating distances for closed reactions, parallelized.
                    self.closed_reactions.append(
                        (reacts[:-1], f'{tot_reaction_str}',\
                        f':: lifetime: {lifetime}',\
                        f'(from {self.open_reactions[reacts][0]} to {count})',\

                        f' At {self.open_reactions[reacts][0]} we have:',\
#                       f' ; distinct indices R = {self.distinct_indices[indx][0]}',\ # If we want parsing_closed.py module to work, these
#                       f' ; distinct indices P = {self.distinct_indices[indx][1]}',\ # two lines have to be commented (we dont need this info in the Closed_reactions huge array

                        f' ; broken indices = {self.reaction_indices[indx][2]}',\
                        f' ; formed indices = {self.reaction_indices[indx][3]}',\

                        f'Max distance between {self.reaction_indices[indx][2]}: {max_br}',\
                        f'Min distance between {self.reaction_indices[indx][2]}: {min_br}',\

                        f'Max distance between {self.reaction_indices[indx][3]}: {max_fr}',\
                        f'Min distance between {self.reaction_indices[indx][3]}: {min_fr}',\

                        f' At {count} we have:',\
#                       f' ; distinct indices R = {distinct_R}',\ # If we want parsing_closed.py module to work, these
#                       f' ; distinct indices P = {distinct_P}',\ # two lines have to be commented (we dont need this info in the Closed_reactions huge array

                        f' ; broken indices = {broken_indices}',\
                        f' ; formed indices = {formed_indices}',\

                        f'Max distance between {broken_indices}: {max_br_v}',\
                        f'Min distance between {broken_indices}: {min_br_v}',\

                        f'Max distance between {formed_indices}: {max_fr_v}',\
                        f'Min distance between {formed_indices}: {min_fr_v}',\

                         ))

                    self.open_reactions.pop(reacts)
#                   print ('self.open_reactions  = ', self.open_reactions)

                else:

################### BEGIN calculating distances for open reactions, parallelized:
                    iterable = self.traj[count-1:]
                    pool = multiprocessing.Pool()

                    max_br = []
                    min_br = []
                    if broken_indices.size != 0:
                        func = partial(calculate_distances, broken_indices)
                        res = pool.map(func, iterable)

                        for i in range(np.shape(res)[1]):
                            aux_max = max([row[i] for row in res])
                            aux_min = min([row[i] for row in res])
                            max_br.append(aux_max)
                            min_br.append(aux_min)


                    max_fr = []
                    min_fr = []
                    if formed_indices.size != 0:
                        func = partial(calculate_distances, formed_indices)
                        res = pool.map(func, iterable)

                        for i in range(np.shape(res)[1]):
                            aux_max = max([row[i] for row in res])
                            aux_min = min([row[i] for row in res])
                            max_fr.append(aux_max)
                            min_fr.append(aux_min)
################### END calculating distances for open reactions, parallelized:


                    # key is Al_idx and forward reaction
                    # when checking for a closed reaction we need to
                    # use the backward/opposite reaction
                    self.open_reactions[tuple (
                        reacted_idx + [reaction_str])] = (count,\
                        f'broken indices = {broken_indices}',\

#                       f' ; distinct indices R = {distinct_R}',\ # If we want parsing_open.py module to work, these
#                       f' ; distinct indices P = {distinct_P}',\ # two lines have to be commented (we dont need this info in the Open_reactions huge array

                        f'Max distance between {broken_indices}: {max_br}',\
                        f'Min distance between {broken_indices}: {min_br}',\

                        f'formed indices = {formed_indices}',\

                        f'Max distance between {formed_indices}: {max_fr}',\
                        f'Min distance between {formed_indices}: {min_fr}')

                    pool.close()  # uncomment these two if distance is calculated.
                    pool.join()

            previous_components = component_list


def save_components_file(fname, components, matrices):
    np.savez_compressed(fname, components=components, matrices=matrices)


def load_components_file(fname):
    data = np.load(fname)
    return data['components'], data['matrices']

def calculate_distances(selected_indices, image):
    dis = [image.get_distance(row[0], row[1], mic=True) \
           for row in selected_indices]
    return dis


#from parsing_ida_br_fr_mejorado_v3_example_based_fx import table_closed_reactions
def main():

    if os.path.exists("./diff_cm.txt"):
        os.remove("./diff_cm.txt")

    cutoff_dict = {'Al': 1, 'Cl': 1.7, 'H': .37, 'O': 1, 'N': 1, 'C': 1}
    traj = Trajectory(traj_file)
    detect = Detect(traj, cutoff_dict)
    detect.follow()
    print('-' * 80)
    print('-' * 80)


    print('Closed reactions:')
    Closed_reactions = detect.closed_reactions
    print ('Closed_reactions = ', Closed_reactions)
    for indx, i in enumerate(Closed_reactions):
        print(i)

    if Closed_reactions:

        # saving this to pickle:
        strings = [i[1] for i in Closed_reactions]
        fname = "Closed_reactions_dict.pickle"
        from reactions_2_pickle import r2p
        r2p(strings, fname)

        # table closed reactions:
        from parsing_closed import table_closed_reactions
        table_closed_reactions(Closed_reactions)

        # clean the table of closed reactions:
        from parsing_closed_clean import table_closed_reactions_nones,\
                                         table_closed_reactions_more_than_1_1
        table_closed_reactions_nones(Closed_reactions)
        table_closed_reactions_more_than_1_1(Closed_reactions)



    print('-' * 80)
    print('Open reactions:')
    Open_reactions = list(detect.open_reactions.items())
    print ('Open_reactions = ', Open_reactions)
    for i in Open_reactions:
        print(i)

    if Open_reactions:
        # saving this to pickle:
        strings = [i[0][-1] for i in Open_reactions]
        fname = "Open_reactions_dict.pickle"
        from reactions_2_pickle import r2p
        r2p(strings, fname)

        # table open reactions:
        from parsing_open import table_open_reactions
        table_open_reactions(Open_reactions)

        # table open reactions one line per reaction:
        from parsing_open_one_line_per_reaction import table_open_reactions_one_line
        table_open_reactions_one_line(Open_reactions)

        # finding connections between reactions:
        print (detect.distinct_indices)
        print (detect.distinct_strings)
        print (detect.distinct_counts)

        # save these to pickle in case we need them and there is no need to run detect again:
        from data2p import data2p
        fname = ['detect_distinct_indices.pickle', 'detect_distinct_strings.pickle', 'detect_distinct_counts.pickle']
        data2p(detect.distinct_indices, fname[0])
        data2p(detect.distinct_strings, fname[1])
        data2p(detect.distinct_counts, fname[2])

    #   connected open reactions:
        distinct_counts_open = [i[1][0] for i in Open_reactions]
        # obtaining indices:
        all_indx_open = []
        for indx, i in enumerate(detect.distinct_counts):
            for j in distinct_counts_open:
                if i == j:
                    print (indx, i, j)
                    all_indx_open.append(indx)
        distinct_strings_open = [detect.distinct_strings[i] for i in all_indx_open]
        distinct_indices_open = [detect.distinct_indices[i] for i in all_indx_open]
        distinct_counts_open_b = [detect.distinct_counts[i] for i in all_indx_open]

        # save these to pickle in case connect task has to be modified:
        from data2p import data2p
        fname = ['distinct_counts_open.pickle', 'distinct_strings_open.pickle', 'distinct_indices_open.pickle']
        data2p(distinct_counts_open_b, fname[0])
        data2p(distinct_strings_open, fname[1])
        data2p(distinct_indices_open, fname[2])


        from connected_reactions import connect
        filename = "Connected_Open"
        connect(distinct_indices_open, distinct_counts_open_b, distinct_strings_open, filename)


if __name__ == "__main__":
    main()
