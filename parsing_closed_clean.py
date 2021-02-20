
#


from  collections import Counter
import re

def table_closed_reactions_nones(Closed_reactions):

    strings = [i[1] for i in Closed_reactions]
    dict_counter_strings = dict(Counter(strings))

    f = open('Reactions_Closed_Table_nones.tex', 'w')
    print ("""

\\documentclass{article}
\\usepackage[margin=0.3in]{geometry}
\\usepackage{multirow}
\\usepackage{adjustbox}
\\begin{document}

\\begin{table}[]
\\begin{adjustbox}{width=\\hsize, totalheight=\\textheight, keepaspectratio}
\\begin{tabular}{|l|l|l|l|l|l|l|l|}
\\hline
Reaction & N & Interval  & lifetime  & Indices & Max. dist. & Min. dist & Max. dist/Min. dist\\\ \\hline

    """, file=f)
    reaction_str_ini = list(dict_counter_strings.keys())[0]
    targ = re.compile(".*>")
    targ2 = targ.findall(reaction_str_ini)
    myreaction = targ2[0][:-2].replace("->", '$\\rightleftharpoons$')

    N = dict_counter_strings[reaction_str_ini]
    dN = N*2

    print (f"\multirow{{{dN}}}{{*}} {{{myreaction}}} & ", file=f)
    print (f"\multirow{{{dN}}}{{*}} {{{N}}} & ", file=f)

    # In many closed reactions, max.dist and min.dist. between broken/formed bonds
    # are very similar. Thus, we will only consider closed reactions in which the
    # max.dist is at least min.dist + 10% of the min.dist:
    # if max.dist >= 1.1*min.dist    (= min.dist + 0.1*min.dist)
    #    e.g. a case where min.dist = 2.3172, and max.dist = 2.7026
    #    if max.dist >= 1.1*2.3172 >= 2.54892, then this reaction is considered.
    #    e.g. a case where min.dist = 1.9636, and max.dist = 2.0005
    #    if max.dist >= 1.1*1.9636 >= 2.15996, then this reaction is not considered.
    # we set 'thres = max.dist/min.dist = 1.1'
    # If 'max.dist/min.dist >= thres', we save the reaction:
    thres = 1.1
    for m in dict_counter_strings.keys():

        reaction_str = m
        if reaction_str == reaction_str_ini:

            N = dict_counter_strings[reaction_str]
            dN = N*2

            all_interval = []
            all_lif = []

            all_word_ida = []
            all_word_vuelta = []

            all_value_maxs_rounded_ida = []
            all_value_mins_rounded_ida = []

            all_value_maxs_rounded_vuelta = []
            all_value_mins_rounded_vuelta = []

            target_indices = [idx for idx, j in enumerate(strings) if j == reaction_str]
            for j in target_indices:
                i = Closed_reactions[j]

                interval = i[3].strip('(').strip(')')
                all_interval.append(interval)

                lif = i[2].split()[2]
                all_lif.append(lif)

#################         ida:
                indices_ida = [i[j] for j in range(4, 7) if "[]" not in i[j]]
                word_ida = indices_ida[0].replace('we have','') + indices_ida[1].replace(';','')
                all_word_ida.append(word_ida)

                criticals_ida = [i[j] for j in range(7, 11) if "[]:" not in i[j]]

                maxs_star_ida = criticals_ida[0].split(' [')[-1].strip(']')
                maxs_i_list = maxs_star_ida.split(',')
                value_maxs_ida = [float(i) for i in maxs_i_list]
                value_maxs_rounded_ida = [round(i, 4) for i in value_maxs_ida]
                all_value_maxs_rounded_ida.append(value_maxs_rounded_ida)

                mins_star_ida = criticals_ida[1].split(' [')[-1].strip(']')
                mins_i_list = mins_star_ida.split(',')
                value_mins_ida = [float(i) for i in mins_i_list]
                value_mins_rounded_ida = [round(i, 4) for i in value_mins_ida]
                all_value_mins_rounded_ida.append(value_mins_rounded_ida)

