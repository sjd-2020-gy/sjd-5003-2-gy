'''
To the Max main processing
Can start from this module or initiated from tothemaxhome.py

Filename: 
    - tothemaxmain.py 

Called by:
    - tothemaxhome.py (GUI front-end)
    - Command line
    - Developement IDE

Input:   
    - 9 optional arguments - able to be passed in in any order:
        - filename - URL of input raster dataset
        - resolution - Cell size
        - fillsinks - Try filling cells when no downhill slope
        - slopemap - Create slope map - as a percentage, in degrees or both
        - aspectmap - Create aspect map
        - xref - Lower left corner Cartesian map reference (x axis)
        - yref - Lower left corner Cartesian map reference (y axis)
        - hemisphere - Hemisphere of lower left corner Cartesian map reference
        - dispparams - Display Parameter Data
      Note: All arguments but filename have a default value hard coded
      if not supplied.

    - Terrain raster file - URL suppied as a argument
        
Output:
    - Figure (with sub plots - 2 x 2)
        - Elevation map (1)
        - Gradient map (1 or 2)
        - Aspect map (0 or 1)
    - Files
        - snow_slope_map_perc.txt - Slope map data as a percentage
        - snow_slope_map_deg.txt  - Slope map data in degrees
        - snow_aspect_map.txt     - Aspect map data
'''
import csv
import math
import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib as mpl
import neighbourhood as nbh
import surface
import warnings


def pos_int(num_str):
    '''
    Test for a positive integer
    '''
    try:
        if int(num_str) < 1:
            return int(num_str), False
        else:
            return int(num_str), True
    
    except ValueError:
        return math.nan, False
    
#----------------------------------------------------------
# Initialise variables.
#----------------------------------------------------------
DICT_ASPECT = {1:90, 2:135, 4:180, 8:225, 16:270, 32:315, 64:0, 128:45}
CYCLIC_ASPECT = mpl.colors.ListedColormap([
                    'red', 'violet', 'violet', 'royalblue', 'royalblue', 
                    'deepskyblue', 'deepskyblue', 'cyan', 'cyan', 
                    'lime', 'lime', 'yellow', 'yellow', 'orange', 'orange', 
                    'red'])
ARG_NAME = ['--filename', '--resolution', '--fillsinks', '--slopemap', 
            '--aspectmap', '--xref', '--yref', '--hemisphere', '--dispparams']
ARG_DFLT = ['', '50', 'Y', 'D', 'Y', '0', '0', 'N', 'Y']
ARG_DEST = ['file_name', 
            'resolution',
            'fill_sinks',
            'slope_map', 
            'aspect_map',
            'x_ref',
            'y_ref',
            'hemisphere',
            'display_params']
ARG_HELP = ['Raster input file name',
            'Resolution / cell size (metres, integer)',
            'Fill in sinks / holes (Y/N)', 
            'Output slope map as percentages, degress or both (P/D/B)',
            'Output aspect map (Y/N)',
            'Cartesian reference x coordinate (metres, integer)',
            'Cartesian reference y coordinate (metres, integer)',
            'Hemisphere Cartesian coordinaate referebce located in (N/S)',
            'Display parameter data (Y/N)']
terrain = []

#----------------------------------------------------------
# Get and validate command line arguments.
#----------------------------------------------------------
parser = argparse.ArgumentParser()

# Setup arguments
for i in range(len(ARG_NAME)):
    parser.add_argument(ARG_NAME[i], 
                        dest=ARG_DEST[i], 
                        default=ARG_DFLT[i], 
                        help=ARG_HELP[i])

# Bring in arguments.
args = parser.parse_args()

# Store in a list entered arguments and defaults for those not entered.
# Note: order is important for reasigning back.
arg_value = [args.file_name.lower(), 
             args.resolution,
             args.fill_sinks.upper(),
             args.slope_map.upper(),
             args.aspect_map.upper(),
             args.x_ref,
             args.y_ref,
             args.hemisphere.upper(),
             args.display_params.upper()]

arg_err_count = 0

# Validate --filename.
if arg_value[0] == '':
   print(ARG_NAME[0], ': URL not supplied)')
   arg_err_count += 1

