from psychopy import visual, core, event

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
    pregunta_prime = "Humanoide, otra frase graciosa que no apure: vio las palabras SUMAR o REPRESENTAR mientras realizaba las pruebas? \
                  \nResponda presionando una tecla del 1 al 7.\n Si no lo hace sufrira las consecuencias."
    prepararse = "Ahora preparese para la proxima pregunta"
    respuesta_prime = preguntar_prime(ventana, pregunta_prime, prepararse)

    agradecimiento = "Muchas gracias por su colaboracion. Activen el rayo vaporizador.. PZZZZZTTT"
    pregunta_flankers = " Algo gracioso que va a escribir Samuel. Viste los dos numeros?"
    respuesta_flankers = preguntar_prime(ventana, pregunta_flankers, agradecimiento)

    return max(int(respuesta_prime), int(respuesta_flankers))
    

if __name__ == "__main__":
    control_subjetivo()
    