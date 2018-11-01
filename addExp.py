from psychopy import visual, core, event
import random
import controlSubjetivo
import controlObjetivo
import analysis
from trial import Trial

def draw(win, stimuli, time):
    for stimulus in stimuli:
        stimulus.draw()
    win.flip()
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

def generate_mask_texts(win):
    # centro (fixation point en el paper)
    centro = visual.TextStim(win=win, name='centro', text='| |', units='norm', pos=(0,0))
    mascara = visual.TextStim(win=win, name='mascara', text='MWMWMWMWMWM', units='norm', pos=(0, 0))
    mascara_flanker_left = visual.TextStim(win=win, name='mascara_flanker_left', text='##', units='norm', pos=(-0.25, 0))
    mascara_flanker_right = visual.TextStim(win=win, name='mascara_flanker_right', text='##', units='norm', pos=(0.25, 0))
    return centro, mascara, mascara_flanker_left, mascara_flanker_right

#Para el control objetivo deberiamos refactorizar esta funcion y reutilizarla
def experiment(win, correr_hasta):
    #La idea es que tengamos variables de tiempo para las distintas mascaras
    tiempos = [1, 0.08, 0.03, 0.08, 0.1, 0.03, 1.2, 0]

    centro, mascara, mascara_flanker_left, mascara_flanker_right = generate_mask_texts(win)    

    #crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
    clock = core.Clock()
    
    input_list = read_input_file()
    random.shuffle(input_list)

    trial_responses = {}

    ########################################
    # ASCO QUE DEJO SAMUEL AL PASAR POR AQUI

    if correr_hasta == "fin":
        tope = 0
    elif correr_hasta == "mitad":
        tope = len(input_list) // 2
        
    ########################################

    while len(input_list) != tope:  #corro mientras queden estimulos
        trial = input_list.pop(0)
        # prepara target, flankers y primers
        text_prime, text_left, text_right, text_res = trial.generate_stimuli(win)

        # mostrar el centro
        draw(win, {centro}, tiempos[0])
        
        # mostrar mascara    
        draw(win, {mascara}, tiempos[1])
        
        # mostrar primer de acuerdo a lo especificado en pairAndResInputs.txt
        draw(win, {text_prime}, tiempos[2])
        
        # mostrar mascara
        draw(win, {mascara}, tiempos[3])
        
        # mostrar mascara para los flankers junto con el centro
        draw(win, {centro, mascara_flanker_left, mascara_flanker_right}, tiempos[4])
        
        #Mostrar pares y el centro
        draw(win, {centro, text_left, text_right}, tiempos[5])

        # mostrar mascara para los flankers y el centro
        draw(win, {centro, mascara_flanker_left, mascara_flanker_right}, tiempos[6])

        # Mostrar resultado y mascaras para los flankers
        draw(win, {text_res, mascara_flanker_left, mascara_flanker_right}, tiempos[7])

        trial_responses[trial] = event.waitKeys(maxWait=2, keyList=['a', 'l'], timeStamped=True)

    return trial_responses

#Esto lo voy a refactorizar para que no este tan horrible
if __name__ == '__main__':
    trials_by_subject = {}
    control_subjetivo_by_subject = {}
    control_objetivo_by_subject = {}
    win = visual.Window(fullscr=True)
    consigna_experimento = visual.TextStim(win=win, text="Bienvenido al mejor experimento de Neurociencia Cognitiva.\
                                          Presione ESPACIO para comenzar o ESC para cancelar.\n \
                                          Instrucciones:\
                                          Presione L si es una letra \
                                          \nPresione A si es un numero.")
    subject = 0
    correr_hasta_fin = "fin"
    while True:
        consigna_experimento.draw()
        win.flip()
        key = event.waitKeys(keyList=["space", "escape"])[0]
        if key == "space":
            trials_by_subject[subject] = experiment(win, correr_hasta_fin)
            control_subjetivo_by_subject[subject] = controlSubjetivo.control_subjetivo(win)
            control_objetivo_by_subject[subject] = controlObjetivo.control_objetivo(win)
            subject += 1
        elif key == "escape":
            break
    analysis.analyze(trials_by_subject, control_by_subject)