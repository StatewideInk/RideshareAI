import networkx as nx
import matplotlib.pyplot as plt
import time as tm
import threading as td
from random import *
import array as arr

# Constants
seed = 1000;
startLog = tm.time();
timeConst = 1;

# Generates the graph
G = nx.gnp_random_graph(200, 0.02, seed = seed);
#print(G.nodes());

# Class to hold all passenger information
class passengers:
    groupSize = 0;
    pickUpNode = 0;
    destinationNode = 0;
    driverDistance = 999;
    driverID = 0;
    estTime = 0;
    readyToBePickedUp = False;
    droppedOff = False;
    def __init__(self, custID, groupSize, pickUpNode, destinationNode, readyToBePickedUp, droppedOff, driverDistance, driverID, estTime):
        self.custID = custID;
        self.groupSize = groupSize;
        self.pickUpNode = pickUpNode;
        self.destinationNode = destinationNode;
        self.readyToBePickedUp = readyToBePickedUp;
        self.droppedOff = droppedOff;
        self.driverDistance = driverDistance;
        self.driverID = driverID;
        self.estTime = estTime;

# Class to hold all driver information
class drivers:
    driverID = 0;
    currCap = 0;
    currNode = 0;
    dropNode = 0;
    dropDist = 0;
    assignedPassenger = -1;
    def __init__(self, driverID, currCap, currNode, dropNode, dropDist, assignedPassenger):
        self.driverID = driverID;
        self.currCap = currCap;
        self.currNode = currNode;
        self.dropNode = dropNode;
        self.dropDist = dropDist;
        self.assignedPassenger = assignedPassenger;


## Messy, find out how to move these declarations into Main()
# Askes the user for number of drivers and passengers
numDrivers = int(input("Enter the number of drivers for this simulation: "));
numPassengers = int(input("Enter the number of passengers for this simulation: "));

# Creates an array of Drivers with the given input
driver = []
for i in range(0,numDrivers):
    driver.append(drivers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200), randrange(1,50), -1));

# Creates an array of Drivers with the given input
# Some passengers will spawn in with ReadyToBePickedUp = True so that the program doens't end too early
passenger = []
for i in range(0,numPassengers):
    if(i % 3 == 0):
        passenger.append(passengers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200), True, False, 999, 0, 0));
    else:
        passenger.append(passengers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200), False, False, 999, 0, 0));

# Def of main function
def main():
    #print(driver[1].driverID);
    t = 0;
    counter = 0;

    # Loop to call tReset to set passengers to be readyToBePickedUp
    while(t <= counter*timeConst):
        t += 1;
        td.Thread(target = tReset).start();
        tm.sleep(1);
    # td.Thread allows this function to be called at the same time as another
    td.Thread(target = pickup(numDrivers, numPassengers)).start();

# Sets a new passenger to be ready for pickup after timeConst seconds
def tReset():
    global startLog;
    temp = 0;
    done = False;
    if tm.time() - timeConst > startLog:
        startLog = tm.time();
        while(done == False):
            temp = randrange(0, numPassengers);
            if(passenger[temp].droppedOff == False and passenger[temp].readyToBePickedUp == False):
                passenger[temp].readyToBePickedUp == True;
                done = True;

# Function to calculate shortest path available from each driver to each passenger
def pickup(numDrivers, numPassengers):
    # Will find the shortest path from each driver to each passenger
    for j in range(0, numPassengers):
        for i in range(0, numDrivers):
            if passenger[j].readyToBePickedUp == True and nx.has_path(G, driver[i].currNode, passenger[j].pickUpNode):
                if (nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].pickUpNode, weight = 1.5, method = 'dijkstra') <= passenger[j].driverDistance):
                    passenger[j].driverID = driver[i].driverID;
                    passenger[j].estTime = nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].pickUpNode, weight = 1.5, method = 'dijkstra');
                    driver[i].assignedPassenger = j;


                
            #print("shortest path function run");
            if i == numDrivers:
                   i = 0;
        if j == numPassengers:
            j = 0;
            break;

    print("pickup function complete");

main();

