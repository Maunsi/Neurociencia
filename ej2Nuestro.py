from psychopy import visual, core, event #import some libraries from PsychoPy
import psychopy
from psychopy import visual, core

#crear una ventana
win=visual.Window(fullscr=True)

#crear un estimulo visual (circulo)
img = psychopy.visual.Circle(win=win,units="pix",radius=150,fillColor=[-1, -1, -1],lineColor=[-1, -1, -1],edges=128)

#crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
clock = core.Clock()

event.clearEvents()
while clock.getTime() < 5.0:  # correr el script hasta que el clock marque los 5 segundos 
    img.draw()
    win.flip()
    core.wait(0.5)
    win.flip() 
    core.wait(0.5)

list = event.getKeys(keyList=["space"], timeStamped=True)

#file = open("ej1.txt","a")
#file.write(list)
#file.close()
with open('ej2.txt', 'a') as f:
    for item in list:
        f.write("%s\n" % str(item))

print(list)