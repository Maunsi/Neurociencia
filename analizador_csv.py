#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import pandas
from trial import Trial
from scipy import stats
import math
import numpy as np
import time
import matplotlib.pyplot as plt
import random
import glob
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
import statsmodels.api as sm
# Shapiro-Wilk Test
from scipy.stats import shapiro
# Por defecto, ahora, levanta los archivos en resultados_nuevos.

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
	for filepath in glob.iglob('resultados_nuevos/*.csv'):
		df = pandas.read_csv(filepath, names=["Sujeto", "Operacion", "Flanker_izquierdo", "Flanker_derecho", "Target", "Respuesta", "Tiempo_de_respuesta", 
			"Control_operaciones", "Tiempo_control_operacion", "Control_pares", "Tiempo_control_pares", "Control_subjetivo"])
		#consigo los unique, itero para todos los valores para reemplazar los sujetos correctamente
		sujetos = df["Sujeto"].unique()
		mapa = {}
		for sujeto in sujetos:
			mapa[sujeto] = sujeto_final
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
	t_statistic_operaciones, p_value_operaciones = analisis_control_objetivo(df_menores_a_cuatro, "Operacion", lambda x:x, 
		"Control_operaciones", 'sumar', 'representar', 'sumar', 'representar', 'operaciones');
	print "T-test operaciones: {} p valor: {}".format(t_statistic_operaciones, p_value_operaciones)
	print "Control objetivo pares: "
	t_statistic_pares, p_value_pares = analisis_control_objetivo(df, "Flanker_izquierdo", lambda x: x%2, 
		"Control_pares", 0, 1, 'par', 'impar', 'pares');
	print "T-test pares: {} p valor: {}".format(t_statistic_pares, p_value_pares)
	analisis_tiempos(df_menores_a_cuatro)