#################         vuelta:
                indices_vuelta = [i[j] for j in range(11, 14) if "[]" not in i[j]]
                word_vuelta = indices_vuelta[0].replace('we have','') + indices_vuelta[1].replace(';','')
                all_word_vuelta.append(word_vuelta)

                criticals_vuelta = [i[j] for j in range(14, 18) if "[]:" not in i[j]]

                maxs_star_vuelta = criticals_vuelta[0].split(' [')[-1].strip(']')
                maxs_v_list = maxs_star_vuelta.split(',')
                value_maxs_vuelta = [float(i) for i in maxs_v_list]
                value_maxs_rounded_vuelta = [round(i, 4) for i in value_maxs_vuelta]
                all_value_maxs_rounded_vuelta.append(value_maxs_rounded_vuelta)

                mins_star_vuelta = criticals_vuelta[1].split(' [')[-1].strip(']')
                mins_v_list = mins_star_vuelta.split(',')
                value_mins_vuelta = [float(i) for i in mins_v_list]
                value_mins_rounded_vuelta = [round(i, 4) for i in value_mins_vuelta]
                all_value_mins_rounded_vuelta.append(value_mins_rounded_vuelta)

            for k in range(0, len(all_interval)-1):
                if (all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0] >= thres and
                        all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0] >= thres):
                    print (f"\multirow{{2}}{{*}} {{{all_interval[k]}}} & ", file=f)
                    print (f"\multirow{{2}}{{*}} {{{all_lif[k]}}}      & ", file=f)
                    div = all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0]
                    print (f"{{{all_word_ida[k]}}}  &  {{{all_value_maxs_rounded_ida[k]}}} & {{{all_value_mins_rounded_ida[k]}}} & {{{div}}}", file=f)
                    print (f"\\\ \cline{{5-8}}  &  &  &  &  ", file=f)

                    div = all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0]
                    print (f"{{{all_word_vuelta[k]}}}  &  {{{all_value_maxs_rounded_vuelta[k]}}} & {{{all_value_mins_rounded_vuelta[k]}}} & {{{div}}}", file=f)
                    print (f"\\\ \cline{{3-8}}  &  & ", file=f)

                else:
                    print (f"\multirow{{2}}{{*}} {{none}} & ", file=f)
                    print (f"\multirow{{2}}{{*}} {{none}}      & ", file=f)
                    div = all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0]
                    print (f"none  &  none & none & {{{div}}}", file=f)
                    print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                    div = all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0]
                    print (f"none  &  none & none & {{{div}}}", file=f)
                    print (f"\\\ \cline{{3-8}}  &  & ", file=f)


            
            print ('aaaa', all_value_maxs_rounded_ida[-1])
            if (all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0] >= thres and
                    all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0] >= thres):
                print (f"\multirow{{2}}{{*}} {{{all_interval[-1]}}} & ", file=f)
                print (f"\multirow{{2}}{{*}} {{{all_lif[-1]}}}      & ", file=f)
                div = all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0]
                print (f"{{{all_word_ida[-1]}}}  &  {{{all_value_maxs_rounded_ida[-1]}}} & {{{all_value_mins_rounded_ida[-1]}}} & {{{div}}}", file=f)
                print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                div = all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0]
                print (f"{{{all_word_vuelta[-1]}}}  &  {{{all_value_maxs_rounded_vuelta[-1]}}} & {{{all_value_mins_rounded_vuelta[-1]}}} & {{{div}}}", file=f)
                print (f"\\\ \hline ", file=f)

            else:
                print (f"\multirow{{2}}{{*}} {{none}}  & ", file=f)
                print (f"\multirow{{2}}{{*}} {{none}}     & ", file=f)
                div = all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0]
                print (f" none  &  none  & none & {{{div}}}", file=f)
                print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                div = all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0]
                print (f"none  &  none  & none & {{{div}}}", file=f)
                print (f"\\\ \hline ", file=f)

        else:

            targ = re.compile(".*>")
            targ2 = targ.findall(reaction_str)
            myreaction = targ2[0][:-2].replace("->", '$\\rightleftharpoons$')

            N = dict_counter_strings[reaction_str]
            dN = N*2

            print (f"\multirow{{{dN}}}{{*}} {{{myreaction}}} & ", file=f)
            print (f"\multirow{{{dN}}}{{*}} {{{N}}} & ", file=f)

            all_interval = []
            all_lif = []

            all_word_ida = []
            all_word_vuelta = []

            all_value_maxs_rounded_ida = []
            all_value_mins_rounded_ida = []

            all_value_maxs_rounded_vuelta = []
            all_value_mins_rounded_vuelta = []

            target_indices = [idx for idx, j in enumerate(strings) if j == reaction_str]
            for j in target_indices:
                i = Closed_reactions[j]

                interval = i[3].strip('(').strip(')')
                all_interval.append(interval)

                lif = i[2].split()[2]
                all_lif.append(lif)

