# ChemReact: Chemical Speciation and Reaction Mechanisms Identification

The workflow of codes in this repository allow for the identification of species and reaction mechanisms (*open* and *closed* reactions) given an input trajectory as explained in Ref. [1]

[1] Carrasco-Busturia, David et al., "Ab initio Molecular Dynamics Investigations of the Speciation and Reactivity of Deep Eutectic Electrolytes in Aluminum Batteries", ChemSusChem 2021, 14, **2034**

## Input files

The most important input file you need to run these codes is the ab initio or classical molecular dynamics trayectory. For the sake of convenience, it is generally better to input the trajectory file as generated with [ase's "convert" command line option](https://wiki.fysik.dtu.dk/ase/cmdline.html). For instance, given a set of output files containing different ionic steps, this command line option works in the most intuitive way: 

`ase convert OUTCAR_1 OUTCAR_2 OUTCAR_3 trajectory.traj`


## Detecting molecules at each time step

The script `detect_molecules_6.py` will take that trajectory file and will count the number of molecules found at each time step. This results in the generation of files of the type:

`{molecule_formula}.count.txt`

where {molecule_formula} is for instance `CH4N2O` for the urea molecule.

This code runs in parallel: each image is sent to a processor for analysis.

### System specific warning: 

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

## Running averages

Plotting the _type_ and _number_ of molecules found at each fs time step is very confusing. 
It gives a better picture to divide the trajectory in chunks of 500 fs, and make this division every 1 fs, in other words, "moving chunks" of 500 fs:



*In progress:* detailed documentation for user-friendly use.


