import networkx as nx
import matplotlib.pyplot as plt
from random import *
import array as arr

seed = 1000;

G = nx.gnp_random_graph(200, 0.2, seed = seed);
print(G.nodes());

class passengers:
    groupSize = 0;
    pickUpNode = 0;
    destinationNode = 0;
    def __init__(self, custID, groupSize, pickUpNode, destinationNode):
        self.custID = custID;
        self.groupSize = groupSize;
        self.pickUpNode = pickUpNode;
        self.destinationNode = destinationNode;

#Cameron = passengers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200));
#print(Cameron.custID , " " , Cameron.groupSize , " " , Cameron.pickUpNode , " " , Cameron.destinationNode);

class drivers:
    driverID = 0;
    currCap = 0;
    currNode = 0;
    dropNode = 0;
    dropDist = 0;
    def __init__(self, driverID, currCap, currNode, dropNode, dropDist):
        self.driverID = driverID;
        self.currCap = currCap;
        self.currNode = currNode;
        self.dropNode = dropNode;
        self.dropDist = dropDist;

driver = []
for i in range(0,30):
    driver.append(drivers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200), randrange(1,50)));

passenger = []
for i in range(0,150):
    passenger.append(passengers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200)));

print(driver[1].driverID)