#################         ida:
                indices_ida = [i[j] for j in range(4, 7) if "[]" not in i[j]]
                word_ida = indices_ida[0].replace('we have','') + indices_ida[1].replace(';','')
                all_word_ida.append(word_ida)

                criticals_ida = [i[j] for j in range(7, 11) if "[]:" not in i[j]]

                maxs_star_ida = criticals_ida[0].split(' [')[-1].strip(']')
                maxs_i_list = maxs_star_ida.split(',')
                value_maxs_ida = [float(i) for i in maxs_i_list]
                value_maxs_rounded_ida = [round(i, 4) for i in value_maxs_ida]
                all_value_maxs_rounded_ida.append(value_maxs_rounded_ida)

                mins_star_ida = criticals_ida[1].split(' [')[-1].strip(']')
                mins_i_list = mins_star_ida.split(',')
                value_mins_ida = [float(i) for i in mins_i_list]
                value_mins_rounded_ida = [round(i, 4) for i in value_mins_ida]
                all_value_mins_rounded_ida.append(value_mins_rounded_ida)

#################         vuelta:
                indices_vuelta = [i[j] for j in range(11, 14) if "[]" not in i[j]]
                word_vuelta = indices_vuelta[0].replace('we have','') + indices_vuelta[1].replace(';','')
                all_word_vuelta.append(word_vuelta)

                criticals_vuelta = [i[j] for j in range(14, 18) if "[]:" not in i[j]]

                maxs_star_vuelta = criticals_vuelta[0].split(' [')[-1].strip(']')
                maxs_v_list = maxs_star_vuelta.split(',')
                value_maxs_vuelta = [float(i) for i in maxs_v_list]
                value_maxs_rounded_vuelta = [round(i, 4) for i in value_maxs_vuelta]
                all_value_maxs_rounded_vuelta.append(value_maxs_rounded_vuelta)

                mins_star_vuelta = criticals_vuelta[1].split(' [')[-1].strip(']')
                mins_v_list = mins_star_vuelta.split(',')
                value_mins_vuelta = [float(i) for i in mins_v_list]
                value_mins_rounded_vuelta = [round(i, 4) for i in value_mins_vuelta]
                all_value_mins_rounded_vuelta.append(value_mins_rounded_vuelta)

            for k in range(0, len(all_interval)-1):
                if (all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0] >= thres and
                    all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0] >= thres):
                    print (f"\multirow{{2}}{{*}} {{{all_interval[k]}}} & ", file=f)
                    print (f"\multirow{{2}}{{*}} {{{all_lif[k]}}}      & ", file=f)
                    div = all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0]
                    print (f"{{{all_word_ida[k]}}}  &  {{{all_value_maxs_rounded_ida[k]}}} & {{{all_value_mins_rounded_ida[k]}}} & {{{div}}}", file=f)
                    print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                    div = all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0]
                    print (f"{{{all_word_vuelta[k]}}}  &  {{{all_value_maxs_rounded_vuelta[k]}}} & {{{all_value_mins_rounded_vuelta[k]}}} & {{{div}}}", file=f)
                    print (f"\\\ \cline{{3-8}}  &  & ", file=f)

                else:
                    print (f"\multirow{{2}}{{*}} {{none}}  & ", file=f)
                    print (f"\multirow{{2}}{{*}} {{none}}       & ", file=f)
                    div = all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0]
                    print (f"none  &  none & none & {{{div}}}", file=f)
                    print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                    div = all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0]
                    print (f"none   &  none  & none & {{{div}}}", file=f)
                    print (f"\\\ \cline{{3-8}}  &  & ", file=f)


            if (all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0] >= thres and
                all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0] >= thres):
                print (f"\multirow{{2}}{{*}} {{{all_interval[-1]}}} & ", file=f)
                print (f"\multirow{{2}}{{*}} {{{all_lif[-1]}}}      & ", file=f)
                div = all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0]
                print (f"{{{all_word_ida[-1]}}}  &  {{{all_value_maxs_rounded_ida[-1]}}} & {{{all_value_mins_rounded_ida[-1]}}} & {{{div}}}", file=f)
                print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                div = all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0]
                print (f"{{{all_word_vuelta[-1]}}}  &  {{{all_value_maxs_rounded_vuelta[-1]}}} & {{{all_value_mins_rounded_vuelta[-1]}}} & {{{div}}}", file=f)
                print (f"\\\ \hline ", file=f)
            else:
                print (f"\multirow{{2}}{{*}} {{none}} & ", file=f)
                print (f"\multirow{{2}}{{*}} {{none}}       & ", file=f)
                div = all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0]
                print (f"{{none}}   &  none & none & {{{div}}}", file=f)
                print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                div = all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0]
                print (f"none  &  none & none & {{{div}}}", file=f)
                print (f"\\\ \hline ", file=f)

        reaction_str_ini = reaction_str

    print ("""

\\end{tabular}
\\end{adjustbox}
\\caption{\small none: events for which Max.dist/Min.dist $<$ 1.1}
\\end{table}
\\end{document}

    """, file=f)


    f.close()


