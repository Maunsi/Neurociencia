from psychopy import visual, core, event #import some libraries from PsychoPy
import psychopy
from psychopy import visual, core, event
import random

def bienvenida(win):
    bienvenida = visual.TextStim(win=win, text='AAAAAAAREEEE YOUUUUU REAAADYYYYY?')
    tres = visual.TextStim(win=win, text='3')
    dos = visual.TextStim(win=win, text='2')
    uno = visual.TextStim(win=win, text='1')
    
    bienvenida.draw()
    win.flip()
    core.wait(0.5)

    tres.draw()
    win.flip()
    core.wait(0.5)

    dos.draw()
    win.flip()
    core.wait(0.5)

    uno.draw()
    win.flip()
    core.wait(0.5)


def crearTextos():
    textList = []
    inputFile = open("pairAndResInputs.txt", "r")
    for line in inputFile:
        pairString, resString = line.split(" ")
        leftString, rightString = pairString.split
        textLeft = visual.TextStim(win=win, name='textLeft', text=left, units='norm', pos=(-0.5, 0))
        textRight = visual.TextStim(win=win, name='textRight', text=right, units= 'norm', pos=(0.5, 0))
        textRes =  visual.TextStim(win=win, name='textRes', text=res)
        textList.append(((textLeft, textRight), textRes))
    inputFile.close()
    return textList





#crear una ventana
win=visual.Window(fullscr=True)


textList = crearTextos()

#crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
clock = core.Clock()

bienvenida(win)

event.clearEvents()
while len(textList) != 0:  #corro mientras queden estimulos    
    #Mostrar pares
    ((textLeft, textRight), textRes) = textList.pop(0)
    textLeft.draw()
    textRight.draw()
    win.flip()
    core.wait(0.5)
    
    #Mostrar resultado
    textRes.draw()
    win.flip() 
    core.wait(0.5)

pressedKeys = event.getKeys(keyList=["space"], timeStamped=True)


with open("pressedKeys", "w") as f:
    for item in pressedKeys:
        f.write("%s\n" % str(item))
f.close()
