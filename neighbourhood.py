'''
Neighbourhood Data Object

Purpose:
    - Creates a 3 x 3 cell instance from the terrain

Filename: 
    - neighbourhood.py 

Input:
    - Terrain surface Raster data (excluding headers)
    - Terrain resolution / cell size
    - Terrain processing cell row number
    - Terrain processing cell column number
        
Output:
    - Instance of Neighbourhood class

Classes: 
    - Neighbourhood - a 3 x 3 block of cells with the processing cell
        located in the centre (1,1)

Methods:  
    - slope_aspect
    - sink_fill
    - get<var name> (multiple) 
    - Set<var name> (multiple).
'''


import math


#----------------------------------------------------------
# Neighbourhood Class
#----------------------------------------------------------
class Neighbourhood():
    '''
    Processing an instance of a 3 x 3 Neighbourhood.
    '''
    def __init__(self, terrain, resolution, y, x):
        '''
        Initialisation of the Neighbourhood instance 
        with variables relating to:
            - 3 x 3 neighbourhood grid
            - Slope (percentage & degrees)
            - Aspect
        
        Triggered by:
            - tothemaxmain.py
            
        Input:
            - Terrain Raster data (excluding headers)
            - Terrain resolution / cell size
            - Terrain processing cell row number
            - Terrain processing cell column number
            
        Output:
            - 3 x 3 cell instance from the terrain data
        '''
        #---------------------------------------------------------
        # Initialise variables.
        #---------------------------------------------------------
        self.resolution = resolution
        self.y_boundary = len(terrain) - 1
        self.x_boundary = len(terrain[0]) - 1
        self.edge = None
        self.slope = -math.inf
        self.slope_perc = -math.inf
        self.slope_deg = -math.inf
        self.aspect = math.nan       
        self.d8 = []
        
        #---------------------------------------------------------
        # Construct 3 x 3 Neighbourhood grid.
        # Identify, if applicable, direction of adjacent edge.
        #---------------------------------------------------------
        if y == 0 and x == 0:
            self.neighbourhood = [
                    [terrain[y][x]] * 3,
                    [terrain[y][x], terrain[y][x], terrain[y][x+1]],
                    [terrain[y][x], terrain[y+1][x], terrain[y+1][x+1]]]
            self.edge = 'NW'

        elif y == 0 and x < self.x_boundary:
            self.neighbourhood = [
                    [terrain[y][x]] * 3,
                    [terrain[y][x-1], terrain[y][x], terrain[y][x+1]],
                    [terrain[y+1][x-1], terrain[y+1][x], terrain[y+1][x+1]]]
            self.edge = 'N'

        elif y == 0:
            self.neighbourhood = [
                    [terrain[y][x]] * 3,
                    [terrain[y][x-1], terrain[y][x], terrain[y][x]],
                    [terrain[y+1][x-1], terrain[y+1][x], terrain[y][x]]]
            self.edge = 'NE'
 
        elif y < self.y_boundary and x == 0:
            self.neighbourhood = [
                    [terrain[y][x], terrain[y-1][x], terrain[y-1][x+1]],
                    [terrain[y][x], terrain[y][x], terrain[y][x+1]],
                    [terrain[y][x], terrain[y+1][x], terrain[y+1][x+1]]]
            self.edge = 'W'

        elif y < self.y_boundary and x < self.x_boundary:
            self.neighbourhood = [
                    [terrain[y-1][x-1], terrain[y-1][x], terrain[y-1][x+1]],
                    [terrain[y][x-1], terrain[y][x], terrain[y][x+1]],
                    [terrain[y+1][x-1], terrain[y+1][x], terrain[y+1][x+1]]]
            self.edge = 'No Edge'

        elif y < self.y_boundary:
            self.neighbourhood = [
                    [terrain[y-1][x-1], terrain[y-1][x], terrain[y][x]],
                    [terrain[y][x-1], terrain[y][x], terrain[y][x]],
                    [terrain[y+1][x-1], terrain[y+1][x], terrain[y][x]]]
            self.edge = 'E'
                        
        elif x == 0:
            self.neighbourhood = [
                    [terrain[y][x], terrain[y-1][x], terrain[y-1][x+1]],
                    [terrain[y][x], terrain[y][x], terrain[y][x+1]],
                    [terrain[y][x]] * 3]
            self.edge = 'SW'

        elif x < self.x_boundary:
            self.neighbourhood = [
                    [terrain[y-1][x-1], terrain[y-1][x], terrain[y-1][x+1]],
                    [terrain[y][x-1], terrain[y][x], terrain[y][x+1]],
                    [terrain[y][x]] * 3]
            self.edge = 'S'

        else:
            self.neighbourhood = [
                    [terrain[y-1][x-1], terrain[y-1][x], terrain[y][x]],
                    [terrain[y][x-1], terrain[y][x], terrain[y][x]],
                    [terrain[y][x]] * 3]
            self.edge = 'SE'


        #---------------------------------------------------------
        # Seperate the centre Neighbourhood cell from the
        # neighbours and order the neighbours for D8 slope
        # calculation purposes, starting with the East 
        # neighbour and working clockwise.
        #---------------------------------------------------------
        self.centre = self.neighbourhood[1][1] # Processing cell

        self.neighbours = [
                self.neighbourhood[1][2],  # East neighbour
                self.neighbourhood[2][2],  # South-East neighbour
                self.neighbourhood[2][1],  # South neighbour
                self.neighbourhood[2][0],  # South_West neighbour
                self.neighbourhood[1][0],  # West neighbour
                self.neighbourhood[0][0],  # Noth_West neighbour
                self.neighbourhood[0][1],  # North neighbour
                self.neighbourhood[0][2]]  # North-East neighbour
            
           
    def slope_aspect(self, d8_dict, nodata_value):
        '''
        Use this method to identify the maximum downhill gradient of a 
        Neigbourhood, and the applicable aspect using D8 notation.
        
        Start with the East neighbour and work clockwise.

        Triggered by:
            - tothemaxmain.py
            
        Input:
            - D8 dictionary
            - Geo-referenced NoData value 
            
        Output:
            - Slope calculation as a percentage
            - Slope calculation in degrees
            - Aspect of max. gradient (first cell if more than 1 with the same)
            - List of D8 directions containing the same maximum slope 
        '''
        
        #              --Straight edge--    ---------Corner edge--------
        DICT_EDGE = {0:('NE', 'E', 'SE'), 1:('NE', 'E', 'SE', 'S', 'SW'), 
                     2:('SW', 'S', 'SE'), 3:('NW', 'W', 'SW', 'S', 'SE'),
                     4:('NW', 'W', 'SW'), 5:('SW', 'W', 'NW', 'N', 'NE'),
                     6:('NW', 'N', 'NE'), 7:('NW', 'N', 'NE', 'E', 'SE')}
        dist_adjacent  = self.resolution
        dist_diagonal = math.sqrt((self.resolution**2) * 2)

        #---------------------------------------------------------
        # Starting from the East neighbour and working clockwise.
        #---------------------------------------------------------
        for n, neighbour in enumerate(self.neighbours):

            # Do not use if upward gradient
            if self.centre == nodata_value:
                break

            # Do not use if neighbour contains NoData
            if self.neighbours[n] == nodata_value:
                continue
            
            # Do not use if neighbour is outside of the boundaries
            if self.edge in DICT_EDGE[n]:
                continue
            
            # Do not use if upward gradient
            if self.centre - self.neighbours[n] < 0:
                continue

            # Is cells comparison orthogonl or diagonal to each other? 
            # Note: diagonal is when n = 1, 3, 5 or 7)
            if n % 2 == 0:
                if (self.centre - self.neighbours[n]) / dist_adjacent \
                    > self.slope:
                    self.slope = (self.centre - self.neighbours[n]) \
                                 / dist_adjacent
                    self.d8 = [n]
                    self.aspect = d8_dict[2**n]
                    
                elif (self.centre - self.neighbours[n]) / dist_adjacent \
                      == self.slope:
                     self.d8.append(n)

            else:
                if (self.centre - self.neighbours[n]) / dist_diagonal \
                    > self.slope:
                    self.slope = (self.centre - self.neighbours[n]) \
                                  / dist_diagonal
                    self.d8 = [n]
                    self.aspect = d8_dict[2**n]

                elif (self.centre - self.neighbours[n]) / dist_diagonal \
                      == self.slope:
                    self.d8.append(n)

        #---------------------------------------------------------
        # No downhill slope found
        #---------------------------------------------------------
        if math.isinf(self.slope):
            self.slope_perc = math.nan
            self.slope_deg = math.nan
        else:
            self.slope_perc = self.slope * 100
            self.slope_deg = math.atan(self.slope) * 180 / math.pi
        
        
    def sink_fill(self, d8_dict):
        '''
        Use this method to fill the processing cell when it does not have 
        any neighbours that lead downhill from it.
        
        Triggered by:
            - tothemaxmain.py
            
        Input:
            - D8 dictionary
            
        Output:
            - Slope calculation as a percentage
            - Slope calculation in degrees
            - Aspect calculation
            - D8 direction calculation 
        '''
        #---------------------------------------------------------
        # If the processing cell is not an an edge cell, modify 
        # height value equal to the lowest height of the 8
        # neighbours.  Then assign slope and aspect.
        #---------------------------------------------------------
        if self.edge == 'No Edge' and self.neighbours.count(-math.inf) != 8:
            self.slope = 0.0
            self.d8 = [self.neighbours.index(
                            min(n for n in self.neighbours if n != -math.inf))]
            self.aspect = d8_dict[2**self.d8[0]]
        
        #---------------------------------------------------------
        # If the cell is now filled, do more slope calculations. 
        #---------------------------------------------------------
        if math.isinf(self.slope) is False:
            self.slope_perc = self.slope * 100
            self.slope_deg = math.atan(self.slope) * 180 / math.pi
    
    
    #-------------------------------------
    # Get & Set methods
    #-------------------------------------
    @property
    def edge(self):
        '''Get the cell edge indicator'''
        return self._edge
            
    @edge.setter
    def edge(self,val):
        '''Set the cell edge indicator'''
        self._edge = val
            
    @property
    def y_boundary(self):
        '''Get the y axis boundary'''
        return self._y_boundary
            
    @y_boundary.setter
    def y_boundary(self,val):
        '''Set the y axis boundary'''
        self._y_boundary = val
            
    @property
    def x_boundary(self):
        '''Get the x axis boundary'''
        return self._x_boundary
            
    @x_boundary.setter
    def x_boundary(self,val):
        '''Set the x axis boundary'''
        self._x_boundary = val
            
    @property
    def slope(self):
        '''Get the cell to cell rise over run value'''
        return self._slope
            
    @slope.setter
    def slope(self,val):
        '''Set the cell to cell rise over run value'''
        self._slope = val
            
    @property
    def slope_perc(self):
        '''Get the cell to cell slope as a percentage value'''
        return self._slope_perc
            
    @slope_perc.setter
    def slope_perc(self,val):
        '''Set the cell to cell slope as a percentage value'''
        self._slope_perc = val
            
    @property
    def slope_deg(self):
        '''Get the cell to cell slope in degrees value'''
        return self._slope_deg
            
    @slope_deg.setter
    def slope_deg(self,val):
        '''Set the cell to cell slope in degrees value'''
        self._slope_deg = val
            
    @property
    def aspect(self):
        '''Get the cell aspect value'''
        return self._aspect
            
    @aspect.setter
    def aspect(self,val):
        '''Set the cell aspect value'''
        self._aspect = val
            
 