import importlib
import cffi
importlib.reload(cffi)
import numpy as np
import math
import networkx as nx
import mip

#data

n = 15  # number of nodes on the main course
n1 = 15 #number of touristic sites
delta = 50  # max distance before recharge
s = 0   # starting point
t = n  # destination
distance = [20, 32, 11, 37, 7, 14, 22, 5, 35, 17, 23, 3, 26, 24] # distance (in km) between two consecutive location along the main course
deviation = [1.1, 0.7, 0.4, 0.9, 2.1, 1.8, 0.5, 0.4, 1.6, 2.5, 1.4, 0.8, 2.0, 1.3, 0.1] # distance (in km) of the deviation
inst_cost = [1492, 1789, 1914, 1861, 1348, 1769, 1123, 1432, 1564, 1818, 1901, 1265, 1642, 1712, 1756] #cost (in €) of installation of a charging point related to the node