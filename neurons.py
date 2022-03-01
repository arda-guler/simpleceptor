import time

class AI:
    def __init__(self, neurons=[]):
        self.neurons = neurons or []
        
        self.photocells = []
        self.identifier = []
        if len(self.neurons) > 2:
            self.photocells = self.neurons[:-1]
            self.identifier = self.neurons[-1]
            
        self.active = False

    def get_neurons(self):
        if self.active:
            return self.neurons
        else:
            return None

    def get_photocells(self):
        return self.photocells

    def get_photocell(self, x, y):
        adjusted_index = y * 256 + x
        return self.photocells[adjusted_index]

    def get_identifier(self):
        return self.identifier

    def get_active(self):
        return self.active

    def get_photocellWeights(self):
        photocell_weights = []
        for photocell in self.photocells:
            photocell_weights.append(photocell.get_weight())
        return photocell_weights

    def get_numNeurons(self):
        if self.active:
            return len(self.neurons)
        else:
            return None

    def activate(self):
        self.active = True
        print("AI active.")

    def deactivate(self):
        try:
            self.active = False
            print("AI inactive.")
        # hehe :D
        except:
            print("UH-OH. UNABLE TO DEACTIVATE AI. Maybe use kill()?")

    # HAHAHA :D
    # who says no to some unnecessary roleplay drama?
    def kill(self):
        print("Attempting to kill AI!")
        self.active = False
        try:
            del self
            print("AI terminated successfully. R.I.P.")
        except:
            while True:
                try:
                    del self
                    break
                except:
                    print("UNABLE TO TERMINATE AI! UNPLUG ROUTER AND RUN!")
                    time.sleep(1)

class neuron:
    pass

class photocell(neuron):
    def __init__(self, bias, weight=1):
        self.bias = bias
        self.active = False
        self.weight = weight

    def get_bias(self):
        return self.bias

    def get_active(self):
        return self.active

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def update_active(self, brightness):
        if brightness >= self.bias:
            self.active = True
        else:
            self.active = False

    def get_value(self):
        return self.active * self.weight

    def increaseWeight(self, incr):
        self.weight += incr

    def decreaseWeight(self, decr):
        self.weight -= decr

class identifier(neuron):
    def __init__(self, bias, photocells=[]):
        self.bias = bias
        self.active = False
        self.photocells = photocells

    def get_bias(self):
        return self.bias

    def get_active(self):
        return self.active

    def get_photocells(self):
        return self.photocells

    def get_numPhotocells(self):
        return len(self.photocells)

    def update_active(self):
        weightedSum = 0
        for photocell in self.photocells:
            weightedSum += photocell.get_value()

        if weightedSum >= self.bias:
            self.active = True
        else:
            self.active = False
