# ChemReact: Chemical Speciation and Reaction Mechanisms Identification

The workflow of codes in this repository allow for the identification of species and reaction mechanisms (*open* and *closed* reactions) given an input trajectory as explained in Ref. [1]

[1] Carrasco-Busturia, David et al., "Ab initio Molecular Dynamics Investigations of the Speciation and Reactivity of Deep Eutectic Electrolytes in Aluminum Batteries", ChemSusChem 2021, 14, **2034**

## 1. Input files

The most important input file you need to run these codes is the ab initio or classical molecular dynamics trayectory. For the sake of convenience, it is generally better to input the trajectory file as generated with [ase's "convert" command line option](https://wiki.fysik.dtu.dk/ase/cmdline.html). For instance, given a set of output files containing different ionic steps, this command line option works in the most intuitive way: 

`ase convert OUTCAR_1 OUTCAR_2 OUTCAR_3 trajectory.traj`


## 2. Detecting molecules at each time step

The script `detect_molecules_6.py` will take that trajectory file and will count the number of molecules found at each time step. This results in the generation of files of the type:

`{molecule_formula}.count.txt`

where {molecule_formula} is for instance `CH4N2O` for the urea molecule.

This code runs in parallel: each image is sent to a processor for analysis.

### 2.1 System specific warning: 

a) Make sure to modify the radius criteria for each atom for the definition of bonds:

`cutoff_dict = {'Al': 1, 'Cl': 1.7, 'H': .37, 'O': 1, 'N': 1, 'C': 1}`

b) Also this part of the code ensures no Al-Al or Cl-Cl bonds are formed (you may want to modify this as well):

```
    Cl_indices = np.array([a.index for a in atoms if a.symbol == 'Cl'])
    for i in Cl_indices:
        for j in range(len(atoms)):
            if syms[j] != 'Al':
                mat[i, j] = 0
                mat[j, i] = 0
```

## 3. Running averages

Plotting the _type_ and _number_ of molecules found at each fs time step is very confusing. 
It gives a better picture to divide the trajectory in chunks of 500 fs, and make this division every 1 fs, in other words, "moving chunks" of 500 fs:

<!--- ![runn_avg](https://user-images.githubusercontent.com/18029016/132384960-822230b9-b8cf-48ed-ace2-92621f800b97.png&s=200)
--> 

<img src="https://user-images.githubusercontent.com/18029016/132384960-822230b9-b8cf-48ed-ace2-92621f800b97.png" width="20%" height="20%">

<!---  replace ![image](https://your-image-url.type) with <img src="https://your-image-url.type" width="50%" height="50%">
-->

The script `scatter_and_run_average_4.py` uses all the aforementioned `{molecule_formula}.count.txt` files and plots the running average concentration of each molecule, something like this:

[composition_and_running_av_E_6.small.pdf](https://github.com/DavidCdeB/ChemReact/files/7123357/composition_and_running_av_E_6.small.pdf)

<!---![p2](https://user-images.githubusercontent.com/18029016/132387621-cc9fc624-457b-476d-af15-968e95d945e7.png)
-->

<img src="https://user-images.githubusercontent.com/18029016/132387621-cc9fc624-457b-476d-af15-968e95d945e7.png" width="70%" height="70%">

### 3.1 System specific warning: 

Make sure you adapt the numeric-formula-to-chemical-formula conversion:

```
dict_labels = {                                                                                        
        'C2H8AlCl2N4O2'       : '$[$AlCl$_{2}$(ur)$_{2}]^{+}$',
        'Al2Cl7'              : '$[$Al$_{2}$Cl$_{7}]^{-}$',
        'AlCl4'               : '$[$AlCl$_{4}]^{-}$',
        'C2H8Al2Cl5N4O2'      : '$[$Al$_{2}$Cl$_{5}$(ur)$_{2}]^{+}$',
 ...
        'CH4AlCl3N2O'         : '$[$AlCl$_{3}$(ur)$]$',
}
```
```
dict_colors = {                                                                                        
        'C2H8AlCl2N4O2'       :  'green',
        'Al2Cl7'              :  'red',
        'AlCl4'               :  'blue',
        'C2H8Al2Cl5N4O2'      :  'orange',
 ...
        'C2H8Al5Cl15N4O2'     :  'crimson',
}
```

*In progress:* detailed documentation for user-friendly use.


