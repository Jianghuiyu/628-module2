library(readr)
library(dplyr)
library(leaflet)
library(lubridate)
library(tidyverse)
library(stringr)
library(ggplot2)

review = read_csv("shinydata.csv")
names=read_csv("output.csv",col_names = FALSE)
review$name=names$X1
review$date=ymd(review$date)
review$month=month(review$date)


function(input, output, session) {
  data<-reactive({review %>% filter(name==input$res) %>% group_by(longitude,latitude,city) %>%
      summarise(stars = mean(stars))})
  output$map<- renderLeaflet({data() %>%
    leaflet() %>% addTiles() %>%
      addCircles(~longitude,~latitude, weight = 2, fillOpacity= 3,
                 radius = ~100*stars, popup = ~paste("Average Stars:",as.character(signif(stars,digits = 3)),"<br>","City:",city,"<br>","Longitude:", longitude,"<br>","Latitude:", latitude ))})
  data1<- reactive({review %>% filter(name==input$res)%>% group_by(month)%>%
      summarise(stars=mean(stars))})
  output$tsplot<- renderPlot({data1()%>%
    ggplot(aes(month,stars))+geom_line()+scale_x_discrete("Month",limits=1:12)+scale_y_continuous("Average Stars",limits=c(1,5))+ggtitle("Average Stars vs Month")+
      theme(plot.title = element_text(hjust = 0.5))
  })
}
