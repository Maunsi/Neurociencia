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
	df_final = pandas.DataFrame(columns=["Sujeto", "Operacion", "Flanker_izquierdo", "Flanker_derecho", "Target", "Respuesta", "Tiempo_de_respuesta (ms)", 
			"Control_operaciones", "Tiempo_control_operacion", "Control_pares", "Tiempo_control_pares", "Control_subjetivo"])
	for filepath in glob.iglob('Resultados/*.csv'):
		df = pandas.read_csv(filepath, names=["Sujeto", "Operacion", "Flanker_izquierdo", "Flanker_derecho", "Target", "Respuesta", "Tiempo_de_respuesta (ms)", 
			"Control_operaciones", "Tiempo_control_operacion", "Control_pares", "Tiempo_control_pares", "Control_subjetivo"])
		#consigo los unique, itero para todos los valores para reemplazar los sujetos correctamente
		sujetos = df["Sujeto"].unique()
		print "Sujetos del archivo {}, {}".format(filepath, sujetos)
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

	print "Sujetos del dataframe final: {}".format(df_final["Sujeto"].unique())
	return df_final

def analizar(df):
	df_menores_a_cuatro = filtrar_mayores_a_cuatro(df)
	#df_nuevo = filtrar_pruebas_letra(df_menores_a_cuatro)
	analisis_control_objetivo_operacion(df_menores_a_cuatro)
	analisis_control_objetivo_pares(df_menores_a_cuatro)
	analisis_tiempos(df_menores_a_cuatro)

def filtrar_mayores_a_cuatro(df):
	sujetos_antes = len(df["Sujeto"].unique())
	#Filtrar
	df = df[df.Control_subjetivo < 4]
	sujetos_despues = len(df["Sujeto"].unique())

	mean = df["Control_subjetivo"].mean()
	print "Cantidad de sujetxs desechados: {}".format(sujetos_despues-sujetos_antes)
	print "Promedio de visibilidad entre los sujetxs restantes: {}".format(mean)
	print "Resultados sin control subjetivo mayor o igual a cuatro"
	#with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
	#	print(df)
	return df

#Hay una mejor manera seguro
def filtrar_pruebas_letra(df):
	print "Resultados sin trials con letras"
	df = df[np.logical_not(df.Target.str.isalpha())]
	#with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
	#	print(df)
	return df

def analisis_control_objetivo_operacion(df):
	# L = SUMAR, A = REPRESENTAR.
	d_primas = []
	hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales, nones_totales = 0, 0, 0, 0, 0
	sujetos = df.Sujeto.unique()
	print sujetos
	for sujeto in sujetos:
		hits, misses, falsas_alarmas, correct_rejections, nones = 0, 0, 0, 0, 0
		#Para cada row de este sujeto
		for index, row in df.loc[df["Sujeto"] == sujeto].iterrows():
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
		nones_totales += nones
		print "Sujeto: {}, Hits: {}, Misses: {}, Falsas alarmas: {}, Correct Rejections: {}, Nones: {}".format(sujeto, hits, misses, falsas_alarmas, correct_rejections, nones)
	# 	probabilidad_hit = hits/(hits + misses) #hits dividido todos los trials que tuvieron como prime sumar
	# 	probabilidad_falsa_alarma =  falsas_alarmas/(falsas_alarmas + correct_rejections) 
	# 	#falsas alarmas dividido todos los trials que tuvieron como prime representar
	# 	d_prima = 1/promedio_hits - 1/promedio_falsas_alarmas
	# 	d_primas.append(d_prima)
	print "Hits totales: {}, Misses totales: {}, Falsas alarmas totales: {}, Correct Rejections totales: {}, Nones_totales: {}".format(hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales, nones_totales)
	# plt.bar([0,1,2,3], [hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales])  # arguments are passed to np.histogram
	# plt.xticks([0,1,2,3], ["hits", "misses", "false alarms", "correct rejections"])
	# plt.title("Hits Misses Falsas alarmas Rechazos correctos")
	# plt.show()
	# #Tengo la lista de d's
	# t = stats.ttest_1samp(d_primas, 0)
	# print "T-test result: {}".format(t)

