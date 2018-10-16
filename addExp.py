from psychopy import visual, core, event #import some libraries from PsychoPy
import random

def bienvenida(win):
    bienvenida = visual.TextStim(win=win, text='AAAAAAAREEEE YOUUUUU REAAADYYYYY?')
    tres = visual.TextStim(win=win, text='3')
    dos = visual.TextStim(win=win, text='2')
    uno = visual.TextStim(win=win, text='1')
    
    draw(win, {bienvenida}, 1)

    draw(win, {tres}, 1)

    draw(win, {dos}, 1)

    draw(win, {uno}, 1)


def draw(win, stimuli, time):
	for stimulus in stimuli:
		stimulus.draw()
	win.flip()
	core.wait(time)

def crearTextos():
    textList = []
    inputFile = open("pairAndResInputs.txt", "r")
    for line in inputFile:
        pairString, resString = line.split(" ")
        leftString, rightString = pairString.split(",")
        textLeft = visual.TextStim(win=win, name='textLeft', text=leftString, units='norm', pos=(-0.5, 0))
        textRight = visual.TextStim(win=win, name='textRight', text=rightString, units= 'norm', pos=(0.5, 0))
        textRes =  visual.TextStim(win=win, name='textRes', text=resString, units= 'norm', pos=(0, 0))
        textList.append(((textLeft, textRight), textRes))
    inputFile.close()
    return textList

################################################################################################################
#crear una ventana
win=visual.Window(fullscr=True)

# centro(fixation point en el paper)
centro = visual.TextStim(win=win, name='centro', text='| |', units='norm', pos=(0,0))

# mascara
mascara = visual.TextStim(win=win, name='mascara', text='MWMWMWMWMWM', units='norm', pos=(0, 0))

# primers
primerSumar = visual.TextStim(win=win, name='sumar', text='SUMAR', units='norm', pos=(0, 0))
primerRepresentar = visual.TextStim(win=win, name='REPRESENTAR', units='norm', pos=(0, 0))

# mascaras para los flankers
mascaraFlankerLeft = visual.TextStim(win=win, name='mascaraFlankerLeft', text='##', units='norm', pos=(-0.5, 0))
mascaraFlankerRight = visual.TextStim(win=win, name='mascaraFlankerRight', text='##', units='norm', pos=(0.5, 0))


textList= crearTextos()

#crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
clock = core.Clock()

bienvenida(win)

#idea para obtener teclas: hago clear antes de res, y hago getKeys despues de res
event.clearEvents()
pressedKeys = []
while len(textList) != 0:  #corro mientras queden estimulos

    # mostrar el centro
    draw(win, {centro}, 1)
    
    # mostrar mascara    
    draw(win, {mascara}, 1)
    
    # mostrar primer. Por ahora solo muestra 'sumar'.
    draw(win, {primerSumar}, 1)
    
    # mostrar mascara
    draw(win, {mascara}, 1)
    
    # mostrar mascara para los flankers junto con el centro
    draw(win, {centro, mascaraFlankerLeft, mascaraFlankerRight}, 1)
    
    #Mostrar pares y el centro
    ((textLeft, textRight), textRes) = textList.pop(0)
    draw(win, {centro, textLeft, textRight}, 1)
    
    # mostrar mascara para los flankers y el centro
    draw(win, {centro, mascaraFlankerLeft, mascaraFlankerRight}, 1)
    
    #Mostrar resultado y mascaras para los flankers
    draw(win, {textRes, mascaraFlankerLeft, mascaraFlankerRight}, 1)
    
    # prueba: igual que getKeys pero espera el tiempo indicado por maxWait, tal vez sirve para 
    # cortar la prueba en caso de demora o respuesta correcta.
    pressedKeys.append(event.waitKeys(maxWait=1, keyList=["left", "right"], timeStamped=True))
    #pressedKeys.append(event.getKeys(keyList=["left", "right"], timeStamped=True))

with open("pressedKeys", "w") as f:
    for item in pressedKeys:
        f.write("%s\n" % str(item))
f.close()
