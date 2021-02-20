#
import numpy as np

def connect (distinct_indices, distinct_counts, distinct_strings, filename):

    molecule_dictionary = {}

    rows = np.shape(distinct_indices)[0]  # this is the time
    columns = np.shape(distinct_indices)[1] # this is the reactants (columns=0)  or products (columns=1) 

    for i in range(rows):
        for j in range(columns):
            number_of_molecules = np.shape(distinct_indices[i][j])[0]
            for k in range(number_of_molecules):

                list_search = str(distinct_indices[i][j][k])

                # We encountered this molecule before
                if list_search in molecule_dictionary.keys():
                    molecule_dictionary[list_search].append( (i, j, k) )

                # It's the first time we encounter this molecule
                else:
                    molecule_dictionary[list_search] = [ ]
                    molecule_dictionary[list_search].append( (i, j, k) )

    molecule_dictionary_connected = {}

    for key in molecule_dictionary.keys():

        # Populate new dictionary
        if len(molecule_dictionary[key]) > 1:
            molecule_dictionary_connected[key] = molecule_dictionary[key]

    print ('molecule_dictionary = ', molecule_dictionary)
    print ('molecule_dictionary_connected = ', molecule_dictionary_connected)


    f = open(f"{filename}.tex", 'w')

    print ("""
    \\documentclass{article}
    \\usepackage[margin=0.3in]{geometry}
    \\begin{document}
    """, file=f)

    dict_R_or_P = {0: 'Reactant', 1: 'Product'}
    for key in molecule_dictionary_connected:

        time = [item[0] for item in molecule_dictionary_connected[key]]
        R_or_P = [item[1] for item in molecule_dictionary_connected[key]]
        N_Mol = [item[2] for item in molecule_dictionary_connected[key]]
        print (f"{key} is {distinct_strings[time[0]][R_or_P[0]][N_Mol[0]]}:\\\ " , file=f)

        for t, r_or_p, n_mol in zip(time, R_or_P, N_Mol):

            print (f"Appears in time = {distinct_counts[t]} fs as a {dict_R_or_P[r_or_p]}: {distinct_strings[t][r_or_p][n_mol]}\\\ ", file=f)
        print (f"""

        """, file=f)

    print ("""
    \\end{document}

    """, file=f)
    f.close()