def table_closed_reactions_more_than_1_1(Closed_reactions):

    strings = [i[1] for i in Closed_reactions]
    dict_counter_strings = dict(Counter(strings))

    f = open('Reactions_Closed_Table_more_than_1_1.tex', 'w')
    print ("""

\\documentclass{article}
\\usepackage[margin=0.3in]{geometry}
\\usepackage{multirow}
\\usepackage{adjustbox}
\\begin{document}

\\begin{table}[]
\\begin{adjustbox}{width=\\hsize, totalheight=\\textheight, keepaspectratio}
\\begin{tabular}{|l|l|l|l|l|l|l|l|}
\\hline
Reaction & N & Interval  & lifetime  & Indices & Max. dist. & Min. dist & Max. dist/Min. dist\\\ \\hline

    """, file=f)
    reaction_str_ini = list(dict_counter_strings.keys())[0]
    targ = re.compile(".*>")
    targ2 = targ.findall(reaction_str_ini)
    myreaction = targ2[0][:-2].replace("->", '$\\rightleftharpoons$')

    N = dict_counter_strings[reaction_str_ini]
    dN = N*2

    print (f"\multirow{{{dN}}}{{*}} {{{myreaction}}} & ", file=f)
    print (f"\multirow{{{dN}}}{{*}} {{{N}}} & ", file=f)

    thres = 1.1
    for m in dict_counter_strings.keys():

        reaction_str = m
        if reaction_str == reaction_str_ini:

            N = dict_counter_strings[reaction_str]
            dN = N*2

            all_interval = []
            all_lif = []

            all_word_ida = []
            all_word_vuelta = []

            all_value_maxs_rounded_ida = []
            all_value_mins_rounded_ida = []

            all_value_maxs_rounded_vuelta = []
            all_value_mins_rounded_vuelta = []

            target_indices = [idx for idx, j in enumerate(strings) if j == reaction_str]
            for j in target_indices:
                i = Closed_reactions[j]

                interval = i[3].strip('(').strip(')')
                all_interval.append(interval)

                lif = i[2].split()[2]
                all_lif.append(lif)

