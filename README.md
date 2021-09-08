# ChemReact: Chemical Speciation and Reaction Mechanisms Identification

The workflow of codes in this repository allow for the identification of species and reaction mechanisms (*open* and *closed* reactions) given an input trajectory as explained in Ref. [1]

[1] Carrasco-Busturia, David et al., "Ab initio Molecular Dynamics Investigations of the Speciation and Reactivity of Deep Eutectic Electrolytes in Aluminum Batteries", ChemSusChem 2021, 14, **2034**

## 1. Input files

The most important input file you need to run these codes is the ab initio or classical molecular dynamics trayectory. For the sake of convenience, it is generally better to input the trajectory file as generated with [ase's "convert" command line option](https://wiki.fysik.dtu.dk/ase/cmdline.html). For instance, given a set of output files containing different ionic steps, this command line option works in the most intuitive way: 

`ase convert OUTCAR_1 OUTCAR_2 OUTCAR_3 trajectory.traj`


## 2. Speciation: detecting molecules at each time step

The script `detect_molecules_6.py` will take that trajectory file and will count the number of molecules found at each time step. This results in the generation of files of the type:

`{molecule_formula}.count.txt`

where {molecule_formula} is for instance `CH4N2O` for the urea molecule.

This code runs in parallel: each image is sent to a processor for analysis.

The speciation is based on the construction of a connectivity matrix, which after labeling all the atoms with natural numbers, gives information about which atom is connected to which (more information in Ref. [1]).

<img src="https://user-images.githubusercontent.com/18029016/132507269-43e0870e-bac9-4c73-bf6a-5338c370693c.png" width="70%" height="70%">


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

<img src="https://user-images.githubusercontent.com/18029016/132384960-822230b9-b8cf-48ed-ace2-92621f800b97.png" width="20%" height="20%">

The script `scatter_and_run_average_4.py` uses all the aforementioned `{molecule_formula}.count.txt` files and plots the running average concentration of each molecule, something like this:

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

## 4 Detecting chemical reactions 

The script `detect_molecules_6_PII.py` will subtract the matrix elements of the connectivity
matrices involving two times <img src="https://render.githubusercontent.com/render/math?math=t_{1}"> and <img src="https://render.githubusercontent.com/render/math?math=t_{2}">, and it will be then possible to study chemical reactions.
Three cases can be found:

<img src="https://user-images.githubusercontent.com/18029016/132515057-dc01ae7e-bdf3-4529-818d-8e6e37b54542.png" width="50%" height="50%">

so that it is then possible to uniquely identify the indices of those
atoms that form part of a reaction involving bond cleavage or
formation.

Two different scenarios can occur:

1) **Scenario 1**: If the indices involved in the cleavage/formation at a time t1 participate in the reverse 
formation/cleavage reaction at any other given time t2, it has been named as a “closed
reaction”, which is no other than a reversible reaction or a chemical equilibrium.

<img src="https://user-images.githubusercontent.com/18029016/132516852-6561faaa-fc62-4767-9095-b6a85021085a.png" width="50%" height="50%">


1) **Scenario 2**:  If
otherwise, the situation has been classified as an “open
reaction”, which is no other than a irreversible reaction, where broken/formed indices never form/break back
again.

<img src="https://user-images.githubusercontent.com/18029016/132516913-8060f53a-b12d-4b7c-9b5e-80ef89fa4742.png" width="50%" height="50%">

It is also possible to access the information on how much time two atoms remain bonded until they break or vicecersa. In other words, we can access the information about the kietics of the reactions and the lifetime of the intermediate (or product) species.


## Postporcessing

It is also possible to exploit the scripts `parsing_closed_clean.py` and `parsing_open_clean.py` (`detect_molecules_6_PII.py` calls them by default) which generate clear and nice \*tex tables summarizing the reactions, like the following:

1. Reversible reactions:
<img src="https://user-images.githubusercontent.com/18029016/132542241-11b62430-0360-413e-9acd-7425551922ee.png" width="60%" height="60%">

2. Irreversible reactions:
<img src="https://user-images.githubusercontent.com/18029016/132542251-8aae0d22-59dd-4579-b300-310ad8f0c0ef.png" width="50%" height="50%">


*In progress:* detailed documentation for user-friendly use.


