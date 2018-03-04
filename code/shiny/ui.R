library(leaflet)
library(tidyverse)
names=read_csv("output.csv",col_names = FALSE)
data=read_csv("shinydata.csv")
data$name=names$X1

# Choices for drop-downs
vars <- unique(data$name)


navbarPage(title="Yelp" , id="nav",
           
           tabPanel("Interactive map",
                    div(class="outer",
                        
                        tags$head(
                          # Include our custom CSS
                          includeCSS("styles.css")
                        ),
                        
                        # If not using custom CSS, set height of leafletOutput to a number instead of percent
                        leafletOutput("map", width="100%", height="100%"),
                        
                        # Shiny versions prior to 0.11 should use class = "modal" instead.
                        absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                                      draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                                      width = 330, height = "auto",
                                      
                                      h2("Average Stars by Location"),
                                      selectInput("res", "Restaurant", vars),
                                      plotOutput("tsplot",height = 250)
                        )
                    )
           )
)
           
