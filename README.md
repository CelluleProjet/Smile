# Smile
Smile: simple tool for microscope USB camera visualization 

## Contacts
- Yiuri Garino: yiuri.garino@cnrs.fr   

[Cellule Projet](http://impmc.sorbonne-universite.fr/fr/plateformes-et-equipements/cellule-projet.html) @ [IMPMC](http://impmc.sorbonne-universite.fr/en/index.html)

## Installation: setting up the software for the first time

1) Download and install Anaconda
https://docs.anaconda.com/anaconda/install/

2) from anaconda prompt (windows) or terminal (Ubuntu & MAC) add conda-forge channel
```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
``` 

3) create virtual environment with name "Smile" and the necessary libraries
```bash
conda create -n Smile spyder spyder-kernels configparser opencv pillow ghostscript
```

4) activate the virtual environment with
```bash
conda activate Smile 
```

5) launch spyder with
```bash
spyder
```

6) open file **_Smile_Init.py_** and run the program.
This script will search for USB camera and it will create a default _Init_id_n.txt_ file for each USB camera found, with _n_ the camera id number.
Choose the desired camera and rename the corresponding file (i.e. _Init_id_0.txt_) to _Init.txt_

7) open file **_Smile.py_** and run the program.

## Requirements 

In case of direct use:

```
conda install -c conda-forge ghostscript opencv
conda install -c anaconda pillow configparser
```
## _Init.txt_ File
Example:

```
[Camera]
camera_id = 0

[Graphic]
grid_step = 100
grid_width = 2
grid_color = #000000
line_width = 2
line_color = #ffffff

[Zoom]
x 1 = 1
x 2 = 100
x 4 = 10000

[Settings]
width = 1280.0
height = 720.0
brightness = 0
contrast = 32.0
saturation = 64.0
hue = 0.0
gain = -1.0
```
To change the pixel to µm conversion ration, change the values in the second colums of the **[Zoom]** section
+ 1st column: **"x 1"**  is the text visualized in the ComboBox
+ 2nd column: **"1"**  is the pixel to µm conversion ratio associated to the selction "x 1"

**ATTENTION:** to update the new values it is necessary to save the _Init.txt_ file **AND** restart the program

## Basic Usage

A screenshot of the **Camera** page is shown here below:  

The **Grid** button shows/hides the grid spaced by the number of pixels displayed to its right.  
The **Zoom** combo box selects the associated pizel to µm conversion  
To the right of the **Line (pixel/µm)** label the size of the drawn line is shown  
If the **FCC** checkbutton is not selected the left mouse button draws a line  
If the **FCC** check button is selected, the left mouse button will select and draw the data points and the **Circle** button will fit and draw a circle on the data points  
To the right of the **Circle** button the position of the Xc Yc center, the radius Rc and the area of the circle will be displayed in both pixels and µm depending on the zoom selection  

![V230207_Camera](https://user-images.githubusercontent.com/83216683/218143502-5c0643a4-b909-43d4-836c-a3b347fcfc14.PNG)

A screenshot of the **Settings** page is shown here below:  

![V230207_Settings](https://user-images.githubusercontent.com/83216683/218147068-90b81a1b-668e-496c-8c80-bffb6d96f617.PNG)

## Compiled .exe

A version compiled using [pyinstaller](https://pyinstaller.org/en/stable/) under Windos 11 can be found from [this link](https://drive.google.com/drive/folders/1MZFI8nxq0Xk9AffwlsgMmnXqg4MQ3uCN?usp=share_link)  

## Licence

Copyright (c) 2022-2023 Yiuri Garino

License: GPLv3

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
