from psychopy import visual, core, event, gui
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

def read_input_file():
	input_list = []
	input_file = open("pairAndResInputs.txt", "r")
	for line in input_file:
		# rstrip() para evitar que algun \n moleste
		trial_id, prime, pairString, res = line.rstrip().split(" ")
		left, right = pairString.split(",")
		input_list.append((int(trial_id), prime, left, right, res))
	input_file.close()
	return input_list
	
def generate_texts(prime, left, right, res):
	textPrime = visual.TextStim(win=win, name='textPrime', text=prime, units='norm', pos=(0, 0))
	textLeft = visual.TextStim(win=win, name='textLeft', text=left, units='norm', pos=(-0.5, 0))
	textRight = visual.TextStim(win=win, name='textRight', text=right, units= 'norm', pos=(0.5, 0))
	textRes =  visual.TextStim(win=win, name='textRes', text=res, units= 'norm', pos=(0, 0))
	return textPrime, textLeft, textRight, textRes

################################################################################################################

#crear una ventana
win=visual.Window(fullscr=True)

# caja de dialogo
cajaDialogo = gui.Dlg()
cajaDialogo.addField("ID: ")

# centro(fixation point en el paper)
centro = visual.TextStim(win=win, name='centro', text='| |', units='norm', pos=(0,0))

# mascara
mascara = visual.TextStim(win=win, name='mascara', text='MWMWMWMWMWM', units='norm', pos=(0, 0))

# mascaras para los flankers
mascaraFlankerLeft = visual.TextStim(win=win, name='mascaraFlankerLeft', text='##', units='norm', pos=(-0.5, 0))
mascaraFlankerRight = visual.TextStim(win=win, name='mascaraFlankerRight', text='##', units='norm', pos=(0.5, 0))

#crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
clock = core.Clock()

bienvenida(win)

# muestra caja de dialogo. Respuestas en gui.data[i]
cajaDialogo.show()

#idea para obtener teclas: hago clear antes de res, y hago getKeys despues de res
event.clearEvents()
pressedKeys = []

input_list = read_input_file()
random.shuffle(input_list)
n = len(input_list)
trial_by_id = {}
trial_responses_by_id = {}
while len(input_list) != 0:  #corro mientras queden estimulos
	trial_id, prime, left, right, res = input_list.pop(0)
    # prepara target, flankers y primers
	textPrime, textLeft, textRight, textRes = generate_texts(prime, left, right, res)
    
    # mostrar el centro
	draw(win, {centro}, 1)
    
    # mostrar mascara    
	draw(win, {mascara}, 1)
    
    # mostrar primer de acuerdo a lo especificado en pairAndResInputs.txt
	draw(win, {textPrime}, 1)
    
    # mostrar mascara
	draw(win, {mascara}, 1)
    
    # mostrar mascara para los flankers junto con el centro
	draw(win, {centro, mascaraFlankerLeft, mascaraFlankerRight}, 1)
    
    #Mostrar pares y el centro
	draw(win, {centro, textLeft, textRight}, 1)
    
    # mostrar mascara para los flankers y el centro
	draw(win, {centro, mascaraFlankerLeft, mascaraFlankerRight}, 1)
    
    #Mostrar resultado y mascaras para los flankers
	draw(win, {textRes, mascaraFlankerLeft, mascaraFlankerRight}, 1)
    
    # prueba: igual que getKeys pero espera el tiempo indicado por maxWait, tal vez sirve para 
    # cortar la prueba en caso de demora o respuesta correcta.
	
	trial_by_id[trial_id] = (prime, left, right, res)
	keys = []
	keys.append(event.waitKeys(maxWait=2, keyList=["left", "right"], timeStamped=True))
	trial_responses_by_id[trial_id] = keys

with open("results.txt", "w") as f:
	for i in range(n):
		(prime, left, right, res) = trial_by_id[i]
		response = trial_responses_by_id[i]
		f.write("%s\n" % str(i) + " " + prime + " " + left + " " + right + " " + res + " " + str(response) )
f.close()
