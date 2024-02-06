import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Creation of the different assets in the battlespace
class sensor_iads:
    #Physical caracteristics
    G = 33.6
    F = 7
    L = 8
    Ee = 10.8
    Rmin = 9
    l = -8
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.coordinates = [X,Y]
        self.point, = plt.plot(self.X,self.Y,'bs', markersize=10, label='Radar')

    def update(self,x = None,y = None):#allows to update the position of the asset when its coordinates are modified
        if x is None:#we can modify only the absissa
            x = self.X
        if y is None:#or the ordinate
            y = self.Y
        self.X = x#modification of the coordinates
        self.Y = y
        self.point.set_data([x],[y])#update on the graph


    def range(self, aircraft):
        #Calculation of the range
        range_dB = 0.25 * (self.Ee + 2 * self.G + 2 * self.l + 10 * np.log10(aircraft.rcs) - 33 - self.Rmin - self.L - self.F + 204)
        #print(10 ** (range_dB/10) / 1000)
        #Outline of the range
        theta = np.linspace(0, 2 * np.pi, 100)
        x = self.X + 10 ** (range_dB/10) / 1000 * np.cos(theta)
        y = self.Y + 10 ** (range_dB/10) / 1000 * np.sin(theta)
        plt.plot(x, y, label='Range')
        return 10 ** (range_dB/10)


class SEAD_aircraft:
    #Physical caracteristics
    Gj = 3
    Lj = 3
    Pj = 10
    deltaF = 30e6
    rcs = 2
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.coordinates = [X, Y]
        self.point, = plt.plot(self.X, self.Y, 'r^', markersize=10, label='SEAD aircraft')

    def update(self,x = None,y = None):
        if x is None:
            x = self.X
        if y is None:
            y = self.Y
        self.X = x
        self.Y = y
        self.point.set_data([x],[y])

    def is_detected(self,radar, length = None):#tells if the asset is within the detection range of a radar
        if length is None:#in case the detection range has been modify by a jammer
            length = radar.range(self)
        if np.sqrt((self.X - radar.X)**2 + (self.Y - radar.Y)**2) <= length:
            return True
        return False

#Function that applies the jamming effect on the detection range of the radar
def noise_jamming_effect(radar, jammer):
    #Calculation of the new range
    def from_dB(G):#Definition of a function to convert from dB to whatever unit
        return 10**(G/10)
    # Range when the jammer is the aircraft to keep out of the detection range of the radar
    # new_range = np.sqrt((from_dB(radar.Ee) * from_dB(radar.G) * jammer.rcs * jammer.deltaF * from_dB(jammer.Lj)) / (
    #             4 * np.pi * jammer.Pj * from_dB(jammer.Gj) * from_dB(radar.L) * from_dB(radar.Rmin))) / 1000
    # Range when the jammer reduces the detection range to protect a friendly asset from being detected (depends on the
    # distance between the jammer and the radar targeted)
    new_range = np.sqrt((from_dB(radar.Ee) * from_dB(radar.G) * jammer.rcs * jammer.deltaF * from_dB(radar.L) *
                         from_dB(radar.l))**2 / (jammer.Pj * from_dB(jammer.Gj) * from_dB(jammer.Lj) * (4*np.pi)**2 *
                                                ((radar.X - jammer.X)**2 + (radar.Y - jammer.Y)**2)*1000**2))/1000

    print(new_range)
    #Outline
    theta = np.linspace(0, 2 * np.pi, 100)
    x = radar.X + new_range * np.cos(theta)
    y = radar.Y + new_range * np.sin(theta)
    plt.plot(x, y, label='New range')
    return new_range


#Test
radar1 = sensor_iads(400, 300)
EA18G = SEAD_aircraft(100, 300)
print("EA18G is detected before jamming: ")
print(EA18G.is_detected(radar1))
plt.pause(2)
F16 = SEAD_aircraft(362,342)
detected1 = noise_jamming_effect(radar1, EA18G)
print("EA18G is detected while jamming: ")
print(EA18G.is_detected(radar1,detected1))
plt.pause(4)
EA18G.update(-100)
detected2 = noise_jamming_effect(radar1, EA18G)
print('F16 is detected while EA18G is jamming: ')
print(F16.is_detected(radar1,detected2))


plt.legend()
plt.show()
