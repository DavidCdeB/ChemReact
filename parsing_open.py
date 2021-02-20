#

from  collections import Counter
import re

def table_open_reactions(Open_reactions):

    strings = [i[0][-1] for i in Open_reactions]
    dict_counter_strings = dict(Counter(strings))

    f = open('Reactions_Open_Table.tex', 'w')

    print ("""

\\documentclass{article}
\\usepackage[margin=0.3in]{geometry}
\\usepackage{multirow}
\\usepackage{adjustbox}
\\begin{document}

\\begin{table}[]
\\begin{adjustbox}{width=\\hsize, totalheight=\\textheight, keepaspectratio}
\\begin{tabular}{|l|l|l|l|l|l|}
\\hline
Reaction & N & Time  &  Indices & Max. dist. & Min. dist \\\ \\hline

    """, file=f)

    reaction_str_ini = list(dict_counter_strings.keys())[0]
    myreaction = reaction_str_ini.replace("->", '$\\rightarrow$')

    N = dict_counter_strings[reaction_str_ini]
    dN = N*2

    for m in dict_counter_strings.keys():

        reaction_str = m
        print ('reaction_str = ' , reaction_str)
        if reaction_str == reaction_str_ini:
            print ('aa')

            N = dict_counter_strings[reaction_str]
            dN = N*2

            if N == 1:
                print (f"{myreaction} & {N} &", file=f)
            else:
                print (f"\multirow{{{N}}}{{*}} {{{myreaction}}} & ", file=f)
                print (f"\multirow{{{N}}}{{*}} {{{N}}} & ", file=f)

            all_interval = []

            all_word = []

            all_value_maxs_rounded = []
            all_value_mins_rounded = []

            target_indices = [idx for idx, j in enumerate(strings) if j == reaction_str]
            print ('target_indices = ', target_indices)
            for j in target_indices:
                i = Open_reactions[j]

                print ('i = ', i)
                interval = i[1][0]
                print ('interval = ', interval)
                all_interval.append(interval)

                br = i[1][1]
                fr = i[1][4]

                if "[]" in br:
                    word = fr
                elif "[]" in fr:
                    word = br
                else:
                    word = br + "; " + fr
                all_word.append(word)


                maxs_br_str = i[1][2]
                maxs_fr_str = i[1][5]

                if "[]" in maxs_br_str:
                    t = maxs_fr_str
                    maxs_star = t.split(' [')[-1].strip(']')
                    maxs_list = maxs_star.split(',')
                elif "[]" in maxs_fr_str:
                    t = maxs_br_str
                    maxs_star = t.split(' [')[-1].strip(']')
                    maxs_list = maxs_star.split(',')
                else:
                    t = maxs_br_str + "; " + maxs_fr_str
                    maxs_list = []
                    auxmax = t.split('];')
                    for k in auxmax:
                        kmax = k.split(']: ')[-1].strip('[').strip(']')
                        maxs_list.append(kmax)

                value_maxs = [float(i) for i in maxs_list]
                value_maxs_rounded = [round(i, 4) for i in value_maxs]
                all_value_maxs_rounded.append(value_maxs_rounded)

                mins_br_str = i[1][3]
                mins_fr_str = i[1][6]

                if "[]" in mins_br_str:
                    t = mins_fr_str
                    mins_star = t.split(' [')[-1].strip(']')
                    mins_list = mins_star.split(',')
                elif "[]" in mins_fr_str:
                    t = mins_br_str
                    mins_star = t.split(' [')[-1].strip(']')
                    mins_list = mins_star.split(',')
                else:
                    t = mins_br_str + "; " + mins_fr_str
                    mins_list = []
                    auxmin = t.split('];')
                    for k in auxmin:
                        kmin = k.split(']: ')[-1].strip('[').strip(']')
                        mins_list.append(kmin)

                value_mins = [float(i) for i in mins_list]
                value_mins_rounded = [round(i, 4) for i in value_mins]
                all_value_mins_rounded.append(value_mins_rounded)

            if N == 1:
                print (f"{all_interval[0]} & {all_word[0]} & {all_value_maxs_rounded[0]} & {all_value_mins_rounded[0]}", file=f)
    #           print (f"\\\ \hline ", file=f)

            else:
                print (f"{all_interval[0]} & {all_word[0]} & {all_value_maxs_rounded[0]} & {all_value_mins_rounded[0]}", file=f)

                for k in range(1, len(all_interval)):
                    print (f"\\\ \cline{{3-6}}", file=f)
                    print (f"&  &  {all_interval[k]} & {all_word[k]} & {all_value_maxs_rounded[k]} & {all_value_mins_rounded[k]}", file=f)

            print (f"\\\ \hline ", file=f)

        else:
            myreaction = reaction_str.replace("->", '$\\rightarrow$')

            N = dict_counter_strings[reaction_str]
            dN = N*2

            if N == 1:
                print (f"{myreaction} & {N} &", file=f)
            else:
                print (f"\multirow{{{N}}}{{*}} {{{myreaction}}} & ", file=f)
                print (f"\multirow{{{N}}}{{*}} {{{N}}} & ", file=f)

            all_interval = []

            all_word = []

            all_value_maxs_rounded = []
            all_value_mins_rounded = []

            target_indices = [idx for idx, j in enumerate(strings) if j == reaction_str]
            for j in target_indices:
                i = Open_reactions[j]

                interval = i[1][0]
                all_interval.append(interval)

                br = i[1][1]
                fr = i[1][4]

                if "[]" in br:
                    word = fr
                elif "[]" in fr:
                    word = br
                else:
                    word = br + "; " + fr
                all_word.append(word)


                maxs_br_str = i[1][2]
                maxs_fr_str = i[1][5]

                if "[]" in maxs_br_str:
                    t = maxs_fr_str
                    maxs_star = t.split(' [')[-1].strip(']')
                    maxs_list = maxs_star.split(',')
                elif "[]" in maxs_fr_str:
                    t = maxs_br_str
                    maxs_star = t.split(' [')[-1].strip(']')
                    maxs_list = maxs_star.split(',')
                else:
                    t = maxs_br_str + "; " + maxs_fr_str
                    maxs_list = []
                    auxmax = t.split('];')
                    for k in auxmax:
                        kmax = k.split(']: ')[-1].strip('[').strip(']')
                        maxs_list.append(kmax)

                value_maxs = [float(i) for i in maxs_list]
                value_maxs_rounded = [round(i, 4) for i in value_maxs]
                all_value_maxs_rounded.append(value_maxs_rounded)


                mins_br_str = i[1][3]
                mins_fr_str = i[1][6]

                if "[]" in mins_br_str:
                    t = mins_fr_str
                    mins_star = t.split(' [')[-1].strip(']')
                    mins_list = mins_star.split(',')
                elif "[]" in mins_fr_str:
                    t = mins_br_str
                    mins_star = t.split(' [')[-1].strip(']')
                    mins_list = mins_star.split(',')
                else:
                    t = mins_br_str + "; " + mins_fr_str
                    mins_list = []
                    auxmin = t.split('];')
                    for k in auxmin:
                        kmin = k.split(']: ')[-1].strip('[').strip(']')
                        mins_list.append(kmin)

                value_mins = [float(i) for i in mins_list]
                value_mins_rounded = [round(i, 4) for i in value_mins]
                all_value_mins_rounded.append(value_mins_rounded)

            if N == 1:
                print (f"{all_interval[0]} & {all_word[0]} & {all_value_maxs_rounded[0]} & {all_value_mins_rounded[0]}", file=f)

            else:
                print (f"{all_interval[0]} & {all_word[0]} & {all_value_maxs_rounded[0]} & {all_value_mins_rounded[0]}", file=f)

                for k in range(1, len(all_interval)):
                    print (f"\\\ \cline{{3-6}}", file=f)
                    print (f"&  &  {all_interval[k]} & {all_word[k]} & {all_value_maxs_rounded[k]} & {all_value_mins_rounded[k]}", file=f)

            print (f"\\\ \hline ", file=f)

        reaction_str_ini = reaction_str

    print ("""

\\end{tabular}
\\end{adjustbox}
\\end{table}
\\end{document}

    """, file=f)


    f.close()
