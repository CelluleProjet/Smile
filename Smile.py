# -*- coding: utf-8 -*-
"""

Smile: simple tool for microscope USB camera visualization 

Version 230303

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

# Reset for use in Spyder
# from IPython import get_ipython
# #clean Console and Memory
# get_ipython().magic('cls')
# get_ipython().magic('reset -sf')



import tkinter as tk
from tkinter import colorchooser 
from tkinter import filedialog
import time
import cv2
import configparser as cp
from PIL import Image, ImageTk
from tkinter import ttk
from math import sqrt
import numpy as np

resize = 1


class MainWindow():
    
    def __init__(self, window, ):
        res_x = int(448/2) # Image in About
        res_y = int(300/2) # Image in About
        
        self.debug = 0
        self.DirectShow = 1
        
        self.config = cp.ConfigParser()
        self.config.read('Init.txt')
        
        self.camera_id = int(self.config['Camera']['camera_id'])
        self.grid_step = tk.StringVar()
        self.grid_step.set(self.config['Graphic']['grid_step'])
        self.grid_width = int(self.config['Graphic']['grid_width'])
        self.grid_color = self.config['Graphic']['grid_color']
        self.line_width = int(self.config['Graphic']['line_width'])
        self.line_color = self.config['Graphic']['line_color']
        self.points = []
        
        if self.debug:
            sticky_a = 'e'
            padx = 2
            pady = 2
        else:
            sticky_a = 'nesw'
            padx = 2
            pady = 2
        self.line_lenght_pixel = 0
        
        self.window = window
        self.window.protocol("WM_DELETE_WINDOW", self.ExitApplication) #Intercept the close button
        self.window.configure(background='DimGray')
        self.window.wm_title("Smile Version 230303")
        self.prop_list_name = ["WIDTH",
"HEIGHT",
"BRIGHTNESS",
"CONTRAST",
"SATURATION",
"HUE",
"GAIN"]
        self.prop_list = [cv2.CAP_PROP_FRAME_WIDTH,
cv2.CAP_PROP_FRAME_HEIGHT,
cv2.CAP_PROP_BRIGHTNESS,
cv2.CAP_PROP_CONTRAST,
cv2.CAP_PROP_SATURATION,
cv2.CAP_PROP_HUE,
cv2.CAP_PROP_GAIN]

        self.prop_list_var = []
        self.prop_list_entry = []
        self.n = ttk.Notebook(self.window)
        if resize:
            self.window.grid_columnconfigure(0, weight=1)
            self.window.grid_rowconfigure(0, weight=1)
        

        if self.DirectShow:
            self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(self.camera_id)
        
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280 )
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.interval = 20 # Interval in ms to get the latest frame
        
        # Create canvas for image
        if self.debug:
            self.mainframe_pag_A = tk.Frame(self.n, bg = 'blue' )  #, width=400, height=280 first page, which would get widgets gridded into it
        else:
            self.mainframe_pag_A = ttk.Frame(root, borderwidth=5, relief="sunken")
        self.mainframe_pag_A.grid(column =0, row = 0)
        
        #mainframe_pag_A First line
        
        self.ck_grid_value = tk.IntVar() 
        self.ck_grid_value.set(0)
        
        ck_grid = ttk.Checkbutton(self.mainframe_pag_A, text = "Grid", command = self.update_grid, variable = self.ck_grid_value)
        ck_grid.grid(column=0, row=0, sticky = sticky_a, padx = padx, pady = pady)
        
        grid_step_entry = ttk.Entry(self.mainframe_pag_A, textvariable=self.grid_step, width = 8)
        grid_step_entry.grid(column=1, row=0, sticky = sticky_a, padx = padx, pady = pady)
        
        ttk.Label(self.mainframe_pag_A, text = "Zoom :", anchor="e").grid(column = 2, row = 0, sticky = sticky_a, padx = padx, pady = pady)
        
        self.vlist = []
        self.vlist_um = []
        
        self.Combo = ttk.Combobox(self.mainframe_pag_A, values = self.vlist, width = 8) #, font='sans 10 bold'
        
        self.Combo.bind("<<ComboboxSelected>>", self.change_range)
        self.Combo.grid(column=3, row=0, sticky = sticky_a, padx = padx, pady = pady)
        self.Combo.state(["readonly"])
        
        ttk.Label(self.mainframe_pag_A, text = "Line (pixel / µm) :", anchor="e").grid(column = 4, row = 0, sticky = sticky_a, padx = padx, pady = pady)
        
        self.line_lenght = tk.StringVar()
        self.line_lenght.set("0.00")
        ttk.Label(self.mainframe_pag_A, textvariable = self.line_lenght).grid(column = 5, row = 0, sticky = sticky_a, padx = padx, pady = pady)
        
        #save_button = ttk.Button(self.mainframe_pag_A, text="Save", command=self.save_command)
        save_button = tk.Button(master=self.mainframe_pag_A, text="Save", command=self.save_command, fg = "white", font='sans 10 bold', bg = "forest green")
        save_button.grid(column=6, row=0, sticky = sticky_a, padx = padx, pady = pady)
        
        #clear_button = ttk.Button(self.mainframe_pag_A, text="Clear", command=self.delete_line)
        clear_button = tk.Button(master=self.mainframe_pag_A, text="Clear", command=self.delete_line, fg = "white", font='sans 10 bold', bg = "RoyalBlue2")
        clear_button.grid(column=7, row=0, sticky = sticky_a, padx = padx, pady = pady)
        
        #mainframe_pag_A Second line
        
        self.ck_FCC_value = tk.IntVar() 
        self.ck_FCC_value.set(0)
        ck_FCC = ttk.Checkbutton(self.mainframe_pag_A, text = "FCC", command = self.update_FCC, variable = self.ck_FCC_value)
        ck_FCC.grid(column=0, row=1, sticky = sticky_a, padx = padx, pady = pady)
        
        #circle_button = ttk.Button(self.mainframe_pag_A, text="Circle", command=self.circle)
        circle_button = tk.Button(master=self.mainframe_pag_A, text="Circle", command=self.circle, fg = "white", font='sans 10 bold', bg = "RoyalBlue2")
        circle_button.grid(column=1, row=1, sticky = sticky_a, padx = padx, pady = pady)
        
        self.circle_label_value = tk.StringVar()
        self.circle_label_value.set('Circle Area')
        circle_label = ttk.Label(self.mainframe_pag_A, textvariable=self.circle_label_value, anchor='w')
        circle_label.grid(column=0, row=2, columnspan=6, sticky = sticky_a, padx = padx, pady = pady)
        
        self.ck_line_h_value = tk.IntVar() 
        self.ck_line_h_value.set(0)
        
        self.ck_line_v_value = tk.IntVar() 
        self.ck_line_v_value.set(0)
        
        ck_line_h = ttk.Checkbutton(self.mainframe_pag_A, text = "H Line", variable = self.ck_line_h_value, command = self.h_or_v)
        ck_line_h.grid(column=4, row=1, sticky = "e", padx = padx, pady = pady)
        
        ck_line_v  = ttk.Checkbutton(self.mainframe_pag_A, text = "V Line", variable = self.ck_line_v_value, command = self.v_or_h)
        ck_line_v.grid(column=5, row=1, sticky = sticky_a, padx = padx, pady = pady)
        
        self.canvas = tk.Canvas(self.mainframe_pag_A, width=self.width, height=self.height)
        self.canvas.grid(column=0, row = 3, columnspan = 8, rowspan = 80, sticky = sticky_a, padx = padx, pady = pady)
        
        if resize:
            for x in range(8):
                tk.Grid.columnconfigure(self.mainframe_pag_A, x, weight=1)
            tk.Grid.rowconfigure(self.mainframe_pag_A, 3, weight=1)
        
        # bindings
        self.canvas.bind("<Button-1>", self.xy_grid)
        self.canvas.bind("<B1-Motion>", self.update_line)
        self.canvas.bind("<B1-ButtonRelease>", self.finish_line)
        
        # Update image on canvas
        self.update_image()
        
        mainframe_pag_B = ttk.Frame(self.n, borderwidth=5, relief="sunken")
        mainframe_pag_B.grid(column=0, row=0)
        
        for i, value in enumerate(self.prop_list_name):
            l = tk.Label(mainframe_pag_B,text = self.prop_list_name[i], anchor="w")
            l.grid(row=i,column=0, sticky = 'nesw')
            exec(f"var_{i} = tk.StringVar()")
            exec(f"self.prop_list_var.append(var_{i})")
            exec(f"var_{i}.set(self.cap.get(self.prop_list[i]))")
            l = tk.Label(mainframe_pag_B,textvariable = self.prop_list_var[i])
            l.grid(row=i,column=1)
            _ = str(self.prop_list_var[i].get())
            e = tk.Entry(mainframe_pag_B)
            e.insert(-1, _)
            exec("self.prop_list_entry.append(e)")
            e.grid(row=i,column=2)
            
        self.load_init_config()
        self.Combo.current(0)
        
        set_prop_button = ttk.Button(mainframe_pag_B, text="Set", command=self.set_new_prop)
        set_prop_button.grid(column=2, row=len(self.prop_list_name), sticky = sticky_a, padx = padx, pady = pady)
        
        color_label = ttk.Label(mainframe_pag_B,text = "Colors", anchor="w")
        color_label.grid(column=0, row=len(self.prop_list_name)+1, sticky = sticky_a, padx = padx, pady = pady)
        
        color_label = ttk.Label(mainframe_pag_B,text = "Grid", anchor="w")
        color_label.grid(column=1, row=len(self.prop_list_name)+1, sticky = sticky_a, padx = padx, pady = pady)
        
        color_label = ttk.Label(mainframe_pag_B,text = "Lines", anchor="w")
        color_label.grid(column=1, row=len(self.prop_list_name)+2, sticky = sticky_a, padx = padx, pady = pady)
        
        self.color_grid_button = tk.Button(mainframe_pag_B, background = self.grid_color, command = self.grid_color_select)
        self.color_grid_button.grid(column=2, row=len(self.prop_list_name)+1, sticky = sticky_a, padx = padx, pady = pady)
        
        self.color_line_button = tk.Button(mainframe_pag_B, background = self.line_color, command = self.line_color_select)
        self.color_line_button.grid(column=2, row=len(self.prop_list_name)+2, sticky = sticky_a, padx = padx, pady = pady)
        
        save_prop_button = ttk.Button(mainframe_pag_B, text="Save", command=self.save_config)
        save_prop_button.grid(column=1, row=len(self.prop_list_name)+3, sticky = sticky_a, padx = padx, pady = pady)
        
        load_prop_button = ttk.Button(mainframe_pag_B, text="Load", command=self.load_config)
        load_prop_button.grid(column=2, row=len(self.prop_list_name)+3, sticky = sticky_a, padx = padx, pady = pady)
        
        mainframe_pag_C = ttk.Frame(self.n, borderwidth=25, relief="ridge", width = res_x*2, height = res_y*2)
        mainframe_pag_C.grid(column=0, row=0)
        
        self.photo_IMPMC = ImageTk.PhotoImage(Image.open("logo_IMPMC.jpg").resize((res_x, res_y)))
        self.photo_CP = ImageTk.PhotoImage(Image.open("logo_CP.jpg").resize((res_x, res_y)))
        self.About = """
        
