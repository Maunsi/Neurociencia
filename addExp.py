from psychopy import visual, core, event
import random
import controlSubjetivo
import controlObjetivo
import analysis
from trial import Trial

def agradecimiento(ventana, nombre_imagen):
    imagen = visual.ImageStim(ventana, image=nombre_imagen)
    imagen.draw()
    ventana.flip()
    core.wait(3)

def draw(ventana, stimuli, time=0):
    for stimulus in stimuli:
        stimulus.draw()
    ventana.flip()
    core.wait(time)

def read_input_file():
    input_list = []
    input_file = open("pairAndResInputs.txt", "r")
    for line in input_file:
        # rstrip() para evitar que algun \n moleste
        prime, pairString, res = line.rstrip().split(" ")
        left, right = pairString.split(",")
        trial = Trial(prime, int(left), int(right), res) #res es una string porque a veces es una latra
        input_list.append(trial)
    input_file.close()
    return input_list

def generate_mask_texts(ventana):
    # centro (fixation point en el paper)
    centro = visual.TextStim(win=ventana, name='centro', text='| |', units='norm', pos=(0,0))
    mascara = visual.TextStim(win=ventana, name='mascara', text='MWMWMWMWMWM', units='norm', pos=(0, 0))
    mascara_flanker_left = visual.TextStim(win=ventana, name='mascara_flanker_left', text='##', units='norm', pos=(-0.25, 0))
    mascara_flanker_right = visual.TextStim(win=ventana, name='mascara_flanker_right', text='##', units='norm', pos=(0.25, 0))
   
    return centro, mascara, mascara_flanker_left, mascara_flanker_right

def dibujar_stimuli(ventana, text_prime, text_left, text_right, text_res, centro, mascara, mascara_flanker_left,
    mascara_flanker_right):

    tiempos = [1, 0.08, 0.03, 0.08, 0.1, 0.03, 1.2, 0]

    draw(ventana, {centro}, tiempos[0])

    # mostrar mascara    
    draw(ventana, {mascara}, tiempos[1])
        
    # mostrar primer de acuerdo a lo especificado en pairAndResInputs.txt
    draw(ventana, {text_prime}, tiempos[2])
        
    # mostrar mascara
    draw(ventana, {mascara}, tiempos[3])
        
    # mostrar mascara para los flankers junto con el centro
    draw(ventana, {centro, mascara_flanker_left, mascara_flanker_right}, tiempos[4])
        
    #Mostrar pares y el centro
    draw(ventana, {centro, text_left, text_right}, tiempos[5])

    # mostrar mascara para los flankers y el centro
    draw(ventana, {centro, mascara_flanker_left, mascara_flanker_right}, tiempos[6])

    # Mostrar resultado y mascaras para los flankers
    draw(ventana, {text_res, mascara_flanker_left, mascara_flanker_right}, tiempos[7])

#Para el control objetivo deberiamos refactorizar esta funcion y reutilizarla
def experiment(ventana):
    centro, mascara, mascara_flanker_left, mascara_flanker_right = generate_mask_texts(ventana)    
    trial_responses = {}

    while len(input_list) != 0:  #corro mientras queden estimulos
        trial = input_list.pop(0)
        # prepara target, flankers y primers
        text_prime, text_left, text_right, text_res = trial.generate_stimuli(ventana)
        dibujar_stimuli(ventana, text_prime, text_left, text_right, text_res, centro, mascara, mascara_flanker_left,
                        mascara_flanker_right)
        trial_responses[trial] = event.waitKeys(maxWait=2, keyList=['a', 'l'], timeStamped=True)

    return trial_responses

#Esto lo voy a refactorizar para que no este tan horrible
if __name__ == '__main__':
    input_list = read_input_file()
    random.shuffle(input_list)
    trials_by_subject = {}
    control_subjetivo_by_subject = {}
    control_objetivo_by_subject = {}
    ventana = visual.Window(fullscr=True)
    consigna_experimento = visual.TextStim(win=ventana, text="Bienvenido al mejor experimento de Neurociencia Cognitiva.\
                                          Presione ESPACIO para comenzar o ESC para cancelar.\n \
                                          Instrucciones:\
                                          Presione L si es una letra \
                                          \nPresione A si es un numero.")
    subject = 0
    while True:
        consigna_experimento.draw()
        ventana.flip()
        key = event.waitKeys(keyList=["space", "escape"])[0]
        if key == "space":
            trials_by_subject[subject] = experiment(ventana)
            control_subjetivo_by_subject[subject] = controlSubjetivo.control_subjetivo(ventana)
            control_objetivo_by_subject[subject] = controlObjetivo.control_objetivo(ventana)
            agradecimiento(ventana, "agradecimiento.png")
            subject += 1
        elif key == "escape":
            break
    analysis.analyze(trials_by_subject, control_subjetivo_by_subject, control_objetivo_by_subject)