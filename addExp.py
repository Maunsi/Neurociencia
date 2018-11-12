#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event
import random
import control
import analizador
import analizador_csv
import math
import time
import sys
from trial import Trial


def agradecimiento(ventana, nombre_imagen):
	imagen = visual.ImageStim(ventana, image=nombre_imagen)
	imagen.draw()
	ventana.flip()
	core.wait(3)

def read_input_file(modo_inputs):
	input_list = []
	if modo_inputs == "prueba":
		input_file = open("pairAndResInputs.txt", "r")
	if modo_inputs == "biblia":
		input_file = open("pairAndResInputsBIBLIA.txt", "r")
	try:
		for line in input_file:
			# rstrip() para evitar que algun \n moleste
			prime, pairString, res = line.rstrip().split(" ")
			left, right = pairString.split(",")
			trial = Trial(prime, int(left), int(right), res) #res es una string porque a veces es una latra
			input_list.append(trial)
		input_file.close()
	except UnboundLocalError as error:
		print(error)
		print("\nRecordar debes: es prueba o biblia. Escribir bien debes.\n")
		sys.exit()

	return input_list

def generar_textos_mascaras(ventana):
	# centro (fixation point en el paper)
	centro = visual.TextStim(win=ventana, text='| |', units='cm', pos=(0,0))
	mascara = visual.TextStim(win=ventana, text='MWMWMWMWMWM', units='cm', pos=(0, 0))
	mascara_post_prime = visual.TextStim(win=ventana, text='$$$$$$$$$$$', units='cm', pos=(0, 0))
	mascara_flanker_left = visual.TextStim(win=ventana, text='##', units='cm', pos=(-3.929, 0))
	mascara_flanker_right = visual.TextStim(win=ventana, text='##', units='cm', pos=(3.929, 0))

	return centro, mascara, mascara_post_prime, mascara_flanker_left, mascara_flanker_right

def draw(ventana, estimulos, frames=1):
	for frame in range(frames):
		for estimulo in estimulos:
			estimulo.draw()
		ventana.flip()

def dibujar_estimulos(ventana, text_prime, text_left, text_right, text_res, mascaras):
	#Asumo refresh rate de 60hz
	frames = [61, 5, 2, 5, 6, 2, 72] #Corresponden a tiempo*60frames/segundo

	[centro, mascara, mascara_post_prime, mascara_izquierda, mascara_derecha] = mascaras

	draw(ventana, {centro}, frames[0])

	# mostrar mascara
	draw(ventana, {mascara}, frames[1])
	
	# mostrar primer de acuerdo a lo especificado en pairAndResInputs.txt
	draw(ventana, {text_prime}, frames[2])
	
	# mostrar mascara
	draw(ventana, {mascara_post_prime}, frames[3])
		
	# mostrar mascara para los flankers junto con el centro
	draw(ventana, {centro, mascara_izquierda, mascara_derecha}, frames[4])
		
	#Mostrar pares y el centro
	draw(ventana, {centro, text_left, text_right}, frames[5])

	# mostrar mascara para los flankers y el centro
	draw(ventana, {centro, mascara_izquierda, mascara_derecha}, frames[6])

	# Mostrar resultado y mascaras para los flankers
	draw(ventana, {text_res, mascara_izquierda, mascara_derecha})

def experimento(ventana, estimulos, mascaras):
	clock = core.Clock()
	random.shuffle(estimulos)
	respuestas_por_prueba = {} #Diccionario que tiene para cada prueba sus respuestas

	for estimulo in estimulos:
		# prepara target, flankers y primers
		text_prime, text_left, text_right, text_res = estimulo.generate_stimuli(ventana)
		dibujar_estimulos(ventana, text_prime, text_left, text_right, text_res, mascaras)
		clock.reset()
		respuestas_por_prueba[estimulo] = event.waitKeys(keyList=['a', 'l'], 
												timeStamped=clock)
		ventana.flip()
	#diccionario de prueba->tupla de respuesta
	return respuestas_por_prueba

def rutina_experimentos(modo_inputs):
	ventana = visual.Window(fullscr=True, monitor="addExp", color=(0,0,0))
	ventana.flip()
	ventana.mouseVisible = False
	estimulos = read_input_file(modo_inputs)
	pruebas_y_resultados = {}
	control_subjetivo = 0
	control_objetivo_operaciones= {}
	control_objetivo_pares= {}
	consigna_experimento = visual.TextStim(win=ventana, text=u"Bienvenido al mejor experimento de Neurociencia Cognitiva.\
								\n\nINSTRUCCIONES:\
								\nLa tarea consiste en categorizar lo más rápido y preciso que pueda,\
                                si el símbolo que aparece en el centro de la pantalla es un número o una letra.\
								\n * Presione L si es una letra \
								\n * Presione A si es un número.\
                                \n\nPresione ESPACIO para comenzar.")
	centro, mascara, mascara_post_prime, mascara_izquierda, mascara_derecha = generar_textos_mascaras(ventana)
	mascaras = [centro, mascara, mascara_post_prime, mascara_izquierda, mascara_derecha]
	consigna_experimento.draw()
	ventana.flip()
	key = event.waitKeys(keyList=["space", "escape"])[0]
	if key == "space":
		pruebas_y_resultados = experimento(ventana, estimulos, mascaras)
		control_subjetivo = control.control_subjetivo(ventana)
		control_objetivo_operaciones, control_objetivo_pares = control.control_objetivo(ventana, estimulos, mascaras)
		agradecimiento(ventana, "agradecimiento.png")
		#analizador.escribir_resultados(pruebas_y_resultados, control_subjetivo, control_objetivo_operaciones, control_objetivo_pares);
		analizador_csv.escribir_resultados(pruebas_y_resultados, 
		control_subjetivo, control_objetivo_operaciones, control_objetivo_pares)
	
if __name__ == '__main__':
	try:
		rutina_experimentos(sys.argv[1])
	except IndexError as error:
		print(error)
		print("Pasarle la opción de lectura al programa debes.\
			\npython addExp.py prueba \
			\npython addExp.py biblia\n")