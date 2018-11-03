from psychopy import visual, core, event
import random
import control
import analizador
from trial import Trial

def agradecimiento(ventana, nombre_imagen):
	imagen = visual.ImageStim(ventana, image=nombre_imagen)
	imagen.draw()
	ventana.flip()
	core.wait(3)

def read_input_file():
	input_list = []
	input_file = open("pairAndResInputs.txt", "r")
	for line in input_file:
		# rstrip() para evitar que algun \n moleste
		prime, pairString, res = line.rstrip().split(" ")
		left, right = pairString.split(",")
		trial = Trial(prime, int(left), int(right), res) #res es una string porque a veces es una latra
		input_list.append(trial)
	input_file.close()
	return input_list

def generar_textos_mascaras(ventana):
    # centro (fixation point en el paper)
    centro = visual.TextStim(win=ventana, name='centro', text='| |', units='cm', pos=(0,0))
    mascara = visual.TextStim(win=ventana, name='mascara', text='MWMWMWMWMWM', units='cm', pos=(0, 0))
    mascara_post_prime = visual.TextStim(win=ventana, name='mascara', text='$$$$$$$$$$$', units='cm', pos=(0, 0))
    mascara_flanker_left = visual.TextStim(win=ventana, name='mascara_flanker_left', text='##', units='cm', pos=(-3.929, 0))
    mascara_flanker_right = visual.TextStim(win=ventana, name='mascara_flanker_right', text='##', units='cm', pos=(3.929, 0))

    return centro, mascara, mascara_post_prime, mascara_flanker_left, mascara_flanker_right


def draw(ventana, estimulos, time=0):
	for estimulo in estimulos:
		estimulo.draw()
	ventana.flip()
	core.wait(time)


def dibujar_estimulos(ventana, text_prime, text_left, text_right, text_res, mascaras):
    tiempos = [1, 0.08, 0.03, 0.08, 0.1, 0.03, 1.2]

    centro = mascaras[0]
    mascara = mascaras[1]
    mascara_post_prime = mascaras[2]
    mascara_izquierda = mascaras[3]
    mascara_derecha = mascaras[4]

    draw(ventana, {centro}, tiempos[0])

	# mostrar mascara
    draw(ventana, {mascara}, tiempos[1])
	
    # mostrar primer de acuerdo a lo especificado en pairAndResInputs.txt
    draw(ventana, {text_prime}, tiempos[2])
	
    # mostrar mascara
    draw(ventana, {mascara_post_prime}, tiempos[3])
		
	# mostrar mascara para los flankers junto con el centro
    draw(ventana, {centro, mascara_izquierda, mascara_derecha}, tiempos[4])
		
	#Mostrar pares y el centro
    draw(ventana, {centro, text_left, text_right}, tiempos[5])

	# mostrar mascara para los flankers y el centro
    draw(ventana, {centro, mascara_izquierda, mascara_derecha}, tiempos[6])

	# Mostrar resultado y mascaras para los flankers
    draw(ventana, {text_res, mascara_izquierda, mascara_derecha})

#Para el control objetivo deberiamos refactorizar esta funcion y reutilizarla
def experimento(ventana, estimulos, mascaras):
	random.shuffle(estimulos)

	respuestas_por_prueba = {} #Diccionario que tiene para cada prueba sus respuestas

	for estimulo in estimulos:
		# prepara target, flankers y primers
		text_prime, text_left, text_right, text_res = estimulo.generate_stimuli(ventana)
		dibujar_estimulos(ventana, text_prime, text_left, text_right, text_res, mascaras)
		respuestas_por_prueba[estimulo] = event.waitKeys(maxWait=2, keyList=['a', 'l'], timeStamped=True)

	return respuestas_por_prueba


def rutina_experimentos():
	ventana = visual.Window(fullscr=True, monitor='addExp')
	estimulos = read_input_file()
	pruebas_y_resultados_por_sujeto = {}
	control_subjetivo_por_sujeto = {}
	control_objetivo_operaciones_por_sujeto = {}
	control_objetivo_pares_por_sujeto = {}
	consigna_experimento = visual.TextStim(win=ventana, text="Bienvenido al mejor experimento de Neurociencia Cognitiva.\
										  Presione ESPACIO para comenzar o ESC para cancelar.\n \
										  Instrucciones:\
                                          \n La tarea consiste en categorizar lo mas rapido y preciso que pueda, si el simbolo que aparece en el centro de la pantalla es un numero o una letra\
										  Presione L si es una letra \
										  \nPresione A si es un numero.")
	centro, mascara, mascara_post_prime, mascara_izquierda, mascara_derecha = generar_textos_mascaras(ventana)
	mascaras = [centro, mascara, mascara_post_prime, mascara_izquierda, mascara_derecha]
	sujeto = 0
	while True:
		consigna_experimento.draw()
		ventana.flip()
		key = event.waitKeys(keyList=["space", "escape"])[0]
		if key == "space":
			pruebas_y_resultados_por_sujeto[sujeto] = experimento(ventana, estimulos, mascaras)
			control_subjetivo_por_sujeto[sujeto] = control.control_subjetivo(ventana)
			control_objetivo_operaciones, control_objetivo_pares = control.control_objetivo(ventana, estimulos, mascaras)
			control_objetivo_operaciones_por_sujeto[sujeto] = control_objetivo_operaciones
			control_objetivo_pares_por_sujeto = control_objetivo_pares
			agradecimiento(ventana, "agradecimiento.png")
			sujeto += 1
		elif key == "escape":
			break
	analizador.analizar(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, 
		control_objetivo_pares_por_sujeto);

if __name__ == '__main__':
	rutina_experimentos()
