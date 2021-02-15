import subprocess
import tkinter as tk
window = tk.Tk()
window.wm_attributes('-fullscreen','true')

def startfile():
    app = "/usr/bin/navit"
    subprocess.Popen([app])
    
def run():
    # -fs -> fullscreen
    # tv: -> source path
    subprocess.run(["mplayer", "-fs", "tv:///dev/video0"])
    
        
#def starvideo():
#    rcam = "/usr/mplayer tv:///dev/video0"
#    subprocess.Popen([rcam])
        
#tk.Button(window, text="Open App", command=startfile).pack()
tk.Button(window, text="video", command=run).pack()
#tk.Button(window, text="Open Video", command=startvideo).pack()
tk.Button(window, text="Quit", command=window.destroy).pack()

window.mainloop() 