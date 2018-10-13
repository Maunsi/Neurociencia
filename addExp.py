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
    
#crear una ventana
win=visual.Window(fullscr=True)

# mascara
mascara = visual.TextStim(win=win, name='mascara', text='MWMWMWMWMWM', units='norm', pos=(0, 0))

# primers
primerSumar = visual.TextStim(win=win, name='sumar', text='SUMAR', units='norm', pos=(0, 0))
primerRepresentar = visual.TextStim(win=win, name='REPRESENTAR', units='norm', pos=(0, 0))

# mascaras para los flankers
mascaraFlankerLeft = visual.TextStim(win=win, name='mascaraFlankerLeft', text='##', units='norm', pos=(-0.5, 0))
mascaraFlankerRight = visual.TextStim(win=win, name='mascaraFlankerRight', text='##', units='norm', pos=(0.5, 0))

listPairs = []

#Estamos asumiendo que el primer par corresponde al primer res, etc etc. Rechequear eso
pairFile = open("pairInputs.txt", "r")
for line in pairFile:
    left, right = line.split(",")
    textLeft = visual.TextStim(win=win, name='textLeft', text=left, units='norm', pos=(-0.5, 0))
    textRight = visual.TextStim(win=win, name='textRight', text=right, units='norm', pos=(0.5, 0))
    
    listPairs.append(textLeft)
    listPairs.append(textRight)
pairFile.close()


resFile = open("resInputs.txt", "r")
listRes = []
for line in resFile:
    text = visual.TextStim(win=win, name='res', text=line)
    
    listRes.append(text)
resFile.close()
#crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
clock = core.Clock()

bienvenida(win)

event.clearEvents()
while len(listPairs) != 0:  #corro mientras queden estimulos
    
    # mostrar mascara
    mascara.draw()
    win.flip()
    core.wait(1)
    
    # mostrar primer. Por ahora solo muestra 'sumar'.
    primerSumar.draw()
    win.flip()
    core.wait(1)
    
    # mostrar mascara
    mascara.draw()
    win.flip()
    core.wait(1)
    
    # mostrar mascara para los flankers
    mascaraFlankerLeft.draw()
    mascaraFlankerRight.draw()
    win.flip()
    core.wait(1)
    
    #Mostrar pares
    listPairs.pop(0).draw()
    listPairs.pop(0).draw()
    win.flip()
    core.wait(0.5)
    
    # mostrar mascara para los flankers
    mascaraFlankerLeft.draw()
    mascaraFlankerRight.draw()
    core.wait(1)
    win.flip()
    
    #Mostrar resultado
    listRes.pop(0).draw()
    win.flip() 
    core.wait(0.5)
    

list = event.getKeys(keyList=["space"], timeStamped=True)

#file = open("ej1.txt","a")
#file.write(list)
#file.close()
with open('addExp.txt', 'a') as f:
    for item in list:
        f.write("%s\n" % str(item))

print(list)