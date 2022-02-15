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
    custID = 0;
    groupSize = 0;
    pickUpNode = 0;
    destinationNode = 0;
    driverDistance = 999;
    driverID = 0;
    estTime = 0;
    readyToBePickedUp = False;
    droppedOff = False;
    pickedUp = False;
    def __init__(self, custID, groupSize, pickUpNode, destinationNode, readyToBePickedUp, droppedOff, driverDistance, driverID, estTime, pickedUp):
        self.custID = custID;
        self.groupSize = groupSize;
        self.pickUpNode = pickUpNode;
        self.destinationNode = destinationNode;
        self.readyToBePickedUp = readyToBePickedUp;
        self.droppedOff = droppedOff;
        self.driverDistance = driverDistance;
        self.driverID = driverID;
        self.estTime = estTime;
        self.pickedUp = pickedUp;

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
    driver.append(drivers(randrange(999,9999), 0, randrange(1,200), randrange(1,200), randrange(1,50), -1));

# Creates an array of Drivers with the given input
# Some passengers will spawn in with ReadyToBePickedUp = True so that the program doens't end too early
passenger = []
for i in range(0,numPassengers):

    if(i % 3 == 0):
        passenger.append(passengers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200), True, False, 999, 0, 0, False));
    else:
        passenger.append(passengers(randrange(999,9999), randrange(1,5), randrange(1,200), randrange(1,200), False, False, 999, 0, 0, False));

# Def of main function
def main():

    #print(driver[1].driverID);
    t = 0;
    counter = 0;
    counter2 = 0;

    # Loop to call tReset to set passengers to be readyToBePickedUp
    while(t <= counter*timeConst):
        t += 1;
        td.Thread(target = tReset).start();
        tm.sleep(1);

    # td.Thread allows this function to be called at the same time as another
    # calls pickup, 'numPassengers' times
    while(counter2 <= numPassengers):
        td.Thread(target = pickup(numDrivers, numPassengers)).start();
        counter2 += 1;
        

# Sets a new passenger to be ready for pickup after timeConst seconds
def tReset():
    global startLog;
    temp = 0;
    done = False;

    if tm.time() - timeConst > startLog:
        startLog = tm.time();

        while(done == False):
            temp = randrange(0, numPassengers);

            if(passenger[temp].droppedOff == False and passenger[temp].readyToBePickedUp == False and passenger[temp].pickedUp == False):
                passenger[temp].readyToBePickedUp == True;
                done = True;

# Function to calculate shortest path available from each driver to each passenger
def pickup(numDrivers, numPassengers):
    tempDriver = 0;
    tempPassenger = 0;
    updated = False;

    # Will find the shortest path from each driver to each passenger
    for j in range(0, numPassengers):

        for i in range(0, numDrivers):

            # if ready to be picked up, path exists, and there is room in the car
            if passenger[j].readyToBePickedUp == True and nx.has_path(G, driver[i].currNode, passenger[j].pickUpNode) and ((passenger[j].groupSize + driver[i].currCap) <= 5):

                # find out if the shortest path from driver i to passenger j is less than the previously viewed shortest path (from passenger j to driver i-1)
                if (nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].pickUpNode, weight = 1.5, method = 'dijkstra') <= passenger[j].driverDistance):
                    # updated shortest path and update temp values
                    passenger[j].driverDistance = nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].pickUpNode, weight = 1.5, method = 'dijkstra');
                    tempDriver = i;
                    tempPassenger = j;
                    updated = True;

    if(updated == True):
        print("Driver", driver[tempDriver].driverID, "was assigned to passenger", passenger[tempPassenger].custID, "and is", passenger[tempPassenger].driverDistance, "minutes away.");
        passenger[tempPassenger].readyToBePickedUp = False;
        driver[tempDriver].currCap = driver[tempDriver].currCap + passenger[j].groupSize;
        driver[tempDriver].assignedPassenger = passenger[tempPassenger].custID;
        passenger[tempPassenger].driverID = driver[tempDriver].driverID;
        passenger[tempPassenger].pickedUp = True;
        updated = False;

main();

