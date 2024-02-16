import matplotlib.pyplot as plt
import numpy as np
from Assets import *


# noinspection PyUnreachableCode
def corridor_width(allocation_matrix, aircraft_secured, security_width):
    '''

    :param allocation_matrix: a matrix as a list of list with 2 columns that gives the radars of the scenario and the
     list of jammers that acts on every one of them
    :param aircraft_secured: the aircraft which has to go through the enemy defences
    :param security_width: take into account the minimum width the safe corridor must have
    :return: the width of the safe corridor
    '''
    # L = [[allocation_matrix[i][0].range(allocation_matrix[j + i + 1][0]), 10 * (i + 1) + j + i + 2]
    #      for i in range(len(allocation_matrix)) for j in range(len(allocation_matrix) - i - 1)]
    #
    # # Create a list of all the ranges with their indexs
    # for i in range(len(L)):  # sort by ascendant order the ranges
    #     min_index = i
    #     for j in range(i + 1, len(L)):
    #         if L[j][0] < L[min_index][0]:
    #             min_index = j
    #     L[i], L[min_index] = L[min_index], L[i]
    #
    # widths = L.copy()
    # for i in range(len(L)):  # Calculation of all the width between two cirlces of detection range
    #     widths[i][0] = (L[i][0] - allocation_matrix[L[i][1] // 10 - 1][0].get_detection_range(aircraft_secured, allocation_matrix[L[i][1] // 10 - 1][1])
    #                     - allocation_matrix[L[i][1] % 10 - 1][0].get_detection_range(aircraft_secured, allocation_matrix[L[i][1] % 10 - 1][1]))
    #
    # for i in range(len(allocation_matrix) - 1):  # The len(allocation_matrix) - 1 first widths are sorted by ascendant order
    #     # because they are the basic widths and the highest one is where the corridor will be if there is one
    #     min_index = i
    #     for j in range(i + 1, len(allocation_matrix) - 1):
    #         if L[j][0] < L[min_index][0]:
    #             min_index = j
    #     widths[i], widths[min_index] = widths[min_index], widths[i]
    #
    # corridor = [widths[len(allocation_matrix) - 2][0] - security_width]  # Then, the highest basic width is kept
    # corridor_index = [widths[len(allocation_matrix) - 2][1]]
    # if corridor[0] <= 0:  # If the highest basic width is not positive, then there is no corridor
    #     return False
    #
    # for i in range(len(allocation_matrix), len(widths)):  # If it is the case, the other widths which could obstruct the
    #     # probable safe corridor must be positive too
    #     if widths[i][1] // 10 <= corridor_index[0] // 10 and widths[i][1] % 10 >= corridor_index[0] % 10:
    #         if widths[i][0] - security_width <= 0:
    #             return False
    #         corridor += [widths[i][0] - security_width]
    # # If they are positive, then they must be taken into account to determine the width of the safe corridor
    # width = min(corridor)  # The width is equal to the smallest interesting widths
    # return True, width + security_width

    # Generate a dictionary of all radar ranges with their indices
    ranges_with_indices = {(i+1, j+1): allocation_matrix[i][0].range(allocation_matrix[j][0])
                            for i in range(len(allocation_matrix))
                            for j in range(i + 1, len(allocation_matrix))
                           }

    # Sort the ranges in ascending order
    sorted_ranges = sorted(ranges_with_indices.items(), key=lambda x: x[1])

    # Calculate widths between two circles of detection range
    widths = {key: (value - allocation_matrix[key[0]-1][0].get_detection_range(aircraft_secured, allocation_matrix[key[0]-1][1])
                    -allocation_matrix[key[1]-1][0].get_detection_range(aircraft_secured, allocation_matrix[key[1]-1][1]))
              for key, value in sorted_ranges}
    
    # Create the basic widths list
    basic_widths = []
    for i in range(1, len(allocation_matrix)):
        basic_widths += [[(i, i+1), widths.get((i, i+1))]]

    # Sort the basic widths in ascending order
    basic_widths = sorted(basic_widths, key=lambda x: x[1])

    # Determine if there is a potential safe corridor
    if basic_widths[-1][1] - security_width<= 0:# The highest one is where the corridor will be, if there is one
        return False # If the highest basic width is not positive, then there is no corridor

    # Check if other widths obstruct the potential corridor
    problematic_widths = []
    for key, value in widths.items():
        if key[0] <= basic_widths[-1][0][0] and key[1] >= basic_widths[-1][0][1]:
            if value - security_width <= 0:
                return False # If it is the case, the other widths which could obstruct the probable safe corridor must be positive too
            else:
                problematic_widths += [value]# If they are positive, then they must be taken into account to determine the width of the safe corridor

    # Determine the final width of the safe corridor
    final_width = min(problematic_widths)# The width is equal to the smallest interesting widths
    return True,final_width
