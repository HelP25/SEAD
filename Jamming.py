import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Creation of the different assets in the battlespace
class sensor_iads:
    #Physical caracteristics
    G = 33.6 #gain
    F = 7 #noise
    L = 8 #loss
    Ee = 10.8 #emitted energy
    Pt = 10 * np.log10(7.2e3) #emitted power
    Rmin = 9 #minimum signal-to-noise ration
    l = -8 #wavelength
    Br = 1.37e6 # bandwidth
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

    def range(self, aircraft):#provides the distance between an aircraft and the radar
        return np.linalg.norm(np.array((self.X, self.Y)) -
                                  np.array((aircraft.X, aircraft.Y)))

    def detection(self, aircraft, jammer = None):#tells if the asset is within the detection range of a radar
        if self.range(aircraft) <= self.get_detection_range(aircraft, jammer):
            return True
        return False

    #Function that calculates the range of the sensor, either or not it has been jammed
    def get_detection_range(self, aircraft, jammer = None):
        def from_dB(G):  # Definition of a function to convert from dB to whatever unit
            return 10 ** (G / 10)

        if jammer is None:#if there is no aircraft jamming, then the range is calculated as if the power of the jamming was
                          #equal to 0
            Pj = 0
            Gj = SEAD_aircraft.Gj
            Lj = SEAD_aircraft.Lj
            Bj = SEAD_aircraft.Bj
            # Calculation of the range
            # Range when the jammer is the aircraft to keep out of the detection range of the radar
            # detection_range = ((from_dB(self.Pt) * from_dB(self.G)**2 * aircraft.rcs * from_dB(self.l)**2)
            #                  / ((4 * np.pi)**3 * from_dB(self.L) * from_dB(self.F) * 1.38e-23 * self.Br
            #                     + (4 * np.pi * from_dB(self.L) * jammer.Pj * from_dB(Gj) * self.Br)
            #                     / (from_dB(Lj) * Bj)))**0.5 / 1000

            # Range when the jammer reduces the detection range to protect a friendly asset from being detected (depends on the
            # distance between the jammer and the radar targeted)
            detection_range = ((from_dB(self.Pt) * from_dB(self.G) ** 2 * aircraft.rcs * from_dB(self.l) ** 2)
                / ((4 * np.pi) ** 3 * from_dB(self.L) * from_dB(self.F) * 1.38e-23 * self.Br
                + (4 * np.pi * from_dB(self.L) * Pj * from_dB(Gj) * self.Br)
                / (from_dB(Lj) * Bj))) ** 0.25 / 1000
        else:
            #Calculation of the range
            # Range when the jammer is the aircraft to keep out of the detection range of the radar
            # detection_range = ((from_dB(self.Pt) * from_dB(self.G)**2 * aircraft.rcs * from_dB(self.l)**2)
            #                  / ((4 * np.pi)**3 * from_dB(self.L) * from_dB(self.F) * 1.38e-23 * self.Br
            #                     + (4 * np.pi * from_dB(self.L) * jammer.Pj * from_dB(Gj) * self.Br)
            #                     / (from_dB(Lj) * Bj)))**0.5 / 1000
            # Range when the jammer reduces the detection range to protect a friendly asset from being detected (depends
            # on the distance between the jammer and the radar targeted)
            detection_range = ((from_dB(self.Pt) * from_dB(self.G) ** 2 * aircraft.rcs * from_dB(self.l) ** 2)
                         / ((4 * np.pi) ** 3 * from_dB(self.L) * from_dB(self.F) * 1.38e-23 * self.Br
                            + (4 * np.pi * from_dB(self.L) * jammer.Pj * from_dB(jammer.Gj) * self.Br)
                            / ((self.range(jammer) * 1000) ** 2 * from_dB(jammer.Lj) * jammer.Bj))) ** 0.25 / 1000
        print(detection_range)
        #Outline of the range
        theta = np.linspace(0, 2 * np.pi, 100)
        x = self.X + detection_range * np.cos(theta)
        y = self.Y + detection_range * np.sin(theta)
        plt.plot(x, y, label='Range')
        return detection_range


class SEAD_aircraft:
    #Physical caracteristics
    Gj = 3
    Lj = 3
    Pj = 1
    Bj = 30e6
    rcs = 2
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.coordinates = [X, Y]
        self.point, = plt.plot(self.X, self.Y, 'r^', markersize=10, label='SEAD aircraft')

    def update(self,x = None,y = None):#to update the position of the aircraft on the map if it moved
        if x is None:
            x = self.X
        if y is None:
            y = self.Y
        self.X = x
        self.Y = y
        self.point.set_data([x],[y])




#Test
radar1 = sensor_iads(400, 300)
EA18G = SEAD_aircraft(100, 300)
print("EA18G is detected before jamming: ")
print(radar1.detection(EA18G))
plt.pause(2)
F16 = SEAD_aircraft(362,342)
print("EA18G is detected while jamming: ")
print(radar1.detection(EA18G, EA18G))
print("F16 is detected while EA18G is jamming: ")
print(radar1.detection(F16,EA18G))
plt.pause(4)
EA18G.update(310)
print('F16 is detected while EA18G is jamming: ')
print(radar1.detection(F16,EA18G))


plt.legend()
plt.show()

plt.legend()
plt.show()
