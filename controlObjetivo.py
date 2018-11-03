import random
from psychopy import visual, core, event
from trial import Trial


#Yo descartaria este modulo
def draw(ventana, stimuli, time):
    for stimulus in stimuli:
        stimulus.draw()
    ventana.flip()
    core.wait(time)

def read_input_file():
    input_list = []
    input_file = open("pairAndResInputs.txt", "r")
    for line in input_file:
        prime, pairString, res = line.rstrip().split(" ")
        left, right = pairString.split(",")
        trial = Trial(prime, int(left), int(right), res) 
        input_list.append(trial)
    input_file.close()

    return input_list

def generate_mask_texts(ventana):
    centro = visual.TextStim(win=ventana, name='centro', text='| |', units='norm', pos=(0,0))
    mascara = visual.TextStim(win=ventana, name='mascara', text='MWMWMWMWMWM', units='norm', pos=(0, 0))
    mascara_flanker_left = visual.TextStim(win=ventana, name='mascara_flanker_left', text='##', units='norm', pos=(-0.25, 0))
    mascara_flanker_right = visual.TextStim(win=ventana, name='mascara_flanker_right', text='##', units='norm', pos=(0.25, 0))

    return centro, mascara, mascara_flanker_left, mascara_flanker_right

def dibujar_stimuli(ventana, text_prime, text_left, text_right, text_res, centro, mascara, mascara_flanker_left,
	mascara_flanker_right):
	tiempos = [1, 0.08, 0.03, 0.08, 0.1, 0.03, 1.2, 0]

	# mostrar el centro
	draw(ventana, {centro}, tiempos[0])
	        
	# mostrar mascara    
	draw(ventana, {mascara}, tiempos[1])
	        
	# mostrar primer de acuerdo a lo especificado en pairAndResInputs.txt
	draw(ventana, {text_prime}, tiempos[2])
	        
	# mostrar mascara
	draw(ventana, {mascara}, tiempos[3])
	        
	# mostrar mascara para los flankers junto con el centro
	draw(ventana, {centro, mascara_flanker_left, mascara_flanker_right}, tiempos[4])
	        
	#Mostrar pares y el centro
	draw(ventana, {centro, text_left, text_right}, tiempos[5])

	# mostrar mascara para los flankers y el centro
	draw(ventana, {centro, mascara_flanker_left, mascara_flanker_right}, tiempos[6])

	# Mostrar resultado y mascaras para los flankers
	draw(ventana, {text_res, mascara_flanker_left, mascara_flanker_right}, tiempos[7])

def experiment(ventana, input_list):
    centro, mascara, mascara_flanker_left, mascara_flanker_right = generate_mask_texts(ventana)    
    trial_responses = {}
 
    while len(input_list) != 0:  
        trial = input_list.pop(0)
        text_prime, text_left, text_right, text_res = trial.generate_stimuli(ventana)
        dibujar_stimuli(ventana, text_prime, text_left, text_right, text_res, centro, mascara, mascara_flanker_left,
                        mascara_flanker_right)
        trial_responses[trial] = event.waitKeys(maxWait=2, keyList=['a', 'l'], timeStamped=True)

    return trial_responses

def control_objetivo(ventana):
	input_list = read_input_file()
	random.shuffle(input_list)
	consigna_primera_mitad_texto = "Por favor, querido ser celestial nacido de la bondad misma:\
							  		\nidentifique si en los siguientes trials aparecen las palabras\
							  		SUMAR o REPRESENTAR. \
							  		\nInstrucciones:\
							  		\n\tApretar L si la palabra es SUMAR.\
							  		\n\tApretar A si la palabra es REPRESENTAR.\
							  		\nSi no sabe, mienta y si miente sepa que es peor que Menem.\
							  		\n\nPresione ESPACIO para comenzar. "
	consigna = visual.TextStim(win=ventana, text=consigna_primera_mitad_texto)
	consigna.draw()
	ventana.flip()
	event.waitKeys(keyList=["space"])

	mitad = len(input_list) // 2
	respuestas_primera_mitad = experiment(ventana, input_list[:mitad])

	consigna_segunda_mitad_texto = "Querida persona, buena como el agua mineral, le pedimos ahora que indique\
							  		si el flanker izquierdo es par o impar. Si falla, no vuelve a subir a la\
							  		calesita.\
							  		\nInstrucciones:\
							  		\n\tApretar L si el flanker es PAR.\
							  		\n\tApretar A si el flanker es IMPAR.\
							  		\n\nPresione ESPACIO para comenzar."
	consigna = visual.TextStim(win=ventana, text=consigna_primera_mitad_texto)
	consigna.draw()
	ventana.flip()
	event.waitKeys(keyList=["space"])
	respuestas_segunda_mitad = experiment(ventana, input_list[mitad:])

	# como combino dos diccionarios sin que se pisoteen? Como hago las cosas bien?
	# como vivir de forma excelente? como subir las escaleras sin agotarme?
	return None

if __name__ == "__main__":
	ventana = visual.Window(fullscr=True)
	control_objetivo(ventana)