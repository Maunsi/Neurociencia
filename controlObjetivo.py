import addExp
import random
from psychopy import visual, core, event

""" PROBLEMAS: * el import addExp, tal vez podriamos poner experiment en otro modulo
				 separado de addExp.

			   * asi como esta no corre las dos mitades de los inputs debido a que 
			     experiment vuelve a leer todas las entradas y mezclarlas. Estamos
			     leyendo siempre los mismos inputs mezclados, en lugar de agarrar
			     las dos mitades de las inputs.

			   * devuelve una tupla de diccionarios con las respuestas dado que 
			   	 no solucione el tema de que lea, realmente, las dos mitades. 
			   	 Al mezclar los diccionarios podria perder datos porque sobreescribe
			   	 los keys repetidos.
"""
def correr_mitad(ventana, consigna_texto):
	consigna = visual.TextStim(win=ventana, text=consigna_texto)
	consigna.draw()
	ventana.flip()
	event.waitKeys(keyList=["space"])
	respuestas = addExp.experiment(ventana, "mitad")

	return respuestas

def control_objetivo(ventana):
	consigna_primera_mitad_texto = "Por favor, querido ser celestial nacido de la bondad misma:\
							  		\nidentifique si en los siguientes trials aparecen las palabras\
							  		SUMAR o REPRESENTAR. \
							  		\nInstrucciones:\
							  		\n\tApretar L si la palabra es SUMAR.\
							  		\n\tApretar A si la palabra es REPRESENTAR.\
							  		\nSi no sabe, mienta y si miente sepa que es peor que Menem.\
							  		\n\nPresione ESPACIO para comenzar. "
	respuestas_primera_mitad = correr_mitad(ventana, consigna_primera_mitad_texto)

	consigna_segunda_mitad_texto = "Querida persona, buena como el agua mineral, le pedimos ahora que indique\
							  		si el flanker izquierdo es par o impar. Si falla, no vuelve a subir a la\
							  		calesita.\
							  		\nInstrucciones:\
							  		\n\tApretar L si el flanker es PAR.\
							  		\n\tApretar A si el flanker es IMPAR.\
							  		\n\nPresione ESPACIO para comenzar."
	respuestas_segunda_mitad = correr_mitad(ventana, consigna_segunda_mitad_texto)
	return (respuestas_primera_mitad, respuestas_segunda_mitad)

if __name__ == "__main__":
	control_objetivo()