# -*- coding: utf-8 -*-
"""

Smile_Init: create Init file for the "Smile" pogram

Smile: simple tool for microscope USB camera visualization 

Version 230221

Author: Yiuri Garino @ yiuri.garino@cnrs.fr

Copyright (c) 2022-2023 Yiuri Garino

Download: https://github.com/CelluleProjet/Smile

Requirements:
    
conda install -c conda-forge ghostscript opencv
conda install -c anaconda pillow configparser

License: GPLv3

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

# from IPython import get_ipython
# #clean Console and Memory
# get_ipython().magic('cls')
# get_ipython().magic('reset -sf')

print("""
      
Smile_Init: create Init file for the "Smile" pogram

Version 230221

Author: Yiuri Garino @ yiuri.garino@cnrs.fr

Copyright (c) 2022-2023 Yiuri Garino

Download: https://github.com/CelluleProjet/Smile
      """)
import cv2
import configparser as cp

all_camera_idx_available = []

prop_list_name = ["WIDTH",
"HEIGHT",
"BRIGHTNESS",
"CONTRAST",
"SATURATION",
"HUE",
"GAIN"]

prop_list = [cv2.CAP_PROP_FRAME_WIDTH,
cv2.CAP_PROP_FRAME_HEIGHT,
cv2.CAP_PROP_BRIGHTNESS,
cv2.CAP_PROP_CONTRAST,
cv2.CAP_PROP_SATURATION,
cv2.CAP_PROP_HUE,
cv2.CAP_PROP_GAIN]



    
def save_config(filename):
    for i, value in enumerate(prop_list):
        prop = cap.get(prop_list[i])
        key = prop_list_name[i]
        print(f'{key} = {prop}')
        config['Settings'][key] = str(prop)
    with open(filename, 'w') as configfile:    # save
        config.write(configfile)
        print()
        print(f'Saved {filename}')
        print()
for camera_idx in range(10):
    cap = cv2.VideoCapture(camera_idx)
    
    if cap.isOpened():
        print(f'Camera index available: {camera_idx}')
        print()
        all_camera_idx_available.append(camera_idx)
        config = cp.ConfigParser()
        filename = f'Init_id_{camera_idx}.txt'
        config.read(filename)
        try:
            config['Camera']
        except:
            config.add_section('Camera')
        config['Camera']['camera_id'] = str(camera_idx)
        
        try:
            config['Graphic']
        except:
            config.add_section('Graphic')
            config['Graphic']['grid_step'] = '100'
            config['Graphic']['grid_width'] = '2'
            config['Graphic']['grid_color '] = 'black'
            config['Graphic']['line_width'] = '2'
            config['Graphic']['line_color  '] = 'white'
            
        
        try:
            config['Zoom']
        except:
            config.add_section('Zoom')
            config['Zoom']['x 1'] = '1'
            config['Zoom']['x 2'] = '100'
            config['Zoom']['x 4'] = '10000'
            
        try:
            config['Settings']
        except:
            config.add_section('Settings')
        
        save_config(filename)
        cap.release()
    else:
        print(f'Camera index NOT available: {camera_idx}')


input("Type to quit")