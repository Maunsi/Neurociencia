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
    pregunta_prime = "Humanoide, vio las palabras SUMAR o REPRESENTAR mientras realizaba las pruebas? \
                  \nResponda presionando una tecla del 1 al 7.\n Si no lo hace sufrira las consecuencias."
    prepararse = "Ahora preparese para la proxima pregunta."
    respuesta_prime = preguntar_prime(ventana, pregunta_prime, prepararse)

    pregunta_flankers = "Si, si, estamos al tanto de que su vida no tiene sentido. Si,\
                         podemos ser muy agresivos a pesar de que usted nos ayuda\
                         voluntariamente. Vio los dos numeros? \nResponda presionando una tecla del 1 al 7."
    agradecimiento = "Muchas gracias por su colaboracion. Activen el rayo vaporizador.. PZZZZZTTT"
    respuesta_flankers = preguntar_prime(ventana, pregunta_flankers, agradecimiento)

    return max(int(respuesta_prime), int(respuesta_flankers))

def control_objetivo(ventana, estimulos, mascaras):
    mitad = len(estimulos)//2
    primera_mitad_estimulos = estimulos[:mitad]
    segunda_mitad_estimulos = estimulos[mitad:]
    primera_consigna =  visual.TextStim(win=ventana, text="Por favor, querido ser celestial nacido de la bondad misma:\
                                    \nidentifique si en los siguientes trials aparecen las palabras\
                                    SUMAR o REPRESENTAR. \
                                    \nInstrucciones:\
                                    \n\tApretar L si la palabra es SUMAR.\
                                    \n\tApretar A si la palabra es REPRESENTAR.\
                                    \nSi no sabe, mienta y si miente sepa que es peor que Menem.\
                                    \n\nPresione ESPACIO para comenzar.")

    segunda_consigna =  visual.TextStim(win=ventana, text ="Querida persona, buena como el agua mineral, le pedimos ahora que indique\
                        si el flanker izquierdo es par o impar. Si falla, no vuelve a subir a la\
                        calesita.\
                        \nInstrucciones:\
                        \n\tApretar L si el flanker es PAR.\
                        n\tApretar A si el flanker es IMPAR.\
                        \n\nPresione ESPACIO para comenzar.")
    primera_consigna.draw()
    ventana.flip()
    event.waitKeys(keyList=["space"])
    control_objetivo_operaciones = addExp.experimento(ventana, primera_mitad_estimulos, mascaras)

    segunda_consigna.draw()
    ventana.flip()
    event.waitKeys(keyList=["space"])
    control_objetivo_pares = addExp.experimento(ventana, segunda_mitad_estimulos, mascaras)

    return control_objetivo_operaciones, control_objetivo_pares


if __name__ == "__main__":
    ventana = visual.Window(fullscr=True)
    control_subjetivo(ventana)
    