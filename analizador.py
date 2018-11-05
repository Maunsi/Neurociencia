from trial import Trial
from scipy import stats

def analizar(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto):
	#Como primer paso por las dudas guardamos los resultados en un archivo
	escribir_resultados(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto)
	pruebas_y_resultados_por_sujeto = filtrar_mayores_a_cuatro(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto)
	pruebas_y_resultados_por_sujeto = filtrar_pruebas_letra(pruebas_y_resultados_por_sujeto)
	analisis_control_objetivo(control_objetivo_pares_por_sujeto, control_objetivo_operaciones_por_sujeto)
	pass


def escribir_resultados(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto):
	with open('resultados.txt', 'w') as file:
		#Asumo que todos los sujetos son los mismos en todos los diccionarios y que estan presentes en todos
		for sujeto in pruebas_y_resultados_por_sujeto:
			file.write("Sujeto {}\n".format(sujeto))
			file.write("Resultados: \n")
			pruebas_y_resultados = pruebas_y_resultados_por_sujeto[sujeto]
			escribir_diccionario(file, pruebas_y_resultados, 'letra', 'numero')
			file.write("Resultados control objetivo operaciones: \n")
			control_objetivo_operaciones = control_objetivo_operaciones_por_sujeto[sujeto]
			escribir_diccionario(file, control_objetivo_operaciones, 'sumar', 'representar')
			file.write("Resultados control objetivo pares: \n")
			control_objetivo_pares = control_objetivo_pares_por_sujeto[sujeto]
			escribir_diccionario(file, control_objetivo_pares, 'par', 'impar')
			file.write("Resultados control subjetivo: \n")
			file.write("{}".format(control_subjetivo_por_sujeto[sujeto]))
		file.close()



		# #Primero escribo pruebas_y_resultados_por_sujeto
		# file.write('Resultados del experimento:\n')
		# escribir_diccionario(file, pruebas_y_resultados_por_sujeto, 'letra', 'numero')
		# file.write('Resultados del control subjetivo:\n')
		# for sujeto, control_subjetivo in control_subjetivo_por_sujeto.iteritems():
		# 	s = "Sujeto: {}, respuesta control subjetivo: {}\n".format(sujeto, control_subjetivo)
		# 	file.write(s)
		# file.write('Resultados del control objetivo de operaciones\n')
		# escribir_diccionario(file, control_objetivo_operaciones_por_sujeto, 'sumar', 'representar')
		# file.write('Resultados del control objetivo de pares\n')
		# escribir_diccionario(file, control_objetivo_pares_por_sujeto, 'par', 'impar')
		# file.close()

def escribir_diccionario(file, diccionario, significado_l, significado_a):
	for prueba, resultados in diccionario.iteritems():
		#Aprovecho y transformo las teclas a la respuesta correspondiente
		if resultados is None:
			s = "Trial: {}. No hubo respuesta\n".format(prueba)
			file.write(s)
		else:
			(tecla, timestamp) = resultados[0]
			significado_tecla = significado_l if tecla == 'l' else significado_a
			s = "Trial: {}, respuesta: {}, timestamp: {}\n".format(prueba, significado_tecla, timestamp)
			file.write(s)

def filtrar_pruebas_letra(pruebas_y_resultados_por_sujeto):
	sin_letras = {}
	for subject, trials in pruebas_y_resultados_por_sujeto.iteritems():
		sin_letras[subject] = {}
		for trial, responses in trials.iteritems():
			if not trial.is_letter_trial():
				sin_letras[subject][trial] = responses

	return pruebas_y_resultados_por_sujeto

def filtrar_mayores_a_cuatro(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto):
	amount_dropped = 0
	total = 0
	for subject, control in control_subjetivo_por_sujeto.iteritems():
		if int(control) >= 4:
			pruebas_y_resultados_por_sujeto.pop(subject)
			amount_dropped += 1
		else:
			total += int(control)

	mean = total/len(control_subjetivo_por_sujeto.values())

	print "Cantidad de sujetxs desechados: {}".format(amount_dropped)
	print "Promedio de visibilidad entre los sujetxs restantes: {}".format(mean)

	return pruebas_y_resultados_por_sujeto

def analisis_control_objetivo(control_objetivo_pares_por_sujeto, control_objetivo_operaciones_por_sujeto):
	# L = SUMAR, A = REPRESENTAR.
	d_primas = []
	for sujeto, respuestas_por_prueba in control_objetivo_operaciones_por_sujeto.iteritems():
		hits = 0
		falsas_alarmas = 0
		misses = 0
		correct_rejections = 0
		for prueba, respuestas in respuestas_por_prueba.iteritems():
			if respuestas is not None:
				#respuestas es siempre una lista de un elemento
				(tecla, timestamp) = respuestas[0]
				if prueba.is_sum_trial() and tecla == 'l': # Si la prueba fue sumar y respondi sumar es un hit
					hits += 1
				elif prueba.is_sum_trial() and tecla == 'a': # Si la prueba fue sumar y respondi representar es un miss
					misses +=1
				elif prueba.is_rep_trial() and tecla == 'l': # Si la prueba fue representar y respondi sumar es una falsa alarma
					falsas_alarmas +=1
				elif prueba.is_rep_trial() and tecla == 'a': # Si la prueba fue representar y respondi representar es una correct rejection
					correct_rejections +=1


	# 	probabilidad_hit = hits/(hits + misses) #hits dividido todos los trials que tuvieron como prime sumar
	# 	probabilidad_falsa_alarma =  falsas_alarmas/(falsas_alarmas + correct_rejections) 
	# 	#falsas alarmas dividido todos los trials que tuvieron como prime representar
	# 	d_prima = 1/promedio_hits - 1/promedio_falsas_alarmas
	# 	d_primas.append(d_prima)
	# 	print "Sujeto: {}, Hits: {}, Falsas alarmas: {}, D': ".format(sujeto, hits, falsas_alarmas, d_prima)

	# #Tengo la lista de d's
	# t = stats.ttest_1samp(d_primas, 0)
	# print "T-test result: {}".format(t)