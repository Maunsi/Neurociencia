import csv
#Intento de usar csv. Me canse
def escribir_resultados(pruebas_y_resultados_por_sujeto, control_subjetivo_por_sujeto, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto):
	with open('resultados.csv', mode='w') as csv_file:
		fieldnames = ['sujeto', 'operacion', 'izquierdo', 'derecho', 'res', 'respuesta', 't', 'respuesta_co_operacion', 't_co_operacion', 'respuesta_co_pares', 't_co_pares', 'control_subjetivo']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

		writer.writeheader()
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
	with open('resultados.csv', mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		with open('resultados_legibles.txt', mode= 'w') as file:
			line_count = 0
			for row in csv_reader:
				
				file.write('\t El sujeto {} para el trial {} {} {} {} respondio: {} en {} milisegundos.\n'.format(row["sujeto"], row["operacion"], row["izquierdo"], row["derecho"], row["res"], row["respuesta"], row["t"] ))
				if {row["respuesta_co_operacion"]} != '':
					file.write('\t Para el control objetivo de operacion con el mismo trial respondio: {} en {} milisegundos.\n'.format(row["respuesta_co_operacion"], row["t_co_operacion"]))
				else: #Si no esta en el primero esta en el segundo
					file.write('\t Para el control objetivo de pares con el mismo trial respondio: {} en {} milisegundos.'.format(row["respuesta_co_pares"], row["t_co_pares"]))
				file.write('\t El sujeto reporto una visibilidad de {}\n'.format(row["control_subjetivo"]))
				line_count += 1
		file.close()
		pruebas_y_resultados_por_sujeto = {}
		control_subjetivo_por_sujeto = {}
		control_objetivo_operaciones_por_sujeto = {}
		control_objetivo_pares_por_sujeto = {}
		for row in csv_reader:
			sujeto = row["sujeto"]
			operacion = row["operacion"]
			izquierdo = int(row["izquierdo"])
			derecho = int(row["derecho"])
			res = row["res"]
			trial = Trial(operacion, izquierdo, derecho, res)
			if row["respuesta"] == ''
				pruebas_y_resultados_por_sujeto.get(sujeto, {})[trial] = None
			else:
				respuesta = row["respuesta"]
				timestamp = float(row["t"])
				pruebas_y_resultados_por_sujeto.get(sujeto, {})[trial] = [(respuesta, timestamp)]
			if row["respuesta_co_operacion"] == ''
				control_objetivo_operaciones_por_sujeto.get(sujeto, {})[trial] = None
			else:
				respuesta = row["respuesta_co_operacion"]
				timestamp = float(row["t_co_operacion"])
				control_objetivo_operaciones_por_sujeto.get(sujeto, {})[trial] = [(respuesta, timestamp)]
			if row["respuesta_co_pares"] == ''
				control_objetivo_pares_por_sujeto.get(sujeto, {})[trial] = None
			else:
				respuesta = row["respuesta_co_pares"]
				timestamp = float(row["t_co_pares"])
				control_objetivo_pares_por_sujeto.get(sujeto, {})[trial] = [(respuesta, timestamp)]
			control_subjetivo_por_sujeto[sujeto] = row["control_subjetivo"] 
		return pruebas_y_resultados_por_sujeto, control_subjetivo, control_objetivo_operaciones_por_sujeto, control_objetivo_pares_por_sujeto




