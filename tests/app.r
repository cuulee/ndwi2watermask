library(shiny)
library(leaflet)
library(rgdal)
library(raster)

poly <- st_read("~/proj/sar2watermask/tests/0_latest.geojson")

poly <- poly["geometry"]

                                        #rasterize

r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()

ui <- fluidPage(
  leafletOutput("mymap"),
  p()#,
 # actionButton("recalc", "New points")
)

server <- function(input, output, session) {

    
#    points <- eventReactive(input$recalc, {
#        cbind(rnorm(40) * 2 + 13, rnorm(40) + 48)
#    }, ignoreNULL = FALSE)
    
  output$mymap <- renderLeaflet({
    leaflet(poly) %>%
      addProviderTiles(providers$Stamen.TonerLite,
        options = providerTileOptions(noWrap = TRUE)
        ) %>%
        addPolygons()
#      addMarkers(data = points())
  })
}

shinyApp(ui, server)
