'''
Surface Data Object

Purpose:
    - Read the contents of a surface DEM
    - Basic validation of the content
    - Separate header data from cell data
    
Developer Note:
    - This class can be used for extracting data from any raster DEM dataset.

Filename: 
    - surface.py 

Classes: 
    - SurfaceRaster
    
Methods:
    - read_raster
    - close_raster
    
Input:   
    - Dataset URL
    - CSV field separator
        
Output:
    - Instance of SurfaceRaster class
'''

import sys
import csv
import warnings

#----------------------------------------------------------
# SurfaceRaster Class
#----------------------------------------------------------
class SurfaceRaster():
    '''
    Input raster dataset data object.
    '''
    
    def __init__(self, dataset, separator=' '):
        '''
        Opens input raster dataset.

        Initialises data object instance.
        
        Triggered by:
            - any python program
            
        Input:
            - Dataset URL
            - Dataset data cell seperator
            
        Output:
            - Terrain surface data instance
        '''
        
        # Raster file data variables
        self.f1 = open(dataset, newline='')
        self.reader = csv.reader(self.f1, delimiter=separator)

        # Raseter header data variables
        self.ncols = 0
        self.nrows = 0
        self.xllcorner = 0
        self.xllcenter = 0
        self.yllcorner = 0
        self.yllcenter = 0
        self.cellsize = 0
        self.nodata_value = 0

        # Raster cell data variables
        self.cells = []
        self.cell_count = 0     
        

    def read_raster(self):
        '''
        Use this method to input a surface raster dataset and separate 
        header data (if exists) from cell data.

        Triggered by:
            - any python program
            
        Input:
            - None
            
        Output:
            - Elevation data from input dataset
            - Validation exceptions (corruption, if any) of input dataset
        '''
        for row in self.reader: 

            # Geo-referenced rows will only have two data cells
            if len(row) == 2:
                # Geo-referenced header data
                if row[0].lower() == 'ncols':
                    self.ncols = int(row[1])
                elif row[0].lower() == 'nrows':
                    self.nrows = int(row[1])
                elif row[0].lower() == 'xllcorner':
                    self.xllcorner = int(row[1])
                elif row[0].lower() == 'xllcenter':
                    self.xllcenter = int(row[1])
                elif row[0].lower() == 'yllcorner':
                    self.yllcorner = int(row[1])
                elif row[0].lower() == 'yllcenter':
                    self.yllcenter = int(row[1])
                elif row[0].lower() == 'cellsize':
                    self.cellsize = int(row[1])
                elif row[0].lower() == 'nodata_value':
                    self.nodata_value = int(row[1])
                else:
                    pass
            else:
                # Cell data
                if row[0] == '':
                    row.pop(0)
                if row[-1] == '':
                    row.pop(-1)
                
                # Keep a running count of cells input
                self.cell_count += len(row)
 
                # Validate cell data is numeric
                try:
                    self.cells.append(
                            list(map(lambda row_elem: float(row_elem), row)))
                except:
                    sys.exit('Invalid data encountered in row #'  
                             + str(self.reader.line_num) + ' in raster file.')

        # Check for dataset corruption
        if (self.nrows > 0 
                and self.ncols > 0 
                and self.nrows * self.ncols != self.cell_count) \
            or (self.cell_count % len(self.cells[0]) != 0):
                sys.exit('Inconsistent no. of cells per row in raster file.')

        # If required, calculate corner raster starting reference.
        # Note: ...center and ...corner variables are mutually exclusive.
        if self.xllcenter > 0:
            self.xllcorner = self.xllcenter - (self.xllcenter % self.cellsize)
            
        if self.yllcenter > 0:
            self.yllcorner = self.yllcenter - (self.yllcenter % self.cellsize)


    def close_raster(self):
        '''
        Use this method to close an input raster dataset.

        Triggered by:
            - any python program
            
        Input:
            - None
            
        Output:
            - None
        '''
        self.f1.close() 
