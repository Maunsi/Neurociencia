from psychopy import visual

class Trial():

    def __init__(self, prime, left, right, res):  
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
    
    def is_letter_trial(self):
        return self.res.isalpha()
        
    def __eq__(self, other):
        """Overrides the default implementation""" 
        return self.prime == other.prime and self.left == other.left and self.right == other.right and self.res == other.res
    
    def __hash__(self):
        """ Ni idea pero si hay override de __eq__ es necesario redefinir esta funcion"""
        return id(self)
        
    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __repr__(self):
    	return "{} {} {} {} ".format(self.prime, self.left, self.right, self.res)