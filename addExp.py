from psychopy import visual, core, event#, gui
import random
import controlSubjetivo

class Trial():

    def __init__(self, trial_id, prime, left, right, res):  
        self.prime = prime
        self.left = left
        self.right = right
        self.res = res
        
    def generate_stimuli(self, win):
        text_prime = visual.TextStim(win=win, name='text_prime', text=self.prime, units='norm', pos=(0, 0))
        text_left = visual.TextStim(win=win, name='text_left', text=str(self.left), units='norm', pos=(-0.25, 0))
        text_right = visual.TextStim(win=win, name='text_right', text=str(self.right), units= 'norm', pos=(0.25, 0))
        text_res = visual.TextStim(win=win, name='text_res', text=self.res, units= 'norm', pos=(0, 0))
        return text_prime, text_left, text_right, text_res
    
    def __eq__(self, other):
        """Overrides the default implementation""" 
        return self.prime == other.prime and self.left == other.left and self.right == other.right and self.res == other.res
    
    def __hash__(self):
        """ Ni idea pero si hay override de __eq__ es necesario redefinir esta funcion"""
        return id(self)
        
    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

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
        trial_id, prime, pairString, res = line.rstrip().split(" ")
        left, right = pairString.split(",")
        trial = Trial(int(trial_id), prime, int(left), int(right), res) #res es una string porque a veces es una latra
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

def experiment(win):
    #La idea es que tengamos variables de tiempo para las distintas mascaras
    tiempos = [1, 0.08, 0.03, 0.08, 0.1, 0.03, 1.2, 2]

    centro, mascara, mascara_flanker_left, mascara_flanker_right = generate_mask_texts(win)    

    #crear el objeto clock que sirve para controlar el tiempo (clock cuenta en segundos)
    clock = core.Clock()
    
    input_list = read_input_file()
    random.shuffle(input_list)
    n = len(input_list)
    trial_by_id = {}
    trial_responses_by_id = {}
    trial_responses = {}

    while len(input_list) != 0:  #corro mientras queden estimulos
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

        trial_responses[trial] = event.waitKeys(maxWait=tiempos[7], keyList=["left", "right"], timeStamped=True)
        
    return trial_responses
    
def metrics(trials_by_subject):
    #Cada elemento de la lista tiene un diccionario de trial -> response
    #Este for es para que no quede vacio el metodo, aca deberiamos hacer todas las cuentillas
    for trials in trials_by_subject:
        print trials
    

    # #No hace falta tener un separador, ya sabemos cuanto mide cada experimento (n trials)
    # with open("results.txt", "a") as f:
		# for i in range(n):
			# (prime, left, right, res) = trial_by_id[i]
			# response = trial_responses_by_id[i]
			# s = "{} {} {},{} {} {} ".format(i, prime, left, right, res, response)
			# f.write("%s\n" % s)
		# f.write("*\n")
	# f.close()

if __name__ == '__main__':
    trials_by_subject = []
    while True:
        win = visual.Window(fullscr=True)
        inicio = visual.TextStim(win=win, text="Bienvenido al mejor experimento de Neurociencia Cognitiva.\
                                          Presione ESPACIO para comenzar o ESC para cancelar.\n \
                                          Instrucciones:\
                                          Flecha Izquierda si es una letra \
                                          \nFlecha derecha si es un numero.")
        inicio.draw()
        win.flip()
        key = event.waitKeys(keyList=["space", "escape"])[0]
        if key == "space":
            trials_by_subject.append(experiment(win))
            # hace el control subjetivo. Por ahora escribe el resultado en un .txt aparte. 
            controlSubjetivo.control_subjetivo()
        elif key == "escape":
            break
    metrics(trials_by_subject)