# Validate --resolution, --xref, --yref. 
for i in list([1, 5, 6]): 

    int_val, pos_ind = pos_int(arg_value[i])

    if i == 1 and (int_val == math.nan or pos_ind is False):
        print(ARG_NAME[1], ': Must be a positive integer')
        arg_err_count += 1
       
    elif int_val is math.nan:
        print(ARG_NAME[i], ': Must be an integer')
        arg_err_count += 1
        
    else:
        arg_value[i] = int(arg_value[i])

# Validate --slopemap. 
if arg_value[3] not in ('B', 'D', 'P'):
    print(ARG_NAME[3], ': Must be P(ercentage), D(egrees) or B(oth)')
    arg_err_count += 1

# Validate --hemisphere.
if arg_value[7] not in ('N', 'S'):
    print(ARG_NAME[7], ': Must be N(orthern) or S(outhern)')
    arg_err_count += 1

# All others are Y/N and controlled by check buttons.
# Note: If a string argument contain anything other than Y or N, then the 
# logic will treat it as a N.

  
# Abort if any command line errors.
if arg_err_count > 0:
    parser.exit('Argument error - aborting')

# Reasign back.
args.file_name, args.resolution, args.fill_sinks, args.slope_map, \
        args.aspect_map, args.x_ref, args.y_ref, args.hemisphere, \
        args.display_params \
        = arg_value

# Display back to the user (GUI or command line).
if args.display_params == 'Y':
    print('Processed with the following arguments:' 
          + ',\n - Area file name: ' + args.file_name 
          + ',\n - Area resolution (metres): ' + str(args.resolution) 
          + ',\n - Fill sinks / holes: ' + args.fill_sinks 
          + ',\n - Generate area slope map: ' + args.slope_map 
          + ',\n - Generate area aspect: '  + args.aspect_map 
          + ',\n - Starting x,y reference: ' + str(args.x_ref) 
          + ' ' + str(args.y_ref) 
          + ',\n - Hemisphere: ' + args.hemisphere 
          + '.')


#----------------------------------------------------------
# Read in raster dataset and create terrain instance.
#----------------------------------------------------------
terrain = surface.SurfaceRaster(args.file_name)
terrain.read_raster()
terrain.close_raster()


#----------------------------------------------------------
# Start preparing for the creation of the Neighbourhood 
# instances and subsequent Matpotlib mapping.
#----------------------------------------------------------
if terrain.nrows == 0:
    y_limit = len(terrain.cells)
else:
    y_limit = terrain.nrows
    
if terrain.ncols == 0:
    x_limit = len(terrain.cells[0])
else:
    x_limit = terrain.ncols

gradient = [[0 for i in range(x_limit)] for j in range(y_limit)]

# x,y reference point
x_ext = [f'{args.x_ref:,}' + 'E ' + f'{args.y_ref:,}' + args.hemisphere + ' m', 
         f'{(args.x_ref + (args.resolution * x_limit)):,}' + 'E m']

if args.hemisphere == 'N':
    y_ext = [f'{(args.y_ref + (args.resolution*y_limit)):,}' + 'N m', None]
elif args.hemisphere == 'S' and args.y_ref < args.resolution * y_limit:
    y_ext = [f'{((args.resolution * y_limit) - args.y_ref):,}' + 'N m', None]
else:   
    y_ext = [f'{(args.y_ref - (args.resolution * y_limit)):,}' + 'S m', None]


#----------------------------------------------------------
# Create a Gradient instances of Neighbourhood objects
# (3 x 3 cell objects).
#----------------------------------------------------------
for r, row in enumerate(terrain.cells): 
    
    for c, col in enumerate(row):

        # Create 3 x 3 neighbourhood instance.
        gradient[r][c] = nbh.Neighbourhood(
                                terrain.cells, args.resolution, r, c)
        
        # Handle NoData cell.
        if gradient[r][c].centre == terrain.nodata_value:
            terrain.cells[r][c] = math.nan

        # Calculate slope and aspect.
        gradient[r][c].slope_aspect(DICT_ASPECT, terrain.nodata_value)
        
        # If required, deal with a cell where all its 
        # immediate neighbours are all higher.
        if args.fill_sinks == 'Y' and gradient[r][c].slope == -math.inf:
            gradient[r][c].sink_fill(DICT_ASPECT)


