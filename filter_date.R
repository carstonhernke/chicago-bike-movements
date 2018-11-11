# read in data before
dt = data[data[,"start_time"]>"2017-06-19 00:00:00 UTC",]
dt2 = dt[dt[,"start_time"]<"2017-06-20 00:00:00 UTC",]
write.csv(dt2,file = "/Users/carstonhernke/PycharmProjects/bike_animation/divvy_trips_june19.csv")