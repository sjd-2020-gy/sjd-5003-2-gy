# GEOG5003M - Assignment 2 (201388212)
---
Submission of Python Code, test documentation and test output files for Assignment 2 due 15 May 2020.  

### To the Max!(...imum Gradient...)

This application has been developed using Python 3.7.  The key functional components are:
* Reads a raster dataset containing rows and columns of surface elevation data values.  The app is able to accept both georeferenced and non-georeferenced formatted datasets.
* Performs basic data validation on the input dataset.  No output will be generated if the input dataset fails validation (corruption).
* Calculates slope values (degrees and percentages) for each surface data cell.
* Calculates aspect values for each surface data cell.
* Generates and displays a figure containing the following combinations of maps:
	- (2 maps) DEM map, slope map in degrees (default combination);
	- (2 maps) DEM map, slope map using percentages;
	- (3 maps) DEM map, slope map in degrees, slope map using percentages;
	- (3 maps) DEM map, slope map in degrees, aspect map;
	- (3 maps) DEM map, slope map using percentages, aspect map;
	- (4 maps) DEM map, slope map in degrees, slope map using percentages, aspect map.
* Generates and outputs text files containing rows and columns of:
	- Slope data in degrees (Default);
	- Slope data using percentages;
	- Aspect data.


---
### Contents of Repository

##### Python Files
* tothemaxhome.py  
* tothemaxmain.py  
* surface.py  
* neighbourhood.py
  
##### Test Documents
* Test Cases.pdf  

##### Input Files Used 
* snow.slope (standard file supplied by University of Leeds)  
* nn22.asc (geo-referenced ascii file extracted from Digimap, provided to proove versatility)

##### Output Files Created (Input: snow.slope)
* slope_map_deg_1.txt  (slope map in degrees)  
* slope_map_perc_1.txt (slope map using percentages)
* aspect_map_1.txt     (aspect map)
(note: _n manually appended after run)

##### Output Files Created (Input: nn22.asc)
* slope_map_deg_1.txt  (slope map in degrees)  
* slope_map_perc_1.txt (slope map using percentages)
* aspect_map_1.txt     (aspect map)
(note: _n manually appended after run)

##### Execution Preparation
* Copy all .py files (4) to folder of choice.
* Copy input files (2) to folder of choice.


---
### Run Instructions

##### With GUI
At command prompt, enter:

&emsp;&emsp;***python tothemaxhome.py***  


##### Without GUI
At command prompt, enter:

&emsp;&emsp;***python tothemaxmain.py***  

with any or all of the following optional arguments:  

| --- | --- |  
| ***&#x2010;&#x2010;filename url*** | where url = path and file name of selected input dataset |  
| ***&#x2010;&#x2010;resolution n*** | where n = resolution / cellsize of tthe surface input dataset (numeric) |  
| ***&#x2010;&#x2010;fillsinks  x*** | where x = Fill data cells when no downhill slope leading from it (**Y**es / **N**o*) |  
| ***&#x2010;&#x2010;slopemap x*** | where x = Slope map selection (as a **P**ercentage, in **D**egrees or **B**oth) |  
| ***&#x2010;&#x2010;aspectmap x*** | where x = Aspect map required (**Y**es / **N**o*) |  
| ***&#x2010;&#x2010;xref n*** | where n = Lower left corner Cartesian map reference - x axis (numeric) |  
| ***&#x2010;&#x2010;yref n*** | where n = Lower left corner Cartesian map reference - y axis (numeric) |  
| ***&#x2010;&#x2010;hemisphere x*** | where x = Hemisphere of x,y Cartesian map reference (**N**orthern, **S**outhern) | 
| ***&#x2010;&#x2010;dispparams x*** | where x = Display Parameter Data (**Y**es / **N**o*) |  

*Any other value will be treat as if a **N**o


---
###### Submission Details 
Date: 14 May 2020  
Student Id: 201388212  
Course: Master of Science - Geographical Information Science  
Unit: GEOG5003M - Programming for Geographical Information Analysis (36393)  
