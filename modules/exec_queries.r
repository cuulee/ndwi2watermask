library(mongolite)
library(sf)
library(tidyr)
library(dplyr)
library(jsonlite)

m <- mongo("sar2watermask","sar2watermask","mongodb://localhost:27017/")

#pipeline = '[{
#        "$group":
#            {
#                "_id" : "$properties.id_cogerh",
#                "timeSeries" : { "$push" : { "time" : "$properties.ingestion_time" , "area" : "$properties.area"} }
#            }        
#    }]'

pipeline = '[
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]'


polys=m$aggregate(pipeline,'{"allowDiskUse":true}')

sflist <- list()
for(i in 1:10])
{ 
    datemillis <- as.integer(as.POSIXct(polys$latestIngestion[i])) * 1000
    id <- polys$`_id`[i]
####### not working!!!
    poly = m$find(paste0('{"properties.id_cogerh" : "',id,'", "properties.ingestion_time" : ',datemillis,'"}'))

    poly = m$find(paste0('{"properties.id_cogerh" : ',id,'}'))

    if(poly$geometry$type=="MultiPolygon")
    {
        for(j in 1:poly$geometry$coordinates[[1]])
        {
            latlong[[j]] <- rbind(poly$geometry$coordinates[[1]][[i]][,,1],poly$geometry$coordinates[[1]][[i]][,,2]) %>% t
        }
        sfgPl <- lapply(latlong,st_multipolygon)
    } else if(poly$geometry$type=="Polygon")
    {
        latlong <- rbind(poly$geometry$coordinates[[1]][,,1],poly$geometry$coordinates[[1]][,,2]) %>% t
        sfgPl <- st_polygon(list(latlong))
    }

    sflist[[i]] <- st_geometry(sfgPl) %>% st_sf(.,crs=4326) %>% bind_cols(.,poly$properties)
}


sfPl <- do.call("rbind",sflist)
