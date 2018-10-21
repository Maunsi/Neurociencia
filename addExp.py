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
	text_prime = visual.TextStim(win=win, name='text_prime', text=prime, units='norm', pos=(0, 0))
	text_left = visual.TextStim(win=win, name='text_left', text=left, units='norm', pos=(-0.25, 0))
	text_right = visual.TextStim(win=win, name='text_right', text=right, units= 'norm', pos=(0.25, 0))
	text_res =  visual.TextStim(win=win, name='text_res', text=res, units= 'norm', pos=(0, 0))
	return textPrime, textLeft, textRight, textRes

def generate_mask_texts():
	# centro(fixation point en el paper)
	centro = visual.TextStim(win=win, name='centro', text='| |', units='norm', pos=(0,0))
	# mascara
	mascara = visual.TextStim(win=win, name='mascara', text='MWMWMWMWMWM', units='norm', pos=(0, 0))
	# mascaras para los flankers
	mascara_flanker_left = visual.TextStim(win=win, name='mascara_flanker_left', text='##', units='norm', pos=(-0.5, 0))
	mascara_flanker_right = visual.TextStim(win=win, name='mascara_flanker_right', text='##', units='norm', pos=(0.5, 0))

	return centro, mascara, mascara_flanker_left, mascara_flanker_right

################################################################################################################
<<<<<<< HEAD
def main():
	#crear una ventana
	win=visual.Window(fullscr=True)

	# caja de dialogo
	cajaDialogo = gui.Dlg()
	cajaDialogo.addField("ID: ")

	centro, mascara, mascara_flanker_left, mascara_flanker_right = generate_mask_texts()    

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
		text_prime, text_left, text_right, text_res = generate_texts(prime, left, right, res)
		
		# mostrar el centro
		draw(win, {centro}, 1)
		
		# mostrar mascara    
		draw(win, {mascara}, 1)
		
		# mostrar primer de acuerdo a lo especificado en pairAndResInputs.txt
		draw(win, {text_prime}, 1)
		
		# mostrar mascara
		draw(win, {mascara}, 1)
		
		# mostrar mascara para los flankers junto con el centro
		draw(win, {centro, mascara_flanker_left, mascara_flanker_right}, 1)
		
		#Mostrar pares y el centro
		draw(win, {centro, text_left, text_right}, 1)
		
		# mostrar mascara para los flankers y el centro
		draw(win, {centro, mascaraF_fanker_left, mascara_flanker_right}, 1)
		
		#Mostrar resultado y mascaras para los flankers
		draw(win, {text_res, mascara_flanker_left, mascara_flanker_right}, 1)
		
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
			s = "{} {} {} {} {} {} {}".format(i, prime, left, right, res, response)
			f.write("%s\n" % s)
	f.close()


if __name__ == '__main__':
	main()
