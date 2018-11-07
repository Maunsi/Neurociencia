#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import addExp

def escribir_resultado(resultado, nombre_archivo, modo):
    """ Guarda la respuesta en un archivo de texto.
        recibe: resultado(lista de strings)-> lo que va a guardar en un archivo.
        ------  
                nombre_archivo(string) -> nombre del archivo que va a contener los datos.
                
                modo(string) -> "r", "w" o "a".
    """
    archivo = open(nombre_archivo, modo)
    archivo.write(resultado + "\n") 
    archivo.close()
    
def preguntar_prime(ventana, texto_inicial, texto_final):
    """ Le pregunta al usuario que tanto vio el prime.
        recibe: ventana(Window) -> para saber donde escribir el texto.
        ------- 
                texto_incial(string) -> primera pantalla.
                
                texto_final(string) -> segunda pantalla.
         
         devuelve: respuestas(string) ->  dada por el usuario al apretar la tecla.
         --------- 
    """
    pregunta = visual.TextStim(win=ventana, text=texto_inicial)
    agradecimiento = visual.TextStim(win=ventana, text=texto_final)
    pregunta.draw()
    ventana.flip()
    # lo bueno de waitKeys es que, por defecto, hace un clear events y revisa que la tecla apretada sea la correcta.
    respuesta = "".join(event.waitKeys(keyList=['1', '2', '3', '4', '5', '6', '7']))
    agradecimiento.draw()
    ventana.flip()
    core.wait(1)
    
    return respuesta

def control_subjetivo(ventana):
    """ Crea la ventana, presenta las instrucciones y escribe la respuesta en un archivo.
    """
    pregunta_prime = u"Humanoide, ¿qué tanto pudo identificar las palabras SUMAR o REPRESENTAR mientras realizaba los trials? \
                     \nResponda en la siguiente escala, con el teclado, del 1 al 7. Siendo: \
                     \n1 - No las identifiqué en ninguno de los trials. \
                     \n7 - Las identifiqué en todos los trials.\
                     \n\n1\t\t2\t\t3\t\t4\t\t5\t\t6\t\t7"
    prepararse = u"Siguiente pregunta..."
    respuesta_prime = preguntar_prime(ventana, pregunta_prime, prepararse)

    pregunta_flankers = u"Durante la tarea, previamente a que apareciera el número o letra que usted categorizaba, \
                          aparecían en cada trial\
                          dos números a ambos lados del punto de fijación,\
                          ¿qué tanto pudo identificar estos números? \
                          \nResponda en la siguiente escala, con el teclado, del 1 al 7. Siendo: \
                          \n1 - No las identifiqué en ninguno de los trials. \
                          \n7 - Las identifiqué en todos los trials.\
                          \n\n1\t\t2\t\t3\t\t4\t\t5\t\t6\t\t7"
    agradecimiento = u"Muchas gracias por su colaboración. Activen el rayo vaporizador.. PZZZZZTTT"
    respuesta_flankers = preguntar_prime(ventana, pregunta_flankers, agradecimiento)

    return max(int(respuesta_prime), int(respuesta_flankers))

def control_objetivo(ventana, estimulos, mascaras):
    mitad = len(estimulos)//2
    primera_mitad_estimulos = estimulos[:mitad]
    segunda_mitad_estimulos = estimulos[mitad:]
    primera_consigna =  visual.TextStim(win=ventana, text=u"Por favor, querido ser celestial nacido de la bondad misma:\
                                la tarea consiste en identificar si en los siguientes trials aparecen las palabras REPRESENTAR o SUMAR.\
                                \n\nPresione ESPACIO para continuar.")
    primera_consigna_bis = visual.TextStim(win=ventana, text=u"INSTRUCCIONES:\
                                \n\t * Apretar A si la palabra es REPRESENTAR.\
								\n\t * Apretar L si la palabra es SUMAR.\
                                \nSi no sabe, responda igual, aunque tenga que adivinar. No se estrese.\
                                \n\nPresione ESPACIO para comenzar.")
    segunda_consigna =  visual.TextStim(win=ventana, text =u"Querida persona, durante la tarea, previamente a que apareciera el número o letra que usted\
                                categorizaba, aparecían en cada trial dos números a ambos lados del punto de fijación.\
                                En esta parte necesitamos que indique si el número que se ubica a la izquierda del punto de fijación, es impar o par.\
                                Si no sabe, responda igual, aunque tenga que adivinar. No se estrese.\
                                \n\nPresione ESPACIO para continuar.")
    segunda_consigna_bis = visual.TextStim(win=ventana, text=u"INSTRUCCIONES:\
                                \n * Apretar A si el flanker es IMPAR.\
								\n * Apretar L si el flanker es PAR.\
                                \n\nPresione ESPACIO para comenzar.")
    primera_consigna.draw()
    ventana.flip()
    event.waitKeys(keyList=["space"])
    primera_consigna_bis.draw()
    ventana.flip()
    event.waitKeys(keyList=["space"])
    control_objetivo_operaciones = addExp.experimento(ventana, primera_mitad_estimulos, mascaras)
    segunda_consigna.draw()
    ventana.flip()
    event.waitKeys(keyList=["space"])
    segunda_consigna_bis.draw()
    ventana.flip()
    event.waitKeys(keyList=["space"])
    control_objetivo_pares = addExp.experimento(ventana, segunda_mitad_estimulos, mascaras)

    return control_objetivo_operaciones, control_objetivo_pares


if __name__ == "__main__":
    ventana = visual.Window(fullscr=True)
    control_subjetivo(ventana)
    