#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import pandas
from trial import Trial
from scipy import stats
import numpy as np
import time
import matplotlib.pyplot as plt
import random
import glob
def escribir_resultados(pruebas_y_resultados, control_subjetivo, control_objetivo_operaciones, control_objetivo_pares):
	filename = 'resultados' + str(random.randint(1,100000)) + '.csv'
	with open(filename, mode='w') as csv_file:
		fieldnames = ['sujeto', 'operacion', 'izquierdo', 'derecho', 'res', 'respuesta', 't', 'respuesta_co_operacion', 't_co_operacion', 'respuesta_co_pares', 't_co_pares', 'control_subjetivo']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
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
			respuestas_co_operaciones = control_objetivo_operaciones.get(prueba, None)
			if respuestas_co_operaciones is not None:
				respuesta_co_operacion = 'sumar' if respuestas_co_operaciones[0][0] == 'l' else 'representar'
				t_co_operacion = str(respuestas_co_operaciones[0][1])

			respuesta_co_pares = ''
			t_co_pares = ''
			respuestas_co_pares = control_objetivo_pares.get(prueba, None)
			if respuestas_co_pares is not None:
				respuesta_co_pares = 'par' if respuestas_co_pares[0][0] == 'l' else 'impar'
				t_co_pares = str(respuestas_co_pares[0][1])

			writer.writerow({'sujeto': 0, 'operacion': operacion, 'izquierdo': izquierdo, 'derecho': derecho, 'res': res, 'respuesta': 
				respuesta, 't': t, 'respuesta_co_operacion': respuesta_co_operacion, 't_co_operacion': t_co_operacion, 
				'respuesta_co_pares': respuesta_co_pares, 't_co_pares': t_co_pares, 'control_subjetivo': control_subjetivo});

def leer_resultados():
	#Tengo que iterar por todos los archivos de resultados
	sujeto_final = 0
	df_final = pandas.DataFrame(columns=["Sujeto", "Operacion", "Flanker_izquierdo", "Flanker_derecho", "Target", "Respuesta", "Tiempo_de_respuesta", 
			"Control_operaciones", "Tiempo_control_operacion", "Control_pares", "Tiempo_control_pares", "Control_subjetivo"])
	for filepath in glob.iglob('Resultados/*.csv'):
		df = pandas.read_csv(filepath, names=["Sujeto", "Operacion", "Flanker_izquierdo", "Flanker_derecho", "Target", "Respuesta", "Tiempo_de_respuesta", 
			"Control_operaciones", "Tiempo_control_operacion", "Control_pares", "Tiempo_control_pares", "Control_subjetivo"])
		#consigo los unique, itero para todos los valores para reemplazar los sujetos correctamente
		sujetos = df["Sujeto"].unique()
		mapa = {}
		for sujeto in sujetos:
			mapa[sujeto] = sujeto_final
			print "Sujeto" + str(sujeto)
			print "Sujeto final: " + str(sujeto_final)
			sujeto_final +=1

		df["Sujeto"].replace(mapa, inplace=True)
		#Esto lo hago porque tuve un error al escribir los archivos!!
		df["Control_pares"].replace({'par':'par', 'representar':'impar'}, inplace=True)
		df_final = df_final.append(df, ignore_index=True)
	return df_final

def analizar(df):
	df_menores_a_cuatro = filtrar_mayores_a_cuatro(df)
	#analisis_control_objetivo_operacion(df_menores_a_cuatro)
	#analisis_control_objetivo_pares(df_menores_a_cuatro)
	print "Control objetivo operaciones: "
	funcion_identidad = lambda x:x
	t_statistic_operaciones, p_value_operaciones = analisis_control_objetivo(df_menores_a_cuatro, "Operacion", funcion_identidad, 
		"Control_operaciones", 'sumar', 'representar', 'sumar', 'representar', 'operaciones');
	print "T-test operaciones: {} p valor: {}".format(t_statistic_operaciones, p_value_operaciones)
	funcion_par = lambda x: x%2
	print "Control objetivo pares: "
	t_statistic_pares, p_value_pares = analisis_control_objetivo(df, "Flanker_izquierdo", funcion_par, 
		"Control_pares", 0, 1, 'par', 'impar', 'pares');
	print "T-test pares: {} p valor: {}".format(t_statistic_pares, p_value_pares)
	analisis_tiempos(df_menores_a_cuatro)

