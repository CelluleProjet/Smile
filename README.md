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

6) open file *Smile_Init.py* and run the program.
This script will search for USB camera and it will create a default _Init_id_n.txt_ file for each USB camera found, with _n_ the camera id number.
Chose the desired camera and rename the corresponding file (i.e. _Init_id_0.txt_) to _Init.txt_

7) open file *Smile.py* and run the program.

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
+ 2nd column: **"1"**  is the pixel to µm conversion ration associated to the selction "x 1"

ATTENTION: to update the new values it is necessary to save the _Init.txt_ file **AND** restart the program

## Licence

Copyright (c) 2022-2023 Yiuri Garino

License: GPLv3

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
