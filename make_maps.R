#import points
library(ggmap)
library(ggplot2)
library(readr)
library(geojsonio)
points <- read_csv("~/PycharmProjects/bike_animation/coordinate_times14.csv", col_names = FALSE)

colnames(points) <- c('time','lat','lon')

library(sp)
water <- geojson_read("waterways.geojson", what = "sp")
plot(water)
water_df = fortify(water)

times = seq(1497844800,1497916800,60)
#t = 1497844800
#time <- as.POSIXct(t, origin = '1970-01-01', tz = 'GMT')

for (t in times){
  sub = subset(points, time>t & time<(t+60))
  sub = sub[,c(2,3)]
  time <- as.POSIXct(t, origin = '1970-01-01', tz = 'GMT')
  p <- ggplot() + 
  geom_polygon(aes(x = long,y = lat,group = group),data = water_df, fill = "cadetblue3") +
  coord_cartesian(xlim = c(-87.79089, -87.51322), ylim = c(41.78820, 42.00861)) +
  geom_point(data = sub, aes(x = lon, y = lat),size = .2, colour = "goldenrod2", alpha = .5) +
  annotate("text", label = time, x = -87.560474, y = 42.007253, size = 6, colour = "coral4", family = 'Avenir' face = 'Bold') +
  theme(axis.line=element_blank(),
      axis.text.x=element_blank(),
      axis.text.y=element_blank(),
      axis.ticks=element_blank(),
      axis.title.x=element_blank(),
      axis.title.y=element_blank(),
      legend.position="none",
      panel.background = element_rect(fill = "grey25"),
      panel.border=element_blank(),
      panel.grid.major=element_blank(),
      panel.grid.minor=element_blank(),
      plot.background=element_blank())
  
  fname = paste0("images/",t,".jpg")
  ggsave(filename = fname, plot = p)
}