def filtrar_mayores_a_cuatro(df):
	sujetos_antes = len(df["Sujeto"].unique())
	#Agrego un grafico para ver la distribucion de los valores de control subjetivo
	#controles_subjetivos = []
	#for sujeto in df["Sujeto"].unique():
	#	control_subjetivo = df.loc[df["Sujeto"] == sujeto, "Control_subjetivo"].iloc[0]
	#	print control_subjetivo
	#	controles_subjetivos.append(control_subjetivo)

	#Histograma?

	#Filtrar
	df = df[df.Control_subjetivo < 4]
	sujetos_despues = len(df["Sujeto"].unique())

	mean = df["Control_subjetivo"].mean()
	print "Cantidad de sujetxs desechados: {}".format(sujetos_antes-sujetos_despues)
	print "Promedio de visibilidad entre los sujetxs restantes: {}".format(mean)
	return df

def analisis_control_objetivo(df, columna_estimulo, funcion_estimulo, columna_respuesta, senial_estimulo, ruido_estimulo, senial_respuesta, ruido_respuesta, titulo):
	d_primas = []
	hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales, nones_totales = 0, 0, 0, 0, 0
	sujetos = df.Sujeto.unique()
	for sujeto in sujetos:
		hits, misses, falsas_alarmas, correct_rejections, nones = 0, 0, 0, 0, 0
		#Para cada row de este sujeto
		for index, row in df.loc[df["Sujeto"] == sujeto].iterrows():
			estimulo = row[columna_estimulo]
			estimulo_mod = funcion_estimulo(estimulo)
			respuesta = row[columna_respuesta]
			#La cantidad de nones es el total de estimulos menos todas las otras clasificaciones. Es decir, la mitad de los estimulos (filas)
			if estimulo_mod == senial_estimulo and respuesta == senial_respuesta:
				hits += 1
			elif estimulo_mod == senial_estimulo and respuesta == ruido_respuesta:
				misses +=1
			elif estimulo_mod == ruido_estimulo and respuesta == senial_respuesta:
				falsas_alarmas +=1
			elif estimulo_mod == ruido_estimulo and respuesta == ruido_respuesta: 
				correct_rejections +=1
		estimulos_control_objetivo = df.loc[df["Sujeto"] == sujeto].shape[0]//2
		nones = estimulos_control_objetivo - hits - misses - falsas_alarmas - correct_rejections
		hits_totales += hits
		misses_totales += misses
		falsas_alarmas_totales += falsas_alarmas
		correct_rejections_totales += correct_rejections
		nones_totales += nones
		print "Sujeto: {}, Hits: {}, Misses: {}, Falsas alarmas: {}, Correct Rejections: {}, Nones: {}".format(sujeto, hits, misses, falsas_alarmas, correct_rejections, nones)
		#draw_bar_plot(5, [hits, misses, falsas_alarmas, correct_rejections, nones], 
		#	("Hits", "Misses", "False Alarms", "Correct Rejections", "Nones"), "Control " + str(sujeto))
	 	#ACA LE HICE LA LOG LINEAR TRANSFORM. SI LO SACO HAY QUE AGREGAR CAST A FLOAT PARA FORZAR LA DIVISION CON COMA
	 	probabilidad_hit = (hits+0.5)/(hits + misses+1) #hits dividido todos los trials donde el estimulo era senial
		probabilidad_falsa_alarma = (falsas_alarmas+0.5)/(falsas_alarmas + correct_rejections+1) #falsas alarmas dividido todos los trials que tuvieron estimulo ruido
		print "Probabilidad hit {}".format(probabilidad_hit)
		print "Probabilidad falsa alarma {}".format(probabilidad_falsa_alarma)
		d_prima = stats.norm.ppf(probabilidad_hit) - stats.norm.ppf(probabilidad_falsa_alarma)
	 	d_primas.append(d_prima)
	print "Hits totales: {}, Misses totales: {}, Falsas alarmas totales: {}, Correct Rejections totales: {}, Nones totales: {}".format(hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales, nones_totales)

	draw_bar_plot(5, [hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales, nones_totales],
		("Hits Totales", "Misses Totales", "False Alarms Totales", "Correct Rejections Totales", "Nones totales"), "Control " + titulo)
	#Tengo la lista de d's
	t_statistic, p_value = stats.ttest_1samp(d_primas, 0)
	return t_statistic, p_value


