#

# Nice function for title of graphs:
def titles(folders_P):
    names = {
           'Electrolyte' : 'Reactants @ ',
           'long_paths' : 'Products @ ',

           '1.5_Salt__1_Ur' : '1.5:1 mixture. ',
           '1.5_to_1' : '1.5:1 mixture. ',
           '10_urea_15_AlCl3' : '1.5:1 mixture. ',
           'One_to_one_Salt_Ur' : '1:1 mixture. ',
           'one_to_one_urea_salt' : '1:1 mixture. ',
           '14_urea_7_Al2Cl6' : '1:1 mixture. ',

           '650K_2_300K' : "T = 1000 K + 300 K\n",
           '650K_to_300K' : "T = 1000 K + 300 K\n",
           'at_300K_new' : "T = 300 K\n",
           'at_300K' : "T = 300 K\n",

           'Al2Cl7-__AlCl2Ur2+' : '$[$Al$_{2}$Cl$_{7}]^{-}$ + $[$AlCl$_{2}$(urea)$_{2}]^{+}$',
           'Al2Cl6Ur__plus__AlCl3Ur' : '$[$Al$_{2}$Cl$_{6}$(ur)$]$ + $[$AlCl$_{3}$(ur)$]$',
           'AlCl4-__Al2Cl5Ur2+' : '$[$AlCl$_{4}]^{-}$ + $[$Al$_{2}$Cl$_{5}$(urea)$_{2}]^{+}$' ,
           'AlCl3_ur' : '$[$AlCl$_{3}$ (urea)$]$ + $[$AlCl$_{3}$ (urea)$]$',
           'AlCl4-__AlCl2Ur2+' : '$[$AlCl$_{4}]^{-}$ + $[$AlCl$_{2}$(urea)$_{2}]^{+}$',

           'linked_to_same_Al' : '-(O,O) to same Al atom.',
           'linked_to_diff_Al' : '-(O,O) to diff Al atom.',

           'NaCl' : ' NaCl model',
           'NaCl_prim' : ' NaCl model',
           'CsCl' : ' CsCl model'
    }

    all_suptitles_label = []
    for i in folders_P:
        data = i.split("/")
        data_fmt = []
        for k in data:
            if k in names:
                data_fmt.append(names[k])

        if not '650K_2_300K' in data or not 'at_300K_new' in data or not 'at_300K'  in data or not '650K_to_300K' in data:
            data_fmt.append("T = 1000 K\n")

        data_fmt = list(dict.fromkeys(data_fmt))

        if "Products @ " in data_fmt:
            N_ureas = 16.
        else:
            N_ureas = 12.

        if "Products @ " in data_fmt:
            if not " NaCl model" in data_fmt and not " CsCl model" in data_fmt:
                data_fmt_sorted = [data_fmt[0], data_fmt[1], data_fmt[3], data_fmt[2]]
                data_fmt_sorted.append(" NaCl model")

            if " NaCl model" in data_fmt:
                data_fmt_sorted = [data_fmt[0], data_fmt[1], data_fmt[4], data_fmt[2], data_fmt[3]]

            if " CsCl model" in data_fmt and not "-(O,O) to same Al atom." in data_fmt and not "-(O,O) to diff Al atom." in data_fmt:
               data_fmt_sorted = [data_fmt[0], data_fmt[1], data_fmt[4], data_fmt[2], data_fmt[3]]

            if " CsCl model" in data_fmt and "-(O,O) to same Al atom." in data_fmt:
               data_fmt_sorted = [data_fmt[0], data_fmt[1], data_fmt[5], data_fmt[2], data_fmt[3], data_fmt[4]]

            if " CsCl model" in data_fmt and "-(O,O) to diff Al atom." in data_fmt:
               data_fmt_sorted = [data_fmt[0], data_fmt[1], data_fmt[5], data_fmt[2], data_fmt[3], data_fmt[4]]

            if "-(O,O) to same Al atom." in data_fmt and not " NaCl model" in data_fmt and not " CsCl model" in data_fmt:
                data_fmt_sorted = [data_fmt[0], data_fmt[1], data_fmt[4], data_fmt[2], data_fmt[3]]
                data_fmt_sorted.append(" NaCl model")

            if "-(O,O) to diff Al atom." in data_fmt and not " NaCl model" in data_fmt and not " CsCl model" in data_fmt:
                data_fmt_sorted = [data_fmt[0], data_fmt[1], data_fmt[4], data_fmt[2], data_fmt[3]]
                data_fmt_sorted.append(" NaCl model")

        else:
            r = re.compile(".*Rd.*")
            auxa1 = list(filter(r.match, data)) 
            target_Sd = auxa1[0]
            data_fmt_sorted = [data_fmt[0], data_fmt[1], data_fmt[2], target_Sd]

        suptitle_label = ''.join(data_fmt_sorted)
        all_suptitles_label.append(suptitle_label)

    print ('all_suptitles_label = ', all_suptitles_label)
    return all_suptitles_label

#import re
#folders_P = ["/home/energy/dcabu/long_paths/Correct_rho/1.5_Salt__1_Ur/Al2Cl7-__AlCl2Ur2+/NaCl/23.08.2019/SC_2x2x2/make_ok_poscar_and_potcar/AIMD/Restart_1/650K_2_300K/R3-R19__Analysis_working_indices/R3-R19.traj"]
#allo = titles(folders_P)
#print (allo)

