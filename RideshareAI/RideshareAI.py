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

## Messy, find out how to move these declarations into Main()
# Askes the user for number of drivers and passengers
numDrivers = int(input("Enter the number of drivers for this simulation: "));
numPassengers = int(input("Enter the number of passengers for this simulation: "));

# Creates an array of Drivers with the given input
driver = []
for i in range(0,numDrivers):
    driver.append(drivers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200), randrange(1,50)));

# Creates an array of Drivers with the given input
passenger = []
for i in range(0,numPassengers):
    passenger.append(passengers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200)));

# Def of main function
def main():
    #print(driver[1].driverID);

    pickup(numDrivers, numPassengers);

# Function to calculate shortest path available from each driver to each passenger
def pickup(numDrivers, numPassengers):
    # Will find the shortest path from each driver to each passenger
    for i in range(0, numDrivers):
        for j in range(0, numPassengers):
            print(nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].pickUpNode, weight = 1, method = 'dijkstra'));
            #print("shortest path function run");
            if j == numPassengers:
                   j = 0;
        if i == numDrivers:
            i = 0;
            break;

    print("pickup function complete");

main();

