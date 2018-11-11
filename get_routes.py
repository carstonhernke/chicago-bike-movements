import numpy as np
import requests
import json
import math
import random
#import random
import geopy
from geopy.distance import vincenty
from datetime import datetime

class Coord:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

def convert_to_epoch_a(str_time):
    str_time = str(str_time)
    str_time = str_time.replace('"','')
    utc_time = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
    return epoch_time

def convert_to_epoch_b(str_time):
    str_time = str(str_time)
    str_time = str_time.replace('"', '')
    utc_time = datetime.strptime(str_time, "%m/%d/%Y %H:%M:%S")
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
    return epoch_time

def calculate_initial_compass_bearing(pointA, pointB): #taken from https://gist.github.com/jeromer/2005586
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def generate_start(row,data):
    return Coord(data[row,14],data[row,15])

def generate_end(row,data):
    return Coord(data[row, 16], data[row, 17])

output = []
trip_data = np.genfromtxt("divvy_trips_june19_with_coordinates.csv",delimiter=",", dtype='str')
for i in range(1,trip_data.shape[0]-1):
#for i in range(1,100):
#for i in range(1, 2):
    print("processing "+str(i)+" of "+str(trip_data.shape[0]))
    start = generate_start(i,trip_data)
    end = generate_end(i+1,trip_data )
    loc_str = str(start.lon)+","+str(start.lat)+";"+str(end.lon)+","+str(end.lat)
    payload = {'overview':'full', 'geometries':'geojson', 'alternatives':'3'}
    link = "http://127.0.0.1:5000/route/v1/bicycle/"+str(loc_str)
    #print(link)
    r = requests.get(link, params=payload)
    #print(r)
    rj = json.loads(r.text)
    #print(rj)
    #for i in rj:
     #   o = i[0]['routes']['geometry']['coordinates'][0]
    rn = rj['routes'][0]['geometry']['coordinates'][0] #get lon,lat list
    #print(rn[0])
    rand = random.randint(0,2)
    utc_time = datetime.strptime(trip_data[i][3],"%Y-%m-%d %H:%M:%S")
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
    #route = rj['routes']['geometry']['coordinates']
    total_route_length = rj['routes'][0]['distance']
    total_route_time = int(convert_to_epoch_b(trip_data[i][4])-convert_to_epoch_a(trip_data[i][3])) #from dataset, round to nearest minute
    ex_int_time = 0
    if total_route_length == 0 or total_route_time == 0:
        #print("skipping bc 0")
        continue
    else:
        #print("continuing")
        start = Coord(rj['routes'][0]['geometry']['coordinates'][0][1],rj['routes'][0]['geometry']['coordinates'][0][0])
        start_coordinates = start
        for j in range(0,len(rj['routes'][0]['geometry']['coordinates'])-1):
            end_coordinates = Coord((rj['routes'][0]['geometry']['coordinates'][j+1][1]),(rj['routes'][0]['geometry']['coordinates'][j+1][0]))
            #print("start_coordinates = "+str(start_coordinates))
            #print("end lat = "+str(end_coordinates.lat))
            #print("end lon = "+str(end_coordinates.lon))

            segment_length = vincenty((start_coordinates.lat,start_coordinates.lon),(end_coordinates.lat,end_coordinates.lon)).meters
            #print("segment_length = "+str(segment_length))
            #print("total_route_length = "+str(total_route_length))
            #print("total_route_time = "+str(total_route_time))

            seg_time = int((int(segment_length)/int(total_route_length))*int(total_route_time))
            #print(seg_time)
            #take point1, point2 and find seg_time number of intermediate points
            if seg_time == 0:
                continue
            else:
                int_dist = segment_length/ seg_time
                for k in range (1,seg_time):
                    bearing = calculate_initial_compass_bearing((start_coordinates.lat,start_coordinates.lon),(end_coordinates.lat,end_coordinates.lon))
                    dist = int_dist*k
                    d = geopy.distance.VincentyDistance(meters = dist)
                    start_c = (start_coordinates.lat,start_coordinates.lon)
                    int_point = d.destination(start_c, bearing)
                    int_time = ex_int_time+(60)
                    point_time = int_time + epoch_time #route start time + incremental time
                    output_list = (point_time,int_point[0],int_point[1]) #save point and time, make sure time is in epoch seconds
                    #print(output_list)
                    ex_int_time = int_time
                    output.append(output_list)
            start_coordinates = end_coordinates
print("done with data, now saving...")
output_np = np.array(output)
np.savetxt(fname="coordinate_times14.csv", X=output_np, delimiter=',')