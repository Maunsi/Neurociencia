from psychopy import visual, core, event#, gui
import random

class Trial():

	def __init__(self, prime, left, right, res):
		self.prime = prime
		self.left = left
		self.right = right
		self.res = res
		
	def generate_stimuli(self, win):
		text_prime = visual.TextStim(win=win, name='text_prime', text=self.prime, units='norm', pos=(0, 0))
		text_left = visual.TextStim(win=win, name='text_left', text=str(self.left), units='norm', pos=(-0.25, 0))
		text_right = visual.TextStim(win=win, name='text_right', text=str(self.right), units= 'norm', pos=(0.25, 0))
		text_res = visual.TextStim(win=win, name='text_res', text=self.res, units= 'norm', pos=(0, 0))
		return text_prime, text_left, text_right, text_res
		
	def __eq__(self, other):
    """Overrides the default implementation"""
		return self.prime == other.prime and self.left == other.left and self.right == other.right and self.res == other.res
	
	def __ne__(self, other):
    """Overrides the default implementation (unnecessary in Python 3)"""
		return not self.__eq__(other)

# def bienvenida(win):
	# bienvenida = visual.TextStim(win=win, text='AAAAAAAREEEE YOUUUUU REAAADYYYYY?')
	# tres = visual.TextStim(win=win, text='3')
	# dos = visual.TextStim(win=win, text='2')
	# uno = visual.TextStim(win=win, text='1')
	
	# draw(win, {bienvenida}, 1)

	# draw(win, {tres}, 1)

	# draw(win, {dos}, 1)

	# draw(win, {uno}, 1)


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
		trial = Trial(int(trial_id), prime, int(left), int(right), res) #res es una string porque a veces es una latra
		input_list.append(trial)
	input_file.close()
	return input_list
	

def generate_mask_texts(win):
	# centro (fixation point en el paper)
	centro = visual.TextStim(win=win, name='centro', text='| |', units='norm', pos=(0,0))
	mascara = visual.TextStim(win=win, name='mascara', text='MWMWMWMWMWM', units='norm', pos=(0, 0))
	mascara_flanker_left = visual.TextStim(win=win, name='mascara_flanker_left', text='##', units='norm', pos=(-0.25, 0))
	mascara_flanker_right = visual.TextStim(win=win, name='mascara_flanker_right', text='##', units='norm', pos=(0.25, 0))
	return centro, mascara, mascara_flanker_left, mascara_flanker_right

def experiment(win):
	#crear una ventana

	# caja de dialogo
	#cajaDialogo = gui.Dlg()
	#cajaDialogo.addField("ID: ")

	#La idea es que tengamos variables de tiempo para las distintas mascaras
	tiempos = [1, 0.08, 0.03, 0.08, 0.1, 0.03, 1.2, 2]

	centro, mascara, mascara_flanker_left, mascara_flanker_right = generate_mask_texts(win)    

	#crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
	clock = core.Clock()

	bienvenida(win)

	# muestra caja de dialogo. Respuestas en gui.data[i]
	#cajaDialogo.show()

	#idea para obtener teclas: hago clear antes de res, y hago getKeys despues de res
	event.clearEvents()
	pressedKeys = []

	input_list = read_input_file()
	random.shuffle(input_list)
	n = len(input_list)
	trial_by_id = {}
	trial_responses_by_id = {}

	while len(input_list) != 0:  #corro mientras queden estimulos
		trial = input_list.pop(0)
		# prepara target, flankers y primers
		text_prime, text_left, text_right, text_res = trial.generate_stimuli(win)
		
		# mostrar el centro
		draw(win, {centro}, tiempos[0])
		
		# mostrar mascara    
		draw(win, {mascara}, tiempos[1])
		
		# mostrar primer de acuerdo a lo especificado en pairAndResInputs.txt
		draw(win, {text_prime}, tiempos[2])
		
		# mostrar mascara
		draw(win, {mascara}, tiempos[3])
		
		# mostrar mascara para los flankers junto con el centro
		draw(win, {centro, mascara_flanker_left, mascara_flanker_right}, tiempos[4])
		
		#Mostrar pares y el centro
		draw(win, {centro, text_left, text_right}, tiempos[5])
		
		# mostrar mascara para los flankers y el centro
		draw(win, {centro, mascara_flanker_left, mascara_flanker_right}, tiempos[6])
		
		# Mostrar resultado y mascaras para los flankers
		draw(win, {text_res, mascara_flanker_left, mascara_flanker_right}, tiempos[7])
		
		# prueba: igual que getKeys pero espera el tiempo indicado por maxWait, tal vez sirve para 
		# cortar la prueba en caso de demora o respuesta correcta.
				
		trial_responses[trial] = event.waitKeys(maxWait=tiempos[7], keyList=["left", "right"], timeStamped=True)[0]
	
	return trial_responses
	


def metrics(trials_by_subject):
	#Cada elemento de la lista tiene un diccionario de trial -> response
	#Este for es para que no quede vacio el metodo, aca deberiamos hacer todas las cuentillas
	for trials in trials_by_subject
		print trials
	

	# #No hace falta tener un separador, ya sabemos cuanto mide cada experimento (n trials)
	# with open("results.txt", "a") as f:
		# for i in range(n):
			# (prime, left, right, res) = trial_by_id[i]
			# response = trial_responses_by_id[i]
			# s = "{} {} {},{} {} {} ".format(i, prime, left, right, res, response)
			# f.write("%s\n" % s)
		# f.write("*\n")
	# f.close()


if __name__ == '__main__':
	trials_by_subject = []
	while True:
		win = visual.Window(fullscr=True)
		inicio = visual.TextStim(win=win, text='Bienvenido al mejor experimento de Neurociencia Cognitiva. Presione espacio para comenzar o esc para cancelar. Left -> Letra, Right -> Numero')
		inicio.draw()
		win.flip()
		key = event.waitKeys(keyList=["space", "escape"])
		if key[0] == "space":
			trials_by_subject.append(experiment(win))
		elif key[0] == "escape":
			break
	metrics(trials_by_subject)
		