def analisis_tiempos(df):
	#COINCIDE SIGNIFICA QUE EL TARGET ES IGUAL A LA SUMA DE LOS FLANKERS
	#Por si queremos pasarlo a milisegundos
	#df["Tiempo_de_respuesta"] = df["Tiempo_de_respuesta"]*1000

	df_numero = df.loc[df["Target"].isin(["1","2","3","4","5","6"]) & (df["Tiempo_de_respuesta"] > 0.3) & (df["Tiempo_de_respuesta"] < 1)]
	#Que pasa si multiplico la de tiempo de respuesta por 1000
	df_numero["Target"] = pandas.to_numeric(df_numero["Target"], errors='ignore')

	df_numero_coincide = df_numero.loc[df_numero["Target"] == (df_numero["Flanker_izquierdo"] + df_numero["Flanker_derecho"])]
	df_numero_coincide_suma = df_numero_coincide.loc[df["Operacion"] == 'sumar']
	df_numero_coincide_representar = df_numero_coincide.loc[df["Operacion"] == 'representar']

	df_numero_no_coincide = df_numero.loc[df["Target"] != (df["Flanker_izquierdo"] + df["Flanker_derecho"])]
	df_numero_no_coincide_suma = df_numero_no_coincide.loc[df["Operacion"] == 'sumar']
	df_numero_no_coincide_representar = df_numero_no_coincide.loc[df["Operacion"] == 'representar']

	promedio_suma_coincide = df_numero_coincide_suma["Tiempo_de_respuesta"].mean()
	desviacion_suma_coincide = df_numero_coincide_suma["Tiempo_de_respuesta"].std()
	
	promedio_representar_coincide = df_numero_coincide_representar["Tiempo_de_respuesta"].mean()
	desviacion_representar_coincide = df_numero_coincide_representar["Tiempo_de_respuesta"].std()

	promedio_suma_no_coincide = df_numero_no_coincide_suma["Tiempo_de_respuesta"].mean()
	desviacion_suma_no_coincide = df_numero_no_coincide_suma["Tiempo_de_respuesta"].std()

	promedio_representar_no_coincide = df_numero_no_coincide_representar["Tiempo_de_respuesta"].mean()
	desviacion_representar_no_coincide = df_numero_no_coincide_representar["Tiempo_de_respuesta"].std()
	
	promedios = (promedio_suma_coincide, promedio_suma_no_coincide, promedio_representar_coincide, promedio_representar_no_coincide)
	desviaciones = (desviacion_suma_coincide, desviacion_suma_no_coincide, desviacion_representar_coincide, desviacion_representar_no_coincide)
	etiquetas = ("SumarC", "SumarN", "RepresentaC", "RepresentarN")
	titulo = "Resultados tiempo"
	draw_bar_plot(4, promedios, etiquetas, titulo, desviaciones)

	n_groups = 2

	promedios_coincide = (promedio_suma_coincide, promedio_representar_coincide)
	desviacion_coincide = (desviacion_suma_coincide,desviacion_representar_coincide)

	promedios_no_coincide = (promedio_suma_no_coincide, promedio_representar_no_coincide)
	desviacion_no_coincide = (desviacion_suma_no_coincide, desviacion_representar_no_coincide)

	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.2
	opacity = 0.6

	coincide = ax.bar(index, promedios_coincide, bar_width,
	                alpha=opacity, color='b',
	                yerr=desviacion_coincide,
	                label='Concide')

	no_coincide = ax.bar(index + bar_width, promedios_no_coincide, bar_width,
	                alpha=opacity, color='g',
	                yerr=desviacion_no_coincide,
	                label='No coincide')

	ax.set_xlabel('Operacion')
	ax.set_ylabel('Tiempos de respuesta')
	ax.set_title('Tiempos de respuesta por operacion y tipo de target')
	ax.set_xticks(index + bar_width / 2)
	ax.set_xticklabels(('Sumar', 'Representar'))
	ax.legend()

	fig.tight_layout()
	plt.show()


def draw_bar_plot(n, variables, etiquetas, titulo, desviaciones=None):
	plt.bar(np.arange(n), variables, yerr=desviaciones)
	plt.xticks(np.arange(n), etiquetas)
	plt.title(titulo)
	plt.show()

if __name__ == '__main__':
	df = leer_resultados()
	analizar(df)