#----------------------------------------------------------
# Look for cells that have a list of neighbours with the 
# same maximum downhill gradient.
# 
# From this list and in turn, get the apsect of the 
# neighbourhood in the opposite direction.  If a match, 
# then use this aspect for the current Neighbourhood and 
# ignore the remainder of the list.
#            
# If no matches, take the aspect of the first neighbour
# in the list.
#
# Loop until no more cells can be resolved this way.          
#----------------------------------------------------------
keep_looping = True

while keep_looping:

    keep_looping = False
    
    for r, row in enumerate(terrain.cells): 

        for c, col in enumerate(row):

            # Do if 2 or more D8 downhill directions have been identified.
            if len(gradient[r][c].d8) > 1:
            
                # n = 0 (D8 East)  n = 1 (D8 South-East) 
                # n = 2 (D8 South) n = 3 (D8 South-West) 
                # n = 4 (D8 West)  n = 5 (D8 North-West) 
                # n = 6 (D8 North) n = 7 (D8 North-East)
                for n in gradient[r][c].d8:
    
                    # Edges - Insufficient data - Use the first choice.
                    if (n in (1, 2, 3) and r == 0) \
                       or (n in (5, 6, 7) and r == y_limit - 1) \
                       or (n in (0, 1, 7) and c == 0) \
                       or (n in (3, 4, 5) and c == x_limit - 1):
                        gradient[r][c].d8 = [n]
                        
                    # East cell.
                    # Compare with 3x3 neighbourhood one cell West.
                    elif n == 0:
                        if DICT_ASPECT[2**n] == gradient[r][c-1].aspect:
                            gradient[r][c].aspect = gradient[r][c-1].aspect
                            gradient[r][c].d8 = [n]
                        
                    # Sout-East cell.
                    # Compare with 3x3 neighbourhood one cell North-West.
                    elif n == 1:
                        if DICT_ASPECT[2**n] == gradient[r-1][c-1].aspect:
                            gradient[r][c].aspect = gradient[r-1][c-1].aspect
                            gradient[r][c].d8 = [n]
                        
                    # South cell.
                    # Compare with 3x3 neighbourhood one cell North.
                    elif n == 2:
                        if DICT_ASPECT[2**n] == gradient[r-1][c].aspect:
                            gradient[r][c].aspect = gradient[r-1][c].aspect
                            gradient[r][c].d8 = [n]
                        
                    # South-West cell.
                    # Compare with 3x3 neighbourhood one cell North-East.
                    elif n == 3:
                        if DICT_ASPECT[2**n] == gradient[r-1][c+1].aspect:
                            gradient[r][c].aspect = gradient[r-1][c+1].aspect
                            gradient[r][c].d8 = [n]
                        
                    # West cell.
                    # Compare with 3x3 neighbourhood one cell East.
                    elif n == 4:
                        if DICT_ASPECT[2**n] == gradient[r][c+1].aspect:
                            gradient[r][c].aspect = gradient[r][c+1].aspect
                            gradient[r][c].d8 = [n]
                        
                    # North-West cell.
                    # Compare with 3x3 neighbourhood one cell South-East.
                    elif n == 5:
                        if DICT_ASPECT[2**n] == gradient[r+1][c+1].aspect:
                            gradient[r][c].aspect = gradient[r+1][c+1].aspect
                            gradient[r][c].d8 = [n]
                        
                    # North cell.
                    # Compare with 3x3 neighbourhood one cell South.
                    elif n == 6:
                        if DICT_ASPECT[2**n] == gradient[r+1][c].aspect:
                            gradient[r][c].aspect = gradient[r+1][c].aspect
                            gradient[r][c].d8 = [n]
                        
                    # North-East cell.
                    # Compare with 3x3 neighbourhood one cell South-West.
                    else:
                        if DICT_ASPECT[2**n] == gradient[r+1][c-1].aspect:
                            gradient[r][c].aspect = gradient[r+1][c-1].aspect
                            gradient[r][c].d8 = [n]

                    # If the cell has been resolved, another full iteration
                    # will be required.
                    if len(gradient[r][c].d8) == 1:
                        keep_looping = True
                        break # Don't need to check any remaining options
                              # for this cell.


