from trial import Trial
from scipy import stats
import matplotlib.pyplot as plt

def analizar(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto):
	menores_a_cuatro = filtrar_mayores_a_cuatro(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto)
	sin_letras_menores_a_cuatro = filtrar_pruebas_letra(menores_a_cuatro)
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
			file.write("{}\n".format(control_subjetivo_por_sujeto[sujeto]))
		file.close()


def escribir_diccionario(file, diccionario, significado_l, significado_a):
	for prueba, resultados in diccionario.iteritems():
		#Aprovecho y transformo las teclas a la respuesta correspondiente
		if resultados is None:
			#s = "Trial: {}. No hubo respuesta\n".format(prueba)
			s = "{}\n".format(prueba)
			file.write(s)
		else:
			(tecla, timestamp) = resultados[0]
			significado_tecla = significado_l if tecla == 'l' else significado_a
			#s = "Trial: {}, respuesta: {}, timestamp: {}\n".format(prueba, significado_tecla, timestamp)
			s = "{} {} {}\n".format(prueba, significado_tecla, timestamp)
			file.write(s)

def leer_resultados():
	pruebas_y_resultados_por_sujeto = {}
	control_subjetivo_por_sujeto = {}
	control_objetivo_operaciones_por_sujeto = {}
	control_objetivo_pares_por_sujeto = {}
	with open("resultados.txt", "r") as file:
		lineas = file.readlines()
		idx = 0
		sujeto = 0
		while idx < len(lineas):
			linea = lineas[idx]
			if "Sujeto" in linea:
				sujeto += 1
				idx +=2 #Salteo la de "Resultados"
				linea = lineas[idx]
				pruebas_y_resultados_por_sujeto[sujeto] = {}
				while "Resultados" not in linea:
					#estoy mirando las pruebas
					pruebas_y_resultados_por_sujeto[sujeto] = leer_linea(linea, pruebas_y_resultados_por_sujeto[sujeto])
					idx +=1
					linea = lineas[idx]
				#Estoy en la linea "Resultados control objetivo operaciones"
				idx += 1
				linea = lineas[idx]
				control_objetivo_operaciones_por_sujeto[sujeto] = {}
				while "Resultados" not in linea:
					#estoy mirando el control objetivo por operaciones
					control_objetivo_operaciones_por_sujeto[sujeto] = leer_linea(linea, control_objetivo_operaciones_por_sujeto[sujeto])
					idx +=1
					linea = lineas[idx]
				#Estoy en la linea "Resultados control objetivo pares"
				idx +=1
				linea = lineas[idx]
				control_objetivo_pares_por_sujeto[sujeto] = {}
				while "Resultados" not in linea:
					#Estoy mirando el control objetivo por pares
					control_objetivo_pares_por_sujeto[sujeto] = leer_linea(linea, control_objetivo_pares_por_sujeto[sujeto])
					idx +=1
					linea = lineas[idx]
				#Estoy en la linea "Resultados control subjetivo"
				idx +=1
				linea = lineas[idx]
				control_subjetivo_por_sujeto[sujeto] = int(linea)
				idx +=1
				#Sigo con el siguiente sujeto
			else:
				raise ValueError("Esperaba una linea que dijera Sujeto: numero y encontre: {}".format(line))
	file.close()
	return pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto
		
def leer_linea(linea, diccionario):
	linea_dividida = linea.rstrip().split(" ")
	print linea_dividida
	if len(linea_dividida) == 4:
			#Estoy en el caso None
			[operacion, izquierda, derecha, res] = linea_dividida
			trial = Trial(operacion, int(izquierda), int(derecha), res)
			diccionario[trial] = None
	else:
		[operacion, izquierda, derecha, res, significado_tecla, timestamp] = linea_dividida
		trial = Trial(operacion, int(izquierda), int(derecha), res)
		lista_resultados = []
		lista_resultados.append((significado_tecla, float(timestamp)))
		diccionario[trial] = lista_resultados
	return diccionario
		

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
	hits_totales = 0
	misses_totales = 0
	falsas_alarmas_totales = 0
	correct_rejections_totales = 0
	for sujeto, respuestas_por_prueba in control_objetivo_operaciones_por_sujeto.iteritems():
		hits = 0
		falsas_alarmas = 0
		misses = 0
		correct_rejections = 0
		for prueba, respuestas in respuestas_por_prueba.iteritems():
			if respuestas is not None:
				#respuestas es siempre una lista de un elemento
				(respuesta, timestamp) = respuestas[0]
				if prueba.is_sum_trial() and respuesta == 'sumar': # Si la prueba fue sumar y respondi sumar es un hit
					hits += 1
				elif prueba.is_sum_trial() and respuesta == 'representar': # Si la prueba fue sumar y respondi representar es un miss
					misses +=1
				elif prueba.is_rep_trial() and respuesta == 'sumar': # Si la prueba fue representar y respondi sumar es una falsa alarma
					falsas_alarmas +=1
				elif prueba.is_rep_trial() and respuesta == 'representar': # Si la prueba fue representar y respondi representar es una correct rejection
					correct_rejections +=1
			hits_totales += hits
			misses_totales += misses
			falsas_alarmas_totales += falsas_alarmas
			correct_rejections_totales += correct_rejections
		
	# 	probabilidad_hit = hits/(hits + misses) #hits dividido todos los trials que tuvieron como prime sumar
	# 	probabilidad_falsa_alarma =  falsas_alarmas/(falsas_alarmas + correct_rejections) 
	# 	#falsas alarmas dividido todos los trials que tuvieron como prime representar
	# 	d_prima = 1/promedio_hits - 1/promedio_falsas_alarmas
	# 	d_primas.append(d_prima)
		print "Sujeto: {}, Hits: {}, Misses: {}, Falsas alarmas: {}, Correct Rejections {}".format(sujeto, hits, misses, falsas_alarmas, correct_rejections)
	plt.bar([0,1,2,3], [hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales])  # arguments are passed to np.histogram
	plt.xticks([0,1,2,3], ["hits", "misses", "false alarms", "correct rejections"])
	plt.title("Hits Misses Falsas alarmas Rechazos correctos")
	plt.show()
	# #Tengo la lista de d's
	# t = stats.ttest_1samp(d_primas, 0)
	# print "T-test result: {}".format(t)

if __name__ == '__main__':
	pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto = leer_resultados()
	analizar(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto)