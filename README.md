# To the Max
---
This application was contructed during the study of  
&emsp;&emsp;GEOG5003M - Programming for Geographical Information Analysis,  
&emsp;&emsp;University of Leeds.  

The application primarily selects a Raster ascii dataset and displays an elevation map, 1 or 2 slope maps and an optional aspect map.  Output ascii output files are also generated. 

Defaults, if they exist, are read in from the ascii file.  Using the GUI front-end, once the file has been selected, the user can override them.


---
### Contents of Repository

##### Application Files
* tothemaxhome.py  
* tothemaxmain.py  
* neighbourhood.py
* surface.py  
  
##### Input Datasets
* snow.slope  
* nn22.asc  
  
##### Execution Preparation
* Copy all .py files (4) to folder of choice.
* Copy all input datasets (2) to folder of choice.

---
### Run Instructions

##### With GUI
At command prompt, enter:

&emsp;&emsp;***python tothemaxhome.py***  


##### Without GUI
At command prompt, enter:

&emsp;&emsp;***python tothemaxmain.py***  

with any or all of the following optional arguments:  

| Argument | Description |  
| --- | --- |  
| ***&#x2010;&#x2010;filename url*** | where url = Full path and file name of Raster ascii dataset (string) |  
| ***&#x2010;&#x2010;resolution n*** | where n = Resolution / cell size of Raster ascii dataset (numeric) |  
| ***&#x2010;&#x2010;fillsinks x*** | where x = Fill in sinks where no downhill slope detected from a cell (Y/N*) |  
| ***&#x2010;&#x2010;slopemap x*** | where x = Generate Slope map as a Pentcentage, in Degrees or Both (P/D/B) |  
| ***&#x2010;&#x2010;aspectmap x*** | where x = Generate Aspect map (Y/N*) |  
| ***&#x2010;&#x2010;xref n*** | where n = Lower left corner Cartesian map reference (x axis, numeric) |  
| ***&#x2010;&#x2010;yref y*** | where n = Lower left corner Cartesian map reference (y axis, numeric) |  
| ***&#x2010;&#x2010;hemisphere x*** | where x = Hemisphere of lower left corner Cartesian map reference (N/S) |  
| ***&#x2010;&#x2010;dispparams x*** | where x = Display Parameter Data (Y/N*) |  

*Any other value will be treat as if a N


---
##### Author Details 
Name: To be advised after marking  
Student Id: 201388212  
Course: Master of Science - Geographical Information Science  
Unit: GEOG5003M - Programming for Geographical Information Analysis (36393)  
Published Date: 14 May 2020  

---
##### License Details 
sjd-2020-gy/sjd-5003-2-gy is licensed under the MIT License.