#################         ida:
                indices_ida = [i[j] for j in range(4, 7) if "[]" not in i[j]]
                word_ida = indices_ida[0].replace('we have','') + indices_ida[1].replace(';','')
                all_word_ida.append(word_ida)

                criticals_ida = [i[j] for j in range(7, 11) if "[]:" not in i[j]]

                maxs_star_ida = criticals_ida[0].split(' [')[-1].strip(']')
                maxs_i_list = maxs_star_ida.split(',')
                value_maxs_ida = [float(i) for i in maxs_i_list]
                value_maxs_rounded_ida = [round(i, 4) for i in value_maxs_ida]
                all_value_maxs_rounded_ida.append(value_maxs_rounded_ida)

                mins_star_ida = criticals_ida[1].split(' [')[-1].strip(']')
                mins_i_list = mins_star_ida.split(',')
                value_mins_ida = [float(i) for i in mins_i_list]
                value_mins_rounded_ida = [round(i, 4) for i in value_mins_ida]
                all_value_mins_rounded_ida.append(value_mins_rounded_ida)

#################         vuelta:
                indices_vuelta = [i[j] for j in range(11, 14) if "[]" not in i[j]]
                word_vuelta = indices_vuelta[0].replace('we have','') + indices_vuelta[1].replace(';','')
                all_word_vuelta.append(word_vuelta)

                criticals_vuelta = [i[j] for j in range(14, 18) if "[]:" not in i[j]]

                maxs_star_vuelta = criticals_vuelta[0].split(' [')[-1].strip(']')
                maxs_v_list = maxs_star_vuelta.split(',')
                value_maxs_vuelta = [float(i) for i in maxs_v_list]
                value_maxs_rounded_vuelta = [round(i, 4) for i in value_maxs_vuelta]
                all_value_maxs_rounded_vuelta.append(value_maxs_rounded_vuelta)

                mins_star_vuelta = criticals_vuelta[1].split(' [')[-1].strip(']')
                mins_v_list = mins_star_vuelta.split(',')
                value_mins_vuelta = [float(i) for i in mins_v_list]
                value_mins_rounded_vuelta = [round(i, 4) for i in value_mins_vuelta]
                all_value_mins_rounded_vuelta.append(value_mins_rounded_vuelta)

            for k in range(0, len(all_interval)-1):
                if (all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0] >= thres and
                        all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0] >= thres):
                    print (f"\multirow{{2}}{{*}} {{{all_interval[k]}}} & ", file=f)
                    print (f"\multirow{{2}}{{*}} {{{all_lif[k]}}}      & ", file=f)
                    div = all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0]
                    print (f"{{{all_word_ida[k]}}}  &  {{{all_value_maxs_rounded_ida[k]}}} & {{{all_value_mins_rounded_ida[k]}}} & {{{div}}}", file=f)
                    print (f"\\\ \cline{{5-8}}  &  &  &  &  ", file=f)

                    div = all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0]
                    print (f"{{{all_word_vuelta[k]}}}  &  {{{all_value_maxs_rounded_vuelta[k]}}} & {{{all_value_mins_rounded_vuelta[k]}}} & {{{div}}}", file=f)
                    print (f"\\\ \cline{{3-8}}  &  & ", file=f)

