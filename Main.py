import matplotlib.pyplot as plt
import numpy as np
from Assets import *
from Optimise import *

plt.close('all')

'''
#Test
radar1 = sensor_iads(400, 300)
EA18G = Jammer(210, 300)
print("EA18G is detected before jamming: ")
print(radar1.detection(EA18G))
plt.pause(2)
F16 = aircraft(362,342)
print("EA18G is detected while jamming: ")
print(radar1.detection(EA18G, [EA18G]))
print("F16 is detected while EA18G is jamming: ")
print(radar1.detection(F16,[EA18G]))
plt.pause(4)
EA18G.update(310)
print('F16 is detected while EA18G is jamming: ')
print(radar1.detection(F16,[EA18G]))
plt.pause(3)
EA6B = Jammer(330, 280)
print('F16 is detected while EA18G is jamming: ')
print(radar1.detection(F16,[EA18G, EA6B]))
'''

#Scénario
radar1 = sensor_iads(600, 300)
radar2 = sensor_iads(700, 400)
radar3 = sensor_iads(650, 550)
radar4 = sensor_iads(550, 650)

striker = aircraft(673,481)
jammer1 = Jammer(200, 725)
jammer2 = Jammer(420, 550)
jammer3 = Jammer(420, 400)
jammer4 = Jammer(200, 250)

jammer3.update(450)


#Test
allocation = [[radar1, [jammer4]],
              [radar2, [jammer3]],
              [radar3, [jammer2]],
              [radar4, [jammer1]]]

print(corridor_width(allocation, striker, 2))
print(any_detection(allocation, 20))
print(means_cost())
print(safe_distance())
print(time_constraint())
#plt.legend()
plt.show()