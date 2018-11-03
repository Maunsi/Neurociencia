from trial import Trial

def analizar(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto):
	pruebas_y_resultados_por_sujeto = filtrar_mayores_a_cuatro(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto)
	pruebas_y_resultados_por_sujeto = filtrar_pruebas_letra(pruebas_y_resultados_por_sujeto)
	pass

def filtrar_pruebas_letra(pruebas_y_resultados_por_sujeto):
	sin_letras = {}
	for subject, trials in pruebas_y_resultados_por_sujeto.iteritems():
		sin_letras[subject] = {}
		for trial, responses in trials:
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