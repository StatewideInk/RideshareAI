import networkx as nx
import matplotlib.pyplot as plt
import time as tm
import threading as td
from random import *
import array as arr

# Constants
seed = 1000;
startLog = tm.time();
timeConst = 0.1;
avgDist = 0;
G = nx.gnp_random_graph(200, 0.04, seed = seed);

# Class to hold all passenger information
class passengers:
    passID = 0;
    groupSize = 0;
    pickUpNode = 0;
    destinationNode = 0;
    driverDistance = 999;
    driverID = 0;
    estTime = 0;
    readyToBePickedUp = False;
    droppedOff = False;
    pickedUp = False;
    def __init__(self, passID, groupSize, pickUpNode, destinationNode, readyToBePickedUp, droppedOff, driverDistance, driverID, estTime, pickedUp):
        self.passID = passID;
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
    dropDist = 999;
    assignedPassenger = -1;
    def __init__(self, driverID, currCap, currNode, dropNode, dropDist, assignedPassenger):
        self.driverID = driverID;
        self.currCap = currCap;
        self.currNode = currNode;
        self.dropNode = dropNode;
        self.dropDist = dropDist;
        self.assignedPassenger = assignedPassenger;

# Askes the user for number of drivers and passengers
numDrivers = int(input("Enter the number of drivers for this simulation: "));
numPassengers = int(input("Enter the number of passengers for this simulation: "));

# Creates an array of Drivers with the given input
driver = []
for i in range(0,numDrivers):
    driver.append(drivers(randrange(999,9999), 0, randrange(1,200), 999, randrange(1,50), -1));

# Creates an array of Drivers with the given input
# Some passengers will spawn in with ReadyToBePickedUp = True so that the program doens't end too early
passenger = []
for i in range(0,numPassengers):
    dest = 0;
    x = randrange(1,200)
    y = randrange(1,200, x)
    if(nx.has_path(G, x, y) and x != y and x != nx.isolates(G) and y != nx.isolates(G)):
        dest = y;
    else:
        y = 200
    
    if(i % numPassengers == 1200):
        passenger.append(passengers(randrange(999,9999), randrange(1, 5), x, dest, True, False, 999, 0, 0, False));
    else:
        passenger.append(passengers(randrange(999,9999), randrange(1, 5), x, dest, True, False, 999, 0, 0, False));



# Def of main function
def main(numDrivers, numPassengers):
    t = 0;
    counter = 0;
    counter2 = 0;
    counter3 = 0;
    counter4 = 0;
    done = False;
    # Loop to call tReset to set passengers to be readyToBePickedUp
    while(done == False):
        t += 1;
        td.Thread(target = tReset()).start();
        tm.sleep(timeConst);
        for i in range(0, numPassengers - 1):
            if(passenger[i].readyToBePickedUp == True):
                counter += 1;
                if(counter == numPassengers - 1):
                    done = True;
                    print("Done = True");

    # td.Thread allows this function to be called at the same time as another
    # calls pickup, 'numPassengers' times
    while(passenger[counter2].droppedOff == False and counter2 <= numPassengers or passenger[counter2].pickedUp == True):
            td.Thread(target = pickup(numDrivers, numPassengers, counter3)).start();
            td.Thread(target = dropOff(numDrivers, numPassengers)).start();
            counter2 += 1;
            if(counter2 == numPassengers - 1):
                counter2 = 0;
    print("Average Distance traveled per day by each driver: ",(avgDist/30)/8);
    print("Average Distance traveled per day by entire fleet: ",avgDist/8);
    

# Sets a new passenger to be ready for pickup after timeConst seconds
def tReset():
    global startLog;
    temp = 0;
    done = False;

    if tm.time() - timeConst > startLog:
        startLog = tm.time();
        if(done == False):
            temp = randrange(0, numPassengers);
            if(passenger[temp].readyToBePickedUp == False and passenger[temp].pickedUp == False):
                passenger[temp].readyToBePickedUp = True;
                print("Passenger", temp, "is now ready to be picked up");
                done = True;

# Function to calculate shortest path available from each driver to each passenger
def pickup(numDrivers, numPassengers, counter3):
    tempDriver = 0;
    tempPassenger = 0;
    updated = False;

    # For each passenger
    for j in range(0, numPassengers):
        # Compare to each driver
        for i in range(0, numDrivers):

            # if ready to be picked up, AND path from driver to passenger exists, AND a path from driver to passenger destination exists, AND there is room in the car
            if (passenger[j].readyToBePickedUp == True and nx.has_path(G, driver[i].currNode, passenger[j].pickUpNode) and nx.has_path(G, driver[i].currNode, passenger[j].destinationNode) and (passenger[j].groupSize + driver[i].currCap) <= 5):

                # find out if the shortest path from driver i to passenger j is less than the previously viewed shortest path (from passenger j to driver i-1)
                if (nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].pickUpNode, weight = 1.5, method = 'dijkstra') <= passenger[j].driverDistance):

                    # Update the shortest path from passenger j to driver i, temporarily store driver and passenger number, and set updated to True
                    passenger[j].driverDistance = nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].pickUpNode, weight = 1.5, method = 'dijkstra');
                    global avgDist
                    avgDist += passenger[j].driverDistance;
                    tempDriver = i;
                    tempPassenger = j;
                    updated = True;

        # If there was a new, closer driver found to passenger j (There will be a new driver, this just stores the closest driver out of all of them)
        if(updated == True):
            print("Driver", driver[tempDriver].driverID, "was assigned to passenger", passenger[tempPassenger].passID, "and is", passenger[tempPassenger].driverDistance, "minutes away.");
            counter3 = counter3 + 1;
            passenger[tempPassenger].readyToBePickedUp = False;
            driver[tempDriver].currCap = driver[tempDriver].currCap + passenger[tempPassenger].groupSize;
            driver[tempDriver].assignedPassenger = passenger[tempPassenger].passID;
            passenger[tempPassenger].driverID = driver[tempDriver].driverID;
            passenger[tempPassenger].pickedUp = True;
            driver[i].currNode = passenger[j].pickUpNode;
            updated = False;

#Function to calculate when and where a driver needs to go to drop off a passenger
def dropOff(numDrivers, numPassengers):
    dropCount = 0;
    for i in range(0, numDrivers):
        for j in range(0, numPassengers):
            #make sure that the passenger is ready to be dropped off
            if (driver[i].driverID == passenger[j].driverID and passenger[j].droppedOff == False and passenger[j].pickedUp == True):
                #for every car with a passenger check their shortest dropoff distance
                if(nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].destinationNode, weight = 1.5, method = 'dijkstra') <= driver[i].dropDist):
                    driver[i].dropDist = nx.shortest_path_length(G, source = driver[i].currNode, target = passenger[j].destinationNode, weight = 1.5, method = 'dijkstra');
                    global avgDist 
                    avgDist += driver[i].dropDist;
                    tm.sleep(driver[i].dropDist/1000);
                    driver[i].dropNode = passenger[j].destinationNode;
                    dropCount += 1;
                    print("Dropped off: ", dropCount, " Passenger: ", passenger[j].passID, " was dropped off with: ", passenger[j].groupSize, " at node: ", passenger[j].destinationNode, "by driver: ", passenger[j].driverID);
                    driver[i].currCap -= passenger[j].groupSize;
                    passenger[j].droppedOff = True;  
                    passenger[j].pickedUp = False;

                else:
                    driver[i].dropDist = 999
                    td.Thread(target = dropOff(numDrivers, numPassengers)).start();

    td.Thread(target = pickup(numDrivers, numPassengers, 0)).start();
        
                        
main(numDrivers, numPassengers);

