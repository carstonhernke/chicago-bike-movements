library(plyr)
trips <- divvy_trips_june19
from_stations <- divvy_stations
colnames(from_stations) <- c('from_station_id','lat_from','lon_from')
to_stations <- divvy_stations
colnames(to_stations) <- c('to_station_id','lat_to','lon_to')

#lookups/joins
er1 <- join(trips, from_stations, by = "from_station_id", type = 'left')
er1 <- join(er1, to_stations, by = "to_station_id", type = 'left')
View(er1)

write.csv(er1,file = "/Users/carstonhernke/PycharmProjects/bike_animation/divvy_trips_june19_with_coordinates.csv")
