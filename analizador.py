from trial import Trial
from scipy import stats

def analizar(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto):
	pruebas_y_resultados_por_sujeto = filtrar_mayores_a_cuatro(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto)
	pruebas_y_resultados_por_sujeto = filtrar_pruebas_letra(pruebas_y_resultados_por_sujeto)
	analisis_control_objetivo(control_objetivo_pares_por_sujeto, control_objetivo_operaciones_por_sujeto)
	pass

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


		probabilidad_hit = hits/(hits + misses) #hits dividido todos los trials que tuvieron como prime sumar
		probabilidad_falsa_alarma =  falsas_alarmas/(falsas_alarmas + correct_rejections) 
		#falsas alarmas dividido todos los trials que tuvieron como prime representar
		d_prima = 1/promedio_hits - 1/promedio_falsas_alarmas
		d_primas.append(d_prima)
		print "Sujeto: {}, Hits: {}, Falsas alarmas: {}, D': ".format(sujeto, hits, falsas_alarmas, d_prima)

	#Tengo la lista de d's
	t = stats.ttest_1samp(d_primas, 0)
	print "T-test result: {}".format(t)