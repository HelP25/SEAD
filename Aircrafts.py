import matplotlib.pyplot as plt
import numpy as np


class aircraft:
    rcs = 2
    list = []
    def __init__(self, X, Y, name = None):
        if name is None:
            self.name = 'Aircraft'
            point = 'r>'
        elif name == 'Jammer':
            self.name = name
            point = 'r4'
        else:
            self.name = name
            point = 'b4'
        self.X0 = X
        self.Y0 = Y
        self.X = X
        self.Y = Y
        self.coordinates0 = [self.X0, self.Y0]
        self.coordinates = [self.X, self.Y]
        self.point, = plt.plot(self.X, self.Y, point, markersize=10, label=self.name)
        aircraft.list += [self]

    def update(self,x = None,y = None):#to update the position of the aircraft on the map if it moved
        if x is None:
            x = self.X
        if y is None:
            y = self.Y
        self.X = x
        self.Y = y
        self.coordinates = [self.X, self.Y]
        self.point.set_data([x],[y])



class Jammer(aircraft):
    #Physical caracteristics
    Gj = 3
    Lj = 3
    Pj = 1
    Bj = 30e6
    list = []
    def __init__(self,X,Y):
        self.name = 'Jammer'
        super().__init__(X,Y,self.name)
        Jammer.list += [self]



class Weasel(aircraft):
    #Physical caracteristics
    nb_missiles = 4
    power_missiles = 2
    list = []
    def __init__(self, X, Y):
        self.name = 'Weasel'
        super().__init__(X,Y,self.name)
        Weasel.list += [self]

pass
