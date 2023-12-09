import importlib
import cffi
importlib.reload(cffi)
import networkx as nx
import mip
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def draw_solution(V, A, x):
    g = nx.Graph()
    g.add_nodes_from(V)
    g.add_edges_from([(i,j) for (i,j) in A])
    node_color = ['green' if x[i].x == 1.0 else '#1f78b4' for i in g.nodes]
    nx.draw(
        g, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, alpha=0.9, node_color = node_color,
        with_labels=True
    )
    plt.show()


#data
n = 15  # number of nodes on the main course
n1 = 15 #number of touristic sites
delta = 50  # max distance before recharge
s = 0   # starting point
t = n  # destination
distance = [20, 32, 11, 37, 7, 14, 22, 5, 35, 17, 23, 3, 26, 24] # distance (in km) between two consecutive location along the main course
deviation = [1.1, 0.7, 0.4, 0.9, 2.1, 1.8, 0.5, 0.4, 1.6, 2.5, 1.4, 0.8, 2.0, 1.3, 0.1] # distance (in km) of the deviation
inst_cost = [1492, 1789, 1914, 1861, 1348, 1769, 1123, 1432, 1564, 1818, 1901, 1265, 1642, 1712, 1756] #cost (in €) of installation of a charging point related to the node

# Define the set of vertices of the graph as the list of numbers from 0 to n-1
V = [i for i in range(n)]

# Set of arcs
A = [(i,j) for i in range(n-1)
            for j in range(i+1,i+2,1)]

# Done above, is useful to have nodes that are of a single nature, from the charging station point of view is useless to consider as nodes the set of
# locations, since charges last from tourist site to tourist site this consideration is done by accordingly adjusting arcs to consider:
# starting deviation, distance, ending deviation
new_d = [deviation[i] + distance[i] + deviation[i + 1] for i in range(len(distance))]
arcs_between_nodes = {(i, i+1): new_d[i] for i in range(len(V) - 1)}

#Create graph
g = nx.Graph()
g.add_nodes_from(V)
g.add_edges_from(A)
#pos = {i: (i, 5) for i in range(n)}   #plot as straight line
pos = nx.spring_layout(g)
plt.figure()
nx.draw(
    g, pos, edge_color='black',width=1, linewidths=1,
    node_size=500, alpha=0.9,
    with_labels=True
    )
nx.draw_networkx_edge_labels(
    g, pos, edge_labels=arcs_between_nodes, font_color='red'
    )
plt.axis('off')
plt.show()

# Create model
m = mip.Model()

t = n - 1

# Binary variable, charge_i = | 1 if bike leaves fully charged from node i'
#                             | 0 otherwise
charge = [m.add_var(var_type=mip.BINARY) for i in V]

# Binary variable, x_i = | 1 if decided to build charging station in node i'
#                        | 0 else
x = [m.add_var(var_type=mip.BINARY) for i in V]

# for all nodes between s and t in the graph excluding s and t
for i in V[s + 1:t]:
    # bike leaves node with full charge iff in node there is charging station
    # else bike leaves not fully charges and in node there is no charging station
    # moreover if there is a charging station, the bike charges to full capacity
    m.add_constr(charge[i] == x[i])
# "The cyclist starts with full charge" equivalent to: "The cyclist has charged his bike at station 0"
m.add_constr(charge[s] == 1)
# "The cyclist will reach the last node at low battery" equivalent to: "The cyclist will have to reach last node to charge the battery"
m.add_constr(charge[t] == 1)
# "So there is no need to have a charging station in station 0" equivalent to: "The cyclist comes with filled battery, can do 50km, no need to build nothing"
m.add_constr(x[s] == 0)
# "The cyclist will get the train to go home" equivalent to: "The cyclist will never charge the battery here even if he has no charge"
m.add_constr(x[t] == 0)

# list of arcs between potential charging stations conforming to delta constraint
# all possible paths between potential charging stations shorter than delta are listed as arcs of a graph where are represented all paths achievable with a bike
# with a full charge, assuming that all stations can charge the bike
plausible_charge_lifes = {}
# for all tourist sites
for i in V:
    # for all next tourist sites that are forward the actual one
    for j in V[i:]:     # for j in V from position i to end
        dist = 0.    # dist initialization
        # for all distances between tourist sites that are between the two extremes
        for k in range(i, j):
            # update cumulative distance
            dist += new_d[k]
        # if the cumulative distance is shorter than the charge life delta and if the path starts from a tourist site to a different one
        if dist <= delta and i != j:   # if less than constrain ok
            # add this arc as a feasible voyage between tourist sites on a single charge
            plausible_charge_lifes.update({(i, j): dist})

# The objective function cares about cost of installation not distance, I don't need to distance data, only feasible connections
plausible_charge_arcs = list(plausible_charge_lifes.keys())

# things are hard, can't do multiplication of x[i] * x[j] so need to have this variable
z = {}

# For defining the path between tourist site s and tourist site t, need to define the variable z that is 1 only if the bike leaves fully charged both extremes of the arc of the feasible voyages
# z is associated to each arc, and all arcs with z == 1 are part of the path of charges and discharges from s to t representing a battery discharge
for pca in plausible_charge_arcs:   #pca is a tuple (x,y), pca[0]=x pca[1]=y
    # taken a feasible voyage arc define a binary variable z
    z[pca] = m.add_var(var_type=mip.BINARY) #z is a dictionary of binary variable associated to an arc
    # if origin station hasn't a charging station, z can be at most 0 -> z is 0
    m.add_constr(z[pca] <= charge[pca[0]])
    # if end station hasn't a charging station, z can be at most 0 -> z is 0
    m.add_constr(z[pca] <= charge[pca[1]])
    # z is 1 iff both origin and end station have a charging station
    m.add_constr(z[pca] >= charge[pca[0]] + charge[pca[1]] - 1)
    # the presence of a charging station is given from variable charge that is given from variable xx part of the objective function

# adding flow conservation constraint
# general constraint for flow conservation where
b = {i: 0 for i in V}
# if node is node s, from s exits only one arc
b[s] = 1
# if node is node t, from t enters only one arc
b[t] = -1

for i in V:
    # for all nodes in the graph happens that they have only one entering arc and only one exiting arc except from nodes s and t which are explained above
    m.add_constr(
        # summation of exiting arcs
        mip.xsum(z[pca] for pca in plausible_charge_arcs if pca[0] == i) -
        # summation of entering arcs
        mip.xsum(z[pca] for pca in plausible_charge_arcs if pca[1] == i) ==
        # condition defined in variable b as above
        b[i]
    )

# Objective function: minimize cost of installation
m.objective = mip.minimize(mip.xsum(inst_cost[i] * x[i] for i in V))

m.optimize()

print("Value:", m.objective_value)
draw_solution (V, A, x)