from psychopy import visual, core, event #import some libraries from PsychoPy
import psychopy
from psychopy import visual, core, event
import random

#crear una ventana
win=visual.Window(fullscr=True)

listStimuli = []
for i in range(5):
    left = random.randint(1,5)
    right = random.randint(1,5)
    s = str(left) + "             " + str(right)
    text = visual.TextStim(win=win, name='text', text=s, font=u'Arial', pos=(0, 0), 
    height=0.1, wrapWidth=None, ori=0, color=u'white', colorSpace='rgb', opacity=1,depth=0.0);
    listStimuli.append(text)


#crear un estimulo visual (numero)

#img = visual.Circle(win=win,units="pix",radius=150,fillColor=[-1, -1, -1],lineColor=[-1, -1, -1],edges=128)

#crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
clock = core.Clock()

event.clearEvents()
while clock.getTime() < 5.0:  # correr el script hasta que el clock marque los 5 segundos 
    listStimuli.pop(0).draw()
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