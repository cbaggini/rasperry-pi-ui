#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 16:29:29 2021

@author: cecilia
"""
import subprocess
import tkinter as tk

window = tk.Tk()
window.wm_attributes('-fullscreen','true')

def startfile():
    firefox = "/usr/lib/libreoffice/program/scalc"
    subprocess.Popen([firefox])

tk.Button(window, text="Open", command=startfile).pack()

tk.Button(window, text="Quit", command=window.destroy).pack()

window.mainloop()