#----------------------------------------------------------
# Start mapping using Matplotlib
#----------------------------------------------------------

# There is one user warning being generated by Matplotlib
# that occurs without any established pattern.  Without 
# changing any Arguments, the user warning sometimes occurs
# on consecuative runs and sometimes many executions apart.
# So the following code prevents user warning from being 
# returned.
warnings.filterwarnings('ignore', 
                        message='Warning: converting a masked element to nan', 
                        category=UserWarning, module='matplotlib')

plt.fig = plt.figure('To the Max - Student 201388212')
plt.fig.set_size_inches(13, 9)
plt.fig.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)

#----------------------------------------------------------
# Generate orginal Elevation map
#----------------------------------------------------------
plt.subplot(221).title.set_text('Elevation Map')
plt.imshow(terrain.cells, cmap='gist_gray')
plt.colorbar().set_label('Elevation (m)')
plt.xticks([0, x_limit], x_ext)
plt.yticks([0, y_limit], y_ext)

    
#----------------------------------------------------------
# Generate Aspect map from Gradient instances
#----------------------------------------------------------
if args.aspect_map == ('Y'):
    plt.subplot(222).title.set_text('Aspect Map')
    colormap = plt.imshow([[cells.aspect for cells in gradient[r]] 
                   for r in range(len(gradient))], cmap=CYCLIC_ASPECT)
    plt.clim(0, 360)
    cbar = plt.colorbar(colormap, ticks=np.linspace(0, 360, 17)) 
    cbar.set_ticks(np.arange(0, 361, 45).tolist())
    cbar.set_ticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])
    cbar.set_label('Aspect')
    plt.xticks([0, x_limit], x_ext)
    plt.yticks([0, y_limit], y_ext)


#----------------------------------------------------------
# Generate Slope map(s) from Gradient instances
#----------------------------------------------------------

plt.subplot(223).title.set_text('Gradient Map (1)')

if args.slope_map in ('B', 'D'):
    plt.imshow([[cells.slope_deg for cells in gradient[r]] 
                for r in range(len(gradient))], cmap='winter_r')
    plt.colorbar().set_label('Slope (Degrees)')
else:

    plt.imshow([[cells.slope_perc for cells in gradient[r]] 
                for r in range(len(gradient))], cmap='winter_r')
    plt.colorbar().set_label('Slope (%)')

plt.xticks([0, x_limit], x_ext)
plt.yticks([0, y_limit], y_ext)

if args.slope_map == 'B':
    plt.subplot(224).title.set_text('Gradient Map (2)')
    plt.imshow([[cells.slope_perc for cells in gradient[r]] 
                for r in range(len(gradient))], cmap='winter_r')
    plt.colorbar().set_label('Slope (%)')
    plt.xticks([0, x_limit], x_ext)
    plt.yticks([0, y_limit], y_ext)


#----------------------------------------------------------
# Show all maps requested
#----------------------------------------------------------
plt.show()


#----------------------------------------------------------
# Output datasets
#  - snow_slope_map_perc.txt Slope map data as a percentage
#  - snow_slope_map_deg.txt  Slope map data in degrees
#  - snow_aspect_map.txt     Aspect map data
#----------------------------------------------------------
f2 = open('snow_slope_map_perc.txt', 'w', newline='')
f3 = open('snow_slope_map_deg.txt', 'w', newline='')
f4 = open('snow_aspect_map.txt', 'w', newline='')

output1 = csv.writer(f2, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
output2 = csv.writer(f3, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
output3 = csv.writer(f4, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)


for r in range(len(gradient)):  

    if args.slope_map in ['P', 'B']:
        output1.writerow([round(cells.slope_perc,1) for cells in gradient[r]])

    if args.slope_map in ['D', 'B']:
        output2.writerow([round(cells.slope_deg,1) for cells in gradient[r]])

    if args.aspect_map == 'Y':
        output3.writerow([cells.aspect for cells in gradient[r]])

f2.close() 
f3.close() 
f4.close() 
