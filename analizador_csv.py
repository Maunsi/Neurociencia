import csv
import pandas
from trial import Trial
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
#Intento de usar csv. Me canse
def escribir_resultados(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto):
	with open('resultados.csv', mode='w') as csv_file:
		fieldnames = ['sujeto', 'operacion', 'izquierdo', 'derecho', 'res', 'respuesta', 't', 'respuesta_co_operacion', 't_co_operacion', 'respuesta_co_pares', 't_co_pares', 'control_subjetivo']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		for sujeto, pruebas_y_resultados in pruebas_y_resultados_por_sujeto.iteritems():
			#Asumo que todos tienen los mismos sujetos
			for prueba, respuestas in pruebas_y_resultados.iteritems():
				operacion = prueba.get_prime()
				izquierdo = str(prueba.get_left())
				derecho = str(prueba.get_right())
				res = prueba.get_res()
				if respuestas is None:
					respuesta = ''
					t = ''
				else:
					respuesta = 'letra' if respuestas[0][0] == 'l' else 'numero'
					t = str(respuestas[0][1])

				respuesta_co_operacion = ''
				t_co_operacion = ''
				respuestas_co_operaciones = control_objetivo_operaciones_por_sujeto[sujeto].get(prueba, None)
				if respuestas_co_operaciones is not None:
					respuesta_co_operacion = 'sumar' if respuestas_co_operaciones[0][0] == 'l' else 'representar'
					t_co_operacion = str(respuestas_co_operaciones[0][1])

				respuesta_co_pares = ''
				t_co_pares = ''
				respuestas_co_pares = control_objetivo_pares_por_sujeto[sujeto].get(prueba, None)
				if respuestas_co_pares is not None:
					respuesta_co_pares = 'par' if respuestas_co_pares[0][0] == 'l' else 'representar'
					t_co_pares = str(respuestas_co_pares[0][1])

				control_subjetivo = control_subjetivo_por_sujeto[sujeto]
				writer.writerow({'sujeto': str(sujeto), 'operacion': operacion, 'izquierdo': izquierdo, 'derecho': derecho, 'res': res, 'respuesta': 
					respuesta, 't': t, 'respuesta_co_operacion': respuesta_co_operacion, 't_co_operacion': t_co_operacion, 
					'respuesta_co_pares': respuesta_co_pares, 't_co_pares': t_co_pares, 'control_subjetivo': control_subjetivo});

def leer_resultados():
	#uso pandas
	df = pandas.read_csv('resultados.csv', names=["Sujeto", "Operacion", "Flanker_izquierdo", "Flanker_derecho", "Target", "Respuesta", "Tiempo_de_respuesta (ms)", 
		"Control_operaciones", "Tiempo_control_operacion", "Control_pares", "Tiempo_control_pares", "Control_subjetivo"])
	with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
		print "Resultados"
		print(df)
	return df

def analizar(df):
	df_menores_a_cuatro = filtrar_mayores_a_cuatro(df)
	df_nuevo = filtrar_pruebas_letra(df_menores_a_cuatro)
	analisis_control_objetivo(df_nuevo)

def filtrar_mayores_a_cuatro(df):
	before = df.shape[0]
	df[df["Control_subjetivo"] < 4]
	after = df.shape[0]
	#Habria que dividir por cantidad de trials o algo
	mean = df["Control_subjetivo"].mean()
	#print "Cantidad de sujetxs desechados: {}".format(after-before)
	print "Promedio de visibilidad entre los sujetxs restantes: {}".format(mean)
	print "Resultados sin control subjetivo mayor o igual a cuatro"
	with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
		print(df)
	return df

#Hay una mejor manera seguro
def filtrar_pruebas_letra(df):
	print "Resultados sin trials con letras"
	df = df[np.logical_not(df.Target.str.isalpha())]
	with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
		print(df)
	return df

def analisis_control_objetivo(df):
	# L = SUMAR, A = REPRESENTAR.
	d_primas = []
	hits_totales = 0
	misses_totales = 0
	falsas_alarmas_totales = 0
	correct_rejections_totales = 0
	#Fijarme si hay una manera mas elegante de hacerla
	sujeto, hits, misses, falsas_alarmas, correct_rejections = 0, 0, 0, 0, 0
	misses = 0
	falsas_alarmas = 0
	correct_rejections = 0
	for index, row in df.iterrows():
		#respuestas es siempre una lista de un elemento
		if sujeto != row["Sujeto"]:
			print "Sujeto: {}, Hits: {}, Misses: {}, Falsas alarmas: {}, Correct Rejections {}".format(sujeto, hits, misses, falsas_alarmas, correct_rejections)
			#Encontre un nuevo sujeto
			sujeto = row["Sujeto"]
			hits, misses, falsas_alarmas, correct_rejections = 0, 0, 0, 0
		operacion = row["Operacion"]
		respuesta = row["Control_operaciones"]
		if  operacion == 'sumar' and respuesta == 'sumar': # Si la prueba fue sumar y respondi sumar es un hit
			hits += 1
		elif operacion == 'sumar' and respuesta == 'representar': # Si la prueba fue sumar y respondi representar es un miss
			misses +=1
		elif operacion == 'representar' and respuesta == 'sumar': # Si la prueba fue representar y respondi sumar es una falsa alarma
			falsas_alarmas +=1
		elif operacion == 'representar' and respuesta == 'representar': # Si la prueba fue representar y respondi representar es una correct rejection
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
	print "Hits totales: {}, Misses totales: {}, Falsas alarmas totales: {}, Correct Rejections totales: {}".format(hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales)
	plt.bar([0,1,2,3], [hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales])  # arguments are passed to np.histogram
	plt.xticks([0,1,2,3], ["hits", "misses", "false alarms", "correct rejections"])
	plt.title("Hits Misses Falsas alarmas Rechazos correctos")
	plt.show()
	# #Tengo la lista de d's
	# t = stats.ttest_1samp(d_primas, 0)
	# print "T-test result: {}".format(t)

if __name__ == '__main__':
	df = leer_resultados()
	analizar(df)


