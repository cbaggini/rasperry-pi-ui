import subprocess
import tkinter as tk
import cv2

## main window ##########################################
window = tk.Tk()
window.wm_attributes('-fullscreen','true')
window.geometry('2x2')

window.columnconfigure(0, weight=3)
window.columnconfigure(1, weight=1)


# style
bg_image = tk.PhotoImage(file='imgs/main_bg.gif')
window_bg = tk.Label(window, image = bg_image) 
window_bg.place(x = 0, y = 0, relwidth = 1, relheight = 1) 
window_bg.configure(bg='black')



## App launcher functions ##############################
# Navit
def startfile():
    app = "/usr/bin/navit"
    subprocess.Popen([app])
    
# Reverse camera
def run():
    # -fs -> fullscreen
    # tv: -> source path
    #subprocess.run(["mplayer", "-fs", "tv:///dev/video0"])
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    

## Buttons ############################################
# Quit
img_quit = tk.PhotoImage(file='imgs/quit-icon.gif')
#lab_quit = tk.Label(image=img_quit)
btn_quit = tk.Button(window, command=window.destroy, image = img_quit, borderwidth=0, highlightbackground='black', highlightthickness=0)
btn_quit.grid(row=0, column=0)
#btn_quit.pack()
#lab_quit.pack(pady=20)

#Navit
img_navit = tk.PhotoImage(file='imgs/location-icon.gif')
btn_navit = tk.Button(window, command=startfile, image = img_navit, highlightbackground='black', highlightthickness=0)

btn_navit.grid(row=0, column=1)
#btn_navit.pack()

# Reverse camera
img_camera = tk.PhotoImage(file='imgs/camera-icon.gif')
btn_camera = tk.Button(window, command=run, image = img_camera, highlightbackground='black', highlightthickness=0)

btn_camera.grid(row=0, column=2)
#btn_camera.pack()


window.mainloop() 