#               else:
#                   print (f"\multirow{{2}}{{*}} {{none}} & ", file=f)
#                   print (f"\multirow{{2}}{{*}} {{none}}      & ", file=f)
#                   div = all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0]
#                   print (f"none  &  none & none & {{{div}}}", file=f)
#                   print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
#                   div = all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0]
#                   print (f"none  &  none & none & {{{div}}}", file=f)
#                   print (f"\\\ \cline{{3-8}}  &  & ", file=f)

            
            print ('aaaa', all_value_maxs_rounded_ida[-1])
            if (all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0] >= thres and
                    all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0] >= thres):
                print (f"\multirow{{2}}{{*}} {{{all_interval[-1]}}} & ", file=f)
                print (f"\multirow{{2}}{{*}} {{{all_lif[-1]}}}      & ", file=f)
                div = all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0]
                print (f"{{{all_word_ida[-1]}}}  &  {{{all_value_maxs_rounded_ida[-1]}}} & {{{all_value_mins_rounded_ida[-1]}}} & {{{div}}}", file=f)
                print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                div = all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0]
                print (f"{{{all_word_vuelta[-1]}}}  &  {{{all_value_maxs_rounded_vuelta[-1]}}} & {{{all_value_mins_rounded_vuelta[-1]}}} & {{{div}}}", file=f)
                print (f"\\\ \hline ", file=f)

            else:
#               print (f"\multirow{{2}}{{*}} {{none}}  & ", file=f)
#               print (f"\multirow{{2}}{{*}} {{none}}     & ", file=f)
#               div = all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0]
#               print (f" none  &  none  & none & {{{div}}}", file=f)
#               print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
#               div = all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0]
#               print (f"none  &  none  & none & {{{div}}}", file=f)
                print (f"\\\ \hline ", file=f)

        else:

            targ = re.compile(".*>")
            targ2 = targ.findall(reaction_str)
            myreaction = targ2[0][:-2].replace("->", '$\\rightleftharpoons$')

            N = dict_counter_strings[reaction_str]
            dN = N*2

            print (f"\multirow{{{dN}}}{{*}} {{{myreaction}}} & ", file=f)
            print (f"\multirow{{{dN}}}{{*}} {{{N}}} & ", file=f)

            all_interval = []
            all_lif = []

            all_word_ida = []
            all_word_vuelta = []

            all_value_maxs_rounded_ida = []
            all_value_mins_rounded_ida = []

            all_value_maxs_rounded_vuelta = []
            all_value_mins_rounded_vuelta = []

            target_indices = [idx for idx, j in enumerate(strings) if j == reaction_str]
            for j in target_indices:
                i = Closed_reactions[j]

                interval = i[3].strip('(').strip(')')
                all_interval.append(interval)

                lif = i[2].split()[2]
                all_lif.append(lif)

#################         ida:
                indices_ida = [i[j] for j in range(4, 7) if "[]" not in i[j]]
                word_ida = indices_ida[0].replace('we have','') + indices_ida[1].replace(';','')
                all_word_ida.append(word_ida)

                criticals_ida = [i[j] for j in range(7, 11) if "[]:" not in i[j]]

                maxs_star_ida = criticals_ida[0].split(' [')[-1].strip(']')
                maxs_i_list = maxs_star_ida.split(',')
                value_maxs_ida = [float(i) for i in maxs_i_list]
                value_maxs_rounded_ida = [round(i, 4) for i in value_maxs_ida]
                all_value_maxs_rounded_ida.append(value_maxs_rounded_ida)

                mins_star_ida = criticals_ida[1].split(' [')[-1].strip(']')
                mins_i_list = mins_star_ida.split(',')
                value_mins_ida = [float(i) for i in mins_i_list]
                value_mins_rounded_ida = [round(i, 4) for i in value_mins_ida]
                all_value_mins_rounded_ida.append(value_mins_rounded_ida)

