import sys
# switch to ase_dev:
sys.path.insert(0,"/home/david/ase_dev/ase")

from ase.io import read, write
from ase.io.pov import get_bondpairs
from ase.visualize import view
from ase.data import covalent_radii
import os

print (sys.argv[1])
file = os.path.splitext(sys.argv[1])[0]
print (file)
molecule = read(f'./{file}.xyz')

# 0.5 is the scale by which the gui scales the bonds: "toggle-show-bonds" variable in '~/ase_dev/ase/ase/gui/view.py':
covalent_radii_molecule = covalent_radii[molecule.numbers] * 0.65
print ('covalent_radii_molecule = ', covalent_radii_molecule)

bondpairs = get_bondpairs(molecule, radius=1.5)
print ('bondpairs = ', bondpairs)

#view(molecule)
# ase.visualize.view is going to call the ase local version, not the development one, that's why view(molecule) will be showing the bonds like the default version of ase. This can be changed in ~/ase_dev/visualize/view , but it didn't work.

#sys.exit()
# For  7212.xyz :                                                                                      
#rotation = '19.35877701587121x, -73.10096685014302y, -6.5356238946233525z' # found using ASE-GUI menu 'view -> rotate'

# For  7494.xyz, 7710.xyz, 7758.xyz, 7770.xyz : 
rotation = '-127.79182621445199x, 77.43112047601284y, -138.1905507771526z' # found using ASE-GUI menu 'view -> rotate'


# Common kwargs for eps, png, pov
kwargs = {
    'rotation'      : rotation, # text string with rotation (default='' )
    'radii'         : covalent_radii_molecule, #.85, # float, or a list with one float per atom
#   'colors'        : None,# List: one (r, g, b) tuple per atom
    'show_unit_cell': 0,   # 0, 1, or 2 to not show, show, and show all of cell
    'bondatoms': bondpairs
    }

# Extra kwargs only available for povray (All units in angstrom)
kwargs.update({
    'run_povray'   : True, # Run povray or just write .pov + .ini files
    'display'      : True,# Display while rendering
    'pause'        : True, # Pause when done rendering (only if display)
    'transparent'  : False,# Transparent background
    'canvas_width' : 1200, # Width of canvas in pixels # 200
#   'canvas_height': None, # Height of canvas in pixels
#   'camera_dist'  : 50.,  # Distance from camera to front atom
#   'image_plane'  : None, # Distance from front atom to image plane
#   'camera_type'  : 'perspective', # perspective, ultra_wide_angle
#   'point_lights' : [],             # [[loc1, color1], [loc2, color2],...]
#   'area_light'   : [(2., 3., 40.), # location
#                     'White',       # color
#                     .7, .7, 3, 3], # width, height, Nlamps_x, Nlamps_y
#   'background'   : 'White',        # color
#   'textures'     : None, # Length of atoms list of texture names
#   'celllinewidth': 0.1,  # Radius of the cylinders representing the cell
    })

write(f'{file}.pov', molecule, format='pov', **kwargs)

