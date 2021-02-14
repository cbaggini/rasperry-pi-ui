#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 16:29:29 2021

@author: cecilia
"""
import os
import tkinter as tk

window = tk.Tk()
window.wm_attributes('-fullscreen','true')

firefox = "/usr/lib/libreoffice/program/./scalc"

tk.Button(window, text="Open", command=os.open(firefox,  os.O_RDONLY)).pack()

tk.Button(window, text="Quit", command=window.destroy).pack()

window.mainloop()