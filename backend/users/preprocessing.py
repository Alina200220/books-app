import numpy as np
class SimpleEncoder():

    def __init__(self):
        self.encoder = {}
        self.decoder = {}
        self.encoder_max = 0
        
    def fit(self, rarray):
        
        for r in rarray:
            if r not in self.encoder:
                self.encoder[r] = self.encoder_max
                self.decoder[self.encoder_max] = r
                self.encoder_max += 1

    def transform(self, rarray):
        return np.array([self.encoder[r] if r in self.encoder else -1 for r in rarray])

    def fit_transform(self, rarray):
        self.fit(rarray)
        return self.transform(rarray)


                
        
            