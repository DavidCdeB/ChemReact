
#


from  collections import Counter
import re

def table_closed_reactions(Closed_reactions):

    strings = [i[1] for i in Closed_reactions]
    dict_counter_strings = dict(Counter(strings))

    f = open('Reactions_Closed_Table.tex', 'w')
    print ("""

\\documentclass{article}
\\usepackage[margin=0.3in]{geometry}
\\usepackage{multirow}
\\usepackage{adjustbox}
\\begin{document}

\\begin{table}[]
\\begin{adjustbox}{width=\\hsize, totalheight=\\textheight, keepaspectratio}
\\begin{tabular}{|l|l|l|l|l|l|l|}
\\hline
Reaction & N & Interval  & lifetime  & Indices & Max. dist. & Min. dist \\\ \\hline

    """, file=f)
    reaction_str_ini = list(dict_counter_strings.keys())[0]
    targ = re.compile(".*>")
    targ2 = targ.findall(reaction_str_ini)
    myreaction = targ2[0][:-2].replace("->", '$\\rightleftharpoons$')

    N = dict_counter_strings[reaction_str_ini]
    dN = N*2

    print (f"\multirow{{{dN}}}{{*}} {{{myreaction}}} & ", file=f)
    print (f"\multirow{{{dN}}}{{*}} {{{N}}} & ", file=f)

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
                print (f"\multirow{{2}}{{*}} {{{all_interval[k]}}} & ", file=f)
                print (f"\multirow{{2}}{{*}} {{{all_lif[k]}}}      & ", file=f)
                print (f"{{{all_word_ida[k]}}}  &  {{{all_value_maxs_rounded_ida[k]}}} & {{{all_value_mins_rounded_ida[k]}}}", file=f)
                print (f"\\\ \cline{{5-7}}  &  &  &  & ", file=f)
                print (f"{{{all_word_vuelta[k]}}}  &  {{{all_value_maxs_rounded_vuelta[k]}}} & {{{all_value_mins_rounded_vuelta[k]}}}", file=f)
                print (f"\\\ \cline{{3-7}}  &  & ", file=f)

            print (f"\multirow{{2}}{{*}} {{{all_interval[-1]}}} & ", file=f)
            print (f"\multirow{{2}}{{*}} {{{all_lif[-1]}}}      & ", file=f)
            print (f"{{{all_word_ida[-1]}}}  &  {{{all_value_maxs_rounded_ida[-1]}}} & {{{all_value_mins_rounded_ida[-1]}}}", file=f)
            print (f"\\\ \cline{{5-7}}  &  &  &  & ", file=f)
            print (f"{{{all_word_vuelta[-1]}}}  &  {{{all_value_maxs_rounded_vuelta[-1]}}} & {{{all_value_mins_rounded_vuelta[-1]}}}", file=f)
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
                print (f"\multirow{{2}}{{*}} {{{all_interval[k]}}} & ", file=f)
                print (f"\multirow{{2}}{{*}} {{{all_lif[k]}}}      & ", file=f)
                print (f"{{{all_word_ida[k]}}}  &  {{{all_value_maxs_rounded_ida[k]}}} & {{{all_value_mins_rounded_ida[k]}}}", file=f)
                print (f"\\\ \cline{{5-7}}  &  &  &  & ", file=f)
                print (f"{{{all_word_vuelta[k]}}}  &  {{{all_value_maxs_rounded_vuelta[k]}}} & {{{all_value_mins_rounded_vuelta[k]}}}", file=f)
                print (f"\\\ \cline{{3-7}}  &  & ", file=f)

            print (f"\multirow{{2}}{{*}} {{{all_interval[-1]}}} & ", file=f)
            print (f"\multirow{{2}}{{*}} {{{all_lif[-1]}}}      & ", file=f)
            print (f"{{{all_word_ida[-1]}}}  &  {{{all_value_maxs_rounded_ida[-1]}}} & {{{all_value_mins_rounded_ida[-1]}}}", file=f)
            print (f"\\\ \cline{{5-7}}  &  &  &  & ", file=f)
            print (f"{{{all_word_vuelta[-1]}}}  &  {{{all_value_maxs_rounded_vuelta[-1]}}} & {{{all_value_mins_rounded_vuelta[-1]}}}", file=f)
            print (f"\\\ \hline ", file=f)

        reaction_str_ini = reaction_str

    print ("""

\\end{tabular}
\\end{adjustbox}
\\end{table}
\\end{document}

    """, file=f)


    f.close()