def analisis_control_objetivo_pares(df):
	#with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
	#	print(df)
	#PARA LO DE NONES HABRIA QUE SELECCIONAR SOLO LAS FILAS DONDE HAY FLANKER IZQUIERDO. 
	#PARECE QUE CUANDO ERA IMPAR QUIZAS LA GENTE RESPONDIO MUY TEMPRANO?
	hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales, nones_totales = 0, 0, 0, 0, 0
	sujetos = df.Sujeto.unique()
	print sujetos
	for sujeto in sujetos:
		hits, misses, falsas_alarmas, correct_rejections, nones = 0, 0, 0, 0, 0
		#Para cada row de este sujeto
		for index, row in df.loc[df["Sujeto"] == sujeto].iterrows():
			izq = row["Flanker_izquierdo"]
			par = izq % 2 == 0
			respuesta = row["Control_pares"]
			if  par and respuesta == 'par': # Si el flanker izquierdo era par y respondi par es un hit
				hits += 1
			elif par and respuesta == 'impar': # Si el flanker izquierdo era par y respondi impar es un miss
				misses +=1
			elif not(par) and respuesta == 'par': # Si el flanker izquierdo era impar y respondi par es una falsa alarma
				falsas_alarmas +=1
			elif not(par) and respuesta == 'impar': # Si el flanker izquierdo era impar y respondi impar es una correct rejection
				correct_rejections +=1
		hits_totales += hits
		misses_totales += misses
		falsas_alarmas_totales += falsas_alarmas
		correct_rejections_totales += correct_rejections
		nones_totales += nones
		print "Sujeto: {}, Hits: {}, Misses: {}, Falsas alarmas: {}, Correct Rejections: {}, Nones: {}".format(sujeto, hits, misses, falsas_alarmas, correct_rejections, nones)
	# 	probabilidad_hit = hits/(hits + misses) #hits dividido todos los trials que tuvieron como prime sumar
	# 	probabilidad_falsa_alarma =  falsas_alarmas/(falsas_alarmas + correct_rejections) 
	# 	#falsas alarmas dividido todos los trials que tuvieron como prime representar
	# 	d_prima = 1/promedio_hits - 1/promedio_falsas_alarmas
	# 	d_primas.append(d_prima)
	print "Hits totales: {}, Misses totales: {}, Falsas alarmas totales: {}, Correct Rejections totales: {}, Nones totales: {}".format(hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales, nones_totales)
	# plt.bar([0,1,2,3], [hits_totales, misses_totales, falsas_alarmas_totales, correct_rejections_totales])  # arguments are passed to np.histogram
	# plt.xticks([0,1,2,3], ["hits", "misses", "false alarms", "correct rejections"])
	# plt.title("Hits Misses Falsas alarmas Rechazos correctos")
	# plt.show()
	# #Tengo la lista de d's
	# t = stats.ttest_1samp(d_primas, 0)
	# print "T-test result: {}".format(t)



def analisis_tiempos(df):
	#COINCIDE SIGNIFICA QUE EL TARGET ES IGUAL A LA SUMA DE LOS FLANKERS

	df_numero = df.loc[df["Target"].isin(["1","2","3","4","5","6"]) & (df["Tiempo_de_respuesta (ms)"] > 0.3) & (df["Tiempo_de_respuesta (ms)"] < 1)]
	df["Target"] = pandas.to_numeric(df_numero["Target"], errors='ignore')

	print df_numero
	print "*******************************************"
	print type(df_numero["Flanker_izquierdo"][0])
	print type(df_numero["Target"][0])

	df_numero_coincide = df_numero.loc[df["Target"] == (df["Flanker_izquierdo"] + df["Flanker_derecho"])]
	print df_numero_coincide
	print "*******************************************"
	df_numero_coincide_suma = df_numero_coincide.loc[df["Operacion"] == 'sumar']
	print df_numero_coincide_suma
	print "*******************************************"
	df_numero_coincide_representar = df_numero_coincide.loc[df["Operacion"] == 'representar']
	print df_numero_coincide_representar
	print "*******************************************"


	promedio_suma_coincide = df_numero_coincide_suma.mean()
	print promedio_suma_coincide
	print "*******************************************"
	promedio_representar_coincide = df_numero_coincide_representar.mean()


	df_numero_no_coincide = df_numero.loc[df["Target"] != df["Flanker_izquierdo"] + df["Flanker_derecho"]]
	df_numero_no_coincide_suma = df_numero_no_coincide.loc[df["Operacion"] == 'sumar']
	df_numero_no_coincide_representar = df_numero_no_coincide.loc[df["Operacion"] == 'representar']
	
	promedio_suma_no_coincide = df_numero_no_coincide_suma.mean()
	promedio_representar_no_coincide = df_numero_no_coincide_representar.mean()
	
	plt.bar([0,1,2,3], [promedio_suma_coincide, promedio_suma_no_coincide, promedio_representar_coincide, promedio_representar_no_coincide])  # arguments are passed to np.histogram
	plt.xticks([0,1,2,3], ["SumarC", "SumarN", "RepresentaC", "RepresentarN"])
	plt.title("Resultados tiempo")
	plt.show()



if __name__ == '__main__':
	df = leer_resultados()
	analizar(df)


