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
    

if __name__ == "__main__":
    ventana = visual.Window(fullscr=True)
    bienvenida = "Humanoide, diga sin perder un segundo: vio las palabras sumar o representar mientras realizaba las pruebas? \
Responda presionando una tecla del 1 al 7. Si no lo hace sufrira las consencuencias."
    agradecimiento = "Muchas gracias por su colaboracion. Traigan el rayo vaporizador.. PZZZZZTTT"
    
    respuesta = preguntar_prime(ventana, bienvenida, agradecimiento)
    escribir_resultado(respuesta, "resultadoPreguntaPrime.txt", "a")