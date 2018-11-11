import pandas as pd
import numpy as np

def get_terminal_coordinates(terminal_no, terminal_data):
    #print(terminal_data[terminal_data[:,0]==terminal_no])
    terminals = terminal_data[:,0]
    #print(terminal_data[np.where(terminal_data[:,0]==terminal_no),[1,2]])
    return terminal_data[np.where(terminal_data[:, 0] == terminal_no), [1, 2]]

trip_data = np.genfromtxt("divvy_trips_june19.csv",delimiter=",", dtype='str',skip_header=1)
#trip_data = trip_data[:,[0,2,3,5,6,7]]
terminal_data = np.genfromtxt("divvy_stations.csv",delimiter=",",dtype='str')
terminal_data = terminal_data[:,[0,2,3]]
#print(trip_data.shape)
#print(terminal_data.shape)
#terminal_data = terminal_data.set_index(['Terminal'])
coordinates = np.ndarray(shape=(0,4))
for i in range(0,trip_data.shape[0]):
    start_terminal_id = trip_data[i,5]
    end_terminal_id = trip_data[i,7]
    start_coordinates = get_terminal_coordinates(start_terminal_id,terminal_data) #returns lat lon coordinates
    end_coordinates = get_terminal_coordinates(end_terminal_id,terminal_data)
    d = np.append(start_coordinates,end_coordinates,axis=1)
    print(d)
    coordinates = np.append(coordinates,d,axis=0)
#print(coordinates)
coordinate_data = np.concatenate((trip_data,coordinates),axis=1)
np.savetxt(fname="divvy_trips_with_coordinates.csv", X=coordinate_data, delimiter=',', fmt="%s")
#print(coordinate_data.shape)