def filtrar_mayores_a_cuatro(df):
	sujetos_antes = len(df["Sujeto"].unique())

	#df_nuevo = df.drop_duplicates("Sujeto").loc[:, "Control_subjetivo"]
	#df_nuevo.hist(bins=np.arange(10))
	#print(df_nuevo)
	#.hist(column="Control_subjetivo")
	#plt.show()
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

	df = df.loc[df["Target"].isin(["1","2","3","4","5","6"]) & (df["Tiempo_de_respuesta"] > 0.3) & (df["Tiempo_de_respuesta"] < 1) & (df["Respuesta"]=='numero')]
	#Que pasa si multiplico la de tiempo de respuesta por 1000
	#df.update(df.loc[:, "Target"].apply(pandas.to_numeric, errors='coerce'))
	df["Target"] = pandas.to_numeric(df["Target"], errors='ignore')
	shapiro_test()
	#df.update(df.loc[:, "Tiempo_de_respuesta"].apply(np.log10))
	#Nos quedamos con las columnas que nos importan
	df = df[["Sujeto", "Operacion", "Flanker_izquierdo", "Flanker_derecho", "Target", "Respuesta", "Tiempo_de_respuesta"]]
	df.loc[df["Target"] == (df["Flanker_izquierdo"] + df["Flanker_derecho"]), "Coincide"] = True
	df_coincide_suma = df.loc[(df["Operacion"] == 'sumar') & (df["Coincide"] == True)]
	df_coincide_representar = df.loc[(df["Operacion"] == 'representar') & (df["Coincide"] == True)]


	df.loc[df["Target"] != (df["Flanker_izquierdo"] + df["Flanker_derecho"]), "Coincide"] = False
	df_no_coincide_suma = df.loc[(df["Operacion"] == 'sumar') & (df["Coincide"] == False)]
	df_no_coincide_representar = df.loc[(df["Operacion"] == 'representar') & (df["Coincide"] == False)]
	# print("Df con target numero y tiempo de respuesta correcto")
	# print("Df numero coincide suma")
	# print("Df numero coincide representar")
	# print("Df numero no coincide suma")
	# print("Df numero no coincide representar")
	# pandas.set_option('display.width', 1000)
	# with pandas.option_context('display.max_rows', None, 'display.max_columns', 12):
	# 	print(df.shape)
	# 	print(df)
	# 	print(df_coincide_suma)
	# 	print(df_coincide_representar)
	# 	print(df_no_coincide_suma)
	# 	print(df_no_coincide_representar)

	promedio_suma_coincide = df_coincide_suma["Tiempo_de_respuesta"].mean()
	desviacion_suma_coincide = df_coincide_suma["Tiempo_de_respuesta"].std()
	
	promedio_representar_coincide = df_coincide_representar["Tiempo_de_respuesta"].mean()
	desviacion_representar_coincide = df_coincide_representar["Tiempo_de_respuesta"].std()

	promedio_suma_no_coincide = df_no_coincide_suma["Tiempo_de_respuesta"].mean()
	desviacion_suma_no_coincide = df_no_coincide_suma["Tiempo_de_respuesta"].std()

	promedio_representar_no_coincide = df_no_coincide_representar["Tiempo_de_respuesta"].mean()
	desviacion_representar_no_coincide = df_no_coincide_representar["Tiempo_de_respuesta"].std()

	draw_comparison_plot(promedio_suma_coincide, desviacion_suma_coincide, promedio_representar_coincide, desviacion_representar_coincide, 
		promedio_suma_no_coincide, desviacion_suma_no_coincide, promedio_representar_no_coincide, desviacion_representar_no_coincide);

	df.hist(column="Tiempo_de_respuesta")
	plt.show()

	shapiro_test()

	print "Statsmodel.Formula.Api Method"


	df_coincide = df.loc[df["Coincide"]==True]
	df_no_coincide = df.loc[df["Coincide"]==False]
	promedio_coincide = df_coincide["Tiempo_de_respuesta"].mean()
	desviacion_coincide = df_coincide["Tiempo_de_respuesta"].std()
	promedio_no_coincide = df_no_coincide["Tiempo_de_respuesta"].mean()
	desviacion_no_coincide = df_no_coincide["Tiempo_de_respuesta"].std()
	draw_bar_plot(2, [promedio_coincide, promedio_no_coincide], ("Coincide", "No coincide"), "Comparacion de tiempos de respuesta segun el tipo de target",
		[desviacion_coincide, desviacion_no_coincide]);

	df["Tiempo_de_respuesta"] = np.log10(df["Tiempo_de_respuesta"])
	model = smf.ols(formula='Tiempo_de_respuesta ~ Operacion + Coincide + Operacion:Coincide', data=df).fit()
	anova = anova_lm(model, typ=2)
	print model.params
	print(model.summary())
	print anova


def draw_bar_plot(n, variables, etiquetas, titulo, desviaciones=None):
	plt.bar(np.arange(n), variables, yerr=desviaciones, width=0.5, alpha= 0.6, color='b')
	plt.xticks(np.arange(n), etiquetas)
	plt.title(titulo)
	plt.show()

def draw_comparison_plot(promedio_suma_coincide, desviacion_suma_coincide, promedio_representar_coincide, desviacion_representar_coincide, 
		promedio_suma_no_coincide, desviacion_suma_no_coincide, promedio_representar_no_coincide, desviacion_representar_no_coincide):
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

	print("Suma coincide: tiempo promedio {}, varianza {}".format(promedio_suma_coincide, desviacion_suma_coincide))
	print("Suma no coincide: tiempo promedio {}, varianza {}".format(promedio_suma_no_coincide, desviacion_suma_no_coincide))
	print("Representar coincide: tiempo promedio {}, varianza {}".format(promedio_representar_coincide, desviacion_representar_coincide))
	print("Representar no coincide: tiempo promedio {}, varianza {}".format(promedio_representar_no_coincide, desviacion_representar_no_coincide))

def shapiro_test():
	stat, p = shapiro(df["Tiempo_de_respuesta"])
	print('Statistics=%.3f, p=%.3f' % (stat, p))
	# interpret
	alpha = 0.05
	if p > alpha:
		print('Sample looks Gaussian (fail to reject H0)')
	else:
		print('Sample does not look Gaussian (reject H0)')

if __name__ == '__main__':
	df = leer_resultados()
	analizar(df)


