#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import addExp, sys

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

def dibujar_consigna(ventana, consigna):
    consigna.draw()
    ventana.flip()

def procesar_teclas(ventana, teclas):
    tecla = event.waitKeys(keyList=teclas)[0]
    if tecla == "escape":
        sys.exit()

    return tecla

def preguntar_prime(ventana, consigna):
    """ Le pregunta al usuario que tanto vio el prime.
        recibe: ventana(Window) -> para saber donde escribir el texto.
        ------- 
                texto_incial(string) -> primera pantalla.
                
                texto_final(string) -> segunda pantalla.
         
         devuelve: respuestas(string) ->  dada por el usuario al apretar la tecla.
         --------- 
    """
    teclas = ['1', '2', '3', '4', '5', '6', '7', 'escape']
    addExp.dibujar_img(ventana, consigna)
    respuesta = str(procesar_teclas(ventana, teclas))
    
    return respuesta

def control_subjetivo(ventana):
    """ Crea la ventana, presenta las instrucciones y escribe la respuesta en un archivo.
    """
    pregunta_prime = "subjetivo_instrucciones_primes.png"
    respuesta_prime = preguntar_prime(ventana, pregunta_prime)

    pregunta_flankers = "subjetivo_instrucciones_flanker.png"
    respuesta_flankers = preguntar_prime(ventana, pregunta_flankers)

    return max(int(respuesta_prime), int(respuesta_flankers))

def control_objetivo(ventana, estimulos, mascaras):
    teclas = ["space", "escape"]
    mitad = len(estimulos)//2
    primera_mitad_estimulos = estimulos[:mitad]
    segunda_mitad_estimulos = estimulos[mitad:]
    primera_consigna =  "objetivo_instrucciones_primes.png"
    segunda_consigna =  "objetivo_instrucciones_flanker.png"
    addExp.dibujar_img(ventana, primera_consigna)
    procesar_teclas(ventana, teclas)
    control_objetivo_operaciones = addExp.experimento(ventana, primera_mitad_estimulos, mascaras)
    addExp.dibujar_img(ventana, segunda_consigna)
    procesar_teclas(ventana, teclas)
    control_objetivo_pares = addExp.experimento(ventana, segunda_mitad_estimulos, mascaras)

    return control_objetivo_operaciones, control_objetivo_pares

if __name__ == "__main__":
    ventana = visual.Window(fullscr=True)
    control_subjetivo(ventana)
    