Smile: simple tool for microscope USB camera visualization 

Version 230303

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
        label_CP = tk.Label(mainframe_pag_C, image = self.photo_CP, padx = padx, pady = pady)
        label_CP.grid(row = 0, column = 0, sticky = tk.NSEW)

        label_IMPMC = tk.Label(mainframe_pag_C, image = self.photo_IMPMC, padx = padx, pady = pady)
        label_IMPMC.grid(row = 0, column = 1, sticky = tk.NSEW)

        label_About = tk.Label(mainframe_pag_C, text = self.About, anchor = 'e', justify = "left", padx = padx, pady = pady, wraplength=2*res_x)
        label_About.grid(row = 1, column = 0, columnspan = 2, sticky = tk.NSEW)
        
        self.n.add(self.mainframe_pag_A, text='Camera')
        self.n.add(mainframe_pag_B, text='Settings')
        self.n.add(mainframe_pag_C, text='About')
        
        self.n.grid(sticky = sticky_a, padx = padx, pady = pady)
        self.lines = []
    
    def grid_color_select(self):
        _, new_color = colorchooser.askcolor()
        if new_color:
            self.grid_color = new_color
            self.color_grid_button.config(background = self.grid_color)
        if self.debug:
            print(self.grid_color)
     
    def line_color_select(self):
        _, new_color = colorchooser.askcolor()
        if new_color:
            self.line_color = new_color
            self.color_line_button.config(background = self.line_color)
        if self.debug:
            print(self.line_color)
                    
    def update_FCC(self):
        if self.ck_FCC_value.get():
            # unbinding 
            if self.debug: 
                print("unbinding")
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<B1-ButtonRelease>")
            self.canvas.bind("<Button-1>", self.xy_FCC)
            
        else:
            if self.debug: 
                print("re binding")
            # re - bindings
            self.canvas.bind("<Button-1>", self.xy_grid)
            self.canvas.bind("<B1-Motion>", self.update_line)
            self.canvas.bind("<B1-ButtonRelease>", self.finish_line)
        
    def save_config(self):
        filename = filedialog.asksaveasfilename()
        if filename:
            for i, value in enumerate(self.vlist):
                self.config['Zoom'][value] = self.vlist_um[i]
            for i, value in enumerate(self.prop_list_name):
                self.config['Settings'][value] = self.prop_list_var[i].get()
                
            self.config['Graphic']['line_color'] = self.line_color
            self.config['Graphic']['grid_color'] = self.grid_color
            
            with open(filename, 'w') as configfile:    # save
                self.config.write(configfile)
                if self.debug:
                    print(f"File saved: {configfile}")
        else:
            if self.debug:
                print("No Save file selected")

    def load_config(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.config.read(filename)
            self.grid_color = self.config['Graphic']['grid_color']
            self.line_color = self.config['Graphic']['line_color']
            self.color_line_button.config(background = self.line_color)
            self.color_grid_button.config(background = self.grid_color)
            self.vlist_um = []
            self.vlist = []
            for key in self.config['Zoom']:
                
                self.vlist.append(key)
                self.vlist_um.append(self.config['Zoom'][key])
            self.Combo.config(values = self.vlist) 
            
            for i, value in enumerate(self.prop_list_name):
                if self.debug:
                    print(f"Prop {value} = {self.config['Settings'][value]}")
                c1 = f"self.cap.set(self.prop_list[i]," + self.config['Settings'][value] +")"
                exec(c1)
            for i, value in enumerate(self.prop_list_name):
                c2 = f"self.prop_list_var[{i}].set( " + self.config['Settings'][value] +")"
                exec(c2)
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.canvas.config(width=self.width, height=self.height)
            if self.debug:
                print(f"Res = {self.width} x {self.height}")
                
            #Turn OFF grid
            self.ck_grid_value.set(0)
            self.update_grid()
            if self.debug:
                print(f"File loaded: {filename}")
        else:
            if self.debug:
                print("No Load file selected")
                
    def load_init_config(self):
        self.config.read('Init.txt')
        
        self.vlist_um = []
        self.vlist = []
        for key in self.config['Zoom']:
            
            self.vlist.append(key)
            self.vlist_um.append(self.config['Zoom'][key])
        self.Combo.config(values = self.vlist) 
        
        for i, value in enumerate(self.prop_list_name):
            if self.debug:
                print(f"Prop {value} = {self.config['Settings'][value]}")
            c1 = f"self.cap.set(self.prop_list[i]," + self.config['Settings'][value] +")"
            exec(c1)
        for i, value in enumerate(self.prop_list_name):
            c2 = f"self.prop_list_var[{i}].set( " + self.config['Settings'][value] +")"
            exec(c2)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas.config(width=self.width, height=self.height)
        if self.debug:
            print(f"Res = {self.width} x {self.height}")
            
        #Turn OFF grid
        self.ck_grid_value.set(0)
        self.update_grid()
        
    def set_new_prop(self):
        for i, value in enumerate(self.prop_list_name):
            c1 = f"self.cap.set(self.prop_list[i]," + self.prop_list_entry[i].get() +")"
            exec(c1)
        for i, value in enumerate(self.prop_list_name):
            c2 = f"self.prop_list_var[{i}].set(self.cap.get(self.prop_list[i]))"
            exec(c2)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas.config(width=self.width, height=self.height)
        
        #Turn OFF grid
        self.ck_grid_value.set(0)
        self.update_grid()
    
    def test_command(self):
        print(globals())
        
    def change_range(self, event):
        global peak
        if self.debug:
            print("_-"*30)
            print()
            print(self.Combo.current(), self.Combo.get(), self.vlist_um[self.Combo.current()])
            print()
            print("_-"*30)
        self.Combo.select_clear()

        self.update_line_lenght()
        
    def update_line_lenght(self):
        line_pixel = self.line_lenght_pixel
        ratio = float(self.vlist_um[self.Combo.current()])
        line_um = ratio*line_pixel
        self.line_lenght.set(f"{line_pixel:.02f} / {line_um:.02f}")
        # if self.debug:
        #     print(f"Line R, pixel, um = {ratio:.02f} {line_pixel:.02f} {line_um:.02f} ")
        
    def xy_grid(self, event):
        
        self.startx, self.starty = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        tmp = self.canvas.create_line((self.startx, self.starty, self.startx, self.starty), fill=self.line_color, width=5, tags='custom_line')
        self.lines.append(tmp)
        if self.debug:
            print(f'Click ON x = {self.startx:.02f} y = {self.starty:.02f}')
    
    def xy_FCC(self, event):
        #add point
        _x = round(event.x)
        _y = round(event.y)
        self.points.append([_x,_y])
        self.canvas.create_oval(_x-4, _y-4, _x+4, _y+4, fill=self.line_color, tags='FCC_circle')
        if self.debug:
            print(self.points)
            
            

    def update_line(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        if self.ck_line_h_value.get():
            self.canvas.coords(self.lines[-1],self.startx, self.starty, x, self.starty)
        elif self.ck_line_v_value.get():
            self.canvas.coords(self.lines[-1],self.startx, self.starty, self.startx, y)
        else:
            self.canvas.coords(self.lines[-1],self.startx, self.starty, x, y)

    def h_or_v(self):
        #H selected, turn off V
        self.ck_line_v_value.set(0)
    
    def v_or_h(self):
        #V selected, turn off H
        self.ck_line_h_value.set(0)
            
        
    def finish_line(self, event):
        self.canvas.itemconfigure('custom_line', width=self.line_width) 
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        if self.ck_line_h_value.get():
            self.line_lenght_pixel = abs(x - self.startx)
        elif self.ck_line_v_value.get():
            self.line_lenght_pixel = abs(y - self.starty)
        else:
            self.line_lenght_pixel = sqrt(((x - self.startx))**2 + ((y - self.starty))**2)
            
        
        self.update_line_lenght()
        if self.debug:
            print(f'Click OFF x = {x:.02f} y = {y:.02f}')
            print('Line pixel / um = ' + self.line_lenght.get())

            
    def delete_line(self):
        self.canvas.delete('custom_line')
        self.canvas.delete('FCC_circle')
        if self.debug: print("Custom lines deleted")
    
    def times(self):
        print(time.strftime("%d-%m-%Y-%H-%M-%S"))
    
    def save_command(self):
        filename = time.strftime("Image_%y%m%d_%H%M%S")
        # save postscipt image 
        self.canvas.postscript(file = filename + '.eps') 
        # use PIL to convert to PNG 
        img = Image.open(filename + '.eps') 
        img.save(filename + '.png', 'png') 
    
    def update_image(self):
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = Image.fromarray(self.image) # to PIL format
        self.image = ImageTk.PhotoImage(self.image) # to ImageTk format
        # Update image
        tmp = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        
        # Move new image to background to keep showing lines, points and circles
        self.canvas.tag_lower(tmp)
        
        # Repeat every 'interval' ms
        self.window.after(self.interval, self.update_image)
    
    def update_grid(self):#, event=None):
        if self.ck_grid_value.get():
            # Creates all vertical lines at intevals of self.grid_width
            for i in range(0, int(self.width), int(self.grid_step.get())):
                self.canvas.create_line([(i, 0), (i, int(self.height))], tag='grid_line', width = self.grid_width, fill=self.grid_color)
        
            # Creates all horizontal lines at intevals of self.grid_width
            for i in range(0, int(self.height), int(self.grid_step.get())):
                self.canvas.create_line([(0, i), (int(self.width), i)], tag='grid_line', width = self.grid_width, fill=self.grid_color)
        else:
            self.canvas.delete('grid_line') # Will only remove the grid_line
    
    def Circle_center(self,X,Y):
        U = X - X.mean()
        V = Y - Y.mean()
        Suu = (U**2).sum()
        Suv = (U*V).sum()
        Svv = (V**2).sum()
        Suuu = (U**3).sum()
        Suvv = (U*V**2).sum()
        Svvv = (V**3).sum()
        Svuu = (V*U**2).sum()
        
        A = np.array([[Suu,Suv],[Suv,Svv]])
        B = 0.5 * np.array([Suuu+Suvv,Svvv+Svuu])
        
        Uc, Vc = np.linalg.solve(A,B)
        
        R = np.sqrt(Uc**2+Vc**2+(Suu+Svv)/len(X))
        return np.array([Uc + X.mean(), Vc + Y.mean(), R])
    
    def circle(self):

        x = np.array(self.points)[:,0]
        y = np.array(self.points)[:,1]
        if self.debug:
            print(self.points)
            print(x)
            print(y)
        Xc,Yc,Rc = self.Circle_center(x,y)
        self.canvas.create_oval(Xc-Rc, Yc-Rc, Xc+Rc, Yc+Rc, width = 4, outline =self.line_color, tags='FCC_circle')
        self.points = []
        ratio = float(self.vlist_um[self.Combo.current()])
        mes = f'Circle: Xc / Yc / Rc / Area = [ {Xc:0.1f} / {Yc:0.1f} / {Rc:0.1f} / {np.pi * Rc**2:0.2e} ] pixel [ {Xc*ratio:0.1f} / {Yc*ratio:0.1f} / {Rc*ratio:0.1f} / {np.pi * (Rc*ratio)**2:0.2e}] µm'
        self.circle_label_value.set(mes)
        if self.debug:
            print(mes)
        
    def ExitApplication(self):
        MsgBox = tk.messagebox.askquestion ('Quitting ...','Are you sure you want to quit ?',icon = 'warning')
        if MsgBox == 'yes':
            self.window.quit()     # stops mainloop
            self.window.destroy()
        else:
            tk.messagebox.showinfo('Return','Going back')
    
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    MainWindow(root)
    root.mainloop()
    