#################         vuelta:
                indices_vuelta = [i[j] for j in range(11, 14) if "[]" not in i[j]]
                word_vuelta = indices_vuelta[0].replace('we have','') + indices_vuelta[1].replace(';','')
                all_word_vuelta.append(word_vuelta)

                criticals_vuelta = [i[j] for j in range(14, 18) if "[]:" not in i[j]]

                maxs_star_vuelta = criticals_vuelta[0].split(' [')[-1].strip(']')
                maxs_v_list = maxs_star_vuelta.split(',')
                value_maxs_vuelta = [float(i) for i in maxs_v_list]
                value_maxs_rounded_vuelta = [round(i, 4) for i in value_maxs_vuelta]
                all_value_maxs_rounded_vuelta.append(value_maxs_rounded_vuelta)

                mins_star_vuelta = criticals_vuelta[1].split(' [')[-1].strip(']')
                mins_v_list = mins_star_vuelta.split(',')
                value_mins_vuelta = [float(i) for i in mins_v_list]
                value_mins_rounded_vuelta = [round(i, 4) for i in value_mins_vuelta]
                all_value_mins_rounded_vuelta.append(value_mins_rounded_vuelta)

            for k in range(0, len(all_interval)-1):
                if (all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0] >= thres and
                    all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0] >= thres):
                    print (f"\multirow{{2}}{{*}} {{{all_interval[k]}}} & ", file=f)
                    print (f"\multirow{{2}}{{*}} {{{all_lif[k]}}}      & ", file=f)
                    div = all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0]
                    print (f"{{{all_word_ida[k]}}}  &  {{{all_value_maxs_rounded_ida[k]}}} & {{{all_value_mins_rounded_ida[k]}}} & {{{div}}}", file=f)
                    print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                    div = all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0]
                    print (f"{{{all_word_vuelta[k]}}}  &  {{{all_value_maxs_rounded_vuelta[k]}}} & {{{all_value_mins_rounded_vuelta[k]}}} & {{{div}}}", file=f)
                    print (f"\\\ \cline{{3-8}}  &  & ", file=f)

#               else:
#                   print (f"\multirow{{2}}{{*}} {{none}}  & ", file=f)
#                   print (f"\multirow{{2}}{{*}} {{none}}       & ", file=f)
#                   div = all_value_maxs_rounded_ida[k][0]/all_value_mins_rounded_ida[k][0]
#                   print (f"none  &  none & none & {{{div}}}", file=f)
#                   print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
#                   div = all_value_maxs_rounded_vuelta[k][0]/all_value_mins_rounded_vuelta[k][0]
#                   print (f"none   &  none  & none & {{{div}}}", file=f)
#                   print (f"\\\ \cline{{3-8}}  &  & ", file=f)


            if (all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0] >= thres and
                all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0] >= thres):
                print (f"\multirow{{2}}{{*}} {{{all_interval[-1]}}} & ", file=f)
                print (f"\multirow{{2}}{{*}} {{{all_lif[-1]}}}      & ", file=f)
                div = all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0]
                print (f"{{{all_word_ida[-1]}}}  &  {{{all_value_maxs_rounded_ida[-1]}}} & {{{all_value_mins_rounded_ida[-1]}}} & {{{div}}}", file=f)
                print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
                div = all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0]
                print (f"{{{all_word_vuelta[-1]}}}  &  {{{all_value_maxs_rounded_vuelta[-1]}}} & {{{all_value_mins_rounded_vuelta[-1]}}} & {{{div}}}", file=f)
                print (f"\\\ \hline ", file=f)
            else:
#               print (f"\multirow{{2}}{{*}} {{none}} & ", file=f)
#               print (f"\multirow{{2}}{{*}} {{none}}       & ", file=f)
#               div = all_value_maxs_rounded_ida[-1][0]/all_value_mins_rounded_ida[-1][0]
#               print (f"{{none}}   &  none & none & {{{div}}}", file=f)
#               print (f"\\\ \cline{{5-8}}  &  &  &  & ", file=f)
#               div = all_value_maxs_rounded_vuelta[-1][0]/all_value_mins_rounded_vuelta[-1][0]
#               print (f"none  &  none & none & {{{div}}}", file=f)
                print (f"\\\ \hline ", file=f)

        reaction_str_ini = reaction_str

    print ("""

\\end{tabular}
\\end{adjustbox}
\\caption{\small Only events for which Max.dist/Min.dist $\geq $ 1.1}
\\end{table}
\\end{document}

    """, file=f)


    f.close()



