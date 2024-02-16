import matplotlib.pyplot as plt
import numpy as np
from Assets import *

def any_detection(allocation_matrix, weight):
    """
    :param allocation_matrix: the matrix of all the assets and their allocation
    :param weight: how much the value of the function is increased when the assets or not detected
    :return: the value of the objective function
    """
    for i in range(len(allocation_matrix)):
        for aerial_vehical in aircraft.list:
            if allocation_matrix[i][0].detection(aerial_vehical, allocation_matrix[i][1]):
                return 0
    return weight

def means_cost():
    return len(sensor_iads.list) - len(Jammer.list)

def safe_distance():
    sum = 0
    for radar in sensor_iads.list:
        for jammer in Jammer.list:
            sum += radar.range(jammer)
    return sum

def time_constraint():
    distance = []
    for aerial_vehicule in aircraft.list:
        distance += [np.linalg.norm(np.array(aerial_vehicule.coordinates0) - np.array(aerial_vehicule.coordinates))]
    time = - max(